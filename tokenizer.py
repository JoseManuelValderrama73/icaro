from datasets.load import DatasetDict
from transformers import AutoTokenizer
from datasets import load_dataset
from constants import *
from logger import ExecutionLogger

class TokenizedDataset:
    def __init__(self, settings: dict, dataset: DatasetDict, code_snippet: str, logger: ExecutionLogger):
        self.dataset = dataset
        self.seed = get_seed(settings, logger)

        minimize_factor = settings['minimize_factor']
        if minimize_factor <= 0 or minimize_factor > 1:
            if logger: logger.log_error("TokenizedDataset", "minimize_factor debe estar en el rango (0, 1]")
            if logger: logger.finalize("TokenizedDataset", "FAILED")
            raise ValueError("minimize_factor debe estar en el rango (0, 1]")
        if minimize_factor != 1:
            self.minimize(minimize_factor)
            if logger: logger.log_step("TokenizedDataset", f"Dataset minimized by factor {minimize_factor}", "COMPLETED")

        self.tokenizer = AutoTokenizer.from_pretrained(settings["model_path"], local_files_only=True)
        if logger: logger.log_step("TokenizedDataset", f"Tokenizer {settings['model']} loaded", "COMPLETED")

        if 'train' not in self.dataset or 'test' not in self.dataset:
            self.train_test_split(settings["test_size"])
            if logger: logger.log_step("TokenizedDataset", f"Dataset split into train and test with test size {settings['test_size']}", "COMPLETED")
            
        self.code_snippet = code_snippet
        self.dataset = self.dataset.map(self.tokenize, batched=True, remove_columns=self.dataset['train'].column_names)
        if logger: logger.log_step("TokenizedDataset", "Dataset tokenized", "COMPLETED")
        '''
        try:
            self.dataset.cleanup_cache_files()
        except Exception:
            pass
        '''

    def tokenize(self, examples):
        max_length = min(getattr(self.tokenizer, "model_max_length", 512), 512)
        tk = self.tokenizer(
            examples[self.code_snippet],
            padding="max_length",
            truncation=True,
            max_length=max_length,
            return_tensors=None  # Let Trainer handle tensor conversion
        )
        """ TODO:
        cambiar max_length hasta 786 (max de deberta) o
        ajustar deberta para que acepte el tamaño necesario en main.py
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL, 
            num_labels=2,
            max_position_embeddings=1748  # Adjust model to accept longer sequences
        )
        """
        self.label(tk, examples)
        return tk
    
    def train_test_split(self, test_size):
        """
        Divide el dataset en conjunto de entrenamiento y prueba.
        
        :param test_size: Tamaño del conjunto de prueba. Rango (0, 1)
        :param seed: Semilla para la división aleatoria
        """
        print("[Tokenizer]: Se divide el dataset en 'train' y 'test'")
        train_test = self.dataset['train'].train_test_split(test_size=test_size, seed=self.seed)
        self.dataset = DatasetDict({
            'train': train_test['train'],
            'test': train_test['test']
        })
    
    def minimize(self, factor: float):
        """
        Minimiza el dataset para pruebas rápidas manteniendo el balance de clases.

        :param factor: factor de minimización
        """
        for split in self.dataset.keys():
            # Agregar columna temporal con las etiquetas
            dataset_with_labels = self.dataset[split].map(
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
            self.dataset[split] = combined.shuffle(seed=self.seed).remove_columns(['label_temp'])

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


class TokenizedCastle(TokenizedDataset):
    def __init__(self, settings: dict, logger: ExecutionLogger):
        dataset = load_dataset('json', data_files=settings['dataset_path'], field='tests')
        print(dataset)
        super().__init__(settings, dataset, 'code', logger)

    def get_label(self, example):
        return 1 if example['vulnerable'] else 0

    def label(self, tk, examples):
        # convierto de True y False a 1 y 0
        tk['labels'] = [int(v) for v in examples['vulnerable']]

class TokenizedDraper(TokenizedDataset):
    def __init__(self, settings: dict, logger: ExecutionLogger):
        self.code_snippet = 'functionSource'
        dataset = load_dataset(settings["dataset_path"])
        super().__init__(settings, dataset, self.code_snippet, logger)

    def get_label(self, example):
        return 1 if any(
            example[cwe] 
            for cwe in ['CWE-119', 'CWE-120', 'CWE-469', 'CWE-476', 'CWE-other']
        ) else 0

    def label(self, tk, examples):
        tk['labels'] = []
        for i in range(len(examples[self.code_snippet])):
            has_vulnerability = any(
                examples[cwe][i] 
                for cwe in ['CWE-119', 'CWE-120', 'CWE-469', 'CWE-476', 'CWE-other']
            )
            tk['labels'].append(1 if has_vulnerability else 0)
    
class TokenizedFormAI(TokenizedDataset):
    def __init__(self, settings: dict, logger: ExecutionLogger):
        self.dataset = load_dataset(settings["dataset_path"])
        self.cleanup()
        super().__init__(settings, self.dataset, 'source_code', logger)

    def get_label(self, example):
        return 0 if example['vulnerable_line'] == -1 else 1

    def label(self, tk, examples):
        tk['labels'] = [0 if line == -1 else 1 for line in examples['vulnerable_line']]
    
    def cleanup(self):
        """ Elimina ejemplos no verificados """
        self.dataset = self.dataset.filter(lambda example: example['verification_finished'] == 'yes')

class TokenizedBigVul(TokenizedDataset):
    def __init__(self, settings: dict, logger: ExecutionLogger):
        self.dataset = load_dataset(settings["dataset_path"])
        print(self.dataset)
        self.transform()
        print(self.dataset)
        super().__init__(settings, self.dataset, 'code', logger)

    def transform(self):
        """ Genera un dataset con los ejemplos vulnerables y sus arreglos aparecen por separado """
        from datasets import Dataset, concatenate_datasets
        
        new_splits = {}
        
        for split_name in self.dataset.keys():
            filtered = self.dataset[split_name].filter(lambda example: example['CWE ID'] != None)
            
            vulnerable_data = {
                'code': filtered['func_before'],
                'vulnerable': [1] * len(filtered)
            }
            vulnerable_dataset = Dataset.from_dict(vulnerable_data)
            
            non_vulnerable_data = {
                'code': filtered['func_after'],
                'vulnerable': [0] * len(filtered)
            }
            non_vulnerable_dataset = Dataset.from_dict(non_vulnerable_data)
            
            combined = concatenate_datasets([vulnerable_dataset, non_vulnerable_dataset])
            new_splits[split_name] = combined
        
        self.dataset = DatasetDict(new_splits)
    
    def get_label(self, example):
        return example['vulnerable']

    def label(self, tk, examples):
        tk['labels'] = [int(v) for v in examples['vulnerable']]