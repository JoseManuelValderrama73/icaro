def get_seed(settings: dict) -> int:
    """
    Obtiene una semilla para la aleatoriedad. Si 'seed' está presente en settings, se utiliza ese valor.
    De lo contrario, se genera una semilla determinística basada en la marca de tiempo actual.
    
    :param settings: Configuración que puede contener la semilla
    """
    if 'seed' in settings:
        return settings['seed']
    
    import hashlib
    from datetime import datetime

    timestamp = datetime.now().isoformat()
    hash_object = hashlib.md5(timestamp.encode())
    seed = int(hash_object.hexdigest()[:8], 16)
    print(f"Generated seed: {seed} (timestamp: {timestamp})")
    return seed

TRAINING_LOGGING_DIR = "logs/training/"

def load_settings(file: str):
    import json
    with open(file, 'r') as file:
        settings = json.load(file)
    return settings

def training_output_dir(model, dataset):
    return f"training/{model.split('/')[-1]}/{dataset}"
def model_save_path(model, dataset):
    return f"modelos/{model.split('/')[-1]}/{dataset}"
def tokenizer_save_path(model, dataset):
    return f"tokenizers/{model.split('/')[-1]}/{dataset}"
def finetuning_log_path(model, dataset):
    return f"logs/finetuning/{model.split('/')[-1]}/{dataset}"
def testing_log_path(model, dataset):
    return f"logs/testing/{model.split('/')[-1]}/{dataset}"

