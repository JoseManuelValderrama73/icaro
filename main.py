import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "microsoft/deberta-base-mnli"
tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-base-mnli")
model = AutoModelForSequenceClassification.from_pretrained("microsoft/deberta-base-mnli", device_map="auto")

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
