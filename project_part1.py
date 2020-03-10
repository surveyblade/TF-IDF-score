## Import Libraries and Modules here...
import spacy
from collections import defaultdict
import copy
from itertools import combinations
import math
import string

class InvertedIndex:
    def __init__(self):
        ## You should use these variable to store the term frequencies for tokens and entities...
        self.tf_tokens = defaultdict(dict)
        self.tf_entities = defaultdict(dict)

        ## You should use these variable to store the inverse document frequencies for tokens and entities...
        self.idf_tokens = defaultdict(dict)
        self.idf_entities = defaultdict(dict)

    ## Your implementation for indexing the documents...
    def index_documents(self, documents):
        nlp = spacy.load('en')
        for key in documents:
            doc = nlp(documents[key])
            for token in doc:
                if token.is_stop == False:
                    if token.is_punct == False:
                        if token.text in self.tf_tokens:
                            if key in self.tf_tokens[token.text]:
                                self.tf_tokens[token.text][key] += 1
                            else:
                                self.tf_tokens[token.text][key] = 1
                        else:
                            self.tf_tokens[token.text] = {key:1}
            for ent in doc.ents:
                if ent.text in self.tf_entities:
                    if key in self.tf_entities[ent.text]:
                        self.tf_entities[ent.text][key] += 1
                    else:
                        self.tf_entities[ent.text][key] = 1
                else:
                    self.tf_entities[ent.text] = {key:1}
        for key in self.tf_entities:
            if not ' ' in key:
                if key in self.tf_tokens:
                    for sub_key in self.tf_entities[key]:
                        if sub_key in self.tf_tokens[key]:
                            self.tf_tokens[key][sub_key] -= self.tf_entities[key][sub_key]
                            if self.tf_tokens[key][sub_key] == 0:
                                del self.tf_tokens[key][sub_key]
                    if bool(self.tf_tokens[key]) == False:
                        del self.tf_tokens[key]
                    
        
#        self.idf_tokens = {0:{0:0}}
#        self.idf_entities = {0:{0:0}}
        for doc_id in documents:
            for key in self.tf_tokens:
                if not doc_id in self.tf_tokens[key]:
                    self.idf_tokens[key][doc_id] = 0.0
                else:
                    sum = self.tf_tokens[key][doc_id]
                    TF_norm_tokens = 1 + math.log(1.0 + math.log(sum))
                    if len(documents) != 0:
                        IDF_token = 1 + math.log(len(documents)/(1.0+len(self.tf_tokens[key])))
                    self.idf_tokens[key][doc_id] = TF_norm_tokens*IDF_token
                
                
            for key in self.tf_entities:
                if not doc_id in self.tf_entities[key]:
                    self.idf_entities[key][doc_id] = 0.0
                else:
                    sum = self.tf_entities[key][doc_id]
                    TF_norm_entities = 1 + math.log(sum)
                    if len(documents) != 0:
                        IDF_entity = 1 + math.log(len(documents)/(1.0+len(self.tf_entities[key])))
                    self.idf_entities[key][doc_id] = TF_norm_entities*IDF_entity
        
    ## Your implementation to split the query to tokens and entities...
    def split_query(self, Q, DoE):
        Q_list = []
#        nlp = spacy.load('en')
#        doc = nlp(Q)
#        for token in doc:
#            if token.is_punct == False:
#                if isinstance(token.text, str):
#                    Q_list.append(token.text)
#        punctu = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        Q1 = Q.replace(',','').replace('.','').replace(':','').replace(';','').replace('!','').replace('?','')
        Q_list = Q1.split()
        
        query_dict_list = []
        query_dict = {}
        query_dict['tokens'] = Q_list
        query_dict['entities'] = []
        query_dict_list.append(query_dict)
        DoE_list =[]
        for key in DoE:    
            DoE_list.append(key.split())
        # first loop
        subs = []
        for i in range(0, len(DoE_list)+1):
            temp = [list(x) for x in combinations(DoE_list, i)]
            if len(temp)>0:
                subs.extend(temp)
        for m in range(len(subs)):
            subs[m].sort(key=len,reverse=1) 
#            print(subs[m])
                
        for m in range(len(subs)):
            # k is used to log # of DoE elements in subset
            k = 0
            if bool(subs[m]) == False:
                continue
            temp_query_dict = copy.deepcopy(query_dict)
            temp_Q_list = Q_list.copy()
            for n in range(len(subs[m])):
                i = 0
                j = 0
                while ((i<len(subs[m][n])) and j < len(temp_Q_list)):
                    if subs[m][n][i] == temp_Q_list[j]:
                        temp_Q_list[j] = 0
                        i += 1;
                        j += 1;
                        
                    else:
                        j += 1;
                    if i == len(subs[m][n]):
                        k += 1;
                        break
                    
                if k == len(subs[m]):
                    temp_query_dict['tokens'] = [x for x in temp_Q_list if not isinstance(x, int)]

                    for q in range(len(subs[m])):
                        temp_query_dict['entities'].append(' '.join(map(str, subs[m][q])))
                    query_dict_list.append(temp_query_dict)
        
        result = {}
        for i in range(len(query_dict_list)):
            result[i] = query_dict_list[i]
        return result
        
    ## Your implementation to return the max score among all the query splits...
    def max_score_query(self, query_splits, doc_id):
        max_score = 0.0
        for key,split in query_splits.items():
            token_score = 0.0
            entities_score = 0.0
            for i in split['tokens']:
                if bool(self.idf_tokens[i]) == False:
                    continue
                else:
                    token_score += self.idf_tokens[i][doc_id]
            for i in split['entities']:
                if bool(self.idf_entities[i]) == False:
                    continue
                else:
                    entities_score += self.idf_entities[i][doc_id]
            combined_score = token_score*0.4 + entities_score
            if combined_score > max_score:
                max_score = combined_score
                result = (max_score,split)
            
#            result[key] = [split,{'token_score':token_score,'entities_score':entities_score,'combined_score':combined_score}]
        
        return result
        
        
        ## Output should be a tuple (max_score, {'tokens': [...], 'entities': [...]})
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
