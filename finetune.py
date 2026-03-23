from transformers import TrainerCallback

class EarlyStoppingCallback(TrainerCallback):
    def __init__(self, num_steps):
        self.num_steps = num_steps

    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step >= self.num_steps:
            control.should_training_stop = True
        return control

def get_model(settings):
    from transformers import AutoModelForSequenceClassification

    id2label = {0: "SAFE", 1: "VULNERABLE"}
    label2id = {"SAFE": 0, "VULNERABLE": 1}

    #import os
    #if not os.path.exists(settings["model_path"]):
    #    raise ValueError(f"El path del modelo no existe: {settings['model_path']}. Asegúrate de haber descargado el modelo correctamente según las instrucciones en README.")

    max_length = settings.get("max_length", 1024)
    return AutoModelForSequenceClassification.from_pretrained(
        settings["model_path"], 
        num_labels=2,
        id2label=id2label,
        label2id=label2id,
        max_position_embeddings=max_length + 2, # +2 for RoBERTa special tokens
        ignore_mismatched_sizes=True,
        local_files_only=False
    )
def get_dataset(settings, logger):
    import tokenizer
    dataset = tokenizer.TokenizedCombo(settings, logger)
    
    return dataset

def compute_metrics(eval_pred):
    import numpy as np
    from sklearn.metrics import f1_score, precision_score, recall_score

    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    return {
        "f1":        f1_score(labels, predictions),
        "precision": precision_score(labels, predictions),
        "recall":    recall_score(labels, predictions),
        "accuracy":  (predictions == labels).mean()
    }

def train(model, dataset):
    from transformers import Trainer, TrainingArguments

    training_args = TrainingArguments(
        output_dir=training_output_dir(settings["model"], settings["dataset"]),
        eval_strategy='epoch',
        save_strategy='epoch',
        load_best_model_at_end=True, # en cada epoch guarda el modelo y al final se queda el mejor
        metric_for_best_model="f1",
        greater_is_better=True,
        per_device_train_batch_size=settings["batch_size"],
        per_device_eval_batch_size=settings["batch_size"],
        gradient_accumulation_steps=settings["gradient_accumulation_steps"],
        num_train_epochs=settings["num_epochs"],
        # logs
        logging_dir=TRAINING_LOG_PATH,
        logging_steps=10,
        report_to="tensorboard",
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset['train'],
        eval_dataset=dataset['validation'],
        compute_metrics=compute_metrics,
        processing_class=dataset.tokenizer,
        #data_collator=data_collator,
        callbacks=[EarlyStoppingCallback(num_steps=settings["stopping_steps"])],
    )

    trainer.train()
    return trainer


if __name__ == "__main__":
    from shared import *
    from logger import ExecutionLogger

    settings = load_settings('finetune_settings.json')
    
    # Inicializar logger
    logger = ExecutionLogger('finetuning', settings)
    logger.log_step("finetune.py", "Finetuning execution")
    
    try:
        model = get_model(settings)
        logger.log_step("finetune.py", "Model loaded", "COMPLETED")
        
        dataset = get_dataset(settings, logger)
        logger.log_step("finetune.py", "Dataset loaded", "COMPLETED")
        
        model_save_path = model_save_path(settings["model"], settings["dataset"])
        tokenizer_save_path = tokenizer_save_path(settings["model"], settings["dataset"])
        logger.log("finetune.py", f"Model will be saved to: {model_save_path}")
        logger.log("finetune.py", f"Tokenizer will be saved to: {tokenizer_save_path}")

        trainer = train(model, dataset)
        logger.log_step("finetune.py", "Training process", "COMPLETED")

        trainer.save_model(model_save_path)
        logger.log_step("finetune.py", "Model saved", "COMPLETED")
        
        dataset.tokenizer.save_pretrained(tokenizer_save_path)
        logger.log_step("finetune.py", "Tokenizer saved", "COMPLETED")

        print(f"Modelo guardado exitosamente en {model_save_path}\nTokenizador guardado exitosamente en {tokenizer_save_path}")
        
        logger.finalize("finetune.py", "SUCCESS")
        
    except Exception as e:
        logger.log_error("finetune.py", e)
        logger.finalize("finetune.py", "FAILED")
        raise