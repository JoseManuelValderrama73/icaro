def get_model(settings):
    from transformers import AutoModelForSequenceClassification

    id2label = {0: "SAFE", 1: "VULNERABLE"}
    label2id = {"SAFE": 0, "VULNERABLE": 1}

    import os
    if not os.path.exists(settings["model_path"]):
        raise ValueError(f"El path del modelo no existe: {settings['model_path']}. Asegúrate de haber descargado el modelo correctamente según las instrucciones en README.")

    return AutoModelForSequenceClassification.from_pretrained(
        settings["model_path"], 
        num_labels=2,
        id2label=id2label,
        label2id=label2id,
        local_files_only=True
    )
def get_dataset(settings, logger):
    import tokenizer

    if settings["dataset"] == 'castle':
            dataset = tokenizer.TokenizedCastle(settings, logger)
    elif settings["dataset"] == 'draper':
            dataset = tokenizer.TokenizedDraper(settings, logger)
    elif settings["dataset"] == 'formai':
            dataset = tokenizer.TokenizedFormAI(settings, logger)
    else:
        raise ValueError("Dataset invalido")
    
    return dataset

def compute_metrics(eval_pred):
    import numpy as np

    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    
    accuracy = (predictions == labels).mean()
    return {"accuracy": accuracy}

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
        gradient_accumulation_steps=settings.get("gradient_accumulation_steps", 1),
        num_train_epochs=settings["num_epochs"],
        # logs
        logging_dir=TRAINING_LOG_PATH,
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
    from constants import *
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