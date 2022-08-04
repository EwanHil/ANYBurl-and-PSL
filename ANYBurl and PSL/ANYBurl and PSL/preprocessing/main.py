# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 09:49:29 2022

@author: ewanhilton
"""

from pykeen.datasets import CoDExSmall
from classes.DatasetGenerator import DatasetGenerator

def main():
    dataset = CoDExSmall()
    
    train_triples = dataset.training.mapped_triples.numpy()
    val_triples = dataset.validation.mapped_triples.numpy()
    test_triples = dataset.testing.mapped_triples.numpy()   
    
    generator = DatasetGenerator()
    generator.generate_dataset_file('train.txt','CoDEx',train_triples)
    generator.generate_dataset_file('valid.txt','CoDEx',val_triples)
    generator.generate_dataset_file('test.txt','CoDEx',test_triples)
    
if (__name__ == '__main__'):
    main()