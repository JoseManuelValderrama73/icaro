from datasets.load import DatasetDict
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import numpy as np
import evaluate
from huggingface_hub import login

#login()

# bert tiny necesita padding
"""
"microsoft/deberta-base-mnli"
"google-bert/bert-base-cased"
"prajjwal1/bert-tiny"
"""
MODEL = "google-bert/bert-base-cased"
"""
"SetFit/emotion"
'yelp_review_full'
"""
DATASET = "yelp_review_full"

access_token = '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'


tokenizer = AutoTokenizer.from_pretrained(MODEL, token=access_token)

model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2) # 2 etiquetas: vulnerable o no vulnerable

def tokenize(examples):
    tk = tokenizer(
        examples['code'],
        padding="max_length",
        truncation=True,
        #max_length=512  # Add max_length to prevent excessive padding
    )
    # Convertimos True y False a 1 y 0
    tk['labels'] = [int(v) for v in examples['vulnerable']]
    return tk

dataset = load_dataset('json', data_files='datasets/CASTLE-C250.json', field='tests')
# dividir en train (80%) y test (20%)
train_test = dataset['train'].train_test_split(test_size=0.2, seed=42)
dataset = DatasetDict({
    'train': train_test['train'],
    'test': train_test['test']
})
dataset = dataset.map(tokenize, batched=True)

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    # convert the logits to their predicted class
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(
    output_dir="training/castle",
    eval_strategy='epoch',  # Enable evaluation
    per_device_train_batch_size=10,
    per_device_eval_batch_size=10,
    num_train_epochs=3,
    #logging_dir='./logs',
    #logging_steps=100,
    #save_strategy="epoch",
    #load_best_model_at_end=True,
    #metric_for_best_model="accuracy"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test'],  # Uncomment this
    compute_metrics=compute_metrics,  # Uncomment this
)
trainer.train()
"""

inputs = tokenizer(
    "A soccer game with multiple people playing.",
    "Some people are playing a sport.",
    return_tensors="pt"
).to(model.device)

with torch.no_grad():
    logits = model(**inputs).logits
    predicted_class = logits.argmax().item()

labels = ["contradiction", "neutral", "entailment"]
print(f"The predicted relation is: {labels[predicted_class]}")

"""