def check_dirs(model_path, tokenizer_path, code_path):
    import os

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"La ruta al modelo '{model_path}' no existe.")
    if not os.path.exists(tokenizer_path):
        raise FileNotFoundError(f"La ruta al tokenizador '{tokenizer_path}' no existe.")
    if not os.path.exists(code_path):
        raise FileNotFoundError(f"La ruta {code_path} no existe. Actualiza el archivo de configuración con una ruta válida al código a analizar.")

def get_code(file_path: str) -> str:
    """
    Lee y formatea el código fuente desde un archivo.
    Elimina comentarios y sustituye tabulaciones por espacios.
    """
    import re
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Remove multi-line comments /* */
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove single-line comments //
    code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
    
    # Replace tabs with spaces
    code = code.replace('\t', '    ')
    
    return code

if __name__ == "__main__":
    from constants import *
    from tokenizer import *
    from transformers import pipeline
    from logger import ExecutionLogger


    settings = load_settings('test_settings.json')
    
    # Inicializar logger
    logger = ExecutionLogger('testing', settings)
    logger.log_step("test.py", "Testing execution")
    
    try:
        model = model_save_path(settings["model"], settings["dataset"])
        tokenizer = tokenizer_save_path(settings["model"], settings["dataset"])
        logger.log("test.py", f"Model path: {model}")
        logger.log("test.py", f"Tokenizer path: {tokenizer}")
        
        check_dirs(model, tokenizer, settings["code_file"])
        logger.log_step("check_dirs", "Directories verified", "COMPLETED")

        classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
        logger.log_step("pipeline", "Pipeline loaded", "COMPLETED")

        code = get_code(settings["code_file"])
        logger.log_step("get_code", f"Code from {settings['code_file']} loaded and formatted", "COMPLETED")

        result = classifier(code)
        logger.log("classifier", f"Classification result: {result}")
        
        
        logger.finalize("test.py", "SUCCESS")
        output = "El codigo es vulnerable" if result[0]['label'] == 'VULNERABLE' else "El código es seguro"
        print(output + " con una probabilidad del {:.3f}%".format(result[0]['score'] * 100))
        
    except Exception as e:
        logger.log_error("test.py", e)
        logger.finalize("test.py", "FAILED")
        raise
