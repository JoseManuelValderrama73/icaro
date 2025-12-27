def check_dirs(model_path, tokenizer_path):
    import os

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"{model_path} no existe.")
    if not os.path.exists(tokenizer_path):
        raise FileNotFoundError(f"{tokenizer_path} no existe.")

if __name__ == "__main__":
    from constants import *
    from tokenizer import *
    from huggingface_hub import HfFolder, login
    from transformers import pipeline
    from logger import ExecutionLogger

    if HfFolder.get_token() is None:
        login()

    settings = load_settings('test_settings.json')
    
    # Inicializar logger
    logger = ExecutionLogger('testing', settings)
    logger.log_step("test.py", "Testing execution")
    
    try:
        model = model_save_path(settings["model"], settings["dataset"])
        tokenizer = tokenizer_save_path(settings["model"], settings["dataset"])
        logger.log("test.py", f"Model path: {model}")
        logger.log("test.py", f"Tokenizer path: {tokenizer}")
        
        check_dirs(model, tokenizer)
        logger.log_step("test.py", "Directories verified", "COMPLETED")

        classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
        logger.log_step("test.py", "Pipeline loaded", "COMPLETED")

        result = classifier(settings["code"])
        logger.log("test.py", f"Classification result: {result}")
        
        print(result)
        
        logger.finalize("test.py", "SUCCESS")
        
    except Exception as e:
        logger.log_error("test.py", e)
        logger.finalize("test.py", "FAILED")
        raise
