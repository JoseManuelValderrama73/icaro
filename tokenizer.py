from datasets.load import DatasetDict
from transformers import AutoTokenizer
from datasets import load_dataset
from shared import *
from logger import ExecutionLogger
from enum import Enum

class TransformAction(Enum):
    KEEP = 0
    TO_VULNERABLE = 1
    TO_SAFE = 2

class TokenizedDataset:
    def __init__(self, settings: dict, dataset: DatasetDict, code_snippet: str, logger: ExecutionLogger):
        self.seed = get_seed(settings, logger)
        self.max_length = settings.get("max_length", 1024)

        if settings['minimize_factor'] <= 0 or settings['minimize_factor'] > 1:
            if logger: logger.log_error("TokenizedDataset", "minimize_factor debe estar en el rango (0, 1]")
            if logger: logger.finalize("TokenizedDataset", "FAILED")
            raise ValueError("minimize_factor debe estar en el rango (0, 1]")
        if settings['minimize_factor'] != 1:
            self.minimize(settings['minimize_factor'], dataset)
            if logger: logger.log_step("TokenizedDataset", f"Dataset minimized by factor {settings['minimize_factor']}", "COMPLETED")

        self.tokenizer = AutoTokenizer.from_pretrained(settings["model_path"], local_files_only=True)
        if logger: logger.log_step("TokenizedDataset", f"Tokenizer {settings['model']} loaded", "COMPLETED")

        clean_ds = dataset.map(self.clean_examples, batched=True)
        if logger: logger.log_step("TokenizedDataset", "Dataset cleaned", "COMPLETED")

        self.code_snippet = code_snippet
        self.dataset = clean_ds.map(self.tokenize, batched=True)
        if logger: logger.log_step("TokenizedDataset", "Dataset tokenized", "COMPLETED")
        '''
        try:
            self.dataset.cleanup_cache_files()
        except Exception:
            pass
        '''

    def tokenize(self, examples):
        tk = self.tokenizer(
            examples[self.code_snippet],
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors=None  # Let Trainer handle tensor conversion
        )
        self.label(tk, examples)
        return tk

    def clean_examples(self, examples):
        from shared import clean_code
        examples[self.code_snippet] = [clean_code(c) if c is not None else "" for c in examples[self.code_snippet]]
        return examples
    
    def minimize(self, factor: float, dataset: DatasetDict):
        """
        Minimiza el dataset para pruebas rápidas manteniendo el balance de clases.

        :param factor: factor de minimización
        """
        for split in dataset.keys():
            # Agregar columna temporal con las etiquetas
            dataset_with_labels = dataset[split].map(
                lambda example, idx: {'label_temp': self.get_label(example)}, 
                with_indices=True
            )
            
            # Filtrar por clase
            vulnerable = dataset_with_labels.filter(lambda x: x['label_temp'] == 1)
            non_vulnerable = dataset_with_labels.filter(lambda x: x['label_temp'] == 0)
            
            # Calcular cuántos ejemplos tomar de cada clase
            n_vulnerable = int(len(vulnerable) * factor)
            n_non_vulnerable = int(len(non_vulnerable) * factor)
            
            # Asegurar al menos 1 ejemplo de cada clase si existen
            n_vulnerable = max(1, n_vulnerable) if len(vulnerable) > 0 else 0
            n_non_vulnerable = max(1, n_non_vulnerable) if len(non_vulnerable) > 0 else 0
            
            # Seleccionar ejemplos de cada clase
            sampled_vulnerable = vulnerable.shuffle(seed=self.seed).select(range(min(n_vulnerable, len(vulnerable))))
            sampled_non_vulnerable = non_vulnerable.shuffle(seed=self.seed).select(range(min(n_non_vulnerable, len(non_vulnerable))))
            
            # Combinar y mezclar
            from datasets import concatenate_datasets
            combined = concatenate_datasets([sampled_vulnerable, sampled_non_vulnerable])
            dataset[split] = combined.shuffle(seed=self.seed).remove_columns(['label_temp'])

    def get_label(self, example):
        """
        Extrae la etiqueta de un ejemplo antes de la tokenización.
        
        :param example: ejemplo del dataset
        :return: 1 si es vulnerable, 0 si no
        """
        raise NotImplementedError("Subclase debe implementar el método get_label()")

    def label(self, tk, examples):
        """
        Etiqueta los ejemplos tokenizados.

        :param tk: tokenizaciones
        :param examples: ejemplos originales
        """
        raise NotImplementedError("Subclase debe implementar el método label()")

    def __getitem__(self, idx):
        return self.dataset[idx]

    def __len__(self):
        return len(self.dataset)

class TokenizedCombo(TokenizedDataset):
    def __init__(self, settings: dict, logger: ExecutionLogger):
        paths = settings["dataset_path"].split(",")
            
        from datasets import concatenate_datasets
        combo = None
        for path in paths:
            ds = load_dataset(path)
            path_lower = path.lower()
            if 'bigvul' in path_lower:
                ds = self.transform(TransformAction.KEEP, ds, 'func_before', 'vul', 0)
            elif 'draper' in path_lower:
                ds = self.transform(TransformAction.TO_VULNERABLE, ds, 'functionSource', 'combine', 0)
            elif 'diversevul' in path_lower:
                ds = self.transform(TransformAction.KEEP, ds, 'func', 'target', 0)
            elif 'formai' in path_lower:
                ds = self.cleanup_formai(ds)
                ds = self.transform(TransformAction.TO_VULNERABLE, ds, 'source_code', 'vulnerable_line', -1)
            else:
                raise ValueError(f"Unknown dataset path: {path}")

            print(f"{path}: {len(ds['train'].filter(lambda example: example['vulnerable'] == 1))} / {len(ds['train'])}")    
            
            # Crear splits de validación y test si no existen, sin data leakage
            if 'validation' not in ds.keys() or 'test' not in ds.keys():
                split1 = ds['train'].train_test_split(test_size=0.3, seed=settings['seed'])
                split2 = split1['test'].train_test_split(test_size=0.5, seed=settings['seed'])
                ds = DatasetDict({
                    'train': split1['train'],        # 70%
                    'validation': split2['train'],    # 15%
                    'test': split2['test']            # 15%
                })

            if combo:
                combo = DatasetDict({
                    'train': concatenate_datasets([combo['train'], ds['train']]),
                    'validation': concatenate_datasets([combo['validation'], ds['validation']]),
                    'test': concatenate_datasets([combo['test'], ds['test']])
                })
            else:
                combo = ds

        self.dataset = combo
        # print the percentage of the rows with label 1
        for split_name in self.dataset.keys():
            print(f"Percentage of rows with label 1 in {split_name}: {len(self.dataset[split_name].filter(lambda example: example['vulnerable'] == 1)) / len(self.dataset[split_name]) * 100}%")    
        
        super().__init__(settings, self.dataset, 'code', logger)

    def transform(self, action: TransformAction, dataset, code, label, safe_tag):
        from datasets import Dataset, concatenate_datasets
        
        new_splits = {}
        for split_name in dataset.keys():
            if action == TransformAction.TO_VULNERABLE:
                filtered = dataset[split_name].filter(lambda example: example[label] != safe_tag)
                data = {
                    'code': filtered[code],
                    'vulnerable': [1] * len(filtered)
                }
                new_splits[split_name] = Dataset.from_dict(data)
            elif action == TransformAction.TO_SAFE:
                filtered = dataset[split_name].filter(lambda example: example[label] == safe_tag)
                data = {
                    'code': filtered[code],
                    'vulnerable': [0] * len(filtered)
                }
                new_splits[split_name] = Dataset.from_dict(data)
            elif action == TransformAction.KEEP:
                data = {
                    'code': dataset[split_name][code],
                    'vulnerable': [int(v != safe_tag) for v in dataset[split_name][label]]
                }
                new_splits[split_name] = Dataset.from_dict(data)
        
        return DatasetDict(new_splits)

    def get_label(self, example):
        return example['vulnerable']

    def label(self, tk, examples):
        tk['labels'] = [int(v) for v in examples['vulnerable']]

    def cleanup_formai(self, dataset):
        """ Elimina ejemplos no verificados """
        return dataset.filter(lambda example: example['verification_finished'] == 'yes')

class TokenizedCastle(TokenizedDataset):
    def __init__(self, settings: dict, logger: ExecutionLogger):
        dataset = load_dataset('json', data_files=settings['dataset_path'], field='tests')
        super().__init__(settings, dataset, 'code', logger)

    def get_label(self, example):
        return 1 if example['vulnerable'] else 0

    def label(self, tk, examples):
        # convierto de True y False a 1 y 0
        tk['labels'] = [int(v) for v in examples['vulnerable']]