from classes.EntityConverter import EntityConverter
from tqdm import tqdm

def generate_dataset_file(filename,dataset_name, rels, dataset):
    print(f"Generating {dataset_name} {filename} dataset file in destination: datasets/data/{dataset_name}/{filename}")
    f = open(f"datasets/data/{dataset_name}/{filename}", "w", encoding="utf-8")
    entity_converter = EntityConverter(dataset)
    for head,rel,tail in tqdm(rels):
        #head_name = encode_text(entity_converter.entityindex_to_name[head])
        rel_name = encode_text(entity_converter.relindex_to_name[rel])
        #tail_name = encode_text(entity_converter.entityindex_to_name[tail])
        f.write(f"{head}\t{rel_name}\t{tail}\n")
    f.close()

def encode_text(entity):
    return entity.replace(" ", "_").replace(",","_")
