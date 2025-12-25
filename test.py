if __name__ == "__main__":
    from constants import *
    from tokenizer import *
    from huggingface_hub import HfFolder, login
    from transformers import pipeline

    if HfFolder.get_token() is None:
        login()

    settings = load_settings('test_settings.json')

    classifier = pipeline("text-classification", model=model_save_path(settings["model"], settings["dataset"]), tokenizer=tokenizer_save_path(settings["model"], settings["dataset"]))

    print(classifier(settings["safe_code"]))
