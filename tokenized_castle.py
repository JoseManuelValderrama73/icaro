from datasets.load import DatasetDict
from transformers import AutoTokenizer
from datasets import load_dataset
from constants import *

class TokenizedCastle:
    # TODO: que la semilla sea algo diferente
    def __init__(self, tokenizer_id: str, test_size=.2, seed=42):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)

        self.dataset = load_dataset('json', data_files='datasets/CASTLE-C250.json', field='tests')

        self.train_test_split(test_size, seed)

        self.dataset = self.dataset.map(self.tokenize, batched=True)

    def tokenize(self, examples):
        tk = self.tokenizer(
            examples['code'],
            padding="max_length",
            truncation=True,
            #max_length=512  # Add max_length to prevent excessive padding
        )
        # Convertimos True y False a 1 y 0
        tk['labels'] = [int(v) for v in examples['vulnerable']]
        return tk

    def train_test_split(self, test_size, seed):
        train_test = self.dataset['train'].train_test_split(test_size=test_size, seed=seed)
        self.dataset = DatasetDict({
            'train': train_test['train'],
            'test': train_test['test']
        })

    def __getitem__(self, idx):
        return self.dataset[idx]

    def __len__(self):
        return len(self.dataset)
