from datasets.load import DatasetDict
from transformers import AutoTokenizer
from datasets import load_dataset
from constants import *

class TokenizedCastle:
    # TODO: que la semilla sea algo diferente
    def __init__(self, tokenizer_id: str, test_size=.2, seed=42):
        self.dataset = load_dataset('json', data_files='datasets/CASTLE-C250.json', field='tests')
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)

        # remove any leftover tokenization columns that could have inconsistent lengths
        #token_cols = {'input_ids', 'attention_mask', 'token_type_ids', 'labels', 'special_tokens_mask', 'offset_mapping'}
        #for split in list(self.dataset.keys()):
        #    cols_to_remove = [c for c in self.dataset[split].column_names if c in token_cols]
        #    if cols_to_remove:
        #        self.dataset[split] = self.dataset[split].remove_columns(cols_to_remove)

        self.train_test_split(test_size, seed)

        self.dataset = self.dataset.map(self.tokenize, batched=True)
        '''
        try:
            self.dataset.cleanup_cache_files()
        except Exception:
            pass
        '''

        # optional quick sanity check
        #sample = self.dataset['train'][0]
        #print("tokenizer max_length:", self.max_length)
        #print("sample keys:", list(sample.keys()))
        #if 'input_ids' in sample:
        #    print("len(input_ids):", len(sample['input_ids']))

    def tokenize(self, examples):
        
        # use tokenizer/model max length but cap it to 512 for memory safety
        max_length = min(getattr(self.tokenizer, "model_max_length", 512), 512)
        tk = self.tokenizer(
            examples['code'],
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
        # convierto de True y False a 1 y 0
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
