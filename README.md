# Vulnerabilidad en codigo C

## 1. Configuración del entorno virtual

`pip freeze > requirements.txt` para generar requirements

`pip install -r requirements.txt` para instalar los paquetes en requirements

## 2. Definir variables de entorno

Añadir a .bashrc:

    export HF_HUB_OFFLINE=1
    export TRANSFORMERS_OFFLINE=1
    export HF_DATASETS_OFFLINE=1

Si quieres cambiar el directorio por defecto añade:

    export HF_HOME=directorio deseado
    export TRANSFORMERS_CACHE=$HF_HOME/hub
    export HF_DATASETS_CACHE=$HF_HOME/datasets

## 3. Descargar modelo y dataset

### Modelos

    microsoft/deberta-base
    google-bert/bert-base-cased

`hf download modelo --local-dir $HF_HOME/hub/modelo`

### Datasets

    castle
    draper - claudios/Draper
    formai - Joshfcooper/formai-v2-full

`hf download ds --repo-type dataset --local-dir $HF_HOME/datasets/ds`
