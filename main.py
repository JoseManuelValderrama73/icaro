from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
import numpy as np
import evaluate
from constants import *
from tokenizer import *
from huggingface_hub import HfFolder, login

if HfFolder.get_token() is None:
    login()

"""
# 1. Define el mapeo de nombres
id2label = {0: "SAFE", 1: "VULNERABLE"}
label2id = {"SAFE": 0, "VULNERABLE": 1}

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL, 
    num_labels=2,
    id2label=id2label,
    label2id=label2id
)

if DATASET == 'castle':
    dataset = TokenizedCastle(tokenizer_id=MODEL)
elif DATASET == 'draper':
    dataset = TokenizedDraper(tokenizer_id=MODEL)
elif DATASET == 'formai':
    dataset = TokenizedFormAI(tokenizer_id=MODEL, minimize_factor=.01)

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
    load_best_model_at_end=True, # en cada epoch guarda el modelo y al final se queda el mejor
    metric_for_best_model="accuracy",
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    # logs
    logging_dir='./logs',
    logging_steps=10,
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

trainer.save_model(MODEL_SAVE_PATH)
dataset.tokenizer.save_pretrained(TOKENIZER_SAVE_PATH)

print(f"Modelo guardado exitosamente")
"""

from transformers import pipeline

# 1. Carga tu modelo entrenado y el tokenizador
# Reemplaza "./tu_modelo_entrenado" por la ruta de tu carpeta
classifier = pipeline("text-classification", model=MODEL_SAVE_PATH, tokenizer=TOKENIZER_SAVE_PATH)

# 2. Tu bloque de código C
codigo_c = """
void vulnerable_func(char *str) {
    char buffer[10];
    strcpy(buffer, str); // Posible Buffer Overflow
}
"""
codigo_c_safe = """
#include <stdio.h>

int main() {
    int a = 15;
    int b = 30;
    int suma = a + b;
    
    printf("La suma de %d y %d es: %d\n", a, b, suma);
    return 0;
}
"""

# 3. Realizar la predicción
resultado = classifier(codigo_c)

print(resultado)
# Salida esperada: [{'label': 'VULNERABLE', 'score': 0.98}]