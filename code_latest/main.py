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
from pykeen.datasets import CoDExSmall
from classes.ANYBurlToPSLConverter import ANYBurlToPSLConverter
from classes.RuleImporter import RuleImporter
from classes.EntityConverter import EntityConverter
from classes.DatasetGenerator import encode_text
from tqdm import tqdm

MODEL_NAME = 'ANYBurl and PSL Model'

DATA_DIR = os.path.join('data')

ADDITIONAL_PSL_OPTIONS = {
    'log4j.threshold': 'INFO'
}

ADDITIONAL_CLI_OPTIONS = [
    # '--postgres'
]

MAX_RULES = 10
ANYBURL_RULES_THRESHOLD = 0.6

def main():
    importer = RuleImporter()
    importer.import_rules()

    model = Model(MODEL_NAME)
    dataset = CoDExSmall()
    entity_converter = EntityConverter(dataset)

    #train_triples = dataset.training.mapped_triples.numpy()
    #val_triples = dataset.validation.mapped_triples.numpy()
    #test_triples = dataset.testing.mapped_triples.numpy()  

    # Add Predicates
    add_predicates(model,entity_converter)

    # Add Rules
    add_rules(model,importer.rules)

    # Inference
    results = infer(model,entity_converter)
    write_results(results, model)
 
def add_predicates(model,entity_converter):    
    for relindex,name in entity_converter.relindex_to_name.items():
        predicate = Predicate(encode_text(name), closed = name != 'member of', size = 2)
        model.add_predicate(predicate)

def add_rules(model, rules):
    converter = ANYBurlToPSLConverter(rules)
    print(len(converter.converted_rules))
    total_rules = 0
    for rule in converter.converted_rules:
        if total_rules > MAX_RULES:
            break
        if float(rule.split(':')[0]) > ANYBURL_RULES_THRESHOLD:
            model.add_rule(Rule(rule))
            total_rules += 1
            continue
    
def add_data(model,entity_converter):
    for relindex,name in entity_converter.relindex_to_name.items():     
        
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

def infer(model,entity_converter):
    add_data(model, entity_converter)
    return model.infer(additional_cli_options = ADDITIONAL_CLI_OPTIONS, psl_config = ADDITIONAL_PSL_OPTIONS)
      
def write_results(results, model):
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