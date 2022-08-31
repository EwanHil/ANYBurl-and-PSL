#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Uncomment if you need to install pslpython
#pip install pslpython


# In[2]:


# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 09:49:29 2022

@author: ewanhilton
"""

from classes.DatasetGenerator import generate_dataset_file
from classes.EntityConverter import EntityConverter
from classes.PSLFileBuilder import PSLFileBuilder
from classes.Dataset import get_dataset
from classes.Dataset import get_dataset_name

#Setting this to True is required to get all files needed for PSL,
#but is very costly
CREATE_FILES = True 

def pre_main():
    dataset = get_dataset()
    
    train_triples = dataset.training.mapped_triples.numpy()
    val_triples = dataset.validation.mapped_triples.numpy()
    test_triples = dataset.testing.mapped_triples.numpy()   
    dataset_name = get_dataset_name()
    generate_dataset_file('train.txt',dataset_name,train_triples,dataset)
    generate_dataset_file('valid.txt',dataset_name,val_triples,dataset)
    generate_dataset_file('test.txt',dataset_name,test_triples,dataset)
    
    if CREATE_FILES:       
        train_triples = dataset.training.mapped_triples.numpy()
        val_triples = dataset.validation.mapped_triples.numpy()
        #test_triples = dataset.testing.mapped_triples.numpy()  
    
        entity_converter = EntityConverter(dataset)
        create_files(train_triples,val_triples,entity_converter)
    
    #Create files needed by PSL
def create_files(train_triples, val_triples,entity_converter):    
    filebuilder = PSLFileBuilder(train_triples, val_triples, entity_converter)
    filebuilder.build_map_files()
    filebuilder.build_obs_files()
    #filebuilder.build_target_files()
    filebuilder.build_truth_files()


# In[3]:


# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 08:04:34 2022

@author: ewanhilton
"""
import os

from pslpython.model import Model
from pslpython.partition import Partition
from pslpython.predicate import Predicate
from pslpython.rule import Rule
from classes.Dataset import get_dataset
from classes.ANYBurlToPSLConverter import ANYBurlToPSLConverter
from classes.RuleImporter import RuleImporter
from classes.EntityConverter import EntityConverter
from classes.DatasetGenerator import encode_text
from tqdm import tqdm
from datetime import datetime
from classes.PSLFileBuilder import build_target_files
from classes.DatasetGenerator import encode_text
from classes.PSLFileBuilder import PSLFileBuilder
import glob

MODEL_NAME = 'ANYBurl and PSL Model'

DATA_DIR = os.path.join('data')

ADDITIONAL_PSL_OPTIONS = {
    'log4j.threshold': 'INFO'
}

ADDITIONAL_CLI_OPTIONS = [
    # '--postgres'
]

MAX_RULES = None
ANYBURL_RULES_THRESHOLD = 0.6
PREDICT_PREDICATES_ONE_AT_A_TIME = False

def main():
    print(f"PSL run stated at {get_date_time()}")
    importer = RuleImporter()
    importer.import_rules()
   
    dataset = get_dataset()
    entity_converter = EntityConverter(dataset)

    train_triples = dataset.training.mapped_triples.numpy()
    val_triples = dataset.validation.mapped_triples.numpy()
    #test_triples = dataset.testing.mapped_triples.numpy()  
    
    #Delete all pre-existing predicates from the folder
    for f in glob.glob("inferred-predicates/*"):
                    os.remove(f)
            
    if PREDICT_PREDICATES_ONE_AT_A_TIME :
        for relindex,name in tqdm(entity_converter.relindex_to_name.items()): 
            try:
                model = Model(MODEL_NAME)
                
                #Delete existing targets files so we only deal with one at a time
                for f in glob.glob("data/targets/*"):
                    os.remove(f)
                
                #Add Target Files
                build_target_files(name,relindex, entity_converter, train_triples)
                # Add Predicates
                add_predicates(model,entity_converter,name)

                # Add Rules
                add_rules(model,importer.rules, encode_text(name), name)

                # Add Data
                add_data(model, entity_converter, name)

                # Inference
                results = infer(model)
                write_results(results, model)
            except Exception as e: 
                print(e)
                continue
    else:
        name = "All Predicates"
        model = Model(MODEL_NAME)

        #Add Target Files
        filebuilder = PSLFileBuilder(train_triples, val_triples, entity_converter)
        filebuilder.build_target_files()
        # Add Predicates
        add_predicates(model,entity_converter)

        # Add Rules
        add_rules(model,importer.rules, None)

        # Add Data
        add_data(model, entity_converter)

        # Inference
        results = infer(model)
        write_results(results, model)
    print(f"PSL run ended at {get_date_time()}")
    
def add_predicates(model,entity_converter,target_name=None):
    if target_name is not None:
        print(f"Adding predicates for {target_name}")
    else:
        print("Adding predicates for All Predicates")
    for relindex,name in tqdm(entity_converter.relindex_to_name.items()):
        is_closed = False
        if target_name is not None:
            is_closed = name != target_name
        predicate = Predicate(encode_text(name), closed = is_closed, size = 2)
        model.add_predicate(predicate)

def add_rules(model, rules, name, target_name=None):
    if target_name is not None:
        print(f"Adding rules for {target_name}")
    else:
        print("Adding rules for All Predicates")
    converter = ANYBurlToPSLConverter(rules)
    total_rules = 0
    for rule in tqdm(converter.converted_rules):
        if name is None or rule.split('->')[1].split('(')[0].replace(' ','') == name:
            if MAX_RULES != None and total_rules >= MAX_RULES:
                print(f"Maximum number of rules added ({total_rules} rules added)")
                return
            if float(rule.split(':')[0]) > ANYBURL_RULES_THRESHOLD:
                model.add_rule(Rule(rule))
                total_rules += 1
                continue
                
    if total_rules < 1:
        raise Exception(f"Failed to add any rules. Aborting inference for {target_name}")
    print(f"{total_rules} rules added")
    
def add_data(model,entity_converter, target_name = None):
    if target_name is not None:
        print(f"Adding data for {target_name}")
    else:
        print("Adding data for All Predicates")
        
    for relindex,name in tqdm(entity_converter.relindex_to_name.items()):        
        path = f'data/obs/{encode_text(name)}_obs.txt'
        if path_exists(path): #Check file has content before adding  
            model.get_predicate(encode_text(name)).add_data_file(Partition.OBSERVATIONS, path)

        path =  f'data/targets/{encode_text(name)}_targets.txt'
        if path_exists(path):
            model.get_predicate(encode_text(name)).add_data_file(Partition.TARGETS, path)

        path = f'data/truth/{encode_text(name)}_truth.txt'
        if path_exists(path):
            model.get_predicate(encode_text(name)).add_data_file(Partition.TRUTH, path)
   
def path_exists(path):
    try:
        return os.path.getsize(f"{path}") > 0
    except:
        return False

def infer(model): 
    print(f"Inference starting at {get_date_time()}")
    return model.infer(psl_config = ADDITIONAL_PSL_OPTIONS)
     
def get_date_time():
    return f"{str(datetime.now().time()).split('.')[0]} on {datetime.today().strftime('%d-%b-%Y')}"

def write_results(results, model):
    print(f"Inferenced completed at {get_date_time()}")
    out_dir = 'inferred-predicates'
    os.makedirs(out_dir, exist_ok = True)
    print("Writing predicates")
    for predicate in tqdm(model.get_predicates().values()):
        if (predicate.closed()):
            continue       
        try:
            out_path = os.path.join(out_dir, "%s.txt" % (predicate.name()))
            results[predicate].to_csv(out_path, sep = "\t", header = False, index = False)     
        except:
            continue


# In[4]:


pre_main()


# In[5]:


main()


# In[ ]:




