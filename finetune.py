from transformers import EarlyStoppingCallback

def get_model(settings):
    from transformers import AutoModelForSequenceClassification

    id2label = {0: "SAFE", 1: "VULNERABLE"}
    label2id = {"SAFE": 0, "VULNERABLE": 1}

    #import os
    #if not os.path.exists(settings["model_path"]):
    #    raise ValueError(f"El path del modelo no existe: {settings['model_path']}. Asegúrate de haber descargado el modelo correctamente según las instrucciones en README.")

    return AutoModelForSequenceClassification.from_pretrained(
        settings["model_path"], 
        num_labels=2,
        id2label=id2label,
        label2id=label2id,
        local_files_only=True
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
    import torch

    # Detección automática de hardware para usar la mejor precisión mixta posible
    use_bf16 = False
    use_fp16 = False
    if torch.cuda.is_available():
        if torch.cuda.is_bf16_supported():
            use_bf16 = True
            print("🚀 Hardware soporta BF16 (ej. Ampere). Activando precisión mixta BF16.")
        else:
            use_fp16 = True
            print("⚠️ Hardware NO soporta BF16 (ej. Volta/Turing). Activando precisión mixta FP16.")

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
        learning_rate=settings.get("learning_rate", 5e-5),
        warmup_ratio=settings.get("warmup_ratio", 0.0),
        weight_decay=settings.get("weight_decay", 0.0),
        num_train_epochs=settings["num_epochs"],
        # logs
        logging_dir=TRAINING_LOG_PATH,
        logging_steps=10,
        report_to="tensorboard",
        bf16=settings.get("bf16", use_bf16),
        fp16=settings.get("fp16", use_fp16),
        dataloader_num_workers=settings.get("dataloader_num_workers", 4),
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset['train'],
        eval_dataset=dataset['validation'],
        compute_metrics=compute_metrics,
        processing_class=dataset.tokenizer,
        #data_collator=data_collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=settings.get("early_stopping_patience", 3))],
    )

    import os
    from transformers.trainer_utils import get_last_checkpoint
    
    # Intentar recuperar el último checkpoint si el entrenamiento se interrumpió
    last_checkpoint = None
    if os.path.isdir(training_args.output_dir):
        last_checkpoint = get_last_checkpoint(training_args.output_dir)
        
    if last_checkpoint is not None:
        print(f"Resumiendo entrenamiento desde checkpoint: {last_checkpoint}")
        trainer.train(resume_from_checkpoint=last_checkpoint)
    else:
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