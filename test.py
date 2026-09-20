"""
Script principal para la evaluación de modelos (inferencia). Carga los modelos entrenados
previamente y evalúa si archivos de código fuente especificados son seguros o vulnerables.
"""

from shared import *
from logger import ExecutionLogger
from model import Tester


settings = load_settings('test_settings.json')
models = [x.strip() for x in settings['model'].split(",")]
datasets = [x.strip() for x in settings['dataset'].split(",")]
files = [x.strip() for x in settings['code_file'].split(",")]

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
                                        Archivo: {f}""")
            i += 1
            try:
                result = tester.test(m, d, f)
                logger.log_step("test.py", f"{result}", "COMPLETED")
                
                output = "El codigo es vulnerable" if result[0]['label'] == 'VULNERABLE' else "El código es seguro"
                logger.log("test.py", output + " con una probabilidad del {:.3f}%".format(result[0]['score'] * 100) + "\n\n")
                
                
            except Exception as e:
                logger.log_error("test.py", e)
                logger.finalize("test.py", "FAILED")
                raise

logger.finalize("test.py", "SUCCESS")
