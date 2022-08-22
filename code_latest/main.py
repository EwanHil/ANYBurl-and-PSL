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
from classes.DatasetGenerator import DatasetGenerator

MODEL_NAME = 'ANYBurl and PSL Model'

DATA_DIR = os.path.join('data')

ADDITIONAL_PSL_OPTIONS = {
    'log4j.threshold': 'INFO'
}

ADDITIONAL_CLI_OPTIONS = [
    # '--postgres'
]

def main():
    importer = RuleImporter()
    importer.import_rules()
    
    model = Model(MODEL_NAME)
    dataset = CoDExSmall()
    entity_converter = EntityConverter(dataset)
   
    #train_triples = dataset.training.mapped_triples.numpy()
    #val_triples = dataset.validation.mapped_triples.numpy()
    #test_triples = dataset.testing.mapped_triples.numpy()  
    
    generator = DatasetGenerator()
    # Add Predicates
    add_predicates(model,entity_converter,generator)
    
    # Add Rules
    add_rules(model,importer.rules)

    # Inference
    results = infer(model,entity_converter,generator)

    write_results(results, model)
 
def add_predicates(model,entity_converter,generator):    
    for relindex,name in entity_converter.relindex_to_name.items():
        predicate = Predicate(generator.encode_text(name), closed = name == 'member of', size = 2)
        model.add_predicate(predicate)       
    
def add_rules(model, rules):
    converter = ANYBurlToPSLConverter(rules)
    for rule in converter.converted_rules:
        if rule.split('->')[1].split('(')[0].replace(' ','') == 'member%20of':
            model.add_rule(Rule(rule))

def add_data(model,entity_converter,generator):
    for relindex,name in entity_converter.relindex_to_name.items():
        path = f'data/obs/{generator.encode_text(name)}_obs.txt'
        model.get_predicate(generator.encode_text(name)).add_data_file(Partition.OBSERVATIONS, path)
    
        path = f'data/targets/{generator.encode_text(name)}_targets.txt'
        model.get_predicate(generator.encode_text(name)).add_data_file(Partition.TARGETS, path)
    
        path = f'data/truth/{generator.encode_text(name)}_truth.txt'
        model.get_predicate(generator.encode_text(name)).add_data_file(Partition.TRUTH, path)
    
def infer(model,entity_converter,generator):
    add_data(model, entity_converter, generator)
    return model.infer(additional_cli_options = ADDITIONAL_CLI_OPTIONS, psl_config = ADDITIONAL_PSL_OPTIONS)
      
def write_results(results, model):
    out_dir = 'inferred-predicates'
    os.makedirs(out_dir, exist_ok = True)

    for predicate in model.get_predicates().values():
        if (predicate.closed()):
            continue

        out_path = os.path.join(out_dir, "%s.txt" % (predicate.name()))
        results[predicate].to_csv(out_path, sep = "\t", header = False, index = False)       