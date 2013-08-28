'''
Created on Jun 6, 2013

@author: Administrator
'''

PATH = 'C:/Users/Administrator/Google Drive/wangke/csce/information retrivel/books'
POSITIONAL_INDEX_PATH = 'index.json'
K_GRAM_PATH = 'k_gram_index.json'
INVERSE_INDEX_PATH = 'inverse_index.json'

import os
import re
import json

def inverse_index(input_path,output):
    fout3 = open(output,'w')
    index = {}
    words = []
    for fileName in os.listdir(input_path):  
        fin = open(input_path + '/' + fileName,'r');
        for line in fin:
            for word in re.findall('[0-9a-z]+',line.strip().decode('utf-8').lower()):
                if word:
                    words.append((word.encode('utf-8'),fileName))    
                             
    words.sort(key=lambda x:x[0])
      
    for word_doc in words:
        word = word_doc[0]
        doc = word_doc[1]
        if word in index:
            if doc in index[word]:
                index[word][doc] += 1
            else:
                index[word][doc] = 1  
        else:
            frequence = {}
            frequence[doc] = 1
            index[word] = frequence
    
    for word in index:
        index[word] = (len(index[word]),sum([index[word][x] for x in index[word]]),index[word])     
                      
    json.dump(index, fout3)

  
def positional_index(input_path,output):
    fout1 = open(output,'w')
    words = []
    index = {}
    for fileName in os.listdir(input_path):  
        fin = open(input_path + '/' + fileName,'r');
        position = 0;
        for line in fin:
            for word in re.split('[/.,()?!"\'; ]',line.strip()):
                if word:
                    words.append((word.lower(),fileName,position))
                    position += 1
    
    for word_doc_pos in words:
        word = word_doc_pos[0]
        doc = word_doc_pos[1]
        pos = word_doc_pos[2]
        
        if word in index:
            if doc in index[word]:
                index[word][doc].append(pos)
            else:
                positions = []
                positions.append(pos)   
                index[word][doc] = positions
        else:
            index[word] = {}
            positions = []
            positions.append(pos)   
            index[word][doc] = positions 
            
    
    json.dump(index, fout1)
         
def k_gram_index(k,output):
    fout2 = open(output,'w')
    k_grams = {}
    words = []
    for fileName in os.listdir(PATH):  
        fin = open(PATH + '/' + fileName,'r');
        for line in fin:
            for word in re.split('[-/.,()?!"\';:\s ]',line.strip()):
                word = word.lower()
                if (not word in words) and word:
                    length = len(word)
                    t_word = '$' + word + '$'
                    
                    for i in range(length + 2 - k + 1):
                        if k_grams.has_key(t_word[i:i + 2]):
                            k_grams[t_word[i:i + 2]].append(word)
                        else:
                            doc_list = []
                            doc_list.append(word)
                            k_grams[t_word[i:i + 2]] = doc_list
                words.append(word)
    json.dump(k_grams, fout2)
    return k_grams               
                
 
if __name__ == '__main__':
    #positional_index(PATH,'positional_index.json')
    #k_gram_index(2,'k_gram_index.json')
    inverse_index('test_inverse','test_inverse.json')
    
    
    
