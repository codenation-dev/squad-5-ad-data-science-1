import fire
from config import *
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)
from tqdm import tqdm
from sklearn import preprocessing
import collections
import json
import time

def rebuild_portfolio(portfolio, estaticos_market):
    
    """Function that will generate the full portfolio dataset using the
    provided id names on the portfolio file.
    """
    
    print("==> EXPANDING PORTFOLIO DATASET")
    
    full_portfolio = pd.DataFrame()
    for i in tqdm(portfolio['id']):
        selected_id = estaticos_market[estaticos_market['id'].str.contains(i, na=False)]
        full_portfolio = pd.concat([full_portfolio, selected_id], ignore_index=True)
    
    return full_portfolio

def titles_indices(estaticos_market_filter_raw):
    
    """Function that get the index of the provided ids."""
    
    titles = estaticos_market_filter_raw['id']
    indices = pd.Series(estaticos_market_filter_raw.index, index=estaticos_market_filter_raw['id'])
    
    return titles, indices

def get_recommendations(id_n, titles, indices, estaticos_market_filter):
    
    """Function that uses the pairwise metric Cosine Similarity to
    create recommendations based on a portfolio and market data
    """
    
    idx = indices[id_n]
    cosine_sim = cosine_similarity(estaticos_market_filter[idx:idx+1], estaticos_market_filter)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    all_scores = np.array(sim_scores[1:]) # All cosine distances id x market
    sim_scores = np.array(sim_scores[1:1000]) # Number of recomendations per id
    return titles.iloc[sim_scores[:,0]], sim_scores[:,1], all_scores[:,1]

def features(estaticos_market):    
    
    """Function that will generate the dataset for your model. It can
    be the target population, training or validation dataset. You can
    do in this step as well do the task of Feature Engineering.
    """
    
    def filter_null_porcent(col):
        nulls_value = estaticos_market[col].isna().sum()
        percentage = 100*(nulls_value / estaticos_market.shape[0])
        return percentage <= 10.0
    
    def filter_col_numbers(col):
        dtype = estaticos_market_filter[col].dtypes
        return dtype == np.dtype('int64') or dtype == np.dtype('float64')    

    print("==> GENERATING DATASETS AND PREPROCESSING FEATURES")
    
    col_filter = list(filter(filter_null_porcent, estaticos_market.columns))
    estaticos_market_filter = estaticos_market[col_filter]
    col_filter_number = list(filter(filter_col_numbers, estaticos_market_filter.columns))
    
    for col in col_filter_number:
        if col not in ["nu_meses_rescencia", "idade_empresa_anos"]:
            estaticos_market_filter.drop([col], axis=1, inplace=True)
            
    col_exclude = ["fl_matriz", "fl_me", "fl_sa", "fl_epp", "fl_ltda", "fl_st_especial", "fl_spa", "fl_antt",
                  "fl_veiculo", "fl_simples_irregular"]
    
    estaticos_market_filter.drop(col_exclude, axis=1, inplace=True)
    estaticos_market_filter = estaticos_market_filter.fillna(0)
    
    for col in estaticos_market_filter.columns:
        if col not in ["nu_meses_rescencia","idade_empresa_anos", "id"]:
            try:
                estaticos_market_filter[col] = estaticos_market_filter[col].astype('category')
                estaticos_market_filter[col] = estaticos_market_filter[col].cat.codes
                estaticos_market_filter[col] = estaticos_market_filter[col].astype('int')
    
            except KeyError:
                pass
            
    estaticos_market_filter_raw = estaticos_market_filter.copy()
    
    try:
        estaticos_market_filter.drop(['id'], axis=1, inplace=True)
        
    except KeyError:
        pass
    
    estaticos_market_filter = preprocessing.scale(estaticos_market_filter) # feature scaling
    
    return estaticos_market_filter_raw, estaticos_market_filter


def train(**kwargs):
    
    """Function that will run your model, be it a NN, Composite indicator
    or a Decision tree, you name it.

    NOTE
    ----
    config.models_path: workspace/models
    config.data_path: workspace/data

    As convention you should use workspace/data to read your dataset,
    which was build from generate() step. You should save your model
    binary into workspace/models directory.
    """
    print("==> TRAINING YOUR MODEL!")


def metadata(portfolio, score_mean_list, score_max_list, score_min_list, rec_list, portfolio_name):
    
    """Generate metadata for model governance using testing!"""
    
    print("==> TESTING MODEL PERFORMANCE AND GENERATING METADATA")
    mean_score_recommendations = sum(score_mean_list)/len(score_mean_list)
    min_score_recommendations = min(score_min_list)
    max_score_recommendations = max(score_max_list)
    
    check_match = []
    for i in portfolio['id']:    
        if i in rec_list:
            check_match.append(i)
            
    overlap_rec = len(check_match)/len(portfolio['id'])

    my_details = {
       'name': 'Model performance',
       'metrics': {
           'Overlap Portfolio on Rec': round(overlap_rec, 2)*100,
           'Min Cossine Distance': min_score_recommendations,
           'Mean Cossine Distance': mean_score_recommendations,
           'Max Cossine Distance': max_score_recommendations,          
        },
       'source': '{}'.format(portfolio_name)
    }
    
    with open('../workspace/output/performance.json', 'w') as json_file:  
        json.dump(my_details, json_file)
        
    print("==> Performance saved sucessfully on 'output/perfomance.json'!")

def predict(portfolio, titles, indices, estaticos_market_filter):
    
    """Predict: load the trained model and score input_data."""
    
    print("==> PREDICT DATASET")
    rec_list = []
    score_mean_list = []
    score_max_list = []
    score_min_list = []
    first_run = True
    for i in tqdm(portfolio['id']):
        id_empresa, scores, all_scores = get_recommendations(i, titles, indices, estaticos_market_filter)
        score_mean = scores.mean()
        score_max = scores.max()
        score_min = scores.min()
        score_mean_list.append(score_mean)
        score_max_list.append(score_max)
        score_min_list.append(score_min)
        if first_run == True:
            all_scores_result = all_scores
            first_run = False
        all_scores_result = (all_scores_result + all_scores) / 2
        for x, y in zip(id_empresa, scores):
            rec_list.append(x)
            
    counter=collections.Counter(rec_list)
    # Remove duplicates portfolio x recommendations
    for i in portfolio['id']:
        if i in counter:
            del counter[i]

    number_recommendations = 200 # How many final recommendations we want?
    most_commom = counter.most_common(number_recommendations)
    
    recommendations = [x[0] for x in most_commom]

    return recommendations, score_mean_list, score_max_list, score_min_list, rec_list
    
def set_files(portfolio_file, estaticos_market):

    portfolio = rebuild_portfolio(portfolio_file, estaticos_market)
    
    return portfolio

# Run all pipeline sequentially
def run(**kwargs):
    """Run the complete pipeline of the model."""
    
    start_time = time.time()
    print("Running final_project_squad5")
    estaticos_market = pd.read_csv('../'+data_path+'/estaticos_market.csv')
    
    using_portfolio = False
    for key, value in kwargs.items():
        if key == 'portfolio':
            using_portfolio = True
            portfolio_file = pd.read_csv(value)
            portfolio_name = str(value)

    if using_portfolio == False:
        portfolio_name = 'estaticos_portfolio1'
        portfolio_file = pd.read_csv('../'+data_path+'/'+portfolio_name+'.csv')
    
    portfolio = set_files(portfolio_file, estaticos_market)
    
    estaticos_market_filter_raw, estaticos_market_filter = features(estaticos_market)    
    titles, indices = titles_indices(estaticos_market_filter_raw)    
    recommendations, score_mean_list, score_max_list, score_min_list, rec_list = predict(portfolio, titles, indices, estaticos_market_filter)
    
    metadata(portfolio, score_mean_list, score_max_list, score_min_list, rec_list, portfolio_name)
    
    with open('../workspace/output/recommendations.txt', 'w') as f:
        for item in recommendations:
            f.write("%s\n" % item)
            
    print("==> New Leads saved sucessfully on 'output/recommendations.txt'!")
    
    time_to_run = time.time() - start_time
    print("==> The script took %s seconds to run completely." % (round(time_to_run, 2)))

def cli():
    """Caller of the fire cli"""
    return fire.Fire()

if __name__ == '__main__':
    cli()
