from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
import numpy as np
import evaluate, torch
from constants import *
from tokenizer import *
from huggingface_hub import HfFolder, login

if HfFolder.get_token() is None:
    login()

model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2) # 2 etiquetas: vulnerable o no vulnerable
if DATASET == 'castle':
    dataset = TokenizedCastle(tokenizer_id=MODEL)
elif DATASET == 'draper':
    dataset = TokenizedDraper(tokenizer_id=MODEL)
elif DATASET == 'formai':
    dataset = TokenizedFormAI(tokenizer_id=MODEL, minimize_factor=.001)
else:
    raise ValueError("Dataset invalido")

metric = evaluate.load("accuracy")
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(
    output_dir=TRAINING_OUTPUT_DIR,
    eval_strategy='epoch',
    save_strategy='epoch',
    metric_for_best_model="accuracy",
    load_best_model_at_end=True, # en cada epoch guarda el modelo y luego se queda con el mejor
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    # logs
    logging_dir='./logs',
    logging_steps=10,
    save_strategy="epoch",
    report_to="tensorboard",
    #load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test'],
    compute_metrics=compute_metrics,
)

trainer.train()

inputs = dataset.tokenizer(
    """
    #include <stdio.h>

    int main() {
        int a = 15;
        int b = 30;
        int suma = a + b;
        
        printf("La suma de %d y %d es: %d\n", a, b, suma);
        return 0;
    }
    """,
    return_tensors="pt"
).to(model.device)

with torch.no_grad():
    logits = model(**inputs).logits
    predicted_class = logits.argmax().item()

print(f"The predicted relation is: {predicted_class}")