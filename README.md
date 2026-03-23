# Vulnerabilidad en codigo C

## 1. Configuración del entorno virtual

`pip freeze > requirements.txt` para generar requirements

`pip install -r requirements.txt` para instalar los paquetes en requirements

## 2. Descargar modelo y dataset

Añadir a .bashrc:

    export HF_HUB_OFFLINE=0
    export TRANSFORMERS_OFFLINE=0
    export HF_DATASETS_OFFLINE=0

Si quieres cambiar el directorio por defecto añade:

    export HF_HOME=directorio deseado (ej. /mnt/beegfs/jmvs0008/huggingface)
    export TRANSFORMERS_CACHE=$HF_HOME/hub
    export HF_DATASETS_CACHE=$HF_HOME/datasets

### Modelos

    microsoft/deberta-base
    google-bert/bert-base-cased
    microsoft/graphcodebert-base

`hf download modelo --local-dir $HF_HOME/hub/modelo`

### Datasets

    castle
    draper - claudios/Draper
    formai - Joshfcooper/formai-v2-full
    bigvul - bstee615/bigvul

`hf download DS --repo-type dataset --local-dir $HF_HOME/datasets/DS`

## 3. Definir variables de entorno

Cambiar en .bashrc:

    export HF_HUB_OFFLINE=1
    export TRANSFORMERS_OFFLINE=1
    export HF_DATASETS_OFFLINE=1
