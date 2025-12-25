def training_output_dir(model, dataset):
    return f"training/{model.split('/')[-1]}/{dataset}"

def get_model(settings):
    from transformers import AutoModelForSequenceClassification

    id2label = {0: "SAFE", 1: "VULNERABLE"}
    label2id = {"SAFE": 0, "VULNERABLE": 1}
    """
    "microsoft/deberta-base"
    "google-bert/bert-base-cased"
    """
    return AutoModelForSequenceClassification.from_pretrained(
        settings["model"], 
        num_labels=2,
        id2label=id2label,
        label2id=label2id
    )
def get_dataset(settings):
    import tokenizer

    """
    castle
    draper
    formai
    """
    if settings["dataset"] == 'castle':
            dataset = tokenizer.TokenizedCastle(tokenizer_id=settings["model"])
    elif settings["dataset"] == 'draper':
            dataset = tokenizer.TokenizedDraper(tokenizer_id=settings["model"])
    elif settings["dataset"] == 'formai':
            dataset = tokenizer.TokenizedFormAI(tokenizer_id=settings["model"], minimize_factor=.01)
    else:
        raise ValueError("Dataset invalido")
    
    return dataset

def compute_metrics(eval_pred):
    import numpy as np

    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)
def train(model, dataset):
    from transformers import Trainer, TrainingArguments

    training_args = TrainingArguments(
        output_dir=training_output_dir(settings["model"], settings["dataset"]),
        eval_strategy='epoch',
        save_strategy='epoch',
        load_best_model_at_end=True, # en cada epoch guarda el modelo y al final se queda el mejor
        metric_for_best_model="accuracy",
        per_device_train_batch_size=settings["batch_size"],
        per_device_eval_batch_size=settings["batch_size"],
        num_train_epochs=settings["num_epochs"],
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
    return trainer


if __name__ == "__main__":
    import evaluate
    from constants import *
    from huggingface_hub import HfFolder, login

    if HfFolder.get_token() is None:
        login()
    settings = load_settings('finetune_settings.json')
    model = get_model(settings)
    dataset = get_dataset(settings)

    metric = evaluate.load("accuracy")

    trainer = train(model, dataset)

    trainer.save_model(model_save_path(settings["model"], settings["dataset"]))
    dataset.tokenizer.save_pretrained(tokenizer_save_path(settings["model"], settings["dataset"]))

    print(f"Modelo guardado exitosamente")