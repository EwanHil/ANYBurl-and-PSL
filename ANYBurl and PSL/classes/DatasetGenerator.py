from classes.EntityConverter import EntityConverter

class DatasetGenerator():
    def ___init___(self):
        pass
            
    def generate_dataset_file(self, filename, dataset_name, rels):
        f = open(f"datasets/data/{dataset_name}/{filename}", "w")
        entity_converter = EntityConverter()
        for head,rel,tail in rels:
          head_name = encode_text(entity_converter.entityindex_to_name[head])
          rel_name = encode_text(entity_converter.relindex_to_name[rel])
          tail_name = encode_text(entity_converter.entityindex_to_name[tail])
          f.write(f"{head_name}\t{rel_name}\t{tail_name}\n")
          
        f.close()

    def encode_text(self, entity):
        return entity.replace(" ", "%20").replace(",","%2C")
