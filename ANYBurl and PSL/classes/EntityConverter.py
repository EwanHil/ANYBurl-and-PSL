import json

class EntityConverter():
    def __init__(self,dataset):
        with open('classes/json/codex_entities.json', encoding="utf-8") as f:
          codex_entities = json.load(f)
        with open('classes/json/codex_relations.json', encoding="utf-8") as f:
          codex_relations = json.load(f)
        
        self.entityid_to_name = { entityid:codex_entities[entityid]['label'] for entityid in codex_entities }
        self.relid_to_name = { relid:codex_relations[relid]['label'] for relid in codex_relations }
        
        self.entityindex_to_name = { entityindex:self.entityid_to_name[entityid] for entityid,entityindex in dataset.entity_to_id.items() }
        self.relindex_to_name = {relindex:self.relid_to_name[relid] for relid,relindex in dataset.relation_to_id.items() }
        self.entityname_to_index = { name:index for index,name in self.entityindex_to_name.items() }
        self.relname_to_index = { name:index for index,name in self.relindex_to_name.items() }
            