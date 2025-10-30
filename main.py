import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import numpy as np
import evaluate
from huggingface_hub import login

#login()

# bert tiny necesita padding
MODELS = ["microsoft/deberta-base-mnli", "google-bert/bert-base-cased", "prajjwal1/bert-tiny"]
M = 1
DATASETS = ["SetFit/emotion", 'yelp_review_full']
D = 1

access_token = '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'

# cargo un dataset y lo hago mas pequeño para poder entrenarlo rapido
dataset = load_dataset(DATASETS[D])
dataset["train"] = dataset["train"].shuffle(seed=42).select(range(6500))
dataset["test"] = dataset["test"].shuffle(seed=42).select(range(1000))

tokenizer = AutoTokenizer.from_pretrained(MODELS[M], token=access_token)
print(dataset)

model = AutoModelForSequenceClassification.from_pretrained(MODELS[M], num_labels=5)

def tokenize(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

dataset = dataset.map(tokenize, batched=True)

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    # convert the logits to their predicted class
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(
    output_dir="yelp_review_classifier",
    eval_strategy="epoch",
    per_device_train_batch_size=10,
    per_device_eval_batch_size=10,
    num_train_epochs=1,
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics,
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