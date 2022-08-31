from pykeen.datasets import Nations
from pykeen.datasets import CoDExSmall
#Small class so we only need to change database in one place
def get_dataset():
    return Nations()

def get_dataset_name():
    return "Nations"