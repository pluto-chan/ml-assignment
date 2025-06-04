import numpy as np
import pandas as pd
import json
from fastapi import HTTPException

pd.set_option('future.no_silent_downcasting', True)

def process_app_date(app_date):
    try:
        return pd.to_datetime(app_date).date()
    except:
        raise HTTPException(status_code=400, detail='Invalid application date format') 

def try_datetime(date):
    try:
        return pd.to_datetime(date, dayfirst=True).date()
    except:
        return np.nan

def process_contracts(contracts, allow_extra_columns=False, allow_missing_columns=True):

    if type(contracts) in [str, dict, list]:
        try:
            if isinstance(contracts, str):
                if contracts == '':
                    return -3
                contracts = json.loads(contracts)
            
            if isinstance(contracts, dict):
                df_contracts = pd.DataFrame(contracts, index=[0])
            else:
                df_contracts = pd.DataFrame(contracts)
            
            essential_columns = set(['contract_id', 'bank', 'summa', 'loan_summa', 'claim_date', 'claim_id', 'contract_date'])
            
            if len(essential_columns - set(df_contracts.columns)) > 0:
                if allow_missing_columns:
                    for missing_col in list(essential_columns - set(df_contracts.columns)):
                        df_contracts.insert(len(df_contracts.columns), missing_col, ['']*len(df_contracts))
                else:
                    raise HTTPException(status_code=400, detail='Invalid JSON string format in contracts')
                
            if len(set(df_contracts.columns) - essential_columns) > 0:
                if not allow_extra_columns:
                    raise HTTPException(status_code=400, detail='Invalid JSON string format in contracts')
                        
            df_contracts = df_contracts.replace(r'^\s*$', np.nan, regex=True)
            df_contracts['claim_date'] = df_contracts['claim_date'].apply(try_datetime)
            df_contracts['contract_date'] = df_contracts['contract_date'].apply(try_datetime)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail='Invalid JSON string format in contracts') 
        
        return df_contracts
    else:
        try:
            if pd.isna(contracts):
                return -3
        except:
            raise HTTPException(status_code=400, detail='Invalid JSON string format in contracts') 
        
def cc180(app_date, contracts, relevant_time_period = '180 days'):
    start_date = app_date-pd.to_timedelta(relevant_time_period)
    return contracts[contracts['claim_date'] >= start_date].shape[0]
   
def disb_loan_sum(contracts):
    tbc_loans = ['LIZ', 'LOM', 'MKO', 'SUG', '']
    loans = contracts[~contracts['bank'].isin(tbc_loans) & (~contracts['bank'].isnull()) \
                     & (~contracts['contract_date'].isnull())]
    
    if loans.shape[0] == 0:
        return -1
    else:
        return float(loans['loan_summa'].sum())
 
def days_since_last_loan(app_date, contracts):
    contracts = contracts[~contracts['summa'].isnull()]
    
    if contracts.shape[0] == 0:
        return -1
    else:
        last_loan_date = contracts['contract_date'].max()
        
        return (app_date - last_loan_date).days
