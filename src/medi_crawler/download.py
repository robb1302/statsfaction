import pandas as pd
from metapub import PubMedFetcher
from tqdm import tqdm

def get_articles(pmids:list = []):
    """ 
    Function gets articles of list of Pubmed IDs
    """
    if pmids == []:
        raise ValueError("Empty List of IDs")
    fetch = PubMedFetcher()
    dict_return = {}
    for pmid in tqdm(pmids):
        dict_return[pmid] = fetch.article_by_pmid(pmid)
    
    return_df = pd.DataFrame(list(dict_return.items()),columns = ['pmid','articles'])
    return return_df

def get_title(pmids:list = []):
    """ 
    Function gets articles of list of Pubmed IDs
    """
    if pmids == []:
        raise ValueError("Empty List of IDs")
    fetch = PubMedFetcher()
    dict_return = {}
    for pmid in tqdm(pmids):
        dict_return[pmid] = fetch.article_by_pmid(pmid).title
    
    return_df = pd.DataFrame(list(dict_return.items()),columns = ['pmid','title'])
    return return_df

def get_abstract(pmids:list = []):
    """ 
    Function gets articles of list of Pubmed IDs
    """
    if pmids == []:
        raise ValueError("Empty List of IDs")
    fetch = PubMedFetcher()
    dict_return = {}
    for pmid in pmids:
        dict_return[pmid] = fetch.article_by_pmid(pmid).abstract
    
    return_df = pd.DataFrame(list(dict_return.items()),columns = ['pmid','abstract'])
    return return_df

def get_author(pmids:list = []):
    """ 
    Function gets articles of list of Pubmed IDs
    """
    if pmids == []:
        raise ValueError("Empty List of IDs")
    fetch = PubMedFetcher()
    dict_return = {}
    for pmid in pmids:
        dict_return[pmid] = fetch.article_by_pmid(pmid).authors
    
    return_df = pd.DataFrame(list(dict_return.items()),columns = ['pmid','authors'])
    return return_df

def add_info(info,article_dict):
    value = ""
    if info in article_dict:
        value = str(article_dict[info])
    return value

def create_pubmed_series(crawl_columns,article_dict):
    temp = pd.DataFrame([add_info(info = c ,article_dict = article_dict) for c in crawl_columns]).T
    temp.columns = crawl_columns
    return temp

def create_pmid_summary(pmids:list,crawl_columns:list,file_path = 'results.csv'):
    summary_df = pd.DataFrame(columns=crawl_columns)
    fetch = PubMedFetcher()
    for id in tqdm(pmids):
        article_object = fetch.article_by_pmid(id)
        article_dict = article_object.to_dict()

        temp = pd.DataFrame()
        try:
            temp  = create_pubmed_series(crawl_columns,article_dict = article_dict)
        except:
            print("Fehler bei ID",str(id))
        if not temp.empty:
            summary_df = pd.concat([summary_df,pd.DataFrame(temp)],axis=0)

    summary_df.to_csv(file_path)