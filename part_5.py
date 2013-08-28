'''
Created on Jun 13, 2013

@author: Administrator
'''

import numpy,json,math,pickle
from scipy.sparse import lil_matrix
from part_4 import cos_similarity

TWEET_PATH = 'C:/Users/Administrator/workspace/670_hw_1/mars_tweets_medium.json'
ALPHA = 0.1

def build_graph():
    graph = {}
    f = open(TWEET_PATH,'r') 
    ids = set()
    for line in f:
        tw = json.loads(line.strip().decode('UTF-8'))
        tw_mentions = [item['id'] for item in tw['entities']['user_mentions']] 
        if tw_mentions:
            if 'user' in tw:   
                user = tw['user']['id']
                if user in graph:
                    graph[user].extend(tw_mentions)
                else:
                    graph[user] = tw_mentions
                
    for key in graph:
        if key not in graph[key]:
            ids.add(key)
        for name in graph[key]:
            ids.add(name)       
    
    dimension = len(ids) 
    #print dimension
        
    i = 0
    id_index_map = {}
    for item in ids:
        id_index_map[item] = i
        i = i + 1
    
    graph_matrix = lil_matrix((dimension, dimension))  
       
    out_links = [0]*dimension
    for key in graph:       
        for name in graph[key]:
            if key != name:
                graph_matrix[id_index_map[key],id_index_map[name]] = 1
        out_links[id_index_map[key]] = len(graph[key])
    
    f1 = open('graph_matrix','w')
    f2 = open('out_links','w')
    pickle.dump(graph_matrix, f1)
    pickle.dump(out_links, f2)                                     
    return (graph_matrix, out_links)  
 
def fast_new_state(graph_matrix, out_links, old_state):
    dimension = len(out_links)
    new_states = numpy.array([0.0]*dimension)# pass reference will get input change, there is no constant in python, be careful the data type in array
    
    nz_rows = graph_matrix.nonzero()[0]
    nz_cols = graph_matrix.nonzero()[1]    
        
    for i in range(len(nz_rows)):#   
        row = nz_rows[i]
        col = nz_cols[i]
        new_states[col] += old_state[row] * (1-ALPHA) * graph_matrix[row,col]/float(out_links[row])
        #print new_states[col]
    
    nz_sum = sum([old_state[out_links.index(x)] for x in out_links if x != 0])
    z_sum = sum([old_state[out_links.index(x)] for x in out_links if x == 0])
        
    for i in range(dimension):
        new_states[i] +=  nz_sum * ALPHA * (1.0/dimension)
        new_states[i] +=  z_sum * (1.0/dimension)
    
    return new_states               

def fast_state_probability(graph_matrix_path,out_links_path):
    f1 = open(graph_matrix_path,'r')
    f2 = open(out_links_path,'r')
    graph_matrix = pickle.load(f1)
    out_links = pickle.load(f2)
    dimension = graph_matrix.shape[0]
    
    start_states = numpy.array([1.0/dimension]*dimension)
    print start_states
    old_states = start_states
    
    while True:
        states = fast_new_state(graph_matrix,out_links,old_states)
        print states
        if numpy.linalg.norm(states - old_states) < 0.00001:
        #math.acos(cos_similarity(states,old_states)) < (math.pi/180):
            break
        else:
            old_states = states
    
    print states
    return states    
                
    
def build_probabiliy_matrix(graph_matrix_path,out_links_path):      
    f1 = open(graph_matrix_path,'r')
    f2 = open(out_links_path,'r')
    graph_matrix = pickle.load(f1)
    out_links = pickle.load(f2)
    dimension = graph_matrix.shape[0]
             
    probabiliy_matrix = lil_matrix((dimension, dimension))
    
    for i in range(dimension):
        for j in range(dimension):
            if not out_links[i]:
                probabiliy_matrix[i,j] = (1.0/dimension)
            else:
                probabiliy_matrix[i,j] = (float(graph_matrix[i,j])/out_links[i])*(1-ALPHA) + (1.0/dimension)*ALPHA
    
    f1 = open('probability_matrix','w')
    pickle.dump(probabiliy_matrix, f1)
    return probabiliy_matrix

def state_probability(probabiliy_matrix):
    dimension = probabiliy_matrix.shape[0]
    start_states = numpy.array([1.0/dimension]*dimension)
    old_states = start_states
    while True:
        states = numpy.mat(start_states) * probabiliy_matrix
        if math.acos(cos_similarity(states,old_states)) < (math.pi/180):
            break
        else:
            old_states = states
    
    print states
    return states        
    
        
if __name__ == '__main__':
    graph,out_link = build_graph()
    #build_probabiliy_matrix('graph_matrix','out_links')
    #state_probability()
    fast_state_probability('graph_matrix','out_links')