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
from classes.ANYBurlToPSLConverter import ANYBurlToPSLConverter
from classes.PSLFileBuilder import PSLFileBuilder
from classes.RuleImporter import RuleImporter

MODEL_NAME = 'ANYBurl and PSL Model'

DATA_DIR = os.path.join('eval')

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
    create_files()
    
    # Add Predicates
    #add_predicates(model)

    # Add Rules
    add_rules(model, importer.rules)

    # Inference
    #results = infer(model)

    #write_results(results, model)
 
#Create files needed by PSL
def create_files():
    filebuilder = PSLFileBuilder()
    filebuilder.build_map_files()
    filebuilder.build_obs_files()
    filebuilder.build_target_files()
    filebuilder.build_truth_files()
 
def add_predicates(model):
    return
    
def add_rules(model, rules):
    converter = ANYBurlToPSLConverter(rules)
    
    for rule in converter.converted_rules:
         model.add_rule(Rule(rule))

def add_data(model):
    return

def infer(model):
    add_data(model)
    return model.infer(additional_cli_optons = ADDITIONAL_CLI_OPTIONS, psl_config = ADDITIONAL_PSL_OPTIONS)
      
def write_results(results, model):
    out_dir = 'inferred-predicates'
    os.makedirs(out_dir, exist_ok = True)

    for predicate in model.get_predicates().values():
        if (predicate.closed()):
            continue

        out_path = os.path.join(out_dir, "%s.txt" % (predicate.name()))
        results[predicate].to_csv(out_path, sep = "\t", header = False, index = False)       
    
if (__name__ == '__main__'):
    main()