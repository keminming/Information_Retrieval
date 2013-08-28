'''
Created on Jun 9, 2013

@author: Administrator
'''

import sys,json,re

POSITIONAL_INDEX_PATH = 'positional_index.json'
K_GRAM_PATH = 'k_gram_index.json'

def post_filter(doc,words,index_in):
    pos = []
    for i in range(len(words)):
        tmp = [j-i for j in index_in[words[i]][doc]]      
        if not pos:
            pos = tmp
        else:
            pos = set(pos) & set(tmp)
    if pos:
        return True
    else:
        return False        
                            
def search_phrase(index_in,key_words):
    indexs = {}
    for word in key_words:
        indexs[word] = index_in[word].keys()
                          
    result = []
    for key in indexs:
        if result:
            result = set(result) & set(indexs[key])
        else:
            result = set(indexs[key])
    
    for doc in result:
        if not post_filter(doc,key_words,index_in):
            result.remove(doc)
    
    return result        
       
def search_common(index_in,key_word):
    return index_in[key_word].keys()    

def get_grams(word):
    grams = []
    subwords = ('$' + word + '$').split('*')
    for j in range(len(subwords)):
        for i in range(len(subwords[j]) - 1):
            grams.append(subwords[j][i:i+2])
    return grams

def search_wild_card(positional_index,gram_index,wild_card):
    matched_keywords = []
    grams = get_grams(wild_card)   
           
    keywords = []
    for gram in grams:
        if keywords:
            keywords = set(keywords) & set(gram_index[gram])
        else:
            keywords = set(gram_index[gram])
             
    for keyword in keywords:
        if re.match(wild_card.replace('*','.'),keyword):
            matched_keywords.append(keyword)
    
    result = []
    for keyword in matched_keywords:
        result += positional_index[keyword].keys()   
    return result          

def main():
    print sys.argv  
    index_file = open(POSITIONAL_INDEX_PATH,'r')
    index = json.loads(index_file.read())
    #print index 
    k_gram_file = open(K_GRAM_PATH,'r')
    k_grams = json.loads(k_gram_file.read())  
    #print k_grams
    result = []
    for word in sys.argv[1:]:
        if '*' in word:
            if not result:
                result = search_wild_card(index,k_grams,word)
            else:
                result = set(search_wild_card(index,k_grams,word)) &  set(result)
        elif len(word.split()) > 1:
            if not result:
                result = search_phrase(index,word.split())
            else:
                result = set(search_phrase(index,word.split())) &  set(result)  
        else:
            if not result:
                result = search_common(index,word)
            else:
                result = set(search_common(index,word)) &  set(result)                     
 
    print result

if __name__ == '__main__':
    main()