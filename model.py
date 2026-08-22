from logger import ExecutionLogger

class Model:
    def __init__(self, settings: dict, logger: ExecutionLogger):
        self.logger = logger
        self.settings = settings
        self.model = self.__get_model()
        self.dataset = self.__get_dataset()

    def train(self):
        from transformers import Trainer, TrainingArguments, EarlyStoppingCallback
        from shared import NUM_GPUS, TRAINING_LOG_PATH, training_output_dir

        self.logger.log_step("Model::train", "Proceso de entrenamiento", "STARTED")

        use_bf16, use_fp16 = self.__use_mixed_precision()

        training_args = TrainingArguments(
            output_dir=training_output_dir(self.settings["model"], self.settings["dataset"]),
            eval_strategy='epoch',
            save_strategy='epoch',
            load_best_model_at_end=True, # en cada epoch guarda el modelo y al final se queda el mejor
            metric_for_best_model="f1",
            greater_is_better=True,
            per_device_train_batch_size=self.settings["batch_size"],
            per_device_eval_batch_size=self.settings["batch_size"],
            gradient_accumulation_steps=self.settings["gradient_accumulation_steps"],
            learning_rate=self.settings["learning_rate"],
            warmup_ratio=self.settings["warmup_ratio"],
            weight_decay=self.settings["weight_decay"],
            num_train_epochs=self.settings["num_epochs"],
            # logs
            logging_dir=TRAINING_LOG_PATH,
            logging_steps=10,
            report_to="tensorboard",
            bf16=use_bf16,
            fp16=use_fp16,
            dataloader_num_workers=NUM_GPUS,
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset['train'],
            eval_dataset=self.dataset['validation'],
            compute_metrics=self.__compute_metrics,
            processing_class=self.dataset.tokenizer,
            #data_collator=data_collator,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=self.settings["early_stopping_patience"])],
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
            
        self.logger.log_step("Model::train", "Proceso de entrenamiento", "COMPLETED")
        return trainer

    def __get_model(self):
        from transformers import AutoModelForSequenceClassification
        from shared import OFFLINE

        self.logger.log_step("Model::__get_model", "Cargando modelo", "STARTED")

        id2label = {0: "SAFE", 1: "VULNERABLE"}
        label2id = {"SAFE": 0, "VULNERABLE": 1}

        if OFFLINE:
            import os
            if not os.path.exists(settings["model_path"]):
                raise ValueError(f"El path del modelo no existe: {settings['model_path']}. Asegúrate de haber descargado el modelo correctamente según las instrucciones en README.")

        model = AutoModelForSequenceClassification.from_pretrained(
            self.settings["model_path"], 
            num_labels=2,
            id2label=id2label,
            label2id=label2id,
            local_files_only=OFFLINE
        )

        self.logger.log_step("Model::__get_model", "Modelo cargado", "COMPLETED")

        return model
        
    def __get_dataset(self):
        self.logger.log_step("Model::__get_dataset", "Cargando dataset", "STARTED")
        import tokenizer
        dataset = tokenizer.TokenizedCombo(self.settings, self.logger)
        
        self.logger.log_step("Model::__get_dataset", "Dataset cargado", "COMPLETED")
        return dataset

    def __compute_metrics(self, eval_pred):
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

    def __use_mixed_precision(self):
        import torch
        use_bf16, use_fp16 = False, False
        if torch.cuda.is_available():
            if torch.cuda.is_bf16_supported():
                use_bf16 = True
                self.logger.log("Model::__use_mixed_precision", "Hardware soporta BF16. Activando precisión mixta BF16.")
            else:
                use_fp16 = True
                self.logger.log("Model::__use_mixed_precision", "Hardware NO soporta BF16. Activando precisión mixta FP16.")
        else:
            self.logger.log("Model::__use_mixed_precision", "No se ha detectado GPU. Se usará precisión estándar.")
        
        return use_bf16, use_fp16