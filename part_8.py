'''
Created on Jul 1, 2013

@author: Administrator
'''
from part_6 import bing_search

if __name__ == '__main__':
    bing_search('bing','&NewsCategory=%27rt_Entertainment%27','training/business/')
    bing_search('amazon','&NewsCategory=%27rt_Entertainment%27','training/business/')
    bing_search('twitter','&NewsCategory=%27rt_Entertainment%27','training/business/')
    bing_search('yahoo','&NewsCategory=%27rt_Entertainment%27','training/business/')
    bing_search('google','&NewsCategory=%27rt_Entertainment%27','training/business/')
    bing_search('beyonce','&NewsCategory=%27rt_Business%27','training/entertainment/')
    bing_search('bieber','&NewsCategory=%27rt_Business%27','training/entertainment/')
    bing_search('television','&NewsCategory=%27rt_Business%27','training/entertainment/')
    bing_search('movies','&NewsCategory=%27rt_Business%27','training/entertainment/')
    bing_search('music','&NewsCategory=%27rt_Business%27','training/entertainment/')
    bing_search('obama','&NewsCategory=%27rt_Politics%27','training/politics/')
    bing_search('america','&NewsCategory=%27rt_Politics%27','training/politics/')
    bing_search('congress','&NewsCategory=%27rt_Politics%27','training/politics/')
    bing_search('senate','&NewsCategory=%27rt_Politics%27','training/politics/')
    bing_search('lawmakers','&NewsCategory=%27rt_Politics%27','training/politics/')
    
    