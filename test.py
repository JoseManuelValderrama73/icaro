def check_dirs(model_path, tokenizer_path, code_path):
    import os

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"La ruta al modelo '{model_path}' no existe.")
    if not os.path.exists(tokenizer_path):
        raise FileNotFoundError(f"La ruta al tokenizador '{tokenizer_path}' no existe.")
    if not os.path.exists(code_path):
        raise FileNotFoundError(f"La ruta {code_path} no existe. Actualiza el archivo de configuración con una ruta válida al código a analizar.")


if __name__ == "__main__":
    from shared import *
    from tokenizer import *
    from transformers import pipeline
    from logger import ExecutionLogger
    import torch


    settings = load_settings('test_settings.json')
    models = settings['model'].split(",")
    datasets = settings['dataset'].split(",")
    files = settings['code_file'].split(",")

    # Detección automática de GPU para inferencia
    device = 0 if torch.cuda.is_available() else -1

    # Inicializar logger
    logger = ExecutionLogger('testing', settings)
    
    i = 1
    for m in models:
        for d in datasets:
            for f in files:
                logger.log_step("test.py", f"""Testing execution {i}/{len(models)*len(datasets)*len(files)}
                                            Model: {m}
                                            Dataset: {d}
                                            File: {f}
                                            """)
                i += 1
                try:
                    model = model_save_path(m, d)
                    tokenizer = tokenizer_save_path(m, d)
                    logger.log("test.py", f"Model path: {model}")
                    logger.log("test.py", f"Tokenizer path: {tokenizer}")
                    
                    check_dirs(model, tokenizer, f)
                    logger.log_step("check_dirs", "Directories verified", "COMPLETED")

                    classifier = pipeline(
                        "text-classification", 
                        model=model, 
                        tokenizer=tokenizer,
                        truncation=True,
                        max_length=MAX_LENGHT,
                        device=device
                    )
                    logger.log_step("pipeline", "Pipeline loaded", "COMPLETED")

                    code = get_code(f)
                    logger.log_step("get_code", f"Code from {f} loaded and formatted", "COMPLETED")

                    # Check token length to warn if it will be truncated
                    tokens = classifier.tokenizer(code, truncation=False)
                    num_tokens = len(tokens['input_ids'])
                    if num_tokens > MAX_LENGHT:
                        logger.log("test.py", f"⚠️ ¡ADVERTENCIA! El código en {f} tiene {num_tokens} tokens. Supera el max_length configurado ({max_length}) y será truncado. Esto puede empeorar las predicciones.")

                    result = classifier(code)
                    logger.log("classifier", f"Classification result: {result}")
                    
                    output = "El codigo es vulnerable" if result[0]['label'] == 'VULNERABLE' else "El código es seguro"
                    print(output + " con una probabilidad del {:.3f}%".format(result[0]['score'] * 100))
                    
                except Exception as e:
                    logger.log_error("test.py", e)
                    logger.finalize("test.py", "FAILED")
                    raise

    logger.finalize("test.py", "SUCCESS")
