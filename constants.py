# TODO: que la semilla sea algo diferente
SEED = 42

def load_settings(file: str):
    import json
    with open(file, 'r') as file:
        settings = json.load(file)
    return settings

def model_save_path(model, dataset):
    return f"modelos/{model.split('/')[-1]}-{dataset}"
def tokenizer_save_path(model, dataset):
    return f"tokenizers/{model.split('/')[-1]}-{dataset}"

