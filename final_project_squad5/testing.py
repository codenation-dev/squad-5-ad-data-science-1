# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 17:23:19 2019

@author: xpw
"""

from main import *
from config import *
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from tqdm import tqdm_notebook
from sklearn import preprocessing
import pickle
import collections

import matplotlib.pyplot as plt
import seaborn as sns

def save_new_portfolio(portfolio, name):
    portfolio.to_csv(name, index=False)    

estaticos_market = pd.read_csv('../'+data_path+'/estaticos_market.csv')
estaticos_portfolio1 = pd.read_csv('../'+data_path+'/estaticos_portfolio1.csv')
estaticos_portfolio2 = pd.read_csv('../'+data_path+'/estaticos_portfolio2.csv')
estaticos_portfolio3 = pd.read_csv('../'+data_path+'/estaticos_portfolio3.csv')

estaticos_portfolio5 = estaticos_portfolio1[estaticos_portfolio1['sg_uf'].str.match('AM', na=False)]
estaticos_portfolio5 = estaticos_portfolio5[estaticos_portfolio5['de_faixa_faturamento_estimado'].str.match('DE R\$ 81.000,01 A R\$ 360.000,00', na=False)]
estaticos_portfolio5 = estaticos_portfolio5[estaticos_portfolio5['idade_emp_cat'].str.match('5 a 10', na=False)]

# Define portfolio to be used

portfolio = estaticos_portfolio5
portfolio = rebuild_portfolio(portfolio, estaticos_market)


#c = rebuild_portfolio(portfolio, estaticos_market)

#print(c)

#estaticos_market_filter_raw, estaticos_market_filter = features(estaticos_market)

#titles, indices = titles_indices(estaticos_market_filter_raw)

#recommendations = predict(portfolio, titles, indices, estaticos_market_filter)


#estaticos_portfolio4 = "estaticos_portfolio4.csv"
#print(run(estaticos_portfolio4))

name = 'estaticos_portfolio5.csv'
save_new_portfolio(portfolio, name)