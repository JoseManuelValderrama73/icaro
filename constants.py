"""
"microsoft/deberta-base"
"google-bert/bert-base-cased"
"""
MODEL = 'microsoft/deberta-base'

"""
castle
draper
formai
"""
DATASET = 'formai'
TEST_SIZE = 0.2
# TODO: que la semilla sea algo diferente
SEED = 42

TRAINING_OUTPUT_DIR = f"training/{MODEL.split('/')[-1]}/{DATASET}"
MODEL_SAVE_PATH = f"modelos/{MODEL.split('/')[-1]}-{DATASET}"
TOKENIZER_SAVE_PATH = f"tokenizers/{MODEL.split('/')[-1]}-{DATASET}"

BATCH_SIZE = 5
EPOCHS = 1