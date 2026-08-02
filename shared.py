from logger import ExecutionLogger

# EDITABLES
MAX_LENGHT = 512

def training_output_dir(model, dataset):
    return f"training/{model.split('/')[-1]}/{dataset}"

def model_save_path(model, dataset):
    return f"modelos/{model.split('/')[-1]}/{dataset}"
def tokenizer_save_path(model, dataset):
    return f"tokenizers/{model.split('/')[-1]}/{dataset}"

TRAINING_LOG_PATH = "logs/training/"
def finetuning_log_path(model, dataset):
    return f"logs/finetuning/{model.split('/')[-1]}/{dataset}"
def testing_log_path(model, dataset):
    return f"logs/testing/{model.split('/')[-1]}/{dataset}"

# FUNCIONES COMPARTIDAS
def clean_code(code: str) -> str:
    """
    Limpia una cadena de código fuente.
    Elimina comentarios y sustituye tabulaciones por espacios.
    """
    import re
    # Remove multi-line comments /* */
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove single-line comments //
    code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
    
    # Replace tabs with spaces
    code = code.replace('\t', '    ')
    
    return code

def get_code(file_path: str) -> str:
    """
    Lee y formatea el código fuente desde un archivo.
    Elimina comentarios y sustituye tabulaciones por espacios.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    return clean_code(code)

def get_seed(settings: dict, logger: ExecutionLogger) -> int:
    """
    Obtiene una semilla para la aleatoriedad. Si 'seed' está presente en settings, se utiliza ese valor.
    De lo contrario, se genera una semilla determinística basada en la marca de tiempo actual.
    
    :param settings: Configuración que puede contener la semilla
    :param logger: Logger para registrar los pasos
    """

    if 'seed' in settings:
        if logger: logger.log_step("get_seed", f"Generated seed: {settings['seed']} (from settings)", "COMPLETED")
        return settings['seed']
    
    import hashlib
    from datetime import datetime

    timestamp = datetime.now().isoformat()
    hash_object = hashlib.md5(timestamp.encode())
    seed = int(hash_object.hexdigest()[:8], 16)
    if logger: logger.log_step("get_seed", f"Generated seed: {seed} (timestamp: {timestamp})", "COMPLETED")
    return seed

def load_settings(file: str):
    import json
    with open(file, 'r') as file:
        settings = json.load(file)
    return settings