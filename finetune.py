"""
Script principal para realizar el fine-tuning de modelos de lenguaje preentrenados
para la detección de vulnerabilidades en código fuente. Utiliza configuraciones
basadas en archivos JSON.
"""

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
        
        out_model_path = model_save_path(settings["model"], settings["dataset"])
        out_tokenizer_path = tokenizer_save_path(settings["model"], settings["dataset"])
        logger.log("finetune.py", f"El modelo se guardara en: {out_model_path}")
        logger.log("finetune.py", f"El Tokenizador se guardara en: {out_tokenizer_path}")

        trainer = model.train()

        trainer.save_model(out_model_path)
        logger.log_step("finetune.py", "Modelo guardado", "COMPLETED")
        
        model.dataset.tokenizer.save_pretrained(out_tokenizer_path)
        logger.log_step("finetune.py", "Tokenizador guardado", "COMPLETED")

        logger.log("finetune.py", f"Modelo guardado exitosamente en {out_model_path}\nTokenizador guardado exitosamente en {out_tokenizer_path}")
        
        logger.finalize("finetune.py", "SUCCESS")
        
    except Exception as e:
        logger.log_error("finetune.py", e)
        logger.finalize("finetune.py", "FAILED")
        raise