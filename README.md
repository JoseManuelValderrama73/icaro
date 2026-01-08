# Vulnerabilidad en codigo C

### Configuración del entorno virtual

`pip freeze > requirements.txt` para generar requirements

`pip install -r requirements.txt` para instalar los paquetes en requirements

## Opciones de configuración

### Modelos

    microsoft/deberta-base
    google-bert/bert-base-cased

### Datasets

    castle
    draper
    formai

hf download microsoft/deberta-base --local-dir $HF_HOME/hub/microsoft_deberta-base
hf download datasets/imdb --repo-type dataset --local-dir $HF_HOME/datasets/imdb
