if __name__ == "__main__":
    from shared import *
    from logger import ExecutionLogger
    from model import Trainer

    settings = load_settings('finetune_settings.json')
    
    # Inicializar logger
    logger = ExecutionLogger('finetuning', settings)
    logger.log_step("finetune.py", "Ejecutando Finetune")
    
    try:
        model = Trainer(settings, logger)
        
        model_save_path = model_save_path(settings["model"], settings["dataset"])
        tokenizer_save_path = tokenizer_save_path(settings["model"], settings["dataset"])
        logger.log("finetune.py", f"El modelo se guardara en: {model_save_path}")
        logger.log("finetune.py", f"El Tokenizador se guardara en: {tokenizer_save_path}")

        trainer = model.train()

        trainer.save_model(model_save_path)
        logger.log_step("finetune.py", "Modelo guardado", "COMPLETED")
        
        model.dataset.tokenizer.save_pretrained(tokenizer_save_path)
        logger.log_step("finetune.py", "Tokenizador guardado", "COMPLETED")

        logger.log("finetune.py", f"Modelo guardado exitosamente en {model_save_path}\nTokenizador guardado exitosamente en {tokenizer_save_path}")
        
        logger.finalize("finetune.py", "SUCCESS")
        
    except Exception as e:
        logger.log_error("finetune.py", e)
        logger.finalize("finetune.py", "FAILED")
        raise