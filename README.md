# Vulnerabilidad en codigo C

# Setup ADA

## 1. Cambios en el codigo:

1. finetune.py::get_model - descomentar tres lineas y cambiar "local_files_only=True".

## 2. Configuración del entorno virtual

`pip freeze > requirements.txt` para generar requirements

`pip install -r requirements.txt` para instalar los paquetes en requirements

## 3. Descargar modelo y dataset

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

## 4. Definir variables de entorno

Cambiar en .bashrc:

    export HF_HUB_OFFLINE=1
    export TRANSFORMERS_OFFLINE=1
    export HF_DATASETS_OFFLINE=1

## 5. Configuración de parámetros

El proyecto se configura a través de archivos JSON. Estos son todos los parámetros posibles:

### `finetune_settings.json` (Ajuste fino del modelo)

- **`model`**: Nombre base o alias del modelo a ajustar.
- **`model_path`**: Ruta local o ID de Hugging Face del modelo base preentrenado (ej. `microsoft/graphcodebert-base`).
- **`dataset`**: Nombre que se le asignará al dataset combinado resultante.
- **`dataset_path`**: Nombres o IDs en Hugging Face de los datasets a utilizar, separados por comas.
- **`minimize_factor`**: Factor de reducción del dataset. `1` para utilizar todo el dataset, o un valor entre `0` y `1` para tomar solo una fracción.
- **`test_size`**: Porcentaje del dataset que se reservará para evaluación/validación (ej. `0.2` para un 20%).
- **`num_epochs`**: Número de épocas de entrenamiento.
- **`batch_size`**: Tamaño del lote (batch size) tanto para entrenamiento como para evaluación.
- **`gradient_accumulation_steps`**: Número de pasos para la acumulación de gradientes antes de actualizar los pesos.
- **`learning_rate`**: Tasa de aprendizaje inicial.
- **`warmup_ratio`**: Proporción del total de pasos de entrenamiento que se utilizarán para el calentamiento del learning rate.
- **`weight_decay`**: Decaimiento de pesos utilizado por el optimizador.
- **`max_length`**: Longitud máxima (en número de tokens) permitida para las secuencias de entrada.
- **`seed`**: Semilla aleatoria para garantizar la reproducibilidad de los resultados.
- **`stopping_steps`** _(Opcional)_: Pasos máximos para usar en un callback de _Early Stopping_ (detener el entrenamiento antes si se alcanza este global step).
- _(Nota: cualquier campo que empiece por `_` como `_model_path` o `_comment:minimize_factor` es ignorado por el código y actúa como un comentario)._

### `test_settings.json` (Evaluación del modelo ajustado)

- **`model`**: Nombres de los modelos ajustados a evaluar (se pueden poner varios separados por comas).
- **`dataset`**: Nombres de los datasets con los que fue ajustado el modelo (separados por comas) para encontrar su ruta.
- **`code_file`**: Rutas relativas o absolutas de los archivos `.c` que se desean evaluar (separados por comas).
- **`max_length`** _(Opcional)_: Longitud máxima de los tokens; por defecto usará 1024.

### `launcher.sbs` (Lanzador para Slurm)

Define la configuración del trabajo en el clúster:

- **`--partition`**: Cola de ejecución (ej. normal).
- **`--gres=gpu:1`**: Solicitud de GPUs.
- **`--mem`**: Memoria RAM asignada.
- **`--cpus-per-task`**: Hilos/CPU asignados.

## 6. Estructura del Proyecto

El repositorio está organizado en las siguientes carpetas principales:

- **`codigo/`**: Directorio donde se almacenan los códigos fuente `.c` (ej. `suma.c`, datasets de CASTLE, etc.) que se van a procesar y evaluar con los modelos para buscar vulnerabilidades.
- **`datasets/`**: Almacena de forma local los archivos de datos (datasets como _bigvul_, _formai_, etc.) descargados y estructurados (por ejemplo en formato JSON) utilizados en el finetuning.
- **`logs/`**: Guarda los registros (logs) de ejecución estructurados, divididos por procesos como `finetuning` y `testing`. También está `logs_ejecucion` generado por Slurm.
- **`modelos/`**: Carpeta donde se guardan de forma local los modelos que ya han sido ajustados (finetuned) a lo largo del proceso de entrenamiento.
- **`pretrained_models/`**: Ubicación para descargar o cachear de forma local los modelos base sin ajustar de Hugging Face.
- **`tokenizers/`**: Directorio para guardar de forma persistente los tokenizadores locales correspondientes a cada modelo, sean preentrenados o generados durante el ajuste.
- **`training/`**: Directorio usado por Hugging Face `Trainer` para guardar de forma temporal los _checkpoints_ intermedios y resultados del proceso de entrenamiento.
