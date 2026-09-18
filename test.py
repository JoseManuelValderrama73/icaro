from shared import *
from logger import ExecutionLogger
from model import Tester


settings = load_settings('test_settings.json')
models = settings['model'].split(",")
datasets = settings['dataset'].split(",")
files = settings['code_file'].split(",")

# Inicializar logger
logger = ExecutionLogger('testing', settings)
tester = Tester(logger)

i = 1
for m in models:
    for d in datasets:
        for f in files:
            logger.log_step("test.py", f"""Ejecucion {i}/{len(models)*len(datasets)*len(files)}
                                        Modelo: {m}
                                        Dataset: {d}
                                        Archivo: {f}
                                        """)
            i += 1
            try:
                result = tester.test(m, d, f)
                logger.log("classifier", f"Resultado de la clasificación: {result}")
                
                output = "El codigo es vulnerable" if result[0]['label'] == 'VULNERABLE' else "El código es seguro"
                print(output + " con una probabilidad del {:.3f}%".format(result[0]['score'] * 100))
                
            except Exception as e:
                logger.log_error("test.py", e)
                logger.finalize("test.py", "FAILED")
                raise

logger.finalize("test.py", "SUCCESS")
