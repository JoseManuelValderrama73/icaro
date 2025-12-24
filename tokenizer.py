from datasets.load import DatasetDict
from transformers import AutoTokenizer
from datasets import load_dataset
from constants import *

class TokenizedDataset:
    def __init__(self, tokenizer_id: str, dataset, code_snippet, minimize_factor):
        self.dataset = dataset
        if minimize_factor:
            if minimize_factor <= 0 or minimize_factor > 1:
                raise ValueError("minimize_factor debe estar en el rango (0, 1]")
            self.minimize(minimize_factor)

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)

        if 'train' not in self.dataset or 'test' not in self.dataset:
            self.train_test_split(TEST_SIZE, SEED)
            
        self.code_snippet = code_snippet
        self.dataset = self.dataset.map(self.tokenize, batched=True, remove_columns=self.dataset['train'].column_names)
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
    
    def train_test_split(self, test_size, seed):
        """
        Divide el dataset en conjunto de entrenamiento y prueba.
        
        :param test_size: Tamaño del conjunto de prueba. Rango (0, 1)
        :param seed: Semilla para la división aleatoria
        """
        print("[Tokenizer]: Se divide el dataset en 'train' y 'test'")
        train_test = self.dataset['train'].train_test_split(test_size=test_size, seed=seed)
        self.dataset = DatasetDict({
            'train': train_test['train'],
            'test': train_test['test']
        })
    
    def minimize(self, factor):
        """
        Minimiza el dataset para pruebas rápidas.

        :param factor: factor de minimización
        """
        for split in self.dataset.keys():
            self.dataset[split] = self.dataset[split].shuffle(seed=SEED).select(range(int(len(self.dataset[split]) * factor)))

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
    def __init__(self, tokenizer_id: str, minimize_factor=None):
        dataset = load_dataset('json', data_files='datasets/CASTLE-C250.json', field='tests')
        super().__init__(tokenizer_id, dataset, 'code', minimize_factor=minimize_factor)

    def label(self, tk, examples):
        # convierto de True y False a 1 y 0
        tk['labels'] = [int(v) for v in examples['vulnerable']]

class TokenizedDraper(TokenizedDataset):
    def __init__(self, tokenizer_id: str, minimize_factor=None):
        self.code_snippet = 'functionSource'
        dataset = load_dataset("Joshfcooper/formai-v2-full")
        super().__init__(tokenizer_id, dataset, self.code_snippet, minimize_factor=minimize_factor)

    def label(self, tk, examples):
        tk['labels'] = []
        for i in range(len(examples[self.code_snippet])):
            has_vulnerability = any(
                examples[cwe][i] 
                for cwe in ['CWE-119', 'CWE-120', 'CWE-469', 'CWE-476', 'CWE-other']
            )
            tk['labels'].append(1 if has_vulnerability else 0)
    

class TokenizedFormAI(TokenizedDataset):
    def __init__(self, tokenizer_id: str, minimize_factor=None):
        self.code_snippet = "source_code"
        self.dataset = load_dataset("Joshfcooper/formai-v2-full")
        self.cleanup()
        super().__init__(tokenizer_id, self.dataset, self.code_snippet, minimize_factor=minimize_factor)

    def label(self, tk, examples):
        tk['labels'] = [0 if line == -1 else 1 for line in examples['vulnerable_line']]
    
    def cleanup(self):
        """ remove every row where 'verification_finished' is False """
        self.dataset = self.dataset.filter(lambda example: example['verification_finished'] == 'yes')
        
