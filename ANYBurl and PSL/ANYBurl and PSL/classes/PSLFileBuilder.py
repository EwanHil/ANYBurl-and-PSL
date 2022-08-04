class PSLFileBuilder():
    def __init__(self, rels = None):
        if(rels is None):
            self.Rels = []
        else:
            self.Rels = rels

    def build_map_files(self, seperator = "%20"):
      for rel in self.Rels:
        file_name = relindex_to_name[rel].replace(" ", seperator)
        f = open(f"{file_name}_map.txt", "a")
        first_line = True
        items_added = []
        for h,r,t in  train_triples:
          if r == rel and t not in items_added: #Avoid adding duplicates to the map
            items_added.append(t)
            t_map_name = entityindex_to_name[t]
            if first_line:
              f.write(f"{t}\t{t_map_name}")
              first_line = False
            else:
              f.write(f"\n{t}\t{t_map_name}")
        f.close()
        
    def build_obs_files(self):
        return
    
    def build_target_files(self):
        return
    
    def build_truth_files(self):
        return
    