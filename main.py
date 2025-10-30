from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
import numpy as np
import evaluate
from constants import *
from tokenized_castle import TokenizedCastle

#from huggingface_hub import login
#login()

model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2) # 2 etiquetas: vulnerable o no vulnerable

dataset = TokenizedCastle(tokenizer_id=MODEL)

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(
    output_dir=TRAINING_OUTPUT_DIR + 'castle',
    eval_strategy='epoch',  # Enable evaluation
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
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
    eval_dataset=dataset['test'],
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