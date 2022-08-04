from classes.EntityConverter import EntityConverter

class PSLFileBuilder():
    def __init__(self, rels = None):
        if(rels is None):
            self.Rels = []
        else:
            self.Rels = rels

    def build_map_files(self, rels, seperator = "%20"):
      entity_converter = EntityConverter()
      for rel in self.Rels:
        file_name = entity_converter.relindex_to_name[rel].replace(" ", seperator)
        f = open(f"{file_name}_map.txt", "a")
        first_line = True
        items_added = []
        for h,r,t in  rels:
          if r == rel and t not in items_added: #Avoid adding duplicates to the map
            items_added.append(t)
            t_map_name = entity_converter.entityindex_to_name[t]
            if first_line:
              f.write(f"{t}\t{t_map_name}")
              first_line = False
            else:
              f.write(f"\n{t}\t{t_map_name}")
        f.close()
        
    def build_obs_files(self, rels, rel_indices):      
        for relindex,name in rel_indices.items():       
            f = open(f"{name}_obs.txt", "a")
            for h,r,t in rels:
                if r != relindex:
                    continue
            f.close()
            
        return
    
    def build_target_files(self):
        return
    
    def build_truth_files(self):
        return
    