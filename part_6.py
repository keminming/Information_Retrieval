'''
Created on Jun 28, 2013

@author: Administrator
'''

API_KEY = 'Aff2lBhj978dpqdlCMpPDBbrZjqLKi/g3vUclhuCUXY'
BING_URL = 'https://api.datamarket.azure.com/Bing/Search/News?'
PARAM = '&$format=json&$top=15'
BING_RESULT = 'bing/'


import urllib2,json,os,re,time

def bing_search(query,category,root_path):
    words = query.strip().split()
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, 'https://api.datamarket.azure.com/Bing/Search/', '', API_KEY)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler) 
    urllib2.install_opener(opener)
    query = 'Query=%27'
    for word in words:
        query += unicode(word) + '%20'
    p = query.rfind('%20')
    query = query[:p] + '%27'
    
    for i in range(2):
        url = BING_URL + query + category + PARAM + '&$skip=' + str(i*15)
        print url
        req = urllib2.Request(url)
        r = urllib2.urlopen(req)
        result = json.loads(r.read())
        
        print len(result['d']['results'])
        for result in result['d']['results']:
            title = result['Title']
            desc = result['Description']
            content = title + ' ' + desc
            #print desc

            f = open(root_path + re.sub(r'[^\w]','',title),'w')
            f.write(content.encode('utf-8'))
            f.close()
        
def create_bing():  
    if not os.path.exists('bing'):
        os.mkdir('bing')     
    bing_search('texas aggies','',BING_RESULT)
    bing_search('texas longhorns','',BING_RESULT)
    bing_search('duke blue devils','',BING_RESULT)
    bing_search('dallas cowboys','',BING_RESULT)
    bing_search('dallas mavericks','',BING_RESULT)    
    
def create_bing_training():
    if not os.path.exists('bing_training'):
        os.mkdir('bing_training')  
    os.chdir('bing_training')
    if not os.path.exists('texas_aggies'):
        os.mkdir('texas_aggies')
    if not os.path.exists('texas_longhorns'):
        os.mkdir('texas_longhorns')    
    if not os.path.exists('duke_blue_devils'):
        os.mkdir('duke_blue_devils')
    if not os.path.exists('dallas_cowboys'):
        os.mkdir('dallas_cowboys')
    if not os.path.exists('dallas_mavericks'):
        os.mkdir('dallas_mavericks')            
    
    bing_search('texas aggies','','texas_aggies/')
    bing_search('texas longhorns','','texas_longhorns/')
    bing_search('duke blue devils','','duke_blue_devils/')
    bing_search('dallas cowboys','','dallas_cowboys/')
    bing_search('dallas mavericks','','dallas_mavericks/')
          
if __name__ == '__main__':
    create_bing()
    create_bing_training()
    
