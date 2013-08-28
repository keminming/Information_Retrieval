'''
Created on Jul 1, 2013

@author: Administrator
'''
import os,re,pickle,math

def build_vacab():
    vacab_in_mem = set()
    vacab = open('vocab','w')
    names = os.listdir('training')
    os.chdir('training')
    for name in names:
        if os.path.isdir ( name ):
            filenames = os.listdir(name) 
            os.chdir(name)
            for filename in filenames:
                lines = open(filename,'r')
                for line in lines:
                    for word in re.split('[/.,()?!"\'; ]',line.strip().decode('utf-8')):
                        vacab_in_mem.add(word)
            os.chdir('..')            
    
    pickle.dump(vacab_in_mem, vacab)
    os.chdir('..')

def naive_bayes(classes,path):
    f = open('vocab','r')
    v = pickle.load(f)
    prior = {} 
    cond_prob = {}
    os.chdir(path)
    for c in classes:    
        filenames = os.listdir(c)
        os.chdir(c)
        nc = len(filenames) 
        prior[c] = nc/1350.0
        out = open('large_file','w')
        for filename in filenames:
            f = open(filename,'r')
            out.write(f.read())
        out.close()    
        
        word_count = {}            
        inf = open('large_file','r')    
        for line in inf:
            for word in line.strip().split():
                if word and word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1    
        
        total = sum([word_count[word] for word in word_count])             
        for word in v:
            if word in word_count:
                if word in cond_prob:
                    cond_prob[word][c] = float((word_count[word]+ 1))/(total + len(v))
                else:
                    cond_prob[word] = {}
                    cond_prob[word][c] = float((word_count[word]+ 1))/(total + len(v))    
            else:
                if word in cond_prob:
                    cond_prob[word][c] = 1.0/(total + len(v)) 
                else:
                    cond_prob[word] = {}
                    cond_prob[word][c] = 1.0/(total + len(v))
                        
        os.chdir('..')
    os.chdir('..')            
    return (prior,cond_prob)

def classify(d,classes,prior,cond_prob):
    score = {}
    lines = open(d,'r')
    words = [word for line in lines for word in line.decode('utf-8').strip().split()]
    for c in classes:
        score[c] = prior[c]
        for word in words:
            if word in cond_prob:
                score[c] += math.log(cond_prob[word][c])
    return max(score.keys(),key=lambda x:score[x])        
    
if __name__ == '__main__':
    build_vacab()
    classes = ['business','entertainment','politics']
    prior,cond_prob = naive_bayes(classes,'training')
    c = classify('training/business/20_Things_w',classes,prior,cond_prob)
    print c
    
    