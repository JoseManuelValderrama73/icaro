"""
"microsoft/deberta-base"
"google-bert/bert-base-cased"
"""
MODEL = 'microsoft/deberta-base'

"""
'castle'
'draper'
"""
DATASET = 'castle'

TRAINING_OUTPUT_DIR = f"training/{MODEL.split('/')[-1]}/{DATASET}"

BATCH_SIZE = 5
EPOCHS = 1