import json
from classes.Dataset import get_dataset_name
class EntityConverter():
    def __init__(self,dataset, is_json = False):
        
        if is_json:
            with open(f'classes/json/{get_dataset_name}_entities.json', encoding="utf-8") as f:
                entities = json.load(f)
            with open(f'classes/json/{get_dataset_name}_relations.json', encoding="utf-8") as f:
                relations = json.load(f)
            self.entityid_to_name = { entityid:entities[entityid]['label'] for entityid in entities }
            self.relid_to_name = { relid:relations[relid]['label'] for relid in relations }
            self.entityindex_to_name = { entityindex:self.entityid_to_name[entityid] for entityid,entityindex in dataset.entity_to_id.items() }
            self.relindex_to_name = {relindex:self.relid_to_name[relid] for relid,relindex in dataset.relation_to_id.items() }
            self.entityname_to_index = { name:index for index,name in self.entityindex_to_name.items() }
            self.relname_to_index = { name:index for index,name in self.relindex_to_name.items() }
        else:    
            self.entityname_to_index = dataset.entity_to_id
            self.relname_to_index = dataset.relation_to_id
            self.entityindex_to_name =  { index:name for name,index in self.entityname_to_index.items() }
            self.relindex_to_name = { index:name for name,index in self.relname_to_index.items() }
        
            