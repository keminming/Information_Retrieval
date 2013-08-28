'''
Created on Jun 12, 2013

@author: Administrator
'''

import math,sys,json
import numpy as np
from Queue import PriorityQueue

TWEET_TEXT_PATH = 'C:/Users/Administrator/workspace/670_hw_1/tweet/'

def tf_idf_vector(doc,inverse_index,word_map,n):
    d1 = len(word_map)
    tf_idf_vector = np.zeros(d1)
    for word in inverse_index:
        doc_freq = inverse_index[word][0]
        docs = inverse_index[word][2]
        if doc in docs:
            freq = inverse_index[word][2][doc]
            value = (1 + math.log(freq,2)) * math.log(float(n)/doc_freq,2)
            if word in word_map.keys():
                tf_idf_vector[word_map[word]] = value
    
    return tf_idf_vector
    
def tf_idf_all(inverse_index,word_map,doc_map):
    d1 = len(doc_map)
    d2 = len(word_map)
    tf_idf_index = np.zeros((d1,d2))
    tf_idf_dict = {}
    
    for word in inverse_index:
        doc_freq = inverse_index[word][0]
        docs = inverse_index[word][2]
        for doc in docs:
            term_freq = inverse_index[word][2][doc]          
            value = (1 + math.log(float(term_freq),2)) * math.log(float(d1)/doc_freq,2)
            tf_idf_index[doc_map[doc],word_map[word]] = value
            if doc in tf_idf_dict:
                tf_idf_dict[doc][word] = value
            else:
                d = {}
                d[word] = value
                tf_idf_dict[doc] = d

    return  tf_idf_index,tf_idf_dict

def cos_similarity(doc_tf_idf_index,query_tf_idf_index):
    query_norm = np.linalg.norm(query_tf_idf_index)
    doc_norm = np.linalg.norm(doc_tf_idf_index)
    similarity = float(np.dot(doc_tf_idf_index,query_tf_idf_index))/(query_norm * doc_norm) 
    return similarity

def cos_similarity_all_(tf_idf_index,query_tf_idf_index):
    d1 = len(tf_idf_index)
    similarity = []
    query_norm = np.linalg.norm(query_tf_idf_index)
    
    for i in range(d1):
        doc_norm = np.linalg.norm(tf_idf_index[i])
        similarity[i] = np.dot(tf_idf_index[i],query_tf_idf_index)/(query_norm * doc_norm) 
                
    return similarity

def main_1():
    f = open('tweet_index.json')
    inverse_index = json.loads(f.read())
    word_map = {}
    doc_map = {}
    i = 0
    j = 0
    for word in inverse_index:
        word_map[word] = i
        i = i + 1
        for doc in inverse_index[word][2]:
            if doc not in doc_map:
                doc_map[doc] = j
                j = j + 1 
    
    tf_idf_index = tf_idf_all(inverse_index,word_map,doc_map)
    
    query_inverse_index = {}
    for term in sys.argv[1:]:
        if term in query_inverse_index:
            query_inverse_index[term][1] = query_inverse_index[term][1] + 1
            query_inverse_index[term][2]['q'] = query_inverse_index[term][2]['q'] + 1
        else:
            query_inverse_index[term] = (1,1,{'q':1}) 
    
    q_doc_map = {}
    q_doc_map['q'] = 0       
    query_tf_idf_index = tf_idf_all(query_inverse_index,q_doc_map,doc_map)
    similarity = cos_similarity_all_(tf_idf_index,query_tf_idf_index)
    print similarity
      
def main_2():     
    f = open('tweet_index.json')
    inverse_index = json.loads(f.read())
    word_map = {}
    doc_map = {}
    i = 0
    j = 0
    for word in inverse_index:
        word_map[word] = i
        i = i + 1
        for doc in inverse_index[word][2]:
            if doc not in doc_map:
                doc_map[doc] = j
                j = j + 1 
    
    n = len(doc_map)    
    query_inverse_index = {}
    for term in sys.argv[1:]:
        if term in query_inverse_index:
            query_inverse_index[term][1] = query_inverse_index[term][1] + 1
            query_inverse_index[term][2]['q'] = query_inverse_index[term][2]['q'] + 1
        else:
            query_inverse_index[term] = (1,1,{'q':1}) 
        
    query_tf_idf_index = tf_idf_vector('q',query_inverse_index,word_map,n)
    
    similarity_q = PriorityQueue()
    for doc in doc_map.keys()[:1000]:
        doc_tf_idf_index = tf_idf_vector(doc,inverse_index,word_map,n)
        similarity = cos_similarity(doc_tf_idf_index,query_tf_idf_index)
        similarity_q.put((-similarity,doc))#smaller angle, larger cosine value, larger similarity
    
    display_number = 0
    while display_number < 50:
        doc = similarity_q.get()[1]
        print doc
        display_number += 1
      
if __name__ == '__main__':
    #main_2()
    x1 = [1,2,3]
    x2 = [3,2,1]
    p = cos_similarity(x1,x2)
    print p