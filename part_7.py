'''
Created on Jun 28, 2013

@author: Administrator
'''

import sys,json,numpy,os
from part_1 import inverse_index
from part_4 import tf_idf_all,cos_similarity 
import math
import itertools

def k_means(x,k):
    #max_v = max([v for xi in x for v in xi])
    #min_v = min([v for xi in x for v in xi])
    miu = [x[0],x[1],x[2],x[6],x[8]]
            
    #miu = []         
    #for i in range(k):
        #miu.append([random.randint(min_v,max_v) for j in range(len(x[0]))])
    n = 0      
    while n < 50:        
        w = [None]*k     
        for i in range(len(x)):
            dists = [(cos_similarity(x[i],miu[j]),j) for j in range(k)]
            min_center = max(dists,key=lambda x:x[0])[1]
           
            if w[min_center]:
                w[min_center].append(i)
            else:
                l = []
                l.append(i)
                w[min_center] = l
                
        for m in range(k):
            if w[m]:
                centroid = numpy.array([0.0]*len(x[0]))
                for v in w[m]:
                    centroid += x[v]
                miu[m] = centroid/len(w[m]) 
            #else:
                #print 'wrong'
                #sys.exit()           
        n = n + 1  
                                  
    return miu,w
    

def get_class(doc_map):
    c = {}
    dirnames = os.listdir('bing_training')
    os.chdir('bing_training')
    for name in dirnames:
        filenames = os.listdir(name)
        for fname in filenames:
            if fname in doc_map.keys():
                if name in c:
                    c[name].append(doc_map[fname])   
                else:
                    l = []
                    l.append(doc_map[fname])
                    c[name] = l
    return c    
              
def purity(ws,cs,n):  
    gw = {}
    for i in range(len(ws)):
        gw[i] = max([len(set(ws[i])& set(cs[c])) for c in cs])
    purity = (1.0/n) * sum([gw[k] for k in gw]) 

    return purity

def combin(n,m):
    return float(math.factorial(n))/(math.factorial(n-m) * math.factorial(m))

def rand_index(ws,cs,n):
    gw = {}
    for i in range(len(ws)):
        l = {}
        for c in cs:
            l[c] = len(set(ws[i]) & set(cs[c]))
        gw[i] = l
        
    tp_tn_fp_fn = combin(n,2)  
    tp_tn = 0  
    for g in gw.values():
        s = sum([l for l in g.values()])
        if s > 1:
            tp_tn +=  combin(s,2)
             
    tp = sum([combin(l,2) for g in gw.values() for l in g.values() if l > 1])
    fn = 0
    for c in cs:
        l = []
        for g in gw.values():
            l.append(g[c])
        combines = itertools.combinations(l,2)  
        for x,y in combines:
            fn += x*y
            
    tn =  tp_tn_fp_fn - tp_tn - fn
    return float((tp + tn))/tp_tn_fp_fn
            
if __name__ == '__main__':
    inverse_index('bing','bing_index.json')
    f = open('bing_index.json')
    inverse_index = json.loads(f.read())
    
    f1 = open('test_idf','w')
    f2 = open('test_idf2.json','w')
    fj = open('tf_doc.json','r')
    tf_doc = json.loads(fj.read())
        
    word_map = {}
    doc_map = {}
    index_doc_map = {}
    index_word_map = {}
    i = 0
    j = 0
    for word in inverse_index:
        word_map[word] = i
        index_word_map[i] = word
        i = i + 1
        for doc in inverse_index[word][2]:
            if doc not in doc_map:
                doc_map[doc] = j
                index_doc_map[j] = doc
                j = j + 1 
    
    for i in range(len(index_doc_map)):
        print str(i) + ' ' + index_doc_map[i]
    #print doc_map
    print len(word_map),len(doc_map)
    #print inverse_index
    tf_idf_index,tf_idf_dict= tf_idf_all(inverse_index,word_map,doc_map) 
    
    title_map = {}
    word_map_1 = {}
    index_title_map = {}
    i = 0
    j = 0
    for title in tf_doc:
        title_map[title] = i
        index_title_map[i] = title
        #print str(i) + ' ' + title
        i = i + 1
        for word in tf_doc[title]:
            if word not in word_map_1:
                word_map_1[word] = j
                j = j + 1 
                
    d1 = len(title_map)
    d2 = len(word_map_1)
    tf_idf_index_1 = numpy.zeros((d1,d2))
    
    for title in tf_doc:
        for word in tf_doc[title]:
            tf_idf_index_1[title_map[title]][word_map_1[word]] = tf_doc[title][word]
                
            
    json.dump(tf_idf_dict,f2)
      
    print len(tf_idf_index)
      
    miu,w = k_means(tf_idf_index,5)
    for cluster in w:
        if cluster:
            print "\n================================\n"
            for doc_num in cluster:
                print index_doc_map[doc_num] + ' ' 
    print '++++++++++++++++++++++++++++++++++++++++++++++++===='
    
    for key in doc_map.keys():
        print key
    c = get_class(doc_map)
    
    p = purity(w,c,len(tf_idf_index))
    ri = rand_index(w,c,len(tf_idf_index))
    
    print 'purity = %f ri = %f' % (p, ri)
    
    