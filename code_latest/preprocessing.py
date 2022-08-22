# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 09:49:29 2022

@author: ewanhilton
"""


from classes.DatasetGenerator import DatasetGenerator
from classes.EntityConverter import EntityConverter
from classes.PSLFileBuilder import PSLFileBuilder
from pykeen.datasets import CoDExSmall

#Setting this to True is required to get all files needed for PSL,
#but is very costly
CREATE_FILES = True 

def pre_main():
    dataset = CoDExSmall()
    
    train_triples = dataset.training.mapped_triples.numpy()
    val_triples = dataset.validation.mapped_triples.numpy()
    test_triples = dataset.testing.mapped_triples.numpy()   
    
    generator = DatasetGenerator()
    generator.generate_dataset_file('train.txt','CoDEx',train_triples,dataset)
    generator.generate_dataset_file('valid.txt','CoDEx',val_triples,dataset)
    generator.generate_dataset_file('test.txt','CoDEx',test_triples,dataset)
    
    if CREATE_FILES:
        dataset = CoDExSmall()
        
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
    filebuilder.build_target_files()
    filebuilder.build_truth_files()