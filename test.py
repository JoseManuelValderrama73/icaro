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

    if HfFolder.get_token() is None:
        login()

    settings = load_settings('test_settings.json')

    model = model_save_path(settings["model"], settings["dataset"])
    tokenizer = tokenizer_save_path(settings["model"], settings["dataset"])
    check_dirs(model, tokenizer)

    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    print(classifier(settings["safe_code"]))
