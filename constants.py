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
DATASET = 'draper'
TEST_SIZE = 0.2
# TODO: que la semilla sea algo diferente
SEED = 42

TRAINING_OUTPUT_DIR = f"training/{MODEL.split('/')[-1]}/{DATASET}"

BATCH_SIZE = 5
EPOCHS = 1