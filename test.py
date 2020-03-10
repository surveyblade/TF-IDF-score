#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 19:09:43 2019

@author: user
"""

import pickle
import project_part1 as project_part1
import spacy


nlp = spacy.load('en')

fname = './Data/sample_documents.pickle'
#documents = pickle.load(open(fname,"rb"))


documents = {1: 'According to Times of India, President Donald Trump was on his way to New York City after his address at UNGA.',
             2: 'The New York Times mentioned an interesting story about Trump.',
             3: 'I think it would be great if I can travel to New York this summer to see Trump.'}


#index = project_part1.InvertedIndex()
#index.index_documents(documents)
#Q = 'The New New York City Times of India'
#DoE = {'Times of India':0, 'The New York Times':1,'New York City':2}
#query_splits = index.split_query(Q, DoE)
#doc_id = 1
#result = index.max_score_query(query_splits, doc_id)
#print(result)






#index = project_part1.InvertedIndex()
#
#index.index_documents(documents)
#
#print(index.tf_tokens)
#print(index.tf_entities)
#print(index.idf_tokens)
#print(index.idf_entities)
#
#
#
#
Q = ' A A A B C A B C'
DoE = {'A':0 , 'B':1, 'A B C':2}


query_splits = index.split_query(Q, DoE)

for key,split in query_splits.items():
    print(split)
#
#result = index.max_score_query(query_splits, 1)
#print(result)

