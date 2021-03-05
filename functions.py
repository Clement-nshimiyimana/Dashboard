from datetime import datetime as dt
import datetime
from datetime import datetime 
from datetime import date, timedelta	
import time
import gc
import cx_Oracle

from calendar import monthrange

import warnings
warnings.filterwarnings("ignore")
## To assign session Id
import uuid

import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
# from layouts import *

from components import *
from config import *
## For session and enhance performance
# from os import path
# import sys
# sys.path.append(path.join(path.dirname(__file__), '..'))
from app import cache1, TIMEOUT, session_id
import locale
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
## To handle the parameters by url
def parse_query_params(s):
    s = s.lstrip("?")
    return dict(pair.split("=") for pair in s.split("&"))

####################################################################################################
################################## Some useful functions ############################################
#####################################################################################################
## DB connections
userid ="T002CNSH"
password="Changeme01"
host="192.168.186.25"
port = "1521"
SID = "VISIONRW"

## DB parameters
userid_fiorano ="DATASCIENTIST"
password_fiorano="inmRw2019"
host_fiorano="192.168.186.15"
port_fiorano = "1521"
SID_fiorano = "RWESBDB"

## OCH DB parameters
userid_och ="DATASCIENTISTRW"
password_och="RwndDsCt321"
host_och="192.168.202.62"
port_och = "1621"
SID_och = "IMPRODDB"

# ## Get connection to the DB
# def get_connection(userid=userid, password=password, host=host, port=port, SID=SID):
#     """
#     Get access to the DB 
#     """
#     dsn_tns = cx_Oracle.makedsn(host, port, service_name=SID) 
#     conn = cx_Oracle.connect(user=userid, password=password, dsn=dsn_tns) 
#     return conn

# ##connection to fiorano
# def get_connection_fiar(userid=userid_fiorano, password=password_fiorano, host=host_fiorano, port=port_fiorano, SID=SID_fiorano):
#     """
#     Get access to the DB 
#     """
#     dsn_tns = cx_Oracle.makedsn(host, port, service_name=SID_fiorano) 
#     conn1 = cx_Oracle.connect(user=userid_fiorano, password=password_fiorano, dsn=dsn_tns) 
#     return conn1

# ##connection to och
# def get_connection_och(userid=userid_och, password=password_och, host=host_och, port=port_och, SID=SID_och):
#     """
#     Get access to the DB 
#     """
#     dsn_tns = cx_Oracle.makedsn(host, port, service_name=SID_och) 
#     conn2 = cx_Oracle.connect(user=userid_och, password=password_och, dsn=dsn_tns) 
#     return conn2
def get_percentage_label(y):
    
    labels= []
    
    for i in y:
        labels += [str(i)+"%"]
        
    return labels

def format_hover_template(x_label= "Age Range", y_label= "# of Accounts", x_unit=""):
    
    template = (x_label+": %{x} "+x_unit+"<br>"+\
            y_label+": %{y:,.0f}<br>"+\
            "Rate: %{text}<br>"+\
            "Balance: %{customdata:,.0f} RWF"+\
            "<extra></extra>")
    return template

# def format_text_template():
    
#     template = (
#         "%{text}<br>"+\
#         "%{customdata:,.0f} RWF"
#     )
#     return template

def get_previous_month():
    start= str(dt.today().year)+'-'+str(dt.today().month-1)+'-01'
    end= str(dt.today().year)+'-'+str(dt.today().month-1)+'-'+str(monthrange(dt.today().year, dt.today().month-1)[1])
                                                      
    return start, end

def format_(v):
    return "{:,.0f}".format(v)

def format_time_index(idx):
    idxx = [d.replace(", ","-")[1:-1] for d in idx]
    if idxx[0] == "-inf-0.0":
        idxx[0] = "Passed"
    return idxx


def get_rate_suffix(d):
    if len(str(d))==1:
        return '0'+str(d)
    else:
        return str(d)

def format_big_number(d):
    dd = d.astype(str)
    for i in range(d.shape[0]):
        dd[i] = "{:,.0f}".format(d[i])
    
    return dd
    
def add_image_file_name_to_config(d1, d2):
    # if d1 is None:
    #     return d2
    # else:
    d = d1.copy()
    d["toImageButtonOptions"] = d2
    return d

@cache1.memoize(timeout=TIMEOUT)
def get_bnr_current_exchange_rate(session_id):

    for i in range(1,32):
        
        query = """
        SELECT YEAR_MONTH, CURRENCY, RATE_{}
        FROM VISIONRW.Currency_Rates_Daily
        WHERE TO_CHAR(YEAR_MONTH) = {}
        """.format(get_rate_suffix((date.today()-timedelta(i)).day), (date.today()-timedelta(i)).strftime("%Y%m"))

        forex = pd.read_sql(query, con=get_connection())
#         forex1 = forex.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\forex.csv', index=None, header=True)        
#         if forex.shape[0] != 0:

        return forex, i

#####################################################################################################
################################## Overview Page Content Functions###################################
#####################################################################################################

# Writing as a function
def process_chunk(chunk, func):
    grouped_object = chunk.groupby(chunk.index,sort = False) # not sorting results in a minor speedup
    answer = grouped_object.agg(func)
    return answer

#####################################################################
## Read Transactional data
@cache1.memoize(timeout=TIMEOUT)
def get_data_aggregated(session_id, func, chunksize,query, idx_col ):
    
    start_time = time.time()
    
    i = 0 
    for chunk_data in pd.read_sql(query, con=get_connection(), chunksize = chunksize, index_col = idx_col) :
        
        if(i==0):
            result = process_chunk(chunk_data,func)
            print("Number of rows ",result.shape[0])
            print("Loop ",i,"took {:.2f} seconds\n".format(time.time() - start_time))
            i = 1
        else:
            result = result.append(process_chunk(chunk_data,func))
            print("Number of rows ",result.shape[0])
            print("Loop ",i,"took {:.2f} seconds\n".format(time.time() - start_time))
            i += 1
            
        del(chunk_data); gc.collect() 
        start_time = time.time()
        
    # Unique users vs Number of rows after the first computation    
    print("size of result:", len(result))
    check = result.index.unique()
    print("unique user in result:", len(check))

    result.columns = ['_'.join(col).strip() for col in result.columns.values]
    
    index = pd.MultiIndex.from_tuples(result.index)
    result = result.reindex(index)
    
    result.index.names = idx_col
    result = result.reset_index(idx_col)
    
    return result


##################################################CHANNEL'S TRANSACTIONS#############################################
# @cache1.memoize(timeout=TIMEOUT)
# def get_customer_channel_choice(session_id):
# 	# @cache1.memoize(timeout=TIMEOUT)
# 	# get_channel_data_and_serilize(session_id)
# 	channel_trans_query = """
# 	SELECT CONTRACT_ID, CURRENCY, TRANSACTION_CHANNEL, TRAN_AMT
# 	FROM VISIONRW.TRANS_COUNT_FEED_STG
# 	WHERE LENGTH(CONTRACT_ID) = 11
# 	"""

# 	idx_col = ["CONTRACT_ID","CURRENCY","TRANSACTION_CHANNEL"]

# 	chunksize = 2000000

# 	func = {
# 	    "TRAN_AMT":["sum"],
# 	}

# 	result = get_data_aggregated(session_id, func, chunksize,query=channel_trans_query, idx_col=idx_col )

# 	#%% Change all TELLER into PBI
# 	result.TRANSACTION_CHANNEL = np.where(result.TRANSACTION_CHANNEL == "TELLER", "PBI",result.TRANSACTION_CHANNEL)

# 	df1 = result.pivot_table(values="TRAN_AMT_sum", 
# 	                index=["CONTRACT_ID","CURRENCY"], columns=["TRANSACTION_CHANNEL"],
# 	                aggfunc=["count","sum"], fill_value=0, margins=False, 
# 	                dropna=False, margins_name='All')

# 	df1.columns = ['_'.join(col).strip() for col in df1.columns.values]

# 	df1.reset_index(["CONTRACT_ID","CURRENCY"], inplace=True)

# 	#%%
# 	df2 = result.pivot_table(values="TRAN_AMT_sum", index="CONTRACT_ID", 
# 	                        columns=["CURRENCY"],aggfunc=["count","sum"], 
# 	                        fill_value=0, margins=False, dropna=False, margins_name='All')

# 	df2.columns = ['_'.join(col).strip() for col in df2.columns.values]

# 	## Task: automate both some below
# 	count_cols = []
# 	sum_cols = []
# 	for col in df2.columns.values:
# 	    if "count" in col:
# 	        count_cols += [col]
# 	    elif "sum" in col:
# 	        sum_cols += [col]

# 	df2["transaction_no"] = df2[count_cols].sum(axis=1)
# 	df2["transaction_amt_fcy"] = df2[sum_cols].sum(axis=1)

# 	df2 = df2.drop(df2.columns.values[:-2], axis=1)
# 	df2.reset_index("CONTRACT_ID", inplace=True)

# 	#%% Merge both dfs above
# 	df=df1.merge(df2, on="CONTRACT_ID")
# 	df.columns=df.columns.str.lower()
# # 	forex1=df.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\chann_vis.csv',index=None,header=True) 
# 	#%%
# 	## Get the exchange rate from Currency_Rates_Daily table from VisionDB
# 	forex, days_ago = get_bnr_current_exchange_rate(session_id)
# 	mapping ={"RWF":1}
# 	for val in forex.CURRENCY.values:
# 	    if val in df.currency.unique():
# 	        mapping[val] = (forex[val == forex.CURRENCY.values]["RATE_{}".format(get_rate_suffix((date.today()-timedelta(days_ago)).day))]).values[0]

# 	# print(mapping)

# 	## Convert each column of amount to rwf
# 	for col in df.columns.values:
# 	    if "sum" in col:
# 	        df[col] = df.currency.map(mapping)*df[col]

# 	df['transaction_amt_lcy'] = df.currency.map(mapping)*df.transaction_amt_fcy
# 	#     df.drop("currency", axis=1, inplace=True)

# 	#%%
# 	cols_name_map ={}
# 	for col in df.columns.values:
# 	    if "count" in col:
# 	        cols_name_map[col] = col[6:]
# 	    elif "sum" in col:
# 	        cols_name_map[col] = col[4:]+"_amt"

# 	# print(cols_name_map)

# 	df.rename(columns=cols_name_map, inplace=True) # Rename cols

# 	#%% Get channels columns index 
# 	idx = df.columns.values[2:-12]
# 	# print(idx)

# 	## Compute the mean amount per transaction by channel
# 	for col in idx[:9]:
# 	    df[col+"_mean"] = df[col+"_amt"]/ df[col]
# 	    df[col+"_mean"].fillna(0, inplace=True)

# 	## Compute the mean amount per transaction 
# 	df["mean_transact_amt"] = df.transaction_amt_lcy/ df.transaction_no

# 	#%%
# 	df["customer_id"] = df.contract_id.astype(str).str[:-3]

# 	df_grp = df.groupby(["customer_id", "currency"], sort = False)[(df.columns.values[1:-1])].sum()
# 	df_grp.reset_index(["customer_id", "currency"], inplace=True)

# 	## Get channels columns index 
# 	idx = df_grp.columns.values[2:-12]
# 	# print(idx)

# 	## Compute the mean amount per transaction per customer by channel
# 	for col in idx[:8]:
# 	    df_grp[col+"_mean"] = df_grp[col+"_amt"]/ df_grp[col]
# 	    df_grp[col+"_mean"].fillna(0, inplace=True)

# 	## Compute the mean amount per transaction per customer
# 	df_grp["mean_transact_amt"] = df_grp.transaction_amt_lcy/ df_grp.transaction_no

# 	#%% 
# 	## Get channels columns index 
# 	idx = df_grp.columns.values[2:]
# 	# print(idx)

# 	### Customer preferred Channel in terms of amount spent, #of time chose channel
# 	##Get the prefered customer's channel in terms of amount spent
# 	df_grp["prefered_channel_by_amt"] = df_grp[idx[21:-1]].idxmax(axis=1)
# 	df_grp["prefered_channel_by_amt"] = df_grp["prefered_channel_by_amt"].astype(str).str[:-5]

# 	##Get the prefered customer's channel in terms #of time chose channel
# 	df_grp["prefered_channel_by_trans"] = df_grp[idx[:9]].idxmax(axis=1)
# 	# df_grp["prefered_channel_by_trans"] = df_grp["prefered_channel_by_trans"].astype(str).str[:-5]

# 	#%% Get the number of channels a customer already used
# 	df_grp["no_channel_used"] = df_grp[idx[:9]].replace(0, np.nan).count(axis=1).astype(np.uint8)

# 	output_cols = ["customer_id","currency","transaction_amt_fcy","transaction_amt_lcy","prefered_channel_by_amt", "prefered_channel_by_trans", "no_channel_used"]
	
# 	return df_grp.loc[:, output_cols]

##################################################################################################
#######################################KIRA COMPAIN###########################################################
# @cache1.memoize(timeout=TIMEOUT)
# def get_customer_account_trend_data(session_id, cust_type="ALL"):

# 	customer_opening_query = """
#     SELECT VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID,VISIONRW.CUSTOMERS_DLY.CUSTOMER_OPEN_DATE,
#     VISIONRW.CUSTOMERS_DLY.VISION_SBU,VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE,VISIONRW.ACCOUNTS_DLY.SCHEME_CODE,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_OPEN_DATE,VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS,
#     COUNT(DISTINCT ACCOUNT_NO)AS NUM_OF_ACCOUNTS,
#     COUNT(CASE WHEN VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS=0 then 1 end) as ACTIVE,
#     COUNT(CASE WHEN VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS=1 then 1 end) as INACTIVE,
#     COUNT(CASE WHEN VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS=2 then 1 end) as CLOSED,    
#     COUNT(CASE WHEN VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS=3 then 1 end) as DORMANT,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_NO
#     FROM VISIONRW.CUSTOMERS_DLY 
#     INNER JOIN VISIONRW.ACCOUNTS_DLY
#     ON VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID = VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID
#     WHERE VISIONRW.ACCOUNTS_DLY.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26','CAL05' )
#     AND VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID <> 'D000'
#     GROUP BY 
#     VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID,
#     VISIONRW.CUSTOMERS_DLY.CUSTOMER_OPEN_DATE,
#     VISIONRW.CUSTOMERS_DLY.VISION_SBU,VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE,VISIONRW.ACCOUNTS_DLY.SCHEME_CODE,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_OPEN_DATE,VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_NO
#         """
# 	customer_opening = pd.read_sql(customer_opening_query, con=get_connection())
# ##############################################################################################################################################################################################################################################################
@cache1.memoize(timeout=TIMEOUT)
def get_loan_dep_trend(session_id, cust_type="ALL"):  
# 	query="""
#     SELECT 
#     VISIONRW.Fin_Dly_Headers.Year_Month AS Year_Month ,VISIONRW.FRL_Lines_BS.FRL_Attribute_05 AS FRL_Attribute_05 ,
#  ((select FRL_ATTRIBUTE_DESCRIPTION from  VISIONRW.FRL_ATTRIBUTES WHERE FRL_ATTRIBUTE_LEVEL =5 
# AND FRL_Lines_BS.FRL_ATTRIBUTE_05 = FRL_ATTRIBUTE))  AS FRL_Att_05_Description,
# ((select FRL_ATTRIBUTE_DESCRIPTION from  VISIONRW.FRL_ATTRIBUTES WHERE FRL_ATTRIBUTE_LEVEL =1 AND 
# VISIONRW.FRL_Lines_BS.FRL_ATTRIBUTE_01 = FRL_ATTRIBUTE))  AS FRL_Att_01_Description ,
#     VISIONRW.Fin_Dly_Headers.Customer_Id AS Customer_Id,
#     VISIONRW.OUC_Expanded.OUC_Description AS OUC_Description,
#     VISIONRW.Fin_Dly_Headers.Vision_SBU AS Vision_SBU, 
#     VISIONRW.Fin_Dly_Headers.Record_Type AS Record_Type , 
#     VISIONRW.Fin_Dly_Balances.Bal_Type AS Bal_Type , 
#     VISIONRW.Fin_Dly_Headers.Currency AS Currency,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_01*VISIONRW.Currency_Rates_Daily.RATE_01) AS Balance_01,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_02*VISIONRW.Currency_Rates_Daily.RATE_02) AS Balance_02,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_03*VISIONRW.Currency_Rates_Daily.RATE_03) AS Balance_03,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_04*VISIONRW.Currency_Rates_Daily.RATE_04) AS Balance_04,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_05*VISIONRW.Currency_Rates_Daily.RATE_05) AS Balance_05,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_06*VISIONRW.Currency_Rates_Daily.RATE_06) AS Balance_06,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_07*VISIONRW.Currency_Rates_Daily.RATE_07) AS Balance_07,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_08*VISIONRW.Currency_Rates_Daily.RATE_08) AS Balance_08,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_09*VISIONRW.Currency_Rates_Daily.RATE_09) AS Balance_09,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_10*VISIONRW.Currency_Rates_Daily.RATE_10) AS Balance_10,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_11*VISIONRW.Currency_Rates_Daily.RATE_11) AS Balance_11,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_12*VISIONRW.Currency_Rates_Daily.RATE_12) AS Balance_12,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_13*VISIONRW.Currency_Rates_Daily.RATE_13) AS Balance_13,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_14*VISIONRW.Currency_Rates_Daily.RATE_14) AS Balance_14,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_15*VISIONRW.Currency_Rates_Daily.RATE_15) AS Balance_15,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_16*VISIONRW.Currency_Rates_Daily.RATE_16) AS Balance_16,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_17*VISIONRW.Currency_Rates_Daily.RATE_17) AS Balance_17,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_18*VISIONRW.Currency_Rates_Daily.RATE_18) AS Balance_18,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_19*VISIONRW.Currency_Rates_Daily.RATE_19) AS Balance_19,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_20*VISIONRW.Currency_Rates_Daily.RATE_20) AS Balance_20,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_21*VISIONRW.Currency_Rates_Daily.RATE_21) AS Balance_21,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_22*VISIONRW.Currency_Rates_Daily.RATE_22) AS Balance_22,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_23*VISIONRW.Currency_Rates_Daily.RATE_23) AS Balance_23,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_24*VISIONRW.Currency_Rates_Daily.RATE_24) AS Balance_24,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_25*VISIONRW.Currency_Rates_Daily.RATE_25) AS Balance_25,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_26*VISIONRW.Currency_Rates_Daily.RATE_26) AS Balance_26,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_27*VISIONRW.Currency_Rates_Daily.RATE_27) AS Balance_27,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_28*VISIONRW.Currency_Rates_Daily.RATE_28) AS Balance_28,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_29*VISIONRW.Currency_Rates_Daily.RATE_29) AS Balance_29,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_30*VISIONRW.Currency_Rates_Daily.RATE_30) AS Balance_30,
#     SUM(VISIONRW.Fin_Dly_Balances.Balance_31*VISIONRW.Currency_Rates_Daily.RATE_31) AS Balance_31
#     FROM 
#     VISIONRW.Fin_Dly_Headers Fin_Dly_Headers
#     JOIN VISIONRW.Fin_Dly_Balances  Fin_Dly_Balances ON 
#     VISIONRW.Fin_Dly_Headers.Country = VISIONRW.Fin_Dly_Balances.Country AND 
#     VISIONRW.Fin_Dly_Headers.Le_Book = VISIONRW.Fin_Dly_Balances.Le_Book AND 
#     VISIONRW.Fin_Dly_Headers.Year_Month = VISIONRW.Fin_Dly_Balances.Year_Month AND 
#     VISIONRW.Fin_Dly_Headers.Sequence_FD = VISIONRW.Fin_Dly_Balances.Sequence_FD And 
#     VISIONRW.Fin_Dly_Headers.RECORD_TYPE != 9999
#     JOIN VISIONRW.Currency_Rates_Daily ON 
#      VISIONRW.Fin_Dly_Headers.Country = VISIONRW.Currency_Rates_Daily.Country AND 
#      VISIONRW.Fin_Dly_Headers.Le_Book = VISIONRW.Currency_Rates_Daily.Le_Book AND
#      VISIONRW.Fin_Dly_Headers.Year_Month = VISIONRW.Currency_Rates_Daily.Year_Month 
#      AND VISIONRW.Fin_Dly_Headers.currency = VISIONRW.Currency_Rates_Daily.currency 
#      And VISIONRW.Fin_Dly_Headers.RECORD_TYPE != 9999
#     LEFT JOIN VISIONRW.OUC_Expanded  OUC_Expanded ON
#     VISIONRW.Ouc_Expanded.Vision_OUC = VISIONRW.Fin_Dly_Headers.Vision_OUC 
#     And VISIONRW.Fin_Dly_Headers.RECORD_TYPE != 9999
#     LEFT JOIN VISIONRW.VW_Customers_Dly_Expanded  Customers_Dly_Expanded ON
#     VISIONRW.Customers_Dly_Expanded.Country = VISIONRW.Fin_Dly_Headers.Country AND 
#     VISIONRW.Customers_Dly_Expanded.Le_Book = VISIONRW.Fin_Dly_Headers.Le_Book AND 
#     VISIONRW.Customers_Dly_Expanded.Customer_ID = VISIONRW.Fin_Dly_Headers.Customer_ID And 
#     VISIONRW.Fin_Dly_Headers.RECORD_TYPE != 9999
#     JOIN VISIONRW.Fin_Dly_Mappings  Fin_Dly_Mappings ON 
#     VISIONRW.Fin_Dly_Balances.Country = VISIONRW.Fin_Dly_Mappings.Country AND
#     VISIONRW.Fin_Dly_Balances.Le_Book = VISIONRW.Fin_Dly_Mappings.Le_Book AND 
#     VISIONRW.Fin_Dly_Balances.Year_Month = VISIONRW.Fin_Dly_Mappings.Year_Month AND
#     VISIONRW.Fin_Dly_Balances.Sequence_FD = VISIONRW.Fin_Dly_Mappings.Sequence_FD AND 
#     VISIONRW.Fin_Dly_Balances.Dr_Cr_Bal_Ind = VISIONRW.Fin_Dly_Mappings.Dr_Cr_Bal_Ind
#     JOIN VISIONRW.FRL_Lines  FRL_Lines_BS ON 
#     VISIONRW.Fin_Dly_Mappings.FRL_Line_BS = VISIONRW.FRL_Lines_BS.FRL_Line  
#     WHERE VISIONRW.FRL_Lines_BS.FRL_Attribute_05 in  ('FA051050','FA052010') AND  
#     VISIONRW.FRL_Lines_BS.Source_Type = '0' AND  VISIONRW.Fin_Dly_Headers.Record_Type not in  ('9999' ) AND
#     VISIONRW.Fin_Dly_Balances.Bal_Type = '51' AND VISIONRW.Fin_Dly_Headers.CUSTOMER_ID<>'DOOO' 
#     AND VISIONRW.Fin_Dly_Headers.Year_Month>=202003
#     GROUP BY 
#     VISIONRW.Fin_Dly_Headers.Year_Month ,     
#     VISIONRW.FRL_Lines_BS.FRL_Attribute_05,
#      VISIONRW.FRL_Lines_BS.FRL_Attribute_01,   
#     VISIONRW.Fin_Dly_Headers.Customer_Id ,  
#     VISIONRW.OUC_Expanded.OUC_Description , 
#     VISIONRW.Fin_Dly_Headers.Vision_SBU , 
#     VISIONRW.Fin_Dly_Headers.Record_Type , 
#     VISIONRW.Fin_Dly_Balances.Bal_Type , 
#     VISIONRW.Fin_Dly_Headers.Currency
#     """
# 	overd = pd.read_sql(query, con=get_connection())
# 	overd.set_index(['YEAR_MONTH','CURRENCY','FRL_ATTRIBUTE_05','FRL_ATT_05_DESCRIPTION','FRL_ATT_01_DESCRIPTION',
#                      'CUSTOMER_ID','OUC_DESCRIPTION','VISION_SBU','RECORD_TYPE','BAL_TYPE'],inplace=True)# Set yearmonth and currency as index
# 	over = overd.stack()#To transpose a dataframe
# 	over=pd.DataFrame(over)
# 	loan_depos=over.reset_index() # To reset index
# 	loan_depos=loan_depos.rename(columns={0: 'BALANCE','level_10':'DAY'})# to rename columns
# 	d = {'BALANCE_01':1, 'BALANCE_02':2, 'BALANCE_03':3, 'BALANCE_04':4,'BALANCE_05':5, 'BALANCE_06':6,
#      'BALANCE_07':7, 'BALANCE_08':8,'BALANCE_09':9, 'BALANCE_10':10, 'BALANCE_11':11, 'BALANCE_12':12,
#      'BALANCE_13':13, 'BALANCE_14':14, 'BALANCE_15':15, 'BALANCE_16':16,'BALANCE_17':17, 'BALANCE_18':18,
#      'BALANCE_19':19, 'BALANCE_20':20,'BALANCE_21':21, 'BALANCE_22':22, 'BALANCE_23':23, 'BALANCE_24':24,
#      'BALANCE_25':25,'BALANCE_26':26, 'BALANCE_27':27, 'BALANCE_28':28, 'BALANCE_29':29,'BALANCE_30':30, 'BALANCE_31':31 }# change rate to corresponding day
# 	loan_depos['DAY_'] = loan_depos.DAY.map(d) # map day
# 	loan_depos['BALANCE_YEAR'] = loan_depos.YEAR_MONTH.astype(str).str[:4].astype(int)# To change year month in years
# 	loan_depos['BALANCE_MONTH'] = loan_depos.YEAR_MONTH.astype(str).str[4:].astype(int)# To change year month in months
# # conditions for february and other months which have only 30 days
# # 	loan_depos['DROP_FEB'] = np.where(((loan_depos.BALANCE_YEAR%4 != 0) & (loan_depos.DAY_ > 28)),'Y',(np.where(((loan_depos.BALANCE_YEAR%4 == 0) & (loan_depos.DAY_ > 29)),'Y','N')) )
# # ye['DROP_FEB'] = np.where(((ye.YEAR_MONTH == 201902) & (ye.DAY_ > 28)),'Y',(np.where(((ye.YEAR_MONTH == 202002) & (ye.DAY_ > 29)),'Y','N')) )
# 	loan_depos['DROP_MONTHS'] = np.where(((loan_depos.BALANCE_MONTH.isin([4,6,9,11]))&(loan_depos.DAY_>30)),'Y','N')
# # 	loan_depos = loan_depos[loan_depos.DROP_FEB != 'Y']
# 	loan_depos = loan_depos[loan_depos.DROP_MONTHS != 'Y']  
# 	loan_depos['VALUE_DATE'] = loan_depos.apply(lambda row: datetime.strptime(f"{(row.BALANCE_YEAR)}-{(row.BALANCE_MONTH)}-{(row.DAY_)}", '%Y-%m-%d'), axis=1)
# 	loan_depos = loan_depos[['CUSTOMER_ID','YEAR_MONTH','VALUE_DATE','CURRENCY','BALANCE','FRL_ATTRIBUTE_05',
#                              'FRL_ATT_05_DESCRIPTION','FRL_ATT_01_DESCRIPTION','OUC_DESCRIPTION','VISION_SBU']]
# 	loan_depos_csv = loan_depos.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\loan_depos.csv',index=None,header=True)
	loan_depos= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\loan_depos.csv')    
	if cust_type=="ALL":
		pass
	else:
		loan_depos= loan_depos[loan_depos.VISION_SBU==cust_type]
	return loan_depos

@cache1.memoize(timeout=TIMEOUT)
def get_pl(session_id, cust_type="ALL"):    
#     query="""
#     with dates as (
#     --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
#     select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
#     TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
#     ),

#     day_balance as (
#     select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#         from VISIONRW.Fin_Dly_Balances 
#         unpivot ( 
#             balance for column_
#             in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#             ) balance_unpivot 

#            where year_month=(select year_month from dates fetch next 1 row only) 
#     ),

#     default_pl as (SELECT
#         fin_dly_headers.year_month             AS year_month,
#         frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 4
#                 AND frl_lines_pl.frl_attribute_04 = frl_attribute
#         ) ) AS frl_att_04_description,
#         frl_lines_pl.frl_attribute_02          AS frl_attribute_02,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 2
#                 AND frl_lines_pl.frl_attribute_02 = frl_attribute
#         ) ) AS frl_att_02_description,
#         frl_lines_pl.frl_attribute_06          AS frl_attribute_06,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 6
#                 AND frl_lines_pl.frl_attribute_06 = frl_attribute
#         ) ) AS frl_att_06_description,
#         frl_lines_bs.frl_attribute_01          AS frl_attribute_01,
#         ( (
#             SELECT
#                 frl_attribute_description
#            FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 1
#                 AND frl_lines_bs.frl_attribute_01 = frl_attribute
#         ) ) AS frl_att_01_description,
#         product_expanded.product_description   AS product_description,
#         frl_lines_bs.source_type               AS source_type,
#         fin_dly_headers.office_account         AS office_account,
#         ouc_expanded.ouc_description           AS ouc_description,
#         fin_dly_headers.customer_id            AS customer_id,
#         fin_dly_headers.contract_id            AS contract_id,
#         customers_dly_expanded.customer_name   AS customer_name,
#         fin_dly_headers.bs_gl                  AS bs_gl,
#         fin_dly_headers.pl_gl                  AS pl_gl,
#         fin_dly_headers.vision_ouc             AS vision_ouc,
#         fin_dly_headers.vision_sbu             AS vision_sbu,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 3
#                 AND alpha_sub_tab = fin_dly_headers.vision_sbu
#         ) AS vision_sbu_desc,
#         fin_dly_headers.currency               AS currency,
#             accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#             accounts_dly.scheme_code               AS scheme_code,
#         (
#             SELECT
#                alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 171
#                 AND alpha_sub_tab = accounts_dly.scheme_code
#         ) AS scheme_code_desc,
#         accounts_dly.sector_code               AS sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 59
#                 AND alpha_sub_tab = accounts_dly.sector_code
#         ) AS sector_code_desc,
#         accounts_dly.sub_sector_code           AS sub_sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 60
#                 AND alpha_sub_tab = accounts_dly.sub_sector_code
#         ) AS sub_sector_code_desc,
#         fin_dly_headers.record_type            AS record_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 22
#                 AND num_sub_tab = fin_dly_headers.record_type
#         ) AS record_type_desc,
#         fin_dly_balances.bal_type              AS bal_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 24
#                 AND num_sub_tab = fin_dly_balances.bal_type
#         ) AS bal_type_desc,
#         to_number(SUM(fin_dly_balances.balance)) AS balance

#     FROM
#         visionrw.fin_dly_headers             fin_dly_headers
#         JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                                   AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                                   AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                                   AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                                   AND fin_dly_headers.record_type != 9999
#             LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                     AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                     AND (
#             CASE
#                 WHEN fin_dly_headers.contract_id = '0' THEN
#                     fin_dly_headers.office_account
#                 ELSE
#                     fin_dly_headers.contract_id
#             END
#         ) = accounts_dly.account_no
#                                                     AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.ouc_expanded                ouc_expanded ON ouc_expanded.vision_ouc = fin_dly_headers.vision_ouc
#                                                AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                       AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                       AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                       AND fin_dly_headers.record_type != 9999
#         JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                                   AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                                   AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                                   AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                                   AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#         JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#         JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#         JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
#     WHERE
#         fin_dly_headers.year_month=(select year_month from dates fetch next 1 row only) 
#         AND frl_lines_bs.source_type = '0'
#         AND fin_dly_headers.record_type NOT IN (
#             '9999'
#         )
#         AND fin_dly_balances.bal_type = '54'
#     GROUP BY
#         fin_dly_headers.year_month,
#         frl_lines_pl.frl_attribute_04,
#         frl_lines_pl.frl_attribute_02,
#         frl_lines_pl.frl_attribute_06,
#         frl_lines_bs.frl_attribute_01,
#         product_expanded.product_description,
#         frl_lines_bs.source_type,
#         fin_dly_headers.office_account,
#         ouc_expanded.ouc_description,
#         fin_dly_headers.customer_id,
#         fin_dly_headers.contract_id,
#         customers_dly_expanded.customer_name,
#         fin_dly_headers.bs_gl,
#         fin_dly_headers.pl_gl,
#         fin_dly_headers.vision_ouc,
#         fin_dly_headers.vision_sbu,
#         fin_dly_headers.currency,
#         accounts_dly.ACCOUNT_TYPE,
#         accounts_dly.scheme_code,
#         accounts_dly.sector_code,
#         accounts_dly.sub_sector_code,
#         fin_dly_headers.record_type,
#         fin_dly_balances.bal_type)
#         select * from default_pl
#     """
#     PL = pd.read_sql(query, con=get_connection())
#     PL_csv = PL.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\Profitability.csv',index=None,header=True)
    PL = pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\Profitability.csv')
#     PL_pure=PL_.set_index('FRL_ATTRIBUTE_02')
#     PL=PL_pure.drop(index=['FA021610','FA026025','FA021620','FA026110','FA021510','FA021430','FA022270','FA022230','FA026010','FA022260',
#     'FA022290','FA021410','FA024033','FA022320'])    
    if cust_type=="ALL":
        pass
    else:
        PL= PL[PL.VISION_SBU==cust_type]    
    Income=PL[PL.FRL_ATTRIBUTE_04=='FA040100'].BALANCE.sum()
    Expenses=PL[PL.FRL_ATTRIBUTE_04=='FA040200'].BALANCE.sum()
    FC=PL[PL.FRL_ATTRIBUTE_04=='FA040300'].BALANCE.sum()
    
    Loan=PL[PL.ACCOUNT_TYPE=='LAA']
    Overdraft=PL[PL.ACCOUNT_TYPE=='ODA']
    Current=PL[PL.ACCOUNT_TYPE=='CAA']
    Saving=PL[PL.ACCOUNT_TYPE=='SBA']
    Term_Dep=PL[PL.ACCOUNT_TYPE=='TDA']
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Eclair"),"New Eclair", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Investment"),"Investment loans", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Mortgage "),"Mortgage loans", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Personal"),"Personal loans", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Stock"),"Stock loans", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Con"),"Construction Loans", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Vehicle"),"Vehicle loans", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Advance"),"Advance on contract", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Equipment"),"Equipment loans", Loan.PRODUCT_DESCRIPTION) 
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Restructured"),"Restructured loans", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Invoice"),"Invoice/Receivables/Discounting", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Insurance"),"Insurance Premium Financing", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Second"),"Second Housing loans ", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Plot"),"Plot Acquisition loans ", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Home"),"Home Equity", Loan.PRODUCT_DESCRIPTION)
    Loan["PRODUCT_DESCRIPTION"]= np.where(Loan.PRODUCT_DESCRIPTION.str.contains("Working"),"Working Capital Finance", Loan.PRODUCT_DESCRIPTION)    
#######################################################Income#######################################################    
    Loan_product= Loan[Loan.FRL_ATTRIBUTE_04=='FA040100'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no expenses on loans
    Overdraft_product= Overdraft[Overdraft.FRL_ATTRIBUTE_04=='FA040100'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    Saving_product=Saving[Saving.FRL_ATTRIBUTE_04=='FA040100'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no income from saving accounts
    Term_Dep_product=Term_Dep[Term_Dep.FRL_ATTRIBUTE_04=='FA040100'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no income from term deposits accounts
    Current_product=Current[Current.FRL_ATTRIBUTE_04=='FA040100'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
#############################################################Expenses####################################################    
    Loan_product_ex= Loan[Loan.FRL_ATTRIBUTE_04=='FA040200'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no expenses on loans
    Overdraft_product_ex= Overdraft[Overdraft.FRL_ATTRIBUTE_04=='FA040200'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    Saving_product_ex=Saving[Saving.FRL_ATTRIBUTE_04=='FA040200'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    Term_Dep_product_ex=Term_Dep[Term_Dep.FRL_ATTRIBUTE_04=='FA040200'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    Current_product_ex=Current[Current.FRL_ATTRIBUTE_04=='FA040200'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
###############################################################Fees#######################################################
    Loan_product_fee= Loan[Loan.FRL_ATTRIBUTE_04=='FA040300'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no expenses on loans
    Overdraft_product_fee= Overdraft[Overdraft.FRL_ATTRIBUTE_04=='FA040300'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    Saving_product_fee=Saving[Saving.FRL_ATTRIBUTE_04=='FA040300'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    Term_Dep_product_fee=Term_Dep[Term_Dep.FRL_ATTRIBUTE_04=='FA040300'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no fees&commissions
    Current_product_fee=Current[Current.FRL_ATTRIBUTE_04=='FA040300'].groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    
    return (Income,Expenses,FC,Loan_product,Overdraft_product,Saving_product,Term_Dep_product,Current_product,Loan_product_ex,Overdraft_product_ex,Saving_product_ex,Term_Dep_product_ex,Current_product_ex,Loan_product_fee,Overdraft_product_fee,Saving_product_fee,Term_Dep_product_fee,Current_product_fee) 

# @cache1.memoize(timeout=TIMEOUT)
# def get_profit_trend(session_id, cust_type="ALL"):    
#     query="""
#     with dates as (
#     --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
#     select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
#     TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
#     ),

#     day_balance as (
#     select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#         from VISIONRW.Fin_Dly_Balances 
#         unpivot ( 
#             balance for column_
#             in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#             ) balance_unpivot 

#            where year_month between '201912' and  (select year_month from dates fetch next 1 row only) 
#     ),

#     default_pl as (SELECT
#         fin_dly_headers.year_month             AS year_month,
#         frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 4
#                 AND frl_lines_pl.frl_attribute_04 = frl_attribute
#         ) ) AS frl_att_04_description,
#         frl_lines_pl.frl_attribute_02          AS frl_attribute_02,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 2
#                 AND frl_lines_pl.frl_attribute_02 = frl_attribute
#         ) ) AS frl_att_02_description,
#         frl_lines_pl.frl_attribute_06          AS frl_attribute_06,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 6
#                 AND frl_lines_pl.frl_attribute_06 = frl_attribute
#         ) ) AS frl_att_06_description,
#         frl_lines_bs.frl_attribute_01          AS frl_attribute_01,
#         ( (
#             SELECT
#                 frl_attribute_description
#            FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 1
#                 AND frl_lines_bs.frl_attribute_01 = frl_attribute
#         ) ) AS frl_att_01_description,
#         product_expanded.product_description   AS product_description,
#         frl_lines_bs.source_type               AS source_type,
#         fin_dly_headers.office_account         AS office_account,
#         ouc_expanded.ouc_description           AS ouc_description,
#         fin_dly_headers.customer_id            AS customer_id,
#         fin_dly_headers.contract_id            AS contract_id,
#         customers_dly_expanded.customer_name   AS customer_name,
#         fin_dly_headers.bs_gl                  AS bs_gl,
#         fin_dly_headers.pl_gl                  AS pl_gl,
#         fin_dly_headers.vision_ouc             AS vision_ouc,
#         fin_dly_headers.vision_sbu             AS vision_sbu,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 3
#                 AND alpha_sub_tab = fin_dly_headers.vision_sbu
#         ) AS vision_sbu_desc,
#         fin_dly_headers.currency               AS currency,
#             accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#             accounts_dly.scheme_code               AS scheme_code,
#         (
#             SELECT
#                alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 171
#                 AND alpha_sub_tab = accounts_dly.scheme_code
#         ) AS scheme_code_desc,
#         accounts_dly.sector_code               AS sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 59
#                 AND alpha_sub_tab = accounts_dly.sector_code
#         ) AS sector_code_desc,
#         accounts_dly.sub_sector_code           AS sub_sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 60
#                 AND alpha_sub_tab = accounts_dly.sub_sector_code
#         ) AS sub_sector_code_desc,
#         fin_dly_headers.record_type            AS record_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 22
#                 AND num_sub_tab = fin_dly_headers.record_type
#         ) AS record_type_desc,
#         fin_dly_balances.bal_type              AS bal_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 24
#                 AND num_sub_tab = fin_dly_balances.bal_type
#         ) AS bal_type_desc,
#         to_number(SUM(fin_dly_balances.balance)) AS balance 

#     FROM
#         visionrw.fin_dly_headers             fin_dly_headers
#         JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                                   AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                                   AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                                   AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                                   AND fin_dly_headers.record_type != 9999
#             LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                     AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                     AND (
#             CASE
#                 WHEN fin_dly_headers.contract_id = '0' THEN
#                     fin_dly_headers.office_account
#                 ELSE
#                     fin_dly_headers.contract_id
#             END
#         ) = accounts_dly.account_no
#                                                     AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.ouc_expanded                ouc_expanded ON ouc_expanded.vision_ouc = fin_dly_headers.vision_ouc
#                                                AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                       AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                       AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                       AND fin_dly_headers.record_type != 9999
#         JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                                   AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                                   AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                                   AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                                   AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#         JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#         JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#         JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
#     WHERE
#         fin_dly_headers.year_month between '201912' and  (select year_month from dates fetch next 1 row only)
#         AND frl_lines_bs.source_type = '0'
#         AND fin_dly_headers.record_type NOT IN (
#             '9999'
#         )
#         AND fin_dly_balances.bal_type = '54'
#     GROUP BY
#         fin_dly_headers.year_month,
#         frl_lines_pl.frl_attribute_04,
#         frl_lines_pl.frl_attribute_02,
#         frl_lines_pl.frl_attribute_06,
#         frl_lines_bs.frl_attribute_01,
#         product_expanded.product_description,
#         frl_lines_bs.source_type,
#         fin_dly_headers.office_account,
#         ouc_expanded.ouc_description,
#         fin_dly_headers.customer_id,
#         fin_dly_headers.contract_id,
#         customers_dly_expanded.customer_name,
#         fin_dly_headers.bs_gl,
#         fin_dly_headers.pl_gl,
#         fin_dly_headers.vision_ouc,
#         fin_dly_headers.vision_sbu,
#         fin_dly_headers.currency,
#         accounts_dly.ACCOUNT_TYPE,
#         accounts_dly.scheme_code,
#         accounts_dly.sector_code,
#         accounts_dly.sub_sector_code,
#         fin_dly_headers.record_type,
#         fin_dly_balances.bal_type)
#         select year_month,balance,vision_sbu from default_pl
#     """
#     profit = pd.read_sql(query, con=get_connection())
    
#     profit['YEAR'] = profit.YEAR_MONTH.astype(str).str[:4].astype(int)# To change year month in years
#     profit['MONTH'] = profit.YEAR_MONTH.astype(str).str[4:].astype(int)# To change year month in months
#     profit['DATE'] = profit.apply(lambda row: datetime.strptime(f"{(row.YEAR)}-{(row.MONTH)}", '%Y-%m'), axis=1)
    
#     if cust_type=="ALL":
#         pass
#     else:
#         profit= profit[profit.VISION_SBU==cust_type]

#     profit_overtime=profit.groupby('DATE').BALANCE.sum()
   
#     return profit_overtime

@cache1.memoize(timeout=TIMEOUT)
def get_income_trend(session_id, cust_type="ALL"):
#     query="""
#         with dates as (
#     --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
#     select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
#     TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
#     ),

#     day_balance as (
#     select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#         from VISIONRW.Fin_Dly_Balances 
#         unpivot ( 
#             balance for column_
#             in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#             ) balance_unpivot 

#            where year_month between '201912' and  (select year_month from dates fetch next 1 row only) 
#     ),

#     default_pl as (SELECT
#         fin_dly_headers.year_month             AS year_month,
#         frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 4
#                 AND frl_lines_pl.frl_attribute_04 = frl_attribute
#         ) ) AS frl_att_04_description,
#         frl_lines_pl.frl_attribute_02          AS frl_attribute_02,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 2
#                 AND frl_lines_pl.frl_attribute_02 = frl_attribute
#         ) ) AS frl_att_02_description,
#         frl_lines_pl.frl_attribute_06          AS frl_attribute_06,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 6
#                 AND frl_lines_pl.frl_attribute_06 = frl_attribute
#         ) ) AS frl_att_06_description,
#         frl_lines_bs.frl_attribute_01          AS frl_attribute_01,
#         ( (
#             SELECT
#                 frl_attribute_description
#            FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 1
#                 AND frl_lines_bs.frl_attribute_01 = frl_attribute
#         ) ) AS frl_att_01_description,
#         product_expanded.product_description   AS product_description,
#         frl_lines_bs.source_type               AS source_type,
#         fin_dly_headers.office_account         AS office_account,
#         ouc_expanded.ouc_description           AS ouc_description,
#         fin_dly_headers.customer_id            AS customer_id,
#         fin_dly_headers.contract_id            AS contract_id,
#         customers_dly_expanded.customer_name   AS customer_name,
#         fin_dly_headers.bs_gl                  AS bs_gl,
#         fin_dly_headers.pl_gl                  AS pl_gl,
#         fin_dly_headers.vision_ouc             AS vision_ouc,
#         fin_dly_headers.vision_sbu             AS vision_sbu,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 3
#                 AND alpha_sub_tab = fin_dly_headers.vision_sbu
#         ) AS vision_sbu_desc,
#         fin_dly_headers.currency               AS currency,
#             accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#             accounts_dly.scheme_code               AS scheme_code,
#         (
#             SELECT
#                alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 171
#                 AND alpha_sub_tab = accounts_dly.scheme_code
#         ) AS scheme_code_desc,
#         accounts_dly.sector_code               AS sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 59
#                 AND alpha_sub_tab = accounts_dly.sector_code
#         ) AS sector_code_desc,
#         accounts_dly.sub_sector_code           AS sub_sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 60
#                 AND alpha_sub_tab = accounts_dly.sub_sector_code
#         ) AS sub_sector_code_desc,
#         fin_dly_headers.record_type            AS record_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 22
#                 AND num_sub_tab = fin_dly_headers.record_type
#         ) AS record_type_desc,
#         fin_dly_balances.bal_type              AS bal_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 24
#                 AND num_sub_tab = fin_dly_balances.bal_type
#         ) AS bal_type_desc,
#         to_number(SUM(fin_dly_balances.balance)) AS balance 

#     FROM
#         visionrw.fin_dly_headers             fin_dly_headers
#         JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                                   AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                                   AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                                   AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                                   AND fin_dly_headers.record_type != 9999
#             LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                     AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                     AND (
#             CASE
#                 WHEN fin_dly_headers.contract_id = '0' THEN
#                     fin_dly_headers.office_account
#                 ELSE
#                     fin_dly_headers.contract_id
#             END
#         ) = accounts_dly.account_no
#                                                     AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.ouc_expanded                ouc_expanded ON ouc_expanded.vision_ouc = fin_dly_headers.vision_ouc
#                                                AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                       AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                       AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                       AND fin_dly_headers.record_type != 9999
#         JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                                   AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                                   AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                                   AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                                   AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#         JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#         JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#         JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
#     WHERE
#         fin_dly_headers.year_month between '201912' and  (select year_month from dates fetch next 1 row only)
#         AND frl_lines_bs.source_type = '0'
#         AND fin_dly_headers.record_type NOT IN (
#             '9999'
#         )
#         AND fin_dly_balances.bal_type = '54'
#         and frl_lines_pl.frl_attribute_04='FA040100'
#     GROUP BY
#         fin_dly_headers.year_month,
#         frl_lines_pl.frl_attribute_04,
#         frl_lines_pl.frl_attribute_02,
#         frl_lines_pl.frl_attribute_06,
#         frl_lines_bs.frl_attribute_01,
#         product_expanded.product_description,
#         frl_lines_bs.source_type,
#         fin_dly_headers.office_account,
#         ouc_expanded.ouc_description,
#         fin_dly_headers.customer_id,
#         fin_dly_headers.contract_id,
#         customers_dly_expanded.customer_name,
#         fin_dly_headers.bs_gl,
#         fin_dly_headers.pl_gl,
#         fin_dly_headers.vision_ouc,
#         fin_dly_headers.vision_sbu,
#         fin_dly_headers.currency,
#         accounts_dly.ACCOUNT_TYPE,
#         accounts_dly.scheme_code,
#         accounts_dly.sector_code,
#         accounts_dly.sub_sector_code,
#         fin_dly_headers.record_type,
#         fin_dly_balances.bal_type)
#         select * from default_pl
#     """
#     query="""
# with dates as (
# --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
# select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
# TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
# ),

# day_balance as (
# select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#     from VISIONRW.Fin_Dly_Balances 
#     unpivot ( 
#         balance for column_
#         in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#         ) balance_unpivot 

#        where year_month between '201912' and  (select year_month from dates fetch next 1 row only) 
# ),

# default_pl as (SELECT
#     fin_dly_headers.year_month             AS year_month,
#     frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#     ( (
#         SELECT
#             frl_attribute_description
#         FROM
#             visionrw.frl_attributes
#         WHERE
#             frl_attribute_level = 4
#             AND frl_lines_pl.frl_attribute_04 = frl_attribute
#     ) ) AS frl_att_04_description,

#     product_expanded.product_description   AS product_description,
#     frl_lines_bs.source_type               AS source_type,
#     fin_dly_headers.customer_id            AS customer_id,
#     fin_dly_headers.vision_sbu             AS vision_sbu,

#     fin_dly_headers.currency               AS currency,
#         accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#         accounts_dly.scheme_code               AS scheme_code,
   
#     fin_dly_headers.record_type            AS record_type,
#     (
#         SELECT
#             num_subtab_description
#         FROM
#             visionrw.num_sub_tab
#         WHERE
#             num_tab = 22
#             AND num_sub_tab = fin_dly_headers.record_type
#     ) AS record_type_desc,
#     fin_dly_balances.bal_type              AS bal_type,
#     to_number(SUM(fin_dly_balances.balance)) AS balance 

# FROM
#     visionrw.fin_dly_headers             fin_dly_headers
#     JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                               AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                               AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                               AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                               AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                 AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                 AND fin_dly_headers.record_type != 9999

#     LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                   AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                   AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                   AND fin_dly_headers.record_type != 9999
#     JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                               AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                               AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                               AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                               AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#     JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#     JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#     JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
# WHERE
#     fin_dly_headers.year_month between '201912' and  (select year_month from dates fetch next 1 row only)
#     AND frl_lines_bs.source_type = '0'
#     AND fin_dly_headers.record_type NOT IN (
#         '9999'
#     )
#     AND fin_dly_balances.bal_type = '54'
#     and frl_lines_pl.frl_attribute_04='FA040100'
# GROUP BY
#     fin_dly_headers.year_month,
#     frl_lines_pl.frl_attribute_04,
#     product_expanded.product_description,
#     frl_lines_bs.source_type,
#     fin_dly_headers.customer_id,
#     fin_dly_headers.vision_sbu,
#     fin_dly_headers.currency,
#     accounts_dly.ACCOUNT_TYPE,
#     accounts_dly.scheme_code,
#     fin_dly_headers.record_type,
#     fin_dly_balances.bal_type)
#     select * from default_pl
#     """
#     income = pd.read_sql(query, con=get_connection())
#     income_csv = income.to_csv(r'C:\Users\clement nshimiyima\Desktop\imdas_new\Data_im\income.csv',index=None,header=True)
    income=pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\income.csv')
    income['DATE']=pd.to_datetime(income['YEAR_MONTH'].astype(str), format='%Y%m')
    income['DATE']=income['DATE'].dt.to_period('m')  
    income['DATE']=income['DATE'].astype(str) 
#     income_pure=income_.set_index('FRL_ATTRIBUTE_02')
#     income=income_pure.drop(index=['FA021610','FA026025','FA021620','FA026110','FA021510','FA021430','FA022270','FA022230','FA026010','FA022260',
#     'FA022290','FA021410','FA024033','FA022320'])    
    if cust_type=="ALL":
        pass
    else:
        income= income[income.VISION_SBU==cust_type]
        
#     Loan=income[income.ACCOUNT_TYPE=='LAA']
#     Overdraft=income[income.ACCOUNT_TYPE=='ODA']
#     Current=income[income.ACCOUNT_TYPE=='CAA']
#     Saving=income[income.ACCOUNT_TYPE=='SBA']
#     Term_Dep=income[income.ACCOUNT_TYPE=='TDA'] 
#     credit_card=income[(income.ACCOUNT_TYPE=='CAA')&(income.SCHEME_CODE=='CAL05')] 
    income_overtime=income.groupby('DATE').BALANCE.sum()
#     income_balance=income[income.YEAR_MONTH==202003].BALANCE.sum()
    income_trend=income[income.DATE>='2020-03'].groupby('DATE_LAST_MODIFIED').BALANCE.sum()    
############################Group by product############################# 
#     Loan_product= Loan.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no expenses on loans
#     Overdraft_product= Overdraft.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
#     Saving_product=Saving.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no income from saving accounts
#     Term_Dep_product=Term_Dep.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no income from term deposits accounts
#     Current_product=Current.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    
    return income_overtime,income_trend       
    
@cache1.memoize(timeout=TIMEOUT)
def get_expense_trend(session_id, cust_type="ALL"):
#     query="""
#     with dates as (
#     --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
#     select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
#     TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
#     ),

#     day_balance as (
#     select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#         from VISIONRW.Fin_Dly_Balances 
#         unpivot ( 
#             balance for column_
#             in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#             ) balance_unpivot 

#            where year_month between '201912' and  (select year_month from dates fetch next 1 row only) 
#     ),

#     default_pl as (SELECT
    
#         fin_dly_headers.year_month             AS year_month,
#         frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 4
#                 AND frl_lines_pl.frl_attribute_04 = frl_attribute
#         ) ) AS frl_att_04_description,
#         frl_lines_pl.frl_attribute_02          AS frl_attribute_02,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 2
#                 AND frl_lines_pl.frl_attribute_02 = frl_attribute
#         ) ) AS frl_att_02_description,
#         frl_lines_pl.frl_attribute_06          AS frl_attribute_06,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 6
#                 AND frl_lines_pl.frl_attribute_06 = frl_attribute
#         ) ) AS frl_att_06_description,
#         frl_lines_bs.frl_attribute_01          AS frl_attribute_01,
#         ( (
#             SELECT
#                 frl_attribute_description
#            FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 1
#                 AND frl_lines_bs.frl_attribute_01 = frl_attribute
#         ) ) AS frl_att_01_description,
#         product_expanded.product_description   AS product_description,
#         frl_lines_bs.source_type               AS source_type,
#         fin_dly_headers.office_account         AS office_account,
#         ouc_expanded.ouc_description           AS ouc_description,
#         fin_dly_headers.customer_id            AS customer_id,
#         fin_dly_headers.contract_id            AS contract_id,
#         customers_dly_expanded.customer_name   AS customer_name,
#         fin_dly_headers.bs_gl                  AS bs_gl,
#         fin_dly_headers.pl_gl                  AS pl_gl,
#         fin_dly_headers.vision_ouc             AS vision_ouc,
#         fin_dly_headers.vision_sbu             AS vision_sbu,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 3
#                 AND alpha_sub_tab = fin_dly_headers.vision_sbu
#         ) AS vision_sbu_desc,
#         fin_dly_headers.currency               AS currency,
#             accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#             accounts_dly.scheme_code               AS scheme_code,
#         (
#             SELECT
#                alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 171
#                 AND alpha_sub_tab = accounts_dly.scheme_code
#         ) AS scheme_code_desc,
#         accounts_dly.sector_code               AS sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 59
#                 AND alpha_sub_tab = accounts_dly.sector_code
#         ) AS sector_code_desc,
#         accounts_dly.sub_sector_code           AS sub_sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 60
#                 AND alpha_sub_tab = accounts_dly.sub_sector_code
#         ) AS sub_sector_code_desc,
#         fin_dly_headers.record_type            AS record_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 22
#                 AND num_sub_tab = fin_dly_headers.record_type
#         ) AS record_type_desc,
#         fin_dly_balances.bal_type              AS bal_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 24
#                 AND num_sub_tab = fin_dly_balances.bal_type
#         ) AS bal_type_desc,
#         to_number(SUM(fin_dly_balances.balance)) AS balance 

#     FROM
#         visionrw.fin_dly_headers             fin_dly_headers
#         JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                                   AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                                   AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                                   AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                                   AND fin_dly_headers.record_type != 9999
#             LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                     AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                     AND (
#             CASE
#                 WHEN fin_dly_headers.contract_id = '0' THEN
#                     fin_dly_headers.office_account
#                 ELSE
#                     fin_dly_headers.contract_id
#             END
#         ) = accounts_dly.account_no
#                                                    AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.ouc_expanded                ouc_expanded ON ouc_expanded.vision_ouc = fin_dly_headers.vision_ouc
#                                                AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                       AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                       AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                       AND fin_dly_headers.record_type != 9999
#         JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                                   AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                                   AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                                   AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                                   AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#         JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#         JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#         JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
#     WHERE
#         fin_dly_headers.year_month between '201912' and  (select year_month from dates fetch next 1 row only)
#         AND frl_lines_bs.source_type = '0'
#         AND fin_dly_headers.record_type NOT IN (
#             '9999'
#         )
#         AND fin_dly_balances.bal_type = '54'
#         and frl_lines_pl.frl_attribute_04='FA040200'
#     GROUP BY
#         fin_dly_headers.year_month,
#         frl_lines_pl.frl_attribute_04,
#         frl_lines_pl.frl_attribute_02,
#         frl_lines_pl.frl_attribute_06,
#         frl_lines_bs.frl_attribute_01,
#         product_expanded.product_description,
#         frl_lines_bs.source_type,
#         fin_dly_headers.office_account,
#         ouc_expanded.ouc_description,
#         fin_dly_headers.customer_id,
#         fin_dly_headers.contract_id,
#         customers_dly_expanded.customer_name,
#         fin_dly_headers.bs_gl,
#         fin_dly_headers.pl_gl,
#         fin_dly_headers.vision_ouc,
#         fin_dly_headers.vision_sbu,
#         fin_dly_headers.currency,
#         accounts_dly.ACCOUNT_TYPE,
#         accounts_dly.scheme_code,
#         accounts_dly.sector_code,
#         accounts_dly.sub_sector_code,
#         fin_dly_headers.record_type,
#         fin_dly_balances.bal_type)
#         select * from default_pl
#     """    
#     query="""
# with dates as (
# --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
# select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
# TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
# ),

# day_balance as (
# select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#     from VISIONRW.Fin_Dly_Balances 
#     unpivot ( 
#         balance for column_
#         in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#         ) balance_unpivot 

#        where year_month between '201912' and  (select year_month from dates fetch next 1 row only) 
# ),

# default_pl as (SELECT
#     fin_dly_headers.year_month             AS year_month,
#     frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#     ( (
#         SELECT
#             frl_attribute_description
#         FROM
#             visionrw.frl_attributes
#         WHERE
#             frl_attribute_level = 4
#             AND frl_lines_pl.frl_attribute_04 = frl_attribute
#     ) ) AS frl_att_04_description,

#     product_expanded.product_description   AS product_description,
#     frl_lines_bs.source_type               AS source_type,
#     fin_dly_headers.customer_id            AS customer_id,
#     fin_dly_headers.vision_sbu             AS vision_sbu,

#     fin_dly_headers.currency               AS currency,
#         accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#         accounts_dly.scheme_code               AS scheme_code,
   
#     fin_dly_headers.record_type            AS record_type,
#     (
#         SELECT
#             num_subtab_description
#         FROM
#             visionrw.num_sub_tab
#         WHERE
#             num_tab = 22
#             AND num_sub_tab = fin_dly_headers.record_type
#     ) AS record_type_desc,
#     fin_dly_balances.bal_type              AS bal_type,
#     to_number(SUM(fin_dly_balances.balance)) AS balance 

# FROM
#     visionrw.fin_dly_headers             fin_dly_headers
#     JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                               AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                               AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                               AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                               AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                 AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                 AND fin_dly_headers.record_type != 9999

#     LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                   AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                   AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                   AND fin_dly_headers.record_type != 9999
#     JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                               AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                               AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                               AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                               AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#     JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#     JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#     JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
# WHERE
#     fin_dly_headers.year_month between '201912' and  (select year_month from dates fetch next 1 row only)
#     AND frl_lines_bs.source_type = '0'
#     AND fin_dly_headers.record_type NOT IN (
#         '9999'
#     )
#     AND fin_dly_balances.bal_type = '54'
#     and frl_lines_pl.frl_attribute_04='FA040200'
# GROUP BY
#     fin_dly_headers.year_month,
#     frl_lines_pl.frl_attribute_04,
#     product_expanded.product_description,
#     frl_lines_bs.source_type,
#     fin_dly_headers.customer_id,
#     fin_dly_headers.vision_sbu,
#     fin_dly_headers.currency,
#     accounts_dly.ACCOUNT_TYPE,
#     accounts_dly.scheme_code,
#     fin_dly_headers.record_type,
#     fin_dly_balances.bal_type)
#     select * from default_pl
#     """
#     expense = pd.read_sql(query, con=get_connection()) 
#     expense_csv = expense.to_csv(r'C:\Users\clement nshimiyima\Desktop\imdas_new\Data_im\expense.csv',index=None,header=True)
    expense=pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\expense.csv')
    expense['DATE']=pd.to_datetime(expense['YEAR_MONTH'].astype(str), format='%Y%m')
    expense['DATE']=expense['DATE'].dt.to_period('m')     
    expense['DATE']=expense['DATE'].astype(str)   
#     expense_pure=expense_.set_index('FRL_ATTRIBUTE_02')
#     expense=expense_pure.drop(index=['FA021610','FA026025','FA021620','FA026110','FA021510','FA021430','FA022270','FA022230','FA026010','FA022260',
#     'FA022290','FA021410','FA024033','FA022320'])
    if cust_type=="ALL":
        pass
    else:
        expense= expense[expense.VISION_SBU==cust_type]    
#     Loan_ex=expense[expense.ACCOUNT_TYPE=='LAA']
#     Overdraft_ex=expense[expense.ACCOUNT_TYPE=='ODA']
#     Current_ex=expense[expense.ACCOUNT_TYPE=='CAA']
#     Saving_ex=expense[expense.ACCOUNT_TYPE=='SBA']
#     Term_Dep_ex=expense[expense.ACCOUNT_TYPE=='TDA'] 
#     credit_card_ex=expense[(expense.ACCOUNT_TYPE=='CAA')&(expense.SCHEME_CODE=='CAL05')] 
    expense_overtime=expense.groupby('DATE').BALANCE.sum()
#     expense_balance=expense[expense.YEAR_MONTH==202003].BALANCE.sum()
# ############################Group by product############################# 
#     Loan_product_ex= Loan_ex.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no expenses on loans
#     Overdraft_product_ex= Overdraft_ex.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
#     Saving_product_ex=Saving_ex.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
#     Term_Dep_product_ex=Term_Dep_ex.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
#     Current_product_ex=Current_ex.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    
    return expense_overtime       
    
@cache1.memoize(timeout=TIMEOUT)
def get_fees_trend(session_id, cust_type="ALL"):
#     query="""
#     with dates as (
#     --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
#     select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
#     TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
#     ),

#     day_balance as (
#     select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#         from VISIONRW.Fin_Dly_Balances 
#         unpivot ( 
#             balance for column_
#             in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#             ) balance_unpivot 

#            where year_month between '201912' and  (select year_month from dates fetch next 1 row only) 
#     ),

#     default_pl as (SELECT
#         fin_dly_headers.year_month             AS year_month,
#         frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 4
#                 AND frl_lines_pl.frl_attribute_04 = frl_attribute
#         ) ) AS frl_att_04_description,
#         frl_lines_pl.frl_attribute_02          AS frl_attribute_02,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 2
#                 AND frl_lines_pl.frl_attribute_02 = frl_attribute
#         ) ) AS frl_att_02_description,
#         frl_lines_pl.frl_attribute_06          AS frl_attribute_06,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 6
#                 AND frl_lines_pl.frl_attribute_06 = frl_attribute
#         ) ) AS frl_att_06_description,
#         frl_lines_bs.frl_attribute_01          AS frl_attribute_01,
#         ( (
#             SELECT
#                 frl_attribute_description
#            FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 1
#                 AND frl_lines_bs.frl_attribute_01 = frl_attribute
#         ) ) AS frl_att_01_description,
#         product_expanded.product_description   AS product_description,
#         frl_lines_bs.source_type               AS source_type,
#         fin_dly_headers.office_account         AS office_account,
#         ouc_expanded.ouc_description           AS ouc_description,
#         fin_dly_headers.customer_id            AS customer_id,
#         fin_dly_headers.contract_id            AS contract_id,
#         customers_dly_expanded.customer_name   AS customer_name,
#         fin_dly_headers.bs_gl                  AS bs_gl,
#         fin_dly_headers.pl_gl                  AS pl_gl,
#         fin_dly_headers.vision_ouc             AS vision_ouc,
#         fin_dly_headers.vision_sbu             AS vision_sbu,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 3
#                 AND alpha_sub_tab = fin_dly_headers.vision_sbu
#         ) AS vision_sbu_desc,
#         fin_dly_headers.currency               AS currency,
#             accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#             accounts_dly.scheme_code               AS scheme_code,
#         (
#             SELECT
#                alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 171
#                 AND alpha_sub_tab = accounts_dly.scheme_code
#         ) AS scheme_code_desc,
#         accounts_dly.sector_code               AS sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 59
#                 AND alpha_sub_tab = accounts_dly.sector_code
#         ) AS sector_code_desc,
#         accounts_dly.sub_sector_code           AS sub_sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 60
#                 AND alpha_sub_tab = accounts_dly.sub_sector_code
#         ) AS sub_sector_code_desc,
#         fin_dly_headers.record_type            AS record_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 22
#                 AND num_sub_tab = fin_dly_headers.record_type
#         ) AS record_type_desc,
#         fin_dly_balances.bal_type              AS bal_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 24
#                 AND num_sub_tab = fin_dly_balances.bal_type
#         ) AS bal_type_desc,
#         to_number(SUM(fin_dly_balances.balance)) AS balance 

#     FROM
#         visionrw.fin_dly_headers             fin_dly_headers
#         JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                                   AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                                   AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                                   AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                                   AND fin_dly_headers.record_type != 9999
#             LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                     AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                     AND (
#             CASE
#                 WHEN fin_dly_headers.contract_id = '0' THEN
#                     fin_dly_headers.office_account
#                 ELSE
#                     fin_dly_headers.contract_id
#             END
#         ) = accounts_dly.account_no
#                                                     AND fin_dly_headers.record_type != 9999
                                                    
#         LEFT JOIN visionrw.ouc_expanded                ouc_expanded ON ouc_expanded.vision_ouc = fin_dly_headers.vision_ouc
#                                                AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                       AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                       AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                       AND fin_dly_headers.record_type != 9999
#         JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                                   AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                                   AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                                   AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                                   AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#         JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#         JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#         JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
#     WHERE
#         fin_dly_headers.year_month between '201912' and  (select year_month from dates fetch next 1 row only)
#         AND frl_lines_bs.source_type = '0'
#         AND fin_dly_headers.record_type NOT IN (
#             '9999'
#         )
#         AND fin_dly_balances.bal_type = '54'
#         and frl_lines_pl.frl_attribute_04='FA040300'
#     GROUP BY
#         fin_dly_headers.year_month,
#         frl_lines_pl.frl_attribute_04,
#         frl_lines_pl.frl_attribute_02,
#         frl_lines_pl.frl_attribute_06,
#         frl_lines_bs.frl_attribute_01,
#         product_expanded.product_description,
#         frl_lines_bs.source_type,
#         fin_dly_headers.office_account,
#         ouc_expanded.ouc_description,
#         fin_dly_headers.customer_id,
#         fin_dly_headers.contract_id,
#         customers_dly_expanded.customer_name,
#         fin_dly_headers.bs_gl,
#         fin_dly_headers.pl_gl,
#         fin_dly_headers.vision_ouc,
#         fin_dly_headers.vision_sbu,
#         fin_dly_headers.currency,
#         accounts_dly.ACCOUNT_TYPE,
#         accounts_dly.scheme_code,
#         accounts_dly.sector_code,
#         accounts_dly.sub_sector_code,
#         fin_dly_headers.record_type,
#         fin_dly_balances.bal_type)
#         select * from default_pl
#     """
#     query="""
# with dates as (
# --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
# select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
# TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
# ),

# day_balance as (
# select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#     from VISIONRW.Fin_Dly_Balances 
#     unpivot ( 
#         balance for column_
#         in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#         ) balance_unpivot 

#        where year_month between '201912' and  (select year_month from dates fetch next 1 row only) 
# ),

# default_pl as (SELECT
#     fin_dly_headers.year_month             AS year_month,
#     frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#     ( (
#         SELECT
#             frl_attribute_description
#         FROM
#             visionrw.frl_attributes
#         WHERE
#             frl_attribute_level = 4
#             AND frl_lines_pl.frl_attribute_04 = frl_attribute
#     ) ) AS frl_att_04_description,

#     product_expanded.product_description   AS product_description,
#     frl_lines_bs.source_type               AS source_type,
#     fin_dly_headers.customer_id            AS customer_id,
#     fin_dly_headers.vision_sbu             AS vision_sbu,

#     fin_dly_headers.currency               AS currency,
#         accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#         accounts_dly.scheme_code               AS scheme_code,
   
#     fin_dly_headers.record_type            AS record_type,
#     (
#         SELECT
#             num_subtab_description
#         FROM
#             visionrw.num_sub_tab
#         WHERE
#             num_tab = 22
#             AND num_sub_tab = fin_dly_headers.record_type
#     ) AS record_type_desc,
#     fin_dly_balances.bal_type              AS bal_type,
#     to_number(SUM(fin_dly_balances.balance)) AS balance 

# FROM
#     visionrw.fin_dly_headers             fin_dly_headers
#     JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                               AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                               AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                               AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                               AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                 AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                 AND fin_dly_headers.record_type != 9999

#     LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                   AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                   AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                   AND fin_dly_headers.record_type != 9999
#     JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                               AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                               AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                               AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                               AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#     JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#     JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#     JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
# WHERE
#     fin_dly_headers.year_month between '201912' and  (select year_month from dates fetch next 1 row only)
#     AND frl_lines_bs.source_type = '0'
#     AND fin_dly_headers.record_type NOT IN (
#         '9999'
#     )
#     AND fin_dly_balances.bal_type = '54'
#     and frl_lines_pl.frl_attribute_04='FA040300'
# GROUP BY
#     fin_dly_headers.year_month,
#     frl_lines_pl.frl_attribute_04,
#     product_expanded.product_description,
#     frl_lines_bs.source_type,
#     fin_dly_headers.customer_id,
#     fin_dly_headers.vision_sbu,
#     fin_dly_headers.currency,
#     accounts_dly.ACCOUNT_TYPE,
#     accounts_dly.scheme_code,
#     fin_dly_headers.record_type,
#     fin_dly_balances.bal_type)
#     select * from default_pl
#     """
#     fees = pd.read_sql(query, con=get_connection())
#     fees_csv = fees.to_csv(r'C:\Users\clement nshimiyima\Desktop\imdas_new\Data_im\fees.csv',index=None,header=True)
    fees=pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\fees.csv')
#     fees['YEAR'] = fees.YEAR_MONTH.astype(str).str[:4].astype(int)# To change year month in years
#     fees['MONTH'] = fees.YEAR_MONTH.astype(str).str[4:]# To change year month in months
#     fees['DATE'] = fees.apply(lambda row: datetime.strptime(f"{(row.YEAR)}-{(row.MONTH)}", '%Y-%m'), axis=1)
    fees['DATE']=pd.to_datetime(fees['YEAR_MONTH'].astype(str), format='%Y%m')
    fees['DATE']=fees['DATE'].dt.to_period('m')       
    fees['DATE']=fees['DATE'].astype(str)  
#     fees_pure=fees_.set_index('FRL_ATTRIBUTE_02')
#     fees=fees_pure.drop(index=['FA021610','FA026025','FA021620','FA026110','FA021510','FA021430','FA022270','FA022230','FA026010','FA022260',
#     'FA022290','FA021410','FA024033','FA022320'])    
    if cust_type=="ALL":
        pass
    else:
        fees= fees[fees.VISION_SBU==cust_type]     
    
#     Loan_fee=fees[fees.ACCOUNT_TYPE=='LAA']
#     Overdraft_fee=fees[fees.ACCOUNT_TYPE=='ODA']
#     Current_fee=fees[fees.ACCOUNT_TYPE=='CAA']
#     Saving_fee=fees[fees.ACCOUNT_TYPE=='SBA']
#     Term_Dep_fee=fees[fees.ACCOUNT_TYPE=='TDA'] 
#     credit_card=fees[(fees.ACCOUNT_TYPE=='CAA')&(fees.SCHEME_CODE=='CAL05')] 
    fees_overtime=fees.groupby('DATE').BALANCE.sum()
#     fees_balance=fees[fees.YEAR_MONTH==202003].BALANCE.sum()
# ############################Group by product############################# 
#     Loan_product_fee= Loan_fee.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no expenses on loans
#     Overdraft_product_fee= Overdraft_fee.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
#     Saving_product_fee=Saving_fee.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
#     Term_Dep_product_fee=Term_Dep_fee.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()# There is no fees&commissions
#     Current_product_fee=Current_fee.groupby('PRODUCT_DESCRIPTION').BALANCE.sum()
    fees_trend=fees[fees.DATE>='2020-03'].groupby('DATE_LAST_MODIFIED').BALANCE.sum()    
    return fees_overtime,fees_trend  
    
@cache1.memoize(timeout=TIMEOUT)
def get_customer_account_trend_data(session_id, cust_type="ALL", is_loan=False):

# 	customer_opening_query = None
# 	account_opening_query = None
# 	if is_loan:

# 		customer_opening_query = """
# 		SELECT DISTINCT(CUST.CUSTOMER_ID), CUSTOMER_OPEN_DATE, VISION_SBU	
# 		FROM VISIONRW.CUSTOMERS_DLY CUST
# 		INNER JOIN (
# 		    SELECT CUSTOMER_ID, ACCOUNT_TYPE, SCHEME_CODE, ACCOUNT_STATUS,ACCOUNT_OPEN_DATE
# 		    FROM VISIONRW.ACCOUNTS_DLY
# 		) ACC 
# 		ON CUST.CUSTOMER_ID = ACC.CUSTOMER_ID
# 		WHERE ACC.ACCOUNT_TYPE = 'LAA' AND ACCOUNT_STATUS=0 AND CUSTOMER_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd') 
# 			AND SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# 		"""
# 		account_opening_query = """
# 		SELECT ACCOUNT_NO, ACCOUNT_OPEN_DATE, SCHEME_CODE, VISION_SBU, ACCOUNT_STATUS
# 		FROM VISIONRW.ACCOUNTS_DLY  
# 		WHERE CUSTOMER_ID <> 'D000' AND ACCOUNT_TYPE = 'LAA' AND ACCOUNT_STATUS=0 AND SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
#         and ACCOUNT_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd') 
# 		"""
# 	else:
# 		customer_opening_query = """
#     SELECT VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID,VISIONRW.CUSTOMERS_DLY.CUSTOMER_OPEN_DATE AS CUSTOMER_OPEN_DATE,
#     VISIONRW.CUSTOMERS_DLY.VISION_SBU,VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE,VISIONRW.ACCOUNTS_DLY.SCHEME_CODE,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_OPEN_DATE AS ACCOUNT_OPEN_DATE,VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS,
#     COUNT(DISTINCT ACCOUNT_NO)AS NUM_OF_ACCOUNTS,
#     COUNT(CASE WHEN VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS=0 then 1 end) as ACTIVE,
#     COUNT(CASE WHEN VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS=1 then 1 end) as INACTIVE,
#     COUNT(CASE WHEN VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS=3 then 1 end) as DORMANT,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_NO
#     FROM VISIONRW.CUSTOMERS_DLY 
#     INNER JOIN VISIONRW.ACCOUNTS_DLY
#     ON VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID = VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID
#     WHERE VISIONRW.ACCOUNTS_DLY.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26','CAL05' )
#     AND VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS!=2
#     AND VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID <> 'D000'
#     AND VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE <>'LAA'
#     GROUP BY
#     VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID,
#     VISIONRW.CUSTOMERS_DLY.CUSTOMER_OPEN_DATE,
#     VISIONRW.CUSTOMERS_DLY.VISION_SBU,VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE,VISIONRW.ACCOUNTS_DLY.SCHEME_CODE,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_OPEN_DATE,VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_NO
# 		"""
# 		account_opening_query = """
        
# 		SELECT CUSTOMER_ID,ACCOUNT_NO, ACCOUNT_OPEN_DATE AS ACCOUNT_OPEN_DATE, SCHEME_CODE, VISION_SBU,
#         ACCOUNT_STATUS
# 		FROM VISIONRW.ACCOUNTS_DLY  
# 		WHERE CUSTOMER_ID <> 'D000'AND SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26','CAL05')
#         and ACCOUNT_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd')
#         AND ACCOUNT_TYPE <>'LAA'
#         AND ACCOUNT_STATUS!=2
        
# 		"""

# 	customer_opening = pd.read_sql(customer_opening_query, con=get_connection())
# 	account_opening = pd.read_sql(account_opening_query, con=get_connection())
# 	customer_csv = customer_opening.to_csv(r'C:\Users\clement nshimiyima\Downloads\imdas_new\Data_im\customer_opening.csv',header=True)
	customer_opening = pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\customer_opening.csv')    
# 	account_csv = account_opening.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\account_opening.csv',index=None,header=True)
	account_opening = pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\account_opening.csv')    
	## To get ALL, Retail, Corporate or SME Data
	if cust_type=="ALL":
		pass
	else:
		customer_opening= customer_opening[customer_opening.VISION_SBU==cust_type]
		account_opening= account_opening[account_opening.VISION_SBU==cust_type]
        
# 	account_opening.ACCOUNT_TYPE = np.where(account_opening.ACCOUNT_TYPE == "ODA", "CAA",account_opening.ACCOUNT_TYPE)
# 	customer_opening.ACCOUNT_TYPE = np.where(customer_opening.ACCOUNT_TYPE == "ODA", "CAA",customer_opening.ACCOUNT_TYPE)
# 	customer_opening["CUSTOMER_OPEN_DATE"]=customer_opening["CUSTOMER_OPEN_DATE"].dt.to_period('Q').dt.strftime('%YQ%q')
# 	account_Opening["ACCOUNT_OPEN_DATE"]=account_Opening["ACCOUNT_OPEN_DATE"].dt.to_period('Q').dt.strftime('%YQ%q')
# 	ind=pd.date_range('2000-01-01',period=20, freq ='W') 
# 	customer_opening=customer_opening(index=ind)   

	customer_open = customer_opening[customer_opening.CUSTOMER_OPEN_DATE>='2015-01-01'].groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()
	account_open = account_opening[account_opening.ACCOUNT_OPEN_DATE>='2015-01-01'].groupby("ACCOUNT_OPEN_DATE").ACCOUNT_NO.nunique()
# df.date = pd.to_datetime(df.date)    
# df['quarter'] = pd.PeriodIndex(df.date, freq='Q')
#     Mobile_APP['USER_INPUT_DATE']=Mobile_APP.USER_INPUT_DATE.dt.to_period('Q').dt.strftime('%YQ%q')    
#     Mobile_APP['USER_INPUT_DATE']=Mobile_APP.USER_INPUT_DATE.dt.quarter      
# 	customer_opening["CUSTOMER_OPEN_DATE"]=pd.PeriodIndex(customer_opening['CUSTOMER_OPEN_DATE'], freq='Q') 
# 	customer_opening["CUSTOMER_OPEN_DATE"]=pd.to_datetime(customer_opening.CUSTOMER_OPEN_DATE) 
# 	customer_opening["CUSTOMER_OPEN_DATE"]=pd.PeriodIndex(customer_opening.CUSTOMER_OPEN_DATE, freq='Q')
# 	account_opening["ACCOUNT_OPEN_DATE"]=pd.to_datetime(account_opening.ACCOUNT_OPEN_DATE) 
# 	account_opening["ACCOUNT_OPEN_DATE"]=pd.PeriodIndex(account_opening.ACCOUNT_OPEN_DATE, freq='Q') 
	customer_Opening = customer_opening.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()    
# 	account_opening["ACCOUNT_OPEN_DATE"]=pd.PeriodIndex(account_opening['ACCOUNT_OPEN_DATE'], freq='Q') 
# 	account_opening["ACCOUNT_OPEN_DATE"]=account_opening.ACCOUNT_OPEN_DATE.dt.to_period('Q')
	account_Opening = account_opening.groupby("ACCOUNT_OPEN_DATE").ACCOUNT_NO.nunique()
  
    
	active_cust =account_opening[account_opening.ACCOUNT_STATUS==0].CUSTOMER_ID.nunique()
	inactive_cust = account_opening[account_opening.ACCOUNT_STATUS==1].CUSTOMER_ID.nunique()
# 	closed_cust = customer_opening[customer_opening.NUM_OF_ACCOUNTS==customer_opening.CLOSED].CUSTOMER_ID.nunique()
	dormant_cust = account_opening[account_opening.ACCOUNT_STATUS==3].CUSTOMER_ID.nunique()    
	active = account_opening[account_opening.ACCOUNT_STATUS==0].ACCOUNT_NO.nunique()
	inactive = account_opening[account_opening.ACCOUNT_STATUS==1].ACCOUNT_NO.nunique()
# 	closed = account_opening[account_opening.ACCOUNT_STATUS==2].ACCOUNT_NO.nunique()
	dormant = account_opening[account_opening.ACCOUNT_STATUS==3].ACCOUNT_NO.nunique()
    
	return (customer_Opening,account_Opening,customer_open,account_open,active_cust,inactive_cust,active,inactive,dormant,active_cust,inactive_cust,dormant_cust)


##########################################################Deposits vs Loans##################################################
@cache1.memoize(timeout=TIMEOUT)
def get_deposit_loans(session_id, cust_type="ALL"):
# 	query="""
#     with dates as (
#     select LPAD(extract(day from to_date(sysdate-1)),2) as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM')
#     as year_month from dual 
#     ),
#     day_balance as (
#     select year_month,country,le_book,Sequence_FD,to_number(balance) as balance,dr_cr_bal_ind,bal_type
#         from VISIONRW.Fin_Dly_Balances 
#         unpivot ( 
#             balance for column_
#             in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#             ) balance_unpivot 
#        where year_month = (select year_month from dates fetch next 1 row only) and column_ = CONCAT('BALANCE_',(select day from dates fetch next 1 row only))

#     ),
#     day_rate as (
#     select year_month,country,le_book,currency,rate as rate
#         from VISIONRW.Currency_Rates_Daily
#         unpivot ( 
#             rate for column_
#             in (rate_01, rate_02, rate_03, rate_04, rate_05, rate_06, rate_07, rate_08, rate_09, rate_10, rate_11, rate_12, rate_13, rate_14, rate_15, rate_16, rate_17, rate_18, rate_19, rate_20, rate_21, rate_22, rate_23, rate_24, rate_25, rate_26, rate_27, rate_28, rate_29, rate_30, rate_31)
#             ) rate_unpivot 
#        where year_month = (select year_month from dates fetch next 1 row only) 
#        and column_ = CONCAT('RATE_',(select day from dates fetch next 1 row only)) 
#     ),

#     default_data as (
#     SELECT  Fin_Dly_Headers.Country AS Country,
#         Fin_Dly_Headers.LE_Book AS LE_Book ,
#         Fin_Dly_Headers.Year_Month AS Year_Month ,
#         FRL_Lines_BS.FRL_Attribute_05 AS FRL_Attribute_05 ,
#  ((select FRL_ATTRIBUTE_DESCRIPTION from  VISIONRW.FRL_ATTRIBUTES WHERE FRL_ATTRIBUTE_LEVEL =5 
# AND FRL_Lines_BS.FRL_ATTRIBUTE_05 = FRL_ATTRIBUTE))  AS FRL_Att_05_Description,
#         FRL_Lines_BS.FRL_Attribute_01 AS FRL_Attribute_01 ,
#  ((select FRL_ATTRIBUTE_DESCRIPTION from  VISIONRW.FRL_ATTRIBUTES WHERE FRL_ATTRIBUTE_LEVEL =1 
# AND FRL_Lines_BS.FRL_ATTRIBUTE_01 = FRL_ATTRIBUTE))  AS FRL_Att_01_Description, 
#         FRL_Lines_BS.FRL_Attribute_03 AS FRL_Attribute_03 , 
#         Customers_Dly_Expanded.Customer_Id AS Customer_Id ,
#         Fin_Dly_Headers.Vision_SBU AS Vision_SBU , 
#     Fin_Dly_Headers.Record_Type AS Record_Type , Fin_Dly_Balances.Bal_Type AS Bal_Type, 
#     Fin_Dly_Headers.Currency AS Currency ,TRIM(TO_CHAR(Currency_Rates_Daily.rate,'999,999,999,999,999,990.00000')) AS rate,
#     TRIM(TO_CHAR(SUM(Fin_Dly_Balances.balance) ,'999,999,999,999,999,990.00')) AS balance
#     FROM  VISIONRW.Fin_Dly_Headers  Fin_Dly_Headers
#      JOIN day_balance  Fin_Dly_Balances ON 
#         Fin_Dly_Headers.Country = Fin_Dly_Balances.Country AND 
#         Fin_Dly_Headers.Le_Book = Fin_Dly_Balances.Le_Book AND 
#         Fin_Dly_Headers.Year_Month = Fin_Dly_Balances.Year_Month AND 
#         Fin_Dly_Headers.Sequence_FD = Fin_Dly_Balances.Sequence_FD And 
#         Fin_Dly_Headers.RECORD_TYPE != 9999
#      JOIN day_rate  Currency_Rates_Daily ON 
#      Fin_Dly_Headers.Country = Currency_Rates_Daily.Country AND 
#      Fin_Dly_Headers.Le_Book = Currency_Rates_Daily.Le_Book AND
#      Fin_Dly_Headers.Year_Month = Currency_Rates_Daily.Year_Month 
#      AND Fin_Dly_Headers.currency = Currency_Rates_Daily.currency And Fin_Dly_Headers.RECORD_TYPE != 9999
#      LEFT JOIN VISIONRW.VW_Customers_Dly_Expanded  
#      Customers_Dly_Expanded ON Customers_Dly_Expanded.Country = Fin_Dly_Headers.Country 
#      AND Customers_Dly_Expanded.Le_Book = Fin_Dly_Headers.Le_Book 
#      AND Customers_Dly_Expanded.Customer_ID = Fin_Dly_Headers.Customer_ID And
#      Fin_Dly_Headers.RECORD_TYPE != 9999
#      JOIN VISIONRW.Fin_Dly_Mappings  Fin_Dly_Mappings ON 
#      Fin_Dly_Balances.Country = Fin_Dly_Mappings.Country 
#      AND Fin_Dly_Balances.Le_Book = Fin_Dly_Mappings.Le_Book 
#      AND Fin_Dly_Balances.Year_Month = Fin_Dly_Mappings.Year_Month AND 
#      Fin_Dly_Balances.Sequence_FD = Fin_Dly_Mappings.Sequence_FD AND 
#      Fin_Dly_Balances.Dr_Cr_Bal_Ind = Fin_Dly_Mappings.Dr_Cr_Bal_Ind
#      JOIN VISIONRW.MRL_Lines  MRL_Lines ON Fin_Dly_Mappings.MRL_LINE = MRL_Lines.MRL_LINE
#      JOIN VISIONRW.FRL_Lines  FRL_Lines_BS ON Fin_Dly_Mappings.FRL_Line_BS = FRL_Lines_BS.FRL_Line  
#     WHERE  Fin_Dly_Headers.Country = 'RW'
#         AND  Fin_Dly_Headers.LE_Book = '01'
#         AND  FRL_Lines_BS.FRL_Attribute_05 in  ('FA051050','FA052010' ) 
#         AND  FRL_Lines_BS.FRL_Attribute_03 != 'FA031105' 
#         AND  Fin_Dly_Headers.Record_Type not in  ('999' ) 
#         AND  Fin_Dly_Balances.Bal_Type = '51' 
#         AND Fin_Dly_Headers.customer_id<>'DOOO'
#     GROUP BY  Fin_Dly_Headers.Country , Fin_Dly_Headers.LE_Book ,
#     FRL_Lines_BS.FRL_Attribute_01,
#     Fin_Dly_Headers.Year_Month , FRL_Lines_BS.FRL_Attribute_05 , 
#     FRL_Lines_BS.FRL_Attribute_03,
#     Customers_Dly_Expanded.Customer_Id ,
#     Fin_Dly_Headers.Vision_SBU ,
#     Fin_Dly_Headers.Record_Type , Fin_Dly_Balances.Bal_Type,
#     Fin_Dly_Headers.Currency , Currency_Rates_Daily.rate 
#     )
#     SELECT * FROM default_data 
#     """
# 	PL= pd.read_sql(query, con=get_connection())
# 	PL_csv = PL.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\PL.csv',index=None,header=True) 
	PL= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\PL.csv',header=True)        
	if cust_type=="ALL":
		pass
	else:
		PL= PL[PL.VISION_SBU==cust_type]
    # PL["BALANCE"]=PL["BALANCE"].astype(number)
	PL['BALANCE_LCY']=(PL['BALANCE'].apply(locale.atof))*(PL['RATE'].apply(locale.atof))
# 	deposits_details=PL[PL.FRL_ATTRIBUTE_05=='FA052010'].groupby('FRL_ATT_01_DESCRIPTION').BALANCE.sum()     
	return PL

##########################################################Deposits vs Loans##################################################
# @cache1.memoize(timeout=TIMEOUT)
# def get_deposit(session_id, cust_type="ALL"):
# 	query="""
#     with dates as (
#     select LPAD(extract(day from to_date(sysdate-1)),2) as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM')
#     as year_month from dual 
#     ),
#     day_balance as (
#     select year_month,country,le_book,Sequence_FD,to_number(balance) as balance,dr_cr_bal_ind,bal_type
#         from VISIONRW.Fin_Dly_Balances 
#         unpivot ( 
#             balance for column_
#             in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#             ) balance_unpivot 
#        where year_month = (select year_month from dates fetch next 1 row only) and column_ = CONCAT('BALANCE_',(select day from dates fetch next 1 row only))

#     ),
#     day_rate as (
#     select year_month,country,le_book,currency,rate as rate
#         from VISIONRW.Currency_Rates_Daily
#         unpivot ( 
#             rate for column_
#             in (rate_01, rate_02, rate_03, rate_04, rate_05, rate_06, rate_07, rate_08, rate_09, rate_10, rate_11, rate_12, rate_13, rate_14, rate_15, rate_16, rate_17, rate_18, rate_19, rate_20, rate_21, rate_22, rate_23, rate_24, rate_25, rate_26, rate_27, rate_28, rate_29, rate_30, rate_31)
#             ) rate_unpivot 
#        where year_month = (select year_month from dates fetch next 1 row only) 
#        and column_ = CONCAT('RATE_',(select day from dates fetch next 1 row only)) 
#     ),

#     default_data as (
#     SELECT  Fin_Dly_Headers.Country AS Country,
#         Fin_Dly_Headers.LE_Book AS LE_Book ,
#         Fin_Dly_Headers.Year_Month AS Year_Month ,
#         FRL_Lines_BS.FRL_Attribute_05 AS FRL_Attribute_05 ,
#     ((select FRL_ATTRIBUTE_DESCRIPTION from  VISIONRW.FRL_ATTRIBUTES WHERE FRL_ATTRIBUTE_LEVEL =5 
#     AND FRL_Lines_BS.FRL_ATTRIBUTE_05 = FRL_ATTRIBUTE))  AS FRL_Att_05_Description,        
#         FRL_Lines_BS.FRL_Attribute_03 AS FRL_Attribute_03 ,
#         FRL_Lines_BS.FRL_Attribute_01,
#     ((select FRL_ATTRIBUTE_DESCRIPTION from  VISIONRW.FRL_ATTRIBUTES WHERE FRL_ATTRIBUTE_LEVEL =1 
#     AND FRL_Lines_BS.FRL_ATTRIBUTE_01 = FRL_ATTRIBUTE))  AS FRL_Att_01_Description,     
#         Customers_Dly_Expanded.Customer_Id AS Customer_Id ,
#         Fin_Dly_Headers.Vision_SBU AS Vision_SBU , 
#     Fin_Dly_Headers.Record_Type AS Record_Type , Fin_Dly_Balances.Bal_Type AS Bal_Type, 
#     Fin_Dly_Headers.Currency AS Currency ,TO_NUMBER(Currency_Rates_Daily.rate) AS rate,
#     TO_NUMBER(SUM(Fin_Dly_Balances.balance)) AS balance
#     FROM  VISIONRW.Fin_Dly_Headers  Fin_Dly_Headers
#      JOIN day_balance  Fin_Dly_Balances ON 
#         Fin_Dly_Headers.Country = Fin_Dly_Balances.Country AND 
#         Fin_Dly_Headers.Le_Book = Fin_Dly_Balances.Le_Book AND 
#         Fin_Dly_Headers.Year_Month = Fin_Dly_Balances.Year_Month AND 
#         Fin_Dly_Headers.Sequence_FD = Fin_Dly_Balances.Sequence_FD And 
#         Fin_Dly_Headers.RECORD_TYPE != 9999
#      JOIN day_rate  Currency_Rates_Daily ON 
#      Fin_Dly_Headers.Country = Currency_Rates_Daily.Country AND 
#      Fin_Dly_Headers.Le_Book = Currency_Rates_Daily.Le_Book AND
#      Fin_Dly_Headers.Year_Month = Currency_Rates_Daily.Year_Month 
#      AND Fin_Dly_Headers.currency = Currency_Rates_Daily.currency And Fin_Dly_Headers.RECORD_TYPE != 9999
#      LEFT JOIN VISIONRW.VW_Customers_Dly_Expanded  
#      Customers_Dly_Expanded ON Customers_Dly_Expanded.Country = Fin_Dly_Headers.Country 
#      AND Customers_Dly_Expanded.Le_Book = Fin_Dly_Headers.Le_Book 
#      AND Customers_Dly_Expanded.Customer_ID = Fin_Dly_Headers.Customer_ID And
#      Fin_Dly_Headers.RECORD_TYPE != 9999
#      JOIN VISIONRW.Fin_Dly_Mappings  Fin_Dly_Mappings ON 
#      Fin_Dly_Balances.Country = Fin_Dly_Mappings.Country 
#      AND Fin_Dly_Balances.Le_Book = Fin_Dly_Mappings.Le_Book 
#      AND Fin_Dly_Balances.Year_Month = Fin_Dly_Mappings.Year_Month AND 
#      Fin_Dly_Balances.Sequence_FD = Fin_Dly_Mappings.Sequence_FD AND 
#      Fin_Dly_Balances.Dr_Cr_Bal_Ind = Fin_Dly_Mappings.Dr_Cr_Bal_Ind
#      JOIN VISIONRW.MRL_Lines  MRL_Lines ON Fin_Dly_Mappings.MRL_LINE = MRL_Lines.MRL_LINE
#      JOIN VISIONRW.FRL_Lines  FRL_Lines_BS ON Fin_Dly_Mappings.FRL_Line_BS = FRL_Lines_BS.FRL_Line  
#     WHERE  Fin_Dly_Headers.Country = 'RW'
#         AND  Fin_Dly_Headers.LE_Book = '01'
#         AND  FRL_Lines_BS.FRL_Attribute_05='FA052010' 
#         AND  FRL_Lines_BS.FRL_Attribute_03 != 'FA031105' 
#         AND  Fin_Dly_Headers.Record_Type not in  ('999' ) 
#         AND  Fin_Dly_Balances.Bal_Type = '51' 
#         AND Fin_Dly_Headers.customer_id<>'DOOO'
#     GROUP BY  Fin_Dly_Headers.Country , Fin_Dly_Headers.LE_Book ,
#     Fin_Dly_Headers.Year_Month , FRL_Lines_BS.FRL_Attribute_05 , 
#     FRL_Lines_BS.FRL_Attribute_03,
#     FRL_Lines_BS.FRL_Attribute_01,
#     Customers_Dly_Expanded.Customer_Id ,
#     Fin_Dly_Headers.Vision_SBU ,
#     Fin_Dly_Headers.Record_Type , Fin_Dly_Balances.Bal_Type,
#     Fin_Dly_Headers.Currency , Currency_Rates_Daily.rate 
#     )
#     SELECT * FROM default_data 
#     """
# 	deposits= pd.read_sql(query, con=get_connection())
# 	deposits = deposits.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\deposits.csv',index=None,header=True)    
# 	if cust_type=="ALL":
# 		pass
# 	else:
# 		deposits= deposits[deposits.VISION_SBU==cust_type]
#     # PL["BALANCE"]=PL["BALANCE"].astype(number)
# 	deposits["BALANCE_LCY"]=deposits["BALANCE"]*deposits["RATE"]
# 	Current_lcy=deposits[deposits.FRL_ATT_01_DESCRIPTION=='Current Account - LCY'].BALANCE_LCY.sum()
# 	Current_fcy=deposits[deposits.FRL_ATT_01_DESCRIPTION=='Current Account - FCY'].BALANCE_LCY.sum()
# 	Saving_lcy=deposits[deposits.FRL_ATT_01_DESCRIPTION=='Savings - LCY'].BALANCE_LCY.sum()
# 	Saving_fcy=deposits[deposits.FRL_ATT_01_DESCRIPTION=='Savings - FCY'].BALANCE_LCY.sum()    
# 	fix_depo_lcy=deposits[deposits.FRL_ATT_01_DESCRIPTION=='Fixed Deposits - LCY'].BALANCE_LCY.sum()
# 	fix_depo_fcy=deposits[deposits.FRL_ATT_01_DESCRIPTION=='Fixed Deposits - FCY'].BALANCE_LCY.sum()
# 	Margin=deposits[deposits.FRL_ATT_01_DESCRIPTION=='Margin Deposits'].BALANCE_LCY.sum()
# 	interest_pay=deposits[deposits.FRL_ATT_01_DESCRIPTION=='Interest Payable'].BALANCE_LCY.sum()         

# 	return (Current_lcy,Current_fcy,Saving_lcy,Saving_fcy,fix_depo_lcy,fix_depo_fcy,Margin,interest_pay)
#SELECT * from default_data, SELECT * FROM day_rate
@cache1.memoize(timeout=TIMEOUT)
def get_borrowers(session_id, cust_type="ALL"):
#     query = """
#     SELECT CUSTOMER_ID,CONTRACT_ID as OD_ID,VISION_SBU as category,ACCOUNT_TYPE, BALANCE_LCY, SANCTION_LIMIT,SANCTION_DATE, INTEREST_RATE AS INTEREST_OD, MAIN_CLASSIFICATION_DESC AS MAIN_CLASS,BUSINESS_DATE FROM VISIONRW.OD_MASTER WHERE SANCTION_LIMIT>0
#     and BUSINESS_DATE = (
#         SELECT MAX(BUSINESS_DATE)
#         FROM VISIONRW.OD_MASTER
#     )
#     """
#     od = pd.read_sql(query, con=get_connection())
#     od=od.drop_duplicates(subset='OD_ID')
#     query= """
#     SELECT VISIONRW.LOANS_MASTER.CONTRACT_ID, VISIONRW.LOANS_MASTER.CUSTOMER_ID,
#     VISIONRW.LOANS_MASTER.MAIN_CLASSIFICATION_DESC, VISIONRW.LOANS_MASTER.START_DATE,
#     VISIONRW.LOANS_MASTER.MATURITY_DATE, VISIONRW.LOANS_MASTER.GENDER,VISIONRW.LOANS_MASTER.VISION_SBU, VISIONRW.LOANS_MASTER.SCHEME_DESC, 
#     VISIONRW.LOANS_MASTER.OUTSTANDING_PRINCIPAL_LCY, VISIONRW.LOANS_MASTER.APPROVED_AMOUNT, VISIONRW.ACCOUNTS.SCHEME_CODE,
#     VISIONRW.LOANS_MASTER.BUSINESS_DATE
#     FROM VISIONRW.LOANS_MASTER
#     LEFT JOIN VISIONRW.ACCOUNTS ON
#     VISIONRW.LOANS_MASTER.CUSTOMER_ID=VISIONRW.ACCOUNTS.CUSTOMER_ID
#     WHERE TO_CHAR(VISIONRW.LOANS_MASTER.BUSINESS_DATE, 'yyyy-mm-dd') = (
#                 SELECT TO_CHAR(MAX(VISIONRW.LOANS_MASTER.BUSINESS_DATE),'yyyy-mm-dd')
#                 FROM VISIONRW.LOANS_MASTER
#             )
#        AND VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26')
#        AND VISIONRW.LOANS_MASTER.OUTSTANDING_PRINCIPAL_LCY <0
#     """
#     loan=pd.read_sql(query, con=get_connection())
#     loan=loan.drop_duplicates(subset='CONTRACT_ID')   
#     LOANS=pd.merge(loan, od, on='CUSTOMER_ID', how='outer') 
    od=pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\OD.csv')
    loan=pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\loans.csv')    
    LOANS=pd.merge(loan, od, on='CUSTOMER_ID', how='outer')    
    if cust_type=="ALL":
        pass
    else:
        LOANS= LOANS[LOANS.VISION_SBU==cust_type]
#         od=od[od.VISION_SBU==cust_type]
    Borrowers= LOANS.CUSTOMER_ID.nunique()      
    od_cust=LOANS.CUSTOMER_ID.nunique()
    od_accs=LOANS.OD_ID.nunique()
    appr_amount=LOANS.SANCTION_LIMIT.sum()
    outstanding_am=-1*LOANS[LOANS.BALANCE_LCY<0].BALANCE_LCY.sum()
        
    return Borrowers,od_cust, od_accs,appr_amount,outstanding_am

@cache1.memoize(timeout=TIMEOUT)
def get_account_cleared_balance_lcy(session_id, cust_type="ALL"):
# 	account_query = """
# 	SELECT VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID, VISIONRW.ACCOUNTS_DLY.SCHEME_CODE,VISIONRW.CUSTOMERS_EXPANDED.AO_NAME,
#     VISIONRW.ACCOUNTS_DLY.CURRENCY, VISIONRW.ACCOUNTS_DLY.CLEARED_BALANCE, VISIONRW.ACCOUNTS_DLY.VISION_SBU,VISIONRW.ACCOUNTS_DLY.DATE_CREATION,
#      VISIONRW.CUSTOMERS_EXPANDED.CB_ECO_ACT_DESC,
#     VISIONRW.ACCOUNTS_DLY.VISION_OUC,VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,VISIONRW.CUSTOMERS.CUSTOMER_SEX	
# 	FROM VISIONRW.ACCOUNTS_DLY
#     LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON 
#     VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID=VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
#     LEFT JOIN VISIONRW.CUSTOMERS ON
#     VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID=VISIONRW.CUSTOMERS.CUSTOMER_ID
#     LEFT JOIN VISIONRW.CUSTOMERS_EXPANDED ON
#     VISIONRW.CUSTOMERS.CUSTOMER_ID=VISIONRW.CUSTOMERS_EXPANDED.CUSTOMER_ID
    
# 	WHERE VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID <> 'D000' AND VISIONRW.ACCOUNTS_DLY.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# 	"""

# 	account_ = pd.read_sql(account_query, con=get_connection())
# 	balance = account_.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\dep_overdraft.csv', index=None, header=True)
	account_ = pd.read_csv(r'C:\Users\\Administrator\Downloads\imdas_new\Data_im\dep_overdraft.csv')    
	## To get ALL, Retail, Corporate or SME Data
	if cust_type=="ALL":
		pass
	else:
		account_= account_[account_.VISION_SBU==cust_type]
		# account_opening= account_opening[account_opening.VISION_SBU==cust_type]
	## Get the exchange rate from Currency_Rates_Daily table from VisionDB
# 	forex, days_ago = get_bnr_current_exchange_rate(session_id)
# 	mapping ={"RWF":1}
# 	for val in forex.CURRENCY.values:
# 	    if val in account_.CURRENCY.unique():
# 	        mapping[val] = (forex[val == forex.CURRENCY.values]["RATE_{}".format(get_rate_suffix((date.today()-timedelta(days_ago)).day))]).values[0]

# 	account_["CLEARED_BALANCE_LCY"] = account_.CURRENCY.map(mapping)*account_["CLEARED_BALANCE"]    
	positive_amt = account_[account_.CLEARED_BALANCE>0].CLEARED_BALANCE.sum()
	negative_amt = account_[account_.CLEARED_BALANCE<0].CLEARED_BALANCE.sum()
# 	bins=[-np.inf,-0.01,0., np.inf]
# 	bins=[negative_amt,0,positive_amt]
# 	labels=['Overdraft amount', 'Deposit amount']
# 	deposit_overdraft=account_.groupby(pd.cut(account_.CLEARED_BALANCE, bins,labels=labels)).CLEARED_BALANCE.sum()
# 	loans_interest_rate = loans_data.groupby(pd.cut(loans_data['INTEREST_RATE'], bins, include_lowest=True, right = False, labels=labels)).CONTRACT_ID.nunique()
    
# 	deposit_branch=account_[(account_.CLEARED_BALANCE>=0)&(account_.VISION_OUC!='RW01002010')].groupby("VISION_OUC").CLEARED_BALANCE.sum()
# 	overdraft_branch=-1*account_[(account_.CLEARED_BALANCE<0)&(account_.VISION_OUC!='RW01002010')].groupby("VISION_OUC").CLEARED_BALANCE.sum()
# 	deposit_branch_main=account_[(account_.CLEARED_BALANCE>=0)&(account_.VISION_OUC=='RW01002010')].groupby("VISION_OUC").CLEARED_BALANCE.sum()
# 	overdraft_branch_main=-1*account_[(account_.CLEARED_BALANCE<0)&(account_.VISION_OUC=='RW01002010')].groupby("VISION_OUC").CLEARED_BALANCE.sum()
    
# 	deposit_overtime=account_[account_.CLEARED_BALANCE>=0].groupby("DATE_CREATION").CLEARED_BALANCE.sum()
# 	overdraft_overtime=-1*account_[account_.CLEARED_BALANCE<0].groupby("DATE_CREATION").CLEARED_BALANCE.sum()
    
# 	account_['AGE']= (account_.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
# 	bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
# 	labels = ["18-25","25-30","30-35","35-40","40-45","45-50","50-55","55-60","60+"] 

# 	df = account_[(account_.CUSTOMER_SEX=='M')&(account_.CLEARED_BALANCE>=0)&(account_.VISION_SBU=='R')]
# 	male_age_deposit = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CLEARED_BALANCE.sum()
# 	df = account_[(account_.CUSTOMER_SEX=='F')&(account_.CLEARED_BALANCE>=0)&(account_.VISION_SBU=='R')]    
# 	female_age_deposit = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CLEARED_BALANCE.sum()
    
# 	df = account_[(account_.CUSTOMER_SEX=='M')&(account_.CLEARED_BALANCE<0)&(account_.VISION_SBU=='R')]
# 	male_age_overdraft = -1*df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CLEARED_BALANCE.sum()
# 	df = account_[(account_.CUSTOMER_SEX=='F')&(account_.CLEARED_BALANCE<0)&(account_.VISION_SBU=='R')]    
# 	female_age_overdraft = -1*df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CLEARED_BALANCE.sum()
# 	sector_deposit = account_[account_.CLEARED_BALANCE>0].groupby("CB_ECO_ACT_DESC").CLEARED_BALANCE.sum()    
# 	sector_overdraft = -1*account_[account_.CLEARED_BALANCE<0].groupby("CB_ECO_ACT_DESC").CLEARED_BALANCE.sum()
# ##############################################################################################################################
# 	cust_branch = account_.groupby("VISION_OUC").CUSTOMER_ID.nunique()
	return positive_amt, negative_amt 


@cache1.memoize(timeout=TIMEOUT)
def get_customer_sbu_gender_age_segment(session_id,cust_type='ALL'):
# 	query = """
#     SELECT VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID,
#     VISIONRW.CUSTOMERS_DLY.VISION_SBU,
#     VISIONRW.CUSTOMERS_DLY.CUSTOMER_SEX,
#     VISIONRW.CUSTOMERS_DLY.NUM_OF_ACCOUNTS,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE, 
#     VISIONRW.ACCOUNTS_DLY.SCHEME_CODE,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_NO,
#     VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
#     VISIONRW.CUSTOMERS_DLY.CUSTOMER_OPEN_DATE,
#     VISIONRW.ACCOUNTS_DLY.ACCOUNT_OPEN_DATE
#     FROM VISIONRW.CUSTOMERS_DLY
#     LEFT JOIN VISIONRW.ACCOUNTS_DLY ON 
#     VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID=VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID
#     LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON
#     VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID=VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID
#     WHERE VISIONRW.ACCOUNTS_DLY.ACCOUNT_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd') 
#     AND VISIONRW.CUSTOMERS_DLY.CUSTOMER_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd')
#     AND VISIONRW.ACCOUNTS_DLY.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26','CAL05')
#     AND VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE <>'LAA'
# 	"""
# 	customers = pd.read_sql(query, con=get_connection())
# 	age_segment = customers.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\sbu_gender_segment.csv', index=None, header=True) 
	customers = pd.read_csv(r'C:\Users\\Administrator\Downloads\imdas_new\Data_im\customers.csv') 
# 	customers["VISION_SBU"] = np.where((customers.VISION_SBU == "NA")&(customers.CUSTOMER_SEX.isin(["F","M"])), "R", customers["VISION_SBU"])
	
	if cust_type=="ALL":
		pass
	else:
		customers= customers[customers.VISION_SBU==cust_type]
# 		customers= customers[customers.CUSTOMER_OPEN_DATE==year]

	bins=[1, 2, 3, 4, 5, 6,7,8,9,10, np.inf]
	labels = ["1 Account", "2 Accounts", "3 Accounts", "4 Accounts", "5 Accounts","6 Accounts","7 Accounts","8 Accounts","9 Accounts", "10+ Accounts"]
	num_accounts = customers.groupby(pd.cut(customers["NUM_OF_ACCOUNTS"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()
# 	active=customers[customers.ACCOUNT_STATUS==0]
# 	active_num = active.groupby(pd.cut(active["NUM_OF_ACCOUNTS"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()    
# 	inactive=customers[customers.ACCOUNT_STATUS==1]
# 	inactive_num = inactive.groupby(pd.cut(inactive["NUM_OF_ACCOUNTS"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()
# 	dorm=customers[customers.ACCOUNT_STATUS==3]
# 	dorm_num = dorm.groupby(pd.cut(dorm["NUM_OF_ACCOUNTS"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()
# 	clos=customers[customers.ACCOUNT_STATUS==2]
# 	clos_num = clos.groupby(pd.cut(clos["NUM_OF_ACCOUNTS"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()    
	return customers, num_accounts

@cache1.memoize(timeout=TIMEOUT)
def get_accounts_status(session_id, cust_type="ALL"):
# 	query = """
# 	SELECT VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID,VISIONRW.ACCOUNTS_DLY.ACCOUNT_NO, VISIONRW.ACCOUNTS_DLY.ACCOUNT_OPEN_DATE, VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS,VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS_DATE,floor((SYSDATE - TO_DATE(VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS_DATE))/ 365.25) as LIFETIME,VISIONRW.ACCOUNTS_DLY.SCHEME_CODE, VISIONRW.ACCOUNTS_DLY.VISION_SBU,VISIONRW.ACCOUNTS_DLY.VISION_OUC,VISIONRW.CUSTOMERS_EXPANDED.AO_NAME,
#     VISIONRW.CUSTOMERS_EXPANDED.CB_ECO_ACT_DESC,VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE 
# 	FROM VISIONRW.ACCOUNTS_DLY
#     LEFT JOIN VISIONRW.CUSTOMERS_EXPANDED ON
#     VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID=VISIONRW.CUSTOMERS_EXPANDED.CUSTOMER_ID    
# 	WHERE VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID <> 'D000'AND VISIONRW.CUSTOMERS_EXPANDED.CUSTOMER_ID <> 'D000'
#     AND VISIONRW.ACCOUNTS_DLY.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26','CAL05')
#     and VISIONRW.ACCOUNTS_DLY.ACCOUNT_STATUS_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd')
#     AND VISIONRW.ACCOUNTS_DLY.ACCOUNT_TYPE <>'LAA'
# 	"""

# 	account_opening= pd.read_sql(query, con=get_connection())
	account_opening = pd.read_csv(r'C:\Users\\Administrator\Downloads\imdas_new\Data_im\accounts_status.csv')     
	account_opening=account_opening.drop_duplicates(subset='ACCOUNT_NO')
#	acc_status = account_opening.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\accounts_status.csv', index=None, header=True)
	account_opening['ACCOUNT_OPEN_DATE']=pd.to_datetime(account_opening.ACCOUNT_OPEN_DATE, errors='coerce')
	account_opening["ACCOUNT_AGE"] = (account_opening.ACCOUNT_OPEN_DATE.apply(lambda x:(dt.now() - x) // timedelta(days=365.2425))).astype(int)
# 	account_opening["TIME_TO_DATE"]=(account_opening.ACCOUNT_STATUS_DATE-account_opening.ACCOUNT_OPEN_DATE)//timedelta(days=365.2425)  
# 	account_opening["ACCOUNT_AGE"] = (account_opening.ACCOUNT_OPEN_DATE.apply(lambda x:(account_opening.ACCOUNT_STATUS_DATE - x) // timedelta(days=365.2425))).astype(int)

	## To get ALL, Retail, Corporate or SME Data
	if cust_type=="ALL":
		pass
	else:
		# account_= account_[account_.VISION_SBU==cust_type]
		account_opening= account_opening[account_opening.VISION_SBU==cust_type]

	bins=[0, 1, 2, 5, 10, np.inf]
	labels = ["<1 year", "1-2 years", "3-5 years", "6-10 years", ">10 years"]

	df = account_opening[account_opening.ACCOUNT_STATUS == 0]
	active_accounts = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()

	df = account_opening[account_opening.ACCOUNT_STATUS == 1]
	inactive_accounts =df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()

	df = account_opening[account_opening.ACCOUNT_STATUS == 2]
	closed_accounts = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()

	df = account_opening[account_opening.ACCOUNT_STATUS == 3]
	dormant_accounts = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()
    ####################################Account officer#####################################################
	active_off= account_opening[account_opening.ACCOUNT_STATUS==0].groupby('AO_NAME').ACCOUNT_NO.nunique()
	inactive_off= account_opening[account_opening.ACCOUNT_STATUS==1].groupby('AO_NAME').ACCOUNT_NO.nunique()
	closed_off= account_opening[account_opening.ACCOUNT_STATUS==2].groupby('AO_NAME').ACCOUNT_NO.nunique()
	dormant_off= account_opening[account_opening.ACCOUNT_STATUS==3].groupby('AO_NAME').ACCOUNT_NO.nunique()

    ####################################Economic sector#####################################################
# 	active_sec= account_opening[account_opening.ACCOUNT_STATUS==0].groupby('TIME_TO_DATE').CUSTOMER_ID.nunique()
# 	inactive_sec= account_opening[account_opening.ACCOUNT_STATUS==1].groupby('TIME_TO_DATE').CUSTOMER_ID.nunique()
# 	closed_sec= account_opening[account_opening.ACCOUNT_STATUS==2].groupby('TIME_TO_DATE').CUSTOMER_ID.nunique()
# 	dormant_sec= account_opening[account_opening.ACCOUNT_STATUS==3].groupby('TIME_TO_DATE').CUSTOMER_ID.nunique()    
    
    ###################Account status overtime##########################################################
	active_overtime= account_opening[account_opening.ACCOUNT_STATUS==0].groupby('ACCOUNT_STATUS_DATE').ACCOUNT_NO.nunique()
	inactive_overtime= account_opening[account_opening.ACCOUNT_STATUS==1].groupby('ACCOUNT_STATUS_DATE').ACCOUNT_NO.nunique()
	closed_overtime= account_opening[account_opening.ACCOUNT_STATUS==2].groupby('ACCOUNT_STATUS_DATE').ACCOUNT_NO.nunique()
	dormant_overtime= account_opening[account_opening.ACCOUNT_STATUS==3].groupby('ACCOUNT_STATUS_DATE').ACCOUNT_NO.nunique()
    #####################Account status rate#####################################################################
	Account_status=account_opening.groupby('ACCOUNT_STATUS').ACCOUNT_NO.nunique() # all statuses(Active, inactive, dormant, closed)
	Account_active=account_opening[account_opening.ACCOUNT_STATUS==0].ACCOUNT_NO.nunique() 
	Account_inactive=account_opening[account_opening.ACCOUNT_STATUS==1].ACCOUNT_NO.nunique()
	Account_closed=account_opening[account_opening.ACCOUNT_STATUS==2].ACCOUNT_NO.nunique()
	Account_dormant=account_opening[account_opening.ACCOUNT_STATUS==3].ACCOUNT_NO.nunique()    
########################################################Account lifetime #############################################
	active_life= account_opening[account_opening.ACCOUNT_STATUS==0].groupby('LIFETIME').CUSTOMER_ID.nunique()
	inactive_life= account_opening[account_opening.ACCOUNT_STATUS==1].groupby('LIFETIME').CUSTOMER_ID.nunique()
	closed_life= account_opening[account_opening.ACCOUNT_STATUS==2].groupby('LIFETIME').CUSTOMER_ID.nunique()
	dormant_life= account_opening[account_opening.ACCOUNT_STATUS==3].groupby('LIFETIME').CUSTOMER_ID.nunique()   
    
	return (active_accounts, inactive_accounts, closed_accounts, dormant_accounts,active_overtime,
            inactive_overtime,closed_overtime,dormant_overtime,Account_status,active_off,inactive_off,closed_off,dormant_off,
           active_life,inactive_life,closed_life,dormant_life,Account_active,Account_inactive,Account_closed,Account_dormant)

@cache1.memoize(timeout=TIMEOUT)
def get_customer_by_accounts_status(session_id, cust_type="ALL"):
# 	query = """
# 	SELECT DISTINCT(CUST.CUSTOMER_ID), ACC.ACCOUNT_STATUS, CUSTOMER_OPEN_DATE, ACC.VISION_SBU	
# 	FROM VISIONRW.CUSTOMERS_DLY CUST
# 	LEFT JOIN (
# 	SELECT DISTINCT(ACCOUNT_STATUS), CUSTOMER_ID, ACCOUNT_TYPE, SCHEME_CODE, VISION_SBU, ACCOUNT_OPEN_DATE, ACCOUNT_NO
# 	FROM VISIONRW.ACCOUNTS_DLY
# 	) ACC 
# 	ON CUST.CUSTOMER_ID = ACC.CUSTOMER_ID
# 	LEFT JOIN (
# 	SELECT CUSTOMER_ID, DATE_OF_BIRTH
# 	FROM VISIONRW.CUSTOMER_EXTRAS
# 	) CUST_EXT
# 	ON CUST_EXT.CUSTOMER_ID = ACC.CUSTOMER_ID
# 	WHERE CUSTOMER_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd') and  ACCOUNT_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd')
# 	AND ACC.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26','CAL05' ) 
#     AND ACC.ACCOUNT_TYPE <>'LAA'
# 	"""
	
# 	customers = pd.read_sql(query, con=get_connection())
	customers = pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\cust_accounts_status1.csv')    
	customers = customers.drop_duplicates(subset='CUSTOMER_ID', keep="first")
# 	customers_csv = customers.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\cust_accounts_status1.csv', index=None, header=True)
	customers["CUSTOMER_OPEN_DATE"]=pd.to_datetime(customers.CUSTOMER_OPEN_DATE)
	customers["ACCOUNT_AGE"] = (customers.CUSTOMER_OPEN_DATE.apply(lambda x:(dt.now() - x) // timedelta(days=365.2425))).fillna(0).astype(int)

	## To get ALL, Retail, Corporate or SME Data
	if cust_type=="ALL":
		pass
	else:
		customers= customers[customers.VISION_SBU==cust_type]
		# account_opening= account_opening[account_opening.VISION_SBU==cust_type]

	bins=[0, 1, 2, 5, 10, 15, 20, np.inf]
	labels = ["0-1 year", "1-2 years", "2-5 years", "5-10 years", "10-15 years", "15-20 years", "20+ years"]
	
	# all_accounts= customers.groupby(pd.cut(customers["ACCOUNT_AGE"], bins, include_lowest=True)).ACCOUNT_NO.count()

	df = customers[customers.ACCOUNT_STATUS == 0]
	active_customers = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 1]
	inactive_customers =df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 2]
	closed_customers = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 3]
	dormant_customers = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	# ## Age segmentation
	# customers['AGE']= (customers.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
	# bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
	# labels = ["18-25","25-30","30-35","35-40","40-45","45-50","50-55","55-60","60+"] 

	# df = customers[(customers.ACCOUNT_STATUS == 0)&(customers.VISION_SBU == "R")]
	# age_active = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	# df = customers[(customers.ACCOUNT_STATUS == 1)&(customers.VISION_SBU == "R")]
	# age_inactive =df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	# df = customers[(customers.ACCOUNT_STATUS == 2)&(customers.VISION_SBU == "R")]
	# age_closed = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	# df = customers[(customers.ACCOUNT_STATUS == 3)&(customers.VISION_SBU == "R")]
	# age_dormant = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	return (
		active_customers, inactive_customers, closed_customers, dormant_customers,
		# age_active, age_inactive, age_closed, age_dormant
		)

@cache1.memoize(timeout=TIMEOUT)
def get_customer_status_sbu_gender_age(session_id, cust_type='ALL'):
    
# 	query = """
# 	SELECT DISTINCT(CUST.CUSTOMER_ID), CUST_EXT.DATE_OF_BIRTH, VISION_SBU, CUSTOMER_SEX, CUSTOMER_OPEN_DATE, NUM_OF_ACCOUNTS, ACC.ACCOUNT_STATUS
# 	FROM VISIONRW.CUSTOMERS_DLY CUST
# 	LEFT JOIN (
# 	    SELECT CUSTOMER_ID, ACCOUNT_TYPE, SCHEME_CODE, ACCOUNT_STATUS, ACCOUNT_NO,ACCOUNT_OPEN_DATE
# 	    FROM VISIONRW.ACCOUNTS_DLY
# 	) ACC 
# 	ON CUST.CUSTOMER_ID = ACC.CUSTOMER_ID
# 	LEFT JOIN (
# 	    SELECT CUSTOMER_ID, DATE_OF_BIRTH
# 	    FROM VISIONRW.CUSTOMER_EXTRAS
# 	) CUST_EXT
# 	ON CUST_EXT.CUSTOMER_ID = ACC.CUSTOMER_ID
# 	WHERE ACCOUNT_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd') and  CUSTOMER_OPEN_DATE >=TO_DATE('1990-01-01', 'yyyy/mm/dd')
# 	AND ACC.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26','CAL05' )
#     AND ACC.ACCOUNT_TYPE <>'LAA'
# 	"""
# 	customers = pd.read_sql(query, con=get_connection())
	customers = pd.read_csv(r'C:\Users\\Administrator\Downloads\imdas_new\Data_im\accounts_status1_gender_act.csv')    
# 	age_active= customers.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\accounts_status1_gender_act.csv', index=None, header=True)   
# 	customers["VISION_SBU"] = np.where((customers.VISION_SBU == "NA")&(customers.CUSTOMER_SEX.isin(["F","M"])), "R", customers["VISION_SBU"])

	## To get ALL, Retail, Corporate or SME Data
	if cust_type=="ALL":
		pass
	else:
		customers= customers[customers.VISION_SBU==cust_type]
######################################################################################################################################################Account status based on tenure years####################################################################
###############################################################################################################################
	### To get active customer by gender for retail and/or sbu
	customers["CUSTOMER_OPEN_DATE"]=pd.to_datetime(customers.CUSTOMER_OPEN_DATE,errors="coerce")    
	customers["ACCOUNT_AGE"] = (customers.CUSTOMER_OPEN_DATE.apply(lambda x:(dt.now() - x) //  timedelta(days=365.2425))).astype(int)

	bins=[0, 1, 2, 5, 10, 15, 20, np.inf]
	labels = ["0-1 year", "1-2 years", "2-5 years", "5-10 years", "10-15 years", "15-20 years", "20+ years"]

	## Retail: 
	df = customers[customers.ACCOUNT_STATUS == 0]
	active_ = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 1]
	inactive_ =df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 2]
	closed_ = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 3]
	dormant_ = df.groupby(pd.cut(df["ACCOUNT_AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	## Age segmentation
	customers["DATE_OF_BIRTH"]=pd.to_datetime(customers.DATE_OF_BIRTH,errors="coerce")     
	customers['AGE']= (customers.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
	bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
	labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"] 

	df = customers[customers.ACCOUNT_STATUS == 0]
	age_active = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 1]
	age_inactive =df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 2]
	age_closed = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.ACCOUNT_STATUS == 3]
	age_dormant = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()
    
	return (
	    age_active, age_inactive, age_closed, age_dormant,
	)
########################################Branches###############################################################################
@cache1.memoize(timeout=TIMEOUT)
def get_account_branch_level(session_id, cust_type='ALL'):
 
# 	account1_query = """
# # 	SELECT ACCOUNTS_DLY.SCHEME_CODE, ACCOUNTS_DLY.ACCOUNT_TYPE, ACCOUNTS_DLY.ACCOUNT_NO, ACCOUNTS_DLY.ACCOUNT_OPEN_DATE, ACCOUNTS_DLY.VISION_OUC, ACCOUNTS_DLY.VISION_SBU,ACCOUNTS_DLY.ACCOUNT_STATUS,CUSTOMER_EXTRAS.DATE_OF_BIRTH,
# # 		CUSTOMERS_DLY.NUM_OF_ACCOUNTS, CUSTOMERS_DLY.CUSTOMER_ID,CUSTOMERS_DLY.CUSTOMER_OPEN_DATE, CUSTOMERS_DLY.CUSTOMER_SEX
# # 	FROM VISIONRW.ACCOUNTS_DLY, VISIONRW.CUSTOMERS_DLY,VISIONRW.CUSTOMER_EXTRAS
# # 	WHERE VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID = VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID
# #     AND VISIONRW.ACCOUNTS_DLY.CUSTOMER_ID=VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
# # 	AND CUSTOMERS_DLY.CUSTOMER_ID <> 'D000'
# # 	AND ACCOUNTS_DLY.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26','CAL05' )
# #     AND ACCOUNTS_DLY.ACCOUNT_TYPE<>'LAA'
# # 	"""
# 	accounts = pd.read_sql(account1_query, con=get_connection())
	accounts = pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\account_branch.csv')      
	# 	Branch = branch_acc.groupby("VISION_OUC").ACCOUNT_TYPE.count()
# 	account_branch_csv = accounts.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\account_branch.csv',index=None,header=True)
	## To chose customer segment in Retail,Corporate or SME Data.
	if cust_type=="ALL":   
		pass         
	else:
		accounts= accounts[accounts.VISION_SBU==cust_type]
	accounts['DATE_OF_BIRTH']=pd.to_datetime(accounts.DATE_OF_BIRTH, errors='coerce')     
	accounts['AGE']= (accounts.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
	bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
	labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]
    
	accounts.ACCOUNT_TYPE = np.where(accounts.ACCOUNT_TYPE == "ODA", "CAA",accounts.ACCOUNT_TYPE)              
# 	df1 = accounts[accounts.ACCOUNT_TYPE == 'ODA']
# 	overdraft_age =df1.groupby(pd.cut(df1["AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()
	df1 = accounts[accounts.ACCOUNT_TYPE == 'CAA']
	current_acc_age = df1.groupby(pd.cut(df1["AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()
	df1 = accounts[accounts.ACCOUNT_TYPE == 'SBA']
	saving_acc_age = df1.groupby(pd.cut(df1["AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()   
	df1 = accounts[accounts.ACCOUNT_TYPE == 'TDA']
	term_acc_age = df1.groupby(pd.cut(df1["AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()   
# 	df1 = accounts[accounts.ACCOUNT_TYPE == 'LAA']
# 	loan_ac_age = df1.groupby(pd.cut(df1["AGE"], bins, include_lowest=True, right=False, labels=labels)).ACCOUNT_NO.nunique()
    
# 	Df1 = accounts[accounts.ACCOUNT_TYPE == 'ODA']
# 	overdraft = Df1.groupby("VISION_OUC").ACCOUNT_NO.nunique()
	Df1 = accounts[accounts.ACCOUNT_TYPE == 'CAA']
	current_acc = Df1.groupby("VISION_OUC").ACCOUNT_NO.nunique()
	Df1 = accounts[accounts.ACCOUNT_TYPE == 'SBA']
	saving_acc = Df1.groupby("VISION_OUC").ACCOUNT_NO.nunique()   
	Df1 = accounts[accounts.ACCOUNT_TYPE == 'TDA']
	term_acc = Df1.groupby("VISION_OUC").ACCOUNT_NO.nunique()   
# 	Df1 = accounts[accounts.ACCOUNT_TYPE == 'LAA']
# 	loan_ac = Df1.groupby("VISION_OUC").ACCOUNT_NO.nunique()

	####################################overtime#######################################################
	acc_type = accounts.groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()

# 	df1 = accounts[accounts.ACCOUNT_TYPE == 'ODA']
# 	deposit_acc = df1.groupby("CUSTOMER_OPEN_DATE").ACCOUNT_NO.nunique()
	df1 = accounts[accounts.ACCOUNT_TYPE == 'CAA']
	credit_acc = df1.groupby("CUSTOMER_OPEN_DATE").ACCOUNT_NO.nunique()
	df1 = accounts[accounts.ACCOUNT_TYPE == 'SBA']
	youth_acc = df1.groupby("CUSTOMER_OPEN_DATE").ACCOUNT_NO.nunique()   
	df1 = accounts[accounts.ACCOUNT_TYPE == 'TDA']
	term_deposit_acc = df1.groupby("CUSTOMER_OPEN_DATE").ACCOUNT_NO.nunique()   
# 	df1 = accounts[accounts.ACCOUNT_TYPE == 'LAA']
# 	loan_acc = df1.groupby("CUSTOMER_OPEN_DATE").ACCOUNT_NO.nunique()
    
###################Account type vs account status#####################################################
# 	deposit_act = accounts[(accounts.ACCOUNT_TYPE == 'ODA')& (accounts.ACCOUNT_STATUS==0)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
# 	deposit_inact = accounts[(accounts.ACCOUNT_TYPE == 'ODA')& (accounts.ACCOUNT_STATUS==1)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
# 	deposit_clos = accounts[(accounts.ACCOUNT_TYPE == 'ODA')& (accounts.ACCOUNT_STATUS==2)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
# 	deposit_dorm = accounts[(accounts.ACCOUNT_TYPE == 'ODA')& (accounts.ACCOUNT_STATUS==3)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
    
	current_act = accounts[(accounts.ACCOUNT_TYPE == 'CAA')&(accounts.ACCOUNT_STATUS==0)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	current_inact = accounts[(accounts.ACCOUNT_TYPE == 'CAA')&(accounts.ACCOUNT_STATUS==1)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	current_clos = accounts[(accounts.ACCOUNT_TYPE == 'CAA')&(accounts.ACCOUNT_STATUS==2)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	current_dorm = accounts[(accounts.ACCOUNT_TYPE == 'CAA')&(accounts.ACCOUNT_STATUS==3)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
    
	youth_act = accounts[(accounts.ACCOUNT_TYPE == 'SBA')&(accounts.ACCOUNT_STATUS==0)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	youth_inact = accounts[(accounts.ACCOUNT_TYPE == 'SBA')&(accounts.ACCOUNT_STATUS==1)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	youth_clos = accounts[(accounts.ACCOUNT_TYPE == 'SBA')&(accounts.ACCOUNT_STATUS==2)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	youth_dorm = accounts[(accounts.ACCOUNT_TYPE == 'SBA')&(accounts.ACCOUNT_STATUS==3)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
 
	term_deposit_act = accounts[(accounts.ACCOUNT_TYPE == 'TDA')&(accounts.ACCOUNT_STATUS==0)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	term_deposit_inact = accounts[(accounts.ACCOUNT_TYPE == 'TDA')&(accounts.ACCOUNT_STATUS==1)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	term_deposit_clos = accounts[(accounts.ACCOUNT_TYPE == 'TDA')&(accounts.ACCOUNT_STATUS==2)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
	term_deposit_dorm = accounts[(accounts.ACCOUNT_TYPE == 'TDA')&(accounts.ACCOUNT_STATUS==3)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
    
# 	loan_act = accounts[(accounts.ACCOUNT_TYPE == 'LAA')&(accounts.ACCOUNT_STATUS==0)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()   
# 	loan_inact = accounts[(accounts.ACCOUNT_TYPE == 'LAA')&(accounts.ACCOUNT_STATUS==1)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()   
# 	loan_clos = accounts[(accounts.ACCOUNT_TYPE == 'LAA')&(accounts.ACCOUNT_STATUS==2)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()
# 	loan_dorm = accounts[(accounts.ACCOUNT_TYPE == 'LAA')&(accounts.ACCOUNT_STATUS==3)].groupby("ACCOUNT_TYPE").ACCOUNT_NO.nunique()

##########Account status based on account types(overdraft, loan, current,saving.)
	return (
		current_acc, saving_acc, term_acc,credit_acc, youth_acc, term_deposit_acc, 
        acc_type,term_deposit_dorm,term_deposit_clos,term_deposit_inact,term_deposit_act,youth_dorm,
        youth_clos,youth_inact,youth_act,current_dorm,current_clos,
        current_inact,current_act,term_acc_age,saving_acc_age,current_acc_age
	)

# 	return (
# 		current_acc, saving_acc, term_acc,credit_acc,deposit_acc, youth_acc, term_deposit_acc, 
#         acc_type,overdraft,deposit_dorm,deposit_clos,deposit_inact,deposit_act,
#         term_deposit_dorm,term_deposit_clos,term_deposit_inact,term_deposit_act,youth_dorm,
#         youth_clos,youth_inact,youth_act,current_dorm,current_clos,
#         current_inact,current_act,overdraft_age,term_acc_age,saving_acc_age,current_acc_age
# 	)
#############################################################################################################
#############################################################################################################
@cache1.memoize(timeout=TIMEOUT)
def get_loans_dataset(session_id):
# 	query = """
#     SELECT CUSTOMER_ID,CONTRACT_ID as OD_ID,ACCOUNT_TYPE, BALANCE_LCY, SANCTION_LIMIT,SANCTION_DATE,SANCTION_EXP_DATE, INTEREST_RATE AS INTEREST_OD, MAIN_CLASSIFICATION_DESC AS MAIN_CLASS, SCHEME_CODE_DESC,BUSINESS_DATE FROM VISIONRW.OD_MASTER WHERE SANCTION_LIMIT>0
#     and BUSINESS_DATE = (
#         SELECT MAX(BUSINESS_DATE)
#         FROM VISIONRW.OD_MASTER
#     )
#     """
# 	od = pd.read_sql(query, con=get_connection())
# 	od=od.drop_duplicates(subset='OD_ID')   
# 	query= """
# 	SELECT VISIONRW.LOANS_MASTER.CONTRACT_ID, VISIONRW.LOANS_MASTER.CUSTOMER_ID,
#     VISIONRW.LOANS_MASTER.MAIN_CLASSIFICATION_DESC, VISIONRW.LOANS_MASTER.START_DATE,
#     VISIONRW.LOANS_MASTER.MATURITY_DATE, VISIONRW.LOANS_MASTER.GENDER, VISIONRW.LOANS_MASTER.VISION_SBU,VISIONRW.ACCOUNTS.VISION_OUC, VISIONRW.LOANS_MASTER.SCHEME_DESC, VISIONRW.LOANS_MASTER.SEGMENT, VISIONRW.LOANS_MASTER.AO_NAME, 
# 	    VISIONRW.LOANS_MASTER.CURRENCY, VISIONRW.LOANS_MASTER.CURRENCY_RATE, VISIONRW.LOANS_MASTER.OUTSTANDING_PRINCIPAL_LCY, VISIONRW.LOANS_MASTER.OUTSTANDING_INTEREST, VISIONRW.LOANS_MASTER.APPROVED_AMOUNT, VISIONRW.LOANS_MASTER.DISBURSEMENT_AMT,
# 	    VISIONRW.LOANS_MASTER.CHARGES_RECEIVED, VISIONRW.LOANS_MASTER.INTEREST_RATE, VISIONRW.LOANS_MASTER.SECTOR_CODE_DESC, VISIONRW.LOANS_MASTER.BUSINESS_DATE
# 	FROM VISIONRW.LOANS_MASTER
#     LEFT JOIN VISIONRW.ACCOUNTS ON
#     VISIONRW.LOANS_MASTER.CUSTOMER_ID=VISIONRW.ACCOUNTS.CUSTOMER_ID
#  	WHERE TO_CHAR(VISIONRW.LOANS_MASTER.BUSINESS_DATE, 'yyyy-mm-dd') = (
#  	            SELECT TO_CHAR(MAX(VISIONRW.LOANS_MASTER.BUSINESS_DATE),'yyyy-mm-dd')
#  	            FROM VISIONRW.LOANS_MASTER
#  	        )      
#      AND VISIONRW.LOANS_MASTER.OUTSTANDING_PRINCIPAL_LCY<0 AND VISIONRW.LOANS_MASTER.OUTSTANDING_INTEREST<>0            
# 	"""
#    WHERE BUSINESS_DATE >=TO_DATE('2020-02-01', 'yyyy/mm/dd')    
# 	WHERE TO_CHAR(VISIONRW.LOANS_MASTER.BUSINESS_DATE, 'yyyy-mm-dd') = (
# 	            SELECT TO_CHAR(MAX(VISIONRW.LOANS_MASTER.BUSINESS_DATE),'yyyy-mm-dd')
# 	            FROM VISIONRW.LOANS_MASTER
# 	        )    
# 	    AND VISIONRW.LOANS_MASTER.OUTSTANDING_PRINCIPAL_LCY<>0 AND VISIONRW.LOANS_MASTER.OUTSTANDING_INTEREST<>0
#         od=od[od.VISION_SBU==cust_type]
#     od_cust=od.CUSTOMER_ID.nunique()
#     od_accs=od.OD_ID.nunique()
#     appr_amount=od.SANCTION_LIMIT.sum()
#     outstanding_am=-1*od[od.BALANCE_LCY<0].BALANCE_LCY.sum()
# 	loans = pd.read_sql(query, con=get_connection())
	loans = pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\loans.csv')  
# 	loans = pd.merge(LOANS, od, on='CUSTOMER_ID', how='outer') 
# 	loans["appr_amount"]=(loans["APPROVED_AMOUNT"]+loans["SANCTION_LIMIT"])*loans["CURRENCY_RATE"]
# 	loans["out_amount"]=-1*(loans["OUTSTANDING_PRINCIPAL_LCY"]+loans[loans.BALANCE_LCY<0]["BALANCE_LCY"])
# 	loans['CLASS']=np.where((loans['MAIN_CLASSIFICATION_DESC'].isnull() | loans['MAIN_CLASS'].isnull()), (loans['MAIN_CLASSIFICATION_DESC'].fillna(loans['MAIN_CLASS'])) , (np.where(loans['MAIN_CLASSIFICATION_DESC']==loans['MAIN_CLASS'],loans['MAIN_CLASSIFICATION_DESC'],'NON PERFORMING ASSETS'))) 
    
	loans = loans.drop_duplicates(subset=['CONTRACT_ID'])
# 	loans_csv = loans.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\loans.csv', index=None, header=True)
    
# 	loans = loans.loc[(loans.BUSINESS_DATE>start_date)&(loans.BUSINESS_DATE<=end_date)]    
	loans = group_scheme_desc(session_id, loans)

	loans["OUTSTANDING_PRINCIPAL_LCY"] = -1*loans.OUTSTANDING_PRINCIPAL_LCY
	loans["VISION_SBU"] = np.where((loans.VISION_SBU.isnull())&(loans.GENDER.isin(["F","M"])), "R", loans["VISION_SBU"])
	loans["APPROVED_AMOUNT_LCY"] = loans["APPROVED_AMOUNT"]*loans["CURRENCY_RATE"]
	loans["DISBURSEMENT_AMT_LCY"] = loans["DISBURSEMENT_AMT"]*loans["CURRENCY_RATE"]
	loans["NET_INCOME_LCY"] = loans["APPROVED_AMOUNT"]*loans["CURRENCY_RATE"]*loans["INTEREST_RATE"]/100
	loans["OUTSTANDING_INTEREST_LCY"] = loans["OUTSTANDING_INTEREST"]*loans["CURRENCY_RATE"]
	loans["CHARGES_RECEIVED_LCY"] = loans["CHARGES_RECEIVED"]*loans["CURRENCY_RATE"]

	loans.drop(["APPROVED_AMOUNT", "OUTSTANDING_INTEREST", "CHARGES_RECEIVED", "CURRENCY_RATE"], axis=1, inplace=True)

	return loans

# @cache1.memoize(timeout=TIMEOUT)
# def get_od_master_dataset(session_id):
#     query= """
#     SELECT Business_Date ,Contract_ID ,Customer_ID , Customer_Name ,Account_Type ,Vision_SBU ,Ao_Name ,Balance_FCY ,
#         Balance_LCY , Sanction_Date ,Sanction_Exp_Date ,Sanction_Limit ,Excess_Amount ,Days_In_Excess  ,
#         Main_Classification_Desc  ,Interest_Rate ,Tenor_Months AS Tenor_Months  
#     FROM  VISIONRW.OD_MASTER   
#     WHERE OD_MASTER.Balance_LCY < 0  
#         AND  TO_CHAR(OD_MASTER.Business_Date, 'yyyy-mm-dd') = (
#             SELECT TO_CHAR(MAX(Business_Date),'yyyy-mm-dd')
#             FROM VISIONRW.OD_MASTER
#         )
#     """

#     od_loans = pd.read_sql(query, con=get_connection())
    
#     return od_loans

@cache1.memoize(timeout=TIMEOUT)
def get_loan_details(session_id):
	
	loan_info = get_loans_dataset(session_id)

	loan_info['years']= (loan_info.MATURITY_DATE.apply(lambda x:(x- dt.now()) // timedelta(days=365.2425))).fillna(0).astype(int)

	bins=[0, 1, 2, 3,4, 5, np.inf]
	labels = ["0-1 year", "1-2 years", "2-3 years", "3-4 years", "4-5 years", "5+ years"]

	Df = loan_info[(loan_info.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loan_info.VISION_SBU=='R')]
	retail_Perf = Df.groupby(pd.cut(Df['years'], bins, include_lowest=True, right = False, labels=labels)).CUSTOMER_ID.nunique()
	Df = loan_info[(loan_info.MAIN_CLASSIFICATION_DESC== 'NON PERFORMING ASSETS')&(loan_info.VISION_SBU=='R')]
	retail_Non_perf = Df.groupby(pd.cut(Df['years'], bins, include_lowest=True, right = False, labels=labels)).CUSTOMER_ID.nunique()

	Df = loan_info[(loan_info.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loan_info.VISION_SBU=='S')]
	sme_Perf = Df.groupby(pd.cut(Df['years'], bins, include_lowest=True, right = False, labels=labels)).CUSTOMER_ID.nunique()
	Df = loan_info[(loan_info.MAIN_CLASSIFICATION_DESC== 'NON PERFORMING ASSETS')&(loan_info.VISION_SBU=='S')]
	sme_Non_perf = Df.groupby(pd.cut(Df['years'], bins, include_lowest=True, right = False, labels=labels)).CUSTOMER_ID.nunique()

	Df = loan_info[(loan_info.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loan_info.VISION_SBU=='C')]
	corp_Perf = Df.groupby(pd.cut(Df['years'], bins, include_lowest=True, right = False, labels=labels)).CUSTOMER_ID.nunique()
	Df = loan_info[(loan_info.MAIN_CLASSIFICATION_DESC== 'NON PERFORMING ASSETS')&(loan_info.VISION_SBU=='C')]
	corp_Non_perf = Df.groupby(pd.cut(Df['years'], bins, include_lowest=True, right = False, labels=labels)).CUSTOMER_ID.nunique()
    
	return retail_Perf, retail_Non_perf, sme_Perf, sme_Non_perf, corp_Perf, corp_Non_perf

@cache1.memoize(timeout=TIMEOUT)
def group_scheme_desc(session_id, loan_type): # Different loan type
	# warnings.filterwarnings("ignore", 'This pattern has match groups')
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("CLAIR"),"NEW ECLAIR", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("INVESTMENT LOANS- CORPORATE AND SME"),"INVESTMENT LOANS", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("MORTGAGE LOAN STAFF"),"MORTGAGE LOAN", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("PERSONAL LOANS STAFF"),"PERSONAL LOANS ", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("STOCK LOAN- CORPORATE AND SME"),"STOCK LOAN", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("CONTRUCTION LOANS- CORPORATE AND SME"),"CONSTRUCTION LOANS", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("VEHICLE LOAN- CORPORATE AND SME"),"VEHICLE LOAN", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("ADVANCE ON CONTRACT - CORPORATE AND SME"),"ADVANCE ON CONTRACT", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("EQUIPMENT LOAN- CORPORATE AND SME"),"EQUIPMENT LOAN", loan_type.SCHEME_DESC) 
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("RESTRUCTURED LOAN CORPORATE SME"),"RESTRUCTURED LOAN", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("INVOICE/RECEIVABLES/DISCOUNTING- CORPORATE AND SME"),"INVOICE/RECEIVABLES/DISCOUNTING", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("INSURANCE PREMIUM FINANCING"),"INSURANCE PREMIUM FINANCING", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("VEHICLE LOAN-STAFF"),"VEHICLE LOAN", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("CONSTRUCTION LOAN STAFF"),"CONSTRUCTION LOAN ", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("SECOND HOUSING LOAN STAFF"),"SECOND HOUSING LOAN ", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("MORTGAGE LOAN"),"MORTGAGE LOAN", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("RESTRUCTURED LOAN RETAIL"),"RESTRUCTURED LOAN", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("PLOT ACQUISITION LOAN STAFF"),"PLOT ACQUISITION LOAN ", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("HOME EQUITY"),"HOME EQUITY", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("WORKING CAPITAL FINANCE- CORPORATE AND SME"),"WORKING CAPITAL FINANCE", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("CONSTRUCTION LOAN"),"CONSTRUCTION LOAN", loan_type.SCHEME_DESC)
	loan_type["SCHEME_DESC"]= np.where(loan_type.SCHEME_DESC.str.contains("IMPORT LOAN"),"IMPORT LOAN", loan_type.SCHEME_DESC)
	return loan_type
                    
##########################################################################################################################
###################### Loan page layout callback #########################################################################
##########################################################################################################################

@cache1.memoize(timeout=TIMEOUT)
def select_loan_group_options( session_id, loans, value):

    options = None

    if value == "ALL":
        options =  [{'label': val, 'value': val} for val in sorted(loans.SCHEME_DESC.unique())]
    elif value == "RETAIL":
        options = [{'label': val, 'value': val} for val in 
        	sorted(loans[loans.VISION_SBU == 'R' ].SCHEME_DESC.unique())]
#     elif value == "STAFF":
#         options = [{'label': val, 'value': val} for val in 
#         	sorted(loans[loans.VISION_SBU == 'R' ].SCHEME_DESC.unique())]
    elif value == "CORPORATE" :
        options = [{'label': val, 'value': val} for val in 
        	sorted(loans[loans.VISION_SBU == 'C' ].SCHEME_DESC.unique())]
    elif value == "SME":
        options = [{'label': val, 'value': val} for val in 
        	sorted(loans[loans.VISION_SBU == 'S' ].SCHEME_DESC.unique())]
    return options

@cache1.memoize(timeout=TIMEOUT)
def get_loan_dataframe_for_values_selected(session_id, loans, loan_group, loan_selected):

    if loan_selected is None :
        if loan_group == "ALL":
            return loans
        elif loan_group == "RETAIL":
            return loans[loans.VISION_SBU == 'R' ]
#         elif loan_group == "STAFF":
#             return loans[(loans.VISION_SBU == 'R' )& (loans.SCHEME_DESC.str.contains("STAFF"))]
        elif loan_group == "CORPORATE":
            return loans[loans.VISION_SBU == 'C']
        elif loan_group == "SME":
            return loans[loans.VISION_SBU == 'S']
        return options
    
    else :   
        return loans[loans.SCHEME_DESC == loan_selected]

@cache1.memoize(timeout=TIMEOUT)
def get_loan_type_list(session_id, data, loan_group):
	return [d["value"] for d in select_loan_group_options(session_id, data, loan_group)]

@cache1.memoize(timeout=TIMEOUT)
def get_loans_over_time_and_by_sector(session_id, loans, loan_group, loan_selected):
	loans['MATURITY_DATE']=pd.to_datetime(loans.MATURITY_DATE)
	loans.loc[:, 'REMAINING_TIME']= (loans.MATURITY_DATE.apply(lambda x:(x- dt.now()) // timedelta(days=365.2425/12))).fillna(0).astype(int)
	
# 	bins = None
# 	performing = None
# 	# retail_performing = None
# 	# sme_performing = None
# 	# corp_performing = None
# 	non_performing = None
# 	# retail_non_performing = None
# 	# sme_non_performing = None
# 	# corp_non_performing = None
# 	performing_by_sector = None
# 	non_performing_by_sector = None

	if loan_selected is None:
# 		bins = None
		if loan_group == "ALL":
# 			bins = np.arange(0, loans.REMAINING_TIME.max()+4, 3)
# 			bins = [-np.inf]+list(bins)
# 			bins = np.arange(0, loans.REMAINING_TIME.max()+4, 3)
			bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,  np.inf]
			labels=["1month", "2months", "3months", "4months", "5months", "6months", "7months", "8months", "9months", "10months", "11months", "12< months"]
			performing = loans[loans.MAIN_CLASSIFICATION_DESC=="PERFORMING ASSETS"]
			retail_performing = performing[performing.VISION_SBU=="R"]
			sme_performing = performing[performing.VISION_SBU=="S"]
			corp_performing = performing[performing.VISION_SBU=="C"]

			non_performing = loans[loans.MAIN_CLASSIFICATION_DESC=="NON PERFORMING ASSETS"]
			retail_non_performing = non_performing[non_performing.VISION_SBU=="R"]
			sme_non_performing = non_performing[non_performing.VISION_SBU=="S"]
			corp_non_performing = non_performing[non_performing.VISION_SBU=="C"]

			### Performing and non performing loan over time
			performing_over_time = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CUSTOMER_ID.nunique()
			retail_performing_over_time =retail_performing.groupby(pd.cut(retail_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CUSTOMER_ID.nunique()
			sme_performing_over_time =sme_performing.groupby(pd.cut(sme_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CUSTOMER_ID.nunique()
			corp_performing_over_time =corp_performing.groupby(pd.cut(corp_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CUSTOMER_ID.nunique()

			non_performing_over_time =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CUSTOMER_ID.nunique()
			retail_non_performing_over_time =retail_non_performing.groupby(pd.cut(retail_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CUSTOMER_ID.nunique()
			sme_non_performing_over_time =sme_non_performing.groupby(pd.cut(sme_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CUSTOMER_ID.nunique()
			corp_non_performing_over_time =corp_non_performing.groupby(pd.cut(corp_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CUSTOMER_ID.nunique()

			### Get balance of Performing and non performing loan over time
			performing_over_time_balance = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = False, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
			retail_performing_over_time_balance =retail_performing.groupby(pd.cut(retail_performing['REMAINING_TIME'], bins, include_lowest=True, right = True,labels=labels )).OUTSTANDING_PRINCIPAL_LCY.sum()
			sme_performing_over_time_balance =sme_performing.groupby(pd.cut(sme_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
			corp_performing_over_time_balance =corp_performing.groupby(pd.cut(corp_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()

			non_performing_over_time_balance =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
			retail_non_performing_over_time_balance =retail_non_performing.groupby(pd.cut(retail_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
			sme_non_performing_over_time_balance =sme_non_performing.groupby(pd.cut(sme_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
			corp_non_performing_over_time_balance =corp_non_performing.groupby(pd.cut(corp_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()

			## Set the index to string index
			performing_over_time.index = performing_over_time.index.astype(str)
			retail_performing_over_time.index = retail_performing_over_time.index.astype(str)
			sme_performing_over_time.index = sme_performing_over_time.index.astype(str)
			corp_performing_over_time.index = corp_performing_over_time.index.astype(str)

			non_performing_over_time.index = non_performing_over_time.index.astype(str)
			retail_non_performing_over_time.index = retail_non_performing_over_time.index.astype(str)
			sme_non_performing_over_time.index = sme_non_performing_over_time.index.astype(str)
			corp_non_performing_over_time.index = corp_non_performing_over_time.index.astype(str)

			## Get balance Set the index to string index
			performing_over_time_balance.index = performing_over_time_balance.index.astype(str)
			retail_performing_over_time_balance.index = retail_performing_over_time_balance.index.astype(str)
			sme_performing_over_time_balance.index = sme_performing_over_time_balance.index.astype(str)
			corp_performing_over_time_balance.index = corp_performing_over_time_balance.index.astype(str)

			non_performing_over_time_balance.index = non_performing_over_time_balance.index.astype(str)
			retail_non_performing_over_time_balance.index = retail_non_performing_over_time_balance.index.astype(str)
			sme_non_performing_over_time_balance.index = sme_non_performing_over_time_balance.index.astype(str)
			corp_non_performing_over_time_balance.index = corp_non_performing_over_time_balance.index.astype(str)

			### Performing and non performing loan per sector
			performing_by_sector = performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()
			retail_performing_by_sector = retail_performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()
			sme_performing_by_sector = sme_performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()
			corp_performing_by_sector = corp_performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()

			non_performing_by_sector = non_performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()
			retail_non_performing_by_sector = retail_non_performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()
			sme_non_performing_by_sector = sme_non_performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()
			corp_non_performing_by_sector = corp_non_performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()

			### Get balance Performing and non performing loan per sector
			performing_by_sector_balance = performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
			retail_performing_by_sector_balance = retail_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
			sme_performing_by_sector_balance = sme_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
			corp_performing_by_sector_balance = corp_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()

			non_performing_by_sector_balance = non_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
			retail_non_performing_by_sector_balance = retail_non_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
			sme_non_performing_by_sector_balance = sme_non_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
			corp_non_performing_by_sector_balance = corp_non_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()

			return (
			    performing_over_time, retail_performing_over_time, sme_performing_over_time, corp_performing_over_time,
			    non_performing_over_time, retail_non_performing_over_time, sme_non_performing_over_time, corp_non_performing_over_time,
			    performing_by_sector, retail_performing_by_sector, sme_performing_by_sector, corp_performing_by_sector,
			    non_performing_by_sector, retail_non_performing_by_sector, sme_non_performing_by_sector, corp_non_performing_by_sector,
			    performing_over_time_balance, retail_performing_over_time_balance, sme_performing_over_time_balance, corp_performing_over_time_balance,
			    non_performing_over_time_balance, retail_non_performing_over_time_balance, sme_non_performing_over_time_balance, corp_non_performing_over_time_balance,
			    performing_by_sector_balance, retail_performing_by_sector_balance, sme_performing_by_sector_balance, corp_performing_by_sector_balance,
			    non_performing_by_sector_balance, retail_non_performing_by_sector_balance, sme_non_performing_by_sector_balance, corp_non_performing_by_sector_balance
			)

		else:

			performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="PERFORMING ASSETS")&(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, loans, loan_group)))]
			non_performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="NON PERFORMING ASSETS")&(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, loans, loan_group)))]

			### Performing and non performing loan over time
# 			bins = np.arange(0, performing.REMAINING_TIME.max()+4, 3)
# 			bins = [-np.inf]+list(bins)
			bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,  np.inf]
			labels=["1month", "2months", "3months", "4months", "5months", "6months", "7months", "8months", "9months", "10months", "11months", "12< months"]
			performing_over_time = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = False, labels=labels)).CONTRACT_ID.nunique()
			non_performing_over_time =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).CONTRACT_ID.nunique()
			
			### Get balance of Performing and non performing loan over time
			performing_over_time_balance = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = False, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
			non_performing_over_time_balance =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()

			## Set the index to string index
			performing_over_time.index = performing_over_time.index.astype(str)
			non_performing_over_time.index = non_performing_over_time.index.astype(str)

			## Get balance Set the index to string index
			performing_over_time_balance.index = performing_over_time_balance.index.astype(str)
			non_performing_over_time_balance.index = non_performing_over_time_balance.index.astype(str)

			### Performing and non performing loan per sector
			performing_by_sector = performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()
			non_performing_by_sector = non_performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()

			### Get balance Performing and non performing loan per sector
			performing_by_sector_balance = performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
			non_performing_by_sector_balance = non_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()

			return (
			    performing_over_time, non_performing_over_time,
			    performing_by_sector, non_performing_by_sector,
			    performing_over_time_balance, non_performing_over_time_balance,
			    performing_by_sector_balance, non_performing_by_sector_balance
			)
			
	else:
		
		performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="PERFORMING ASSETS")&(loans.SCHEME_DESC==loan_selected)]
		non_performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="NON PERFORMING ASSETS")&(loans.SCHEME_DESC==loan_selected)]

		### Performing and non performing loan over time and per sector
# 		bins = np.arange(0, performing.REMAINING_TIME.max()+4, 3)
# 		bins = [-np.inf]+list(bins)
		bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,  np.inf]
		labels=["1month", "2months", "3months", "4months", "5months", "6months", "7months", "8months", "9months", "10months", "11months", "12< months"]
		performing_over_time = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = True,labels=labels )).CUSTOMER_ID.nunique()
		performing_over_time_balance = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()

		performing_over_time.index = performing_over_time.index.astype(str)
		performing_by_sector = performing.groupby("SECTOR_CODE_DESC").CUSTOMER_ID.nunique()

		performing_by_sector_balance = performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()

		### non performing loan over time andper sector
		non_performing_over_time = None
		non_performing_by_sector = None
		non_performing_over_time_balance = None
		non_performing_by_sector_balance = None


		if non_performing.shape[0] != 0:
			non_performing_over_time =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True,labels=labels )).CUSTOMER_ID.nunique()
			non_performing_over_time_balance =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = True, labels=labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
			
			non_performing_over_time.index = non_performing_over_time.index.astype(str)
			non_performing_over_time_balance.index = non_performing_over_time_balance.index.astype(str)

			non_performing_by_sector = non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			non_performing_by_sector_balance = non_performing.groupby("SECTOR_CODE_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()

		return (
		    performing_over_time, non_performing_over_time,
		    performing_by_sector, non_performing_by_sector,
		    performing_over_time_balance, non_performing_over_time_balance,
		    performing_by_sector_balance, non_performing_by_sector_balance
		)


##############################Age segment##############################################################
@cache1.memoize(timeout=TIMEOUT)
def get_loan_age(session_id, loans, loan_group=None, loan_selected=None):
#     age_query ="""
#     SELECT CUSTOMER_ID, DATE_OF_BIRTH
#     FROM VISIONRW.CUSTOMER_EXTRAS 
#     """ 
#     birth_data = pd.read_sql(age_query, con=get_connection())
    birth_data = pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\loan_age.csv')    
    age = birth_data.merge(loans, on="CUSTOMER_ID", suffixes=["_LOAN", "_AGE"]) 
#     loan_age= birth_data.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\loan_age.csv',index=None,header=True) 
    age = age[age.VISION_SBU == "R"]

    if loan_group is not  None:
        age = age[(age.SCHEME_DESC.isin(get_loan_type_list(session_id, age, loan_group)))]

    if loan_selected is not  None:
        if loan_selected in get_loan_type_list(session_id, loans_data, "RETAIL"):
            age = age[age.SCHEME_DESC == loan_selected]
        else:
            return None
    age['DATE_OF_BIRTH']=pd.to_datetime(age.DATE_OF_BIRTH, errors='coerce')
    age['years']= (age.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
    bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
    Labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]           

    dF = age[(age.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(age.GENDER=='M')]
    age_perf_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).CUSTOMER_ID.nunique()
    age_perf_male_balance = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
    
    dF = age[(age.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(age.GENDER=='M')]
    age_nonperf_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).CUSTOMER_ID.nunique()
    age_nonperf_male_balance = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).OUTSTANDING_PRINCIPAL_LCY.sum()

    dF = age[(age.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(age.GENDER=='F')]
    age_perf_fem = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).CONTRACT_ID.nunique()
    age_perf_fem_balance = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).OUTSTANDING_PRINCIPAL_LCY.sum()
    
    dF = age[(age.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(age.GENDER=='F')]
    age_nonperf_fem = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).CUSTOMER_ID.nunique()
    age_nonperf_fem_balance = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).OUTSTANDING_PRINCIPAL_LCY.sum()

    return (
        age_perf_male, age_nonperf_male, age_perf_fem, age_nonperf_fem,
        age_perf_male_balance, age_nonperf_male_balance, age_perf_fem_balance, age_nonperf_fem_balance
    )

######################################################Overdraft################################################################
# @cache1.memoize(timeout=TIMEOUT)
# def get_overdraft_dataset(session_id ):
#     query = """
#     SELECT VISIONRW.OD_MASTER.CUSTOMER_ID,VISIONRW.OD_MASTER.CONTRACT_ID as OD_ID,
#     VISIONRW.OD_MASTER.ACCOUNT_TYPE, 
#     VISIONRW.OD_MASTER.SCHEME_CODE,VISIONRW.OD_MASTER.BALANCE_LCY, 
#     VISIONRW.OD_MASTER.SANCTION_LIMIT,
#     VISIONRW.OD_MASTER.SANCTION_DATE,
#     VISIONRW.OD_MASTER.SANCTION_EXP_DATE,
#     VISIONRW.OD_MASTER.INTEREST_RATE AS INTEREST_OD, 
#     VISIONRW.OD_MASTER.MAIN_CLASSIFICATION_DESC AS MAIN_CLASS, 
#     VISIONRW.OD_MASTER.VISION_SBU,VISIONRW.OD_MASTER.GENDER,
#     VISIONRW.OD_MASTER.SECTOR_CODE_DESC, 
#     VISIONRW.CUSTOMERS.VISION_OUC,   
#     VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
#     VISIONRW.OD_MASTER.BUSINESS_DATE FROM VISIONRW.OD_MASTER WHERE VISIONRW.OD_MASTER.SANCTION_LIMIT>0 AND 
#     VISIONRW.OD_MASTER.BALANCE_LCY<0
#     and VISIONRW.OD_MASTER.BUSINESS_DATE = (
#         SELECT MAX(VISIONRW.OD_MASTER.BUSINESS_DATE)
#         FROM VISIONRW.OD_MASTER
#     )
#     LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON
#     VISIONRW.OD_MASTER.CUSTOMER_ID=VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
#     LEFT JOIN VISIONRW.CUSTOMERS ON 
#     VISIONRW.OD_MASTER.CUSTOMER_ID=VISIONRW.CUSTOMERS.CUSTOMER_ID
#     """
#     od = pd.read_sql(query, con=get_connection())
#     od=od.drop_duplicates(subset='OD_ID')
# #         od=od[od.VISION_SBU==cust_type]  
#     return od

# @cache1.memoize(timeout=TIMEOUT)
# def group_schemecode_desc(session_id, loan_type): # Different loan type
# 	# warnings.filterwarnings("ignore", 'This pattern has match groups')
# 	loan_type["SCHEME_CODE_DESC"]=np.where(loan_type.SCHEME_CODE_DESC.str.contains("CURRENT"),"OVERDRAFT", loan_type.SCHEME_CODE_DESC)
# 	loan_type["SCHEME_CODE_DESC"]= np.where(loan_type.SCHEME_CODE_DESC.str.contains(" CREDIT"),"CREDIT CARDS", loan_type.SCHEME_CODE_DESC)

# 	return loan_type

# ##########################################################################################################################
# ###################### Overdraft page layout callback #########################################################################
# ##########################################################################################################################

# @cache1.memoize(timeout=TIMEOUT)
# def select_overdraft_group_options( session_id, od, value):

#     options = None

#     if value == "ALL":
#         options =  [{'label': val, 'value': val} for val in sorted(od.SCHEME_CODE_DESC.unique())]
#     elif value == "RETAIL":
#         options = [{'label': val, 'value': val} for val in 
#         	sorted(od[od.VISION_SBU == 'R' ].SCHEME_CODE_DESC.unique())]
#     elif value == "CORPORATE" :
#         options = [{'label': val, 'value': val} for val in 
#         	sorted(od[od.VISION_SBU == 'C' ].SCHEME_CODE_DESC.unique())]
#     elif value == "SME":
#         options = [{'label': val, 'value': val} for val in 
#         	sorted(od[od.VISION_SBU == 'S' ].SCHEME_CODE_DESC.unique())]
#     return options

# @cache1.memoize(timeout=TIMEOUT)
# def get_od_dataframe_for_values_selected(session_id, od, od_group, od_selected):

#     if od_selected is None :
#         if od_group == "ALL":
#             return od
#         elif od_group == "RETAIL":
#             return od[od.VISION_SBU == 'R']
#         elif od_group == "STAFF":
#             return od[od.VISION_SBU == 'R']
#         elif od_group == "CORPORATE":
#             return od[od.VISION_SBU == 'C']
#         elif od_group == "SME":
#             return od[od.VISION_SBU == 'S']
#         return options
    
#     else :   
#         return od[od.SCHEME_CODE_DESC == od_selected]

# @cache1.memoize(timeout=TIMEOUT)
# def get_od_type_list(session_id, data, od_group):
# 	return [d["value"] for d in select_overdraft_group_options(session_id, data, od_group)]
##############################Age segment########################################################
# @cache1.memoize(timeout=TIMEOUT)
# def get_od_age(session_id, od, ad_group=None, od_selected=None):
#     age = age[age.VISION_SBU =="R"] 

#     if od_group is not  None:
#         age = age[(age.SCHEME_DESC.isin(get_loan_type_list(session_id, age, loan_group)))]

#     if loan_selected is not  None:
#         if loan_selected in get_loan_type_list(session_id, loans_data): 
#             age = age[age.SCHEME_DESC == loan_selected] 
#         else:
#             return None
##############################################################################################################################
#######################################FEE INCOME ############################################################################
#####################################################INTEREST INCOME##########################################################
##############################################################################################################################

# def get_net_fee_income(session_id,loan_group, loan_selected):

#     query = """
#     SELECT 
#         FIN_HISTORY_HEADERS.CUSTOMER_ID, FIN_HISTORY_HEADERS.CONTRACT_ID, 
#         FIN_HISTORY_HEADERS.CUSTOMER_OUC, FIN_HISTORY_HEADERS.CURRENCY, 
#         FIN_HISTORY_HEADERS.SEQUENCE_FH SEQUENCE_FH_HISTORY_HEADERS,

#         MRL_EXPANDED.MRL_LINE, MRL_EXPANDED.BAL_TYPE, MRL_EXPANDED.SOURCE_TYPE, 
#         MRL_EXPANDED.MRL_DESCRIPTION, LOANS_MASTER.SCHEME_DESC,LOANS_MASTER.VISION_SBU,

#         FRL_EXPANDED.SOURCE_TYPE, FRL_EXPANDED.FRL_ATTRIBUTE_04,FRL_EXPANDED.FRL_ATTRIBUTE_05, FRL_EXPANDED.FRL_ATT_04_DESCRIPTION, 
#         FRL_EXPANDED.FRL_LINE, FRL_EXPANDED.FRL_DESCRIPTION, FRL_EXPANDED.SOURCE_TYPE, 
#         FRL_EXPANDED.DATE_CREATION DATE_CREATION_FRL_EXPANDED,

#         FIN_HISTORY_BALANCES.BALANCE_01, FIN_HISTORY_BALANCES.BALANCE_02, FIN_HISTORY_BALANCES.BALANCE_03, 
#         FIN_HISTORY_BALANCES.BALANCE_04, FIN_HISTORY_BALANCES.BALANCE_05, 
#         FIN_HISTORY_BALANCES.BALANCE_06, FIN_HISTORY_BALANCES.BALANCE_07, FIN_HISTORY_BALANCES.BALANCE_08, 
#         FIN_HISTORY_BALANCES.BALANCE_09, FIN_HISTORY_BALANCES.BALANCE_10, FIN_HISTORY_BALANCES.BALANCE_11, 
#         FIN_HISTORY_BALANCES.BALANCE_12, 
#         FIN_HISTORY_BALANCES.BALANCE_FULL_YEAR, 
#         FIN_HISTORY_BALANCES.DATE_CREATION, LOANS_MASTER.BUSINESS_DATE
#     FROM VISIONRW.FIN_HISTORY_BALANCES 
#     LEFT JOIN VISIONRW.FIN_HISTORY_HEADERS  ON FIN_HISTORY_BALANCES.YEAR = FIN_HISTORY_HEADERS.YEAR
#         AND FIN_HISTORY_BALANCES.SEQUENCE_FH = FIN_HISTORY_HEADERS.SEQUENCE_FH
#     LEFT JOIN VISIONRW.MRL_EXPANDED ON FIN_HISTORY_HEADERS.MRL_LINE = MRL_EXPANDED.SOURCE_MRL_LINE
#         AND FIN_HISTORY_BALANCES.BAL_TYPE = MRL_EXPANDED.BAL_TYPE
#     LEFT JOIN VISIONRW.FRL_EXPANDED ON FIN_HISTORY_HEADERS.FRL_LINE_PL = FRL_EXPANDED.FRL_LINE
#         AND FIN_HISTORY_BALANCES.BAL_TYPE = FRL_EXPANDED.BAL_TYPE
#     RIGHT JOIN (
#         SELECT CUSTOMER_ID, CONTRACT_ID, SCHEME_DESC, BUSINESS_DATE, VISION_SBU
#         FROM VISIONRW.LOANS_MASTER
#         WHERE TO_CHAR(BUSINESS_DATE, 'yyyy-mm-dd') = (
#                 SELECT TO_CHAR(MAX(BUSINESS_DATE),'yyyy-mm-dd')
#                 FROM VISIONRW.LOANS_MASTER
#             )
#     ) LOANS_MASTER ON FIN_HISTORY_HEADERS.CUSTOMER_ID=LOANS_MASTER.CUSTOMER_ID
#         AND FIN_HISTORY_HEADERS.CONTRACT_ID=LOANS_MASTER.CONTRACT_ID
#     WHERE FIN_HISTORY_BALANCES.BAL_TYPE= '3'
#         AND FIN_HISTORY_HEADERS.CUSTOMER_ID<> 'D000' 
#         AND FIN_HISTORY_HEADERS.CUSTOMER_ID NOT LIKE '%FT000000%'
#         AND MRL_EXPANDED.SOURCE_TYPE= '0' AND FRL_EXPANDED.SOURCE_TYPE= '0'
#         AND FIN_HISTORY_BALANCES.BALANCE_FULL_YEAR <> 0
#         """

#     data = pd.read_sql(query, con=get_connection())
    
#     fee_income= data[data.FRL_ATT_04_DESCRIPTION=='Fees & Commissions']   
#     net_income= data[data.FRL_ATT_04_DESCRIPTION=='Interest Income']
#     fee_inc= fee_income.groupby(['CUSTOMER_ID', 'CONTRACT_ID']).agg({'BALANCE_FULL_YEAR':sum}).reset_index().\
#         rename(columns={'BALANCE_FULL_YEAR':'FEE_INCOME'})
#     net_inc= net_income.groupby(['CUSTOMER_ID', 'CONTRACT_ID']).agg({'BALANCE_FULL_YEAR':sum}).reset_index().\
#         rename(columns={'BALANCE_FULL_YEAR':'NET_INCOME'})
    
#     if loan_group =="ALL":
#         pass
#     else:
#         fee_income= data[(data.FRL_ATT_04_DESCRIPTION=='Fees & Commissions')&(data.VISION_SBU==loan_group)&(data.SCHEME_DESC==loan_selected)]
#         net_income= data[(data.FRL_ATT_04_DESCRIPTION=='Interest Income')&(data.VISION_SBU==loan_group)&(data.SCHEME_DESC==loan_selected)]
# #     fee_income_csv = data.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\fee_income.csv', index=None, header=True) 
#     if loan_selected is not None:
#         fee_income=fee_income[fee_income.SCHEME_DESC==loan_selected]
#         net_income=net_income[net_income.SCHEME_DESC==loan_selected]
#     else:
#         return None
#     fee_inc=fee_income.BALANCE_FULL_YEAR.sum()
#     net_inc=net_income.BALANCE_FULL_YEAR.sum()
    
    
#     age = age[age.VISION_SBU == "R"]

#     if od_group is not  None: 
#         age = age[(age.SCHEME_DESC.isin(get_loan_type_list(session_id, age, loan_group)))]

#     if loan_selected is not  None:
#         if loan_selected in get_loan_type_list(session_id, loans_data, "RETAIL") or loan_selected in get_loan_type_list(session_id, loans_data, "STAFF"):
#             age = age[age.SCHEME_DESC == loan_selected]
#         else:
#             return None    
        
#     if loan_selected is None:
#         if loan_group == "ALL":

#             fee_inc= fee_income.groupby(['CUSTOMER_ID', 'CONTRACT_ID']).agg({'BALANCE_FULL_YEAR':sum}).reset_index().\
#                 rename(columns={'BALANCE_FULL_YEAR':'FEE_INCOME'})
#             net_inc= net_income.groupby(['CUSTOMER_ID', 'CONTRACT_ID']).agg({'BALANCE_FULL_YEAR':sum}).reset_index().\
#                 rename(columns={'BALANCE_FULL_YEAR':'NET_INCOME'})
#             return fee_inc,net_inc
# #             fee_net_inc = net_inc.merge(fee_inc, on=['CUSTOMER_ID', 'CONTRACT_ID'], how='left')
#             fee_net_inc= fee_net_inc.fillna(0)
#         return fee_inc,net_inc
#         else:
# #         if loan_selected is not None:
#             data=data[data.SCHEME_DESC==loan_selected]
#             fee_income= data[(data.FRL_ATTRIBUTE_06== 'FA060600') &(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, data, loan_group)))]   
#             net_income= data[(data.FRL_ATTRIBUTE_06== 'FA060300') &(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, data, loan_group)))]
#             fee_inc= fee_income.groupby(['CUSTOMER_ID', 'CONTRACT_ID']).agg({'BALANCE_FULL_YEAR':sum}).reset_index().\
#                 rename(columns={'BALANCE_FULL_YEAR':'FEE_INCOME'})
#             net_inc= net_income.groupby(['CUSTOMER_ID', 'CONTRACT_ID']).agg({'BALANCE_FULL_YEAR':sum}).reset_index().\
#                 rename(columns={'BALANCE_FULL_YEAR':'NET_INCOME'})
#     return fee_inc,net_inc
#     else:
#         return fee_inc,fee_inc
#############################################################################################
###################### Channels Page  Functions #############################################
#############################################################################################


@cache1.memoize(timeout=TIMEOUT)
def get_och_channels_data(session_id,start, end,selected_channel):
#     query= """
#     SELECT TXNH.TXN_ID, TXNH.TXN_TYPE, TXNH.REQUEST_DATE, TXNH.TXN_DATE, 
#     TXND.TXN_ID,TXND.CP_ACCT_CRN, TXND.TRAN_ACT_ENTITY_ID AS ACCOUNT_NO, TXND.VALUE_DATE, 
#     TXND.CHANNEL_ID,TXNH.USER_INPUT_DATE, TXNH.TOTAL_TXN_AMT_IN_HOMECRN
#     FROM ECECUSER.TXNH
#     RIGHT JOIN ECECUSER.TXND ON TXNH.TXN_ID=TXND.TXN_ID
#     WHERE TXNH.BANK_ID='RW' AND TXND.BANK_ID='RW' 
#     """

# #     och = pd.read_sql(query, con=get_connection(userid_och, password_och, host_och, port_och, SID_och))
    
#     query1 = """SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
# VISIONRW.ACCOUNTS.SCHEME_CODE
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON 
# VISIONRW.CUSTOMERS.CUSTOMER_ID = VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000' 
# """
    
#     customer_details = pd.read_sql(query1, con=get_connection())    
#     txn_df= och.merge(customer_details, on='ACCOUNT_NO')
    txn_df= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\och_channels.csv')
    
    txn_df.USER_INPUT_DATE = pd.to_datetime(txn_df.USER_INPUT_DATE,errors='coerce')    
#     txn_df_csv = txn_df.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\och_channels.csv',index=None,header=True)    
    txn_df= txn_df.set_index('USER_INPUT_DATE').loc[start:end, ['TXN_TYPE', 'TOTAL_TXN_AMT_IN_HOMECRN', 'CHANNEL_ID', 'CP_ACCT_CRN','ACCOUNT_NO','TXN_DATE','DATE_OF_BIRTH','CUSTOMER_SEX','VISION_SBU']]    
    if selected_channel=='All':
        pass
    else:
        txn_df=txn_df[txn_df.VISION_SBU==selected_channel]
        
    iclick_cus= txn_df[txn_df.CHANNEL_ID=='I'].ACCOUNT_NO.nunique()
    Mobile_cus= txn_df[txn_df.CHANNEL_ID=='G'].ACCOUNT_NO.nunique()
    ussd_cus=txn_df[txn_df.CHANNEL_ID=='U'].ACCOUNT_NO.nunique()
#     ##################################channels usage overtime#############################
#     customer=customer_details.CUSTOMER_ID.nunique()    
#     iclick_cus=txn_df[txn_df.CHANNEL_ID=='I'].ACCOUNT_NO.nunique()
#     Mobile_cus=txn_df[txn_df.CHANNEL_ID=='G'].ACCOUNT_NO.nunique()        
#     ussd_cus=txn_df[txn_df.CHANNEL_ID=='U'].ACCOUNT_NO.nunique()
    
    iclick_tran=txn_df[txn_df.CHANNEL_ID=='I'].TOTAL_TXN_AMT_IN_HOMECRN.count()
    Mobile_tran=txn_df[txn_df.CHANNEL_ID=='G'].TOTAL_TXN_AMT_IN_HOMECRN.count()
    ussd_tran=txn_df[txn_df.CHANNEL_ID=='U'].TOTAL_TXN_AMT_IN_HOMECRN.count()
    
    iclick_am=txn_df[txn_df.CHANNEL_ID=='I'].TOTAL_TXN_AMT_IN_HOMECRN.sum()
    Mobile_am=txn_df[txn_df.CHANNEL_ID=='G'].TOTAL_TXN_AMT_IN_HOMECRN.sum()
    ussd_am=txn_df[txn_df.CHANNEL_ID=='U'].TOTAL_TXN_AMT_IN_HOMECRN.sum()    
    
    iclick_trend=txn_df[txn_df.CHANNEL_ID=='I'].groupby('TXN_DATE').ACCOUNT_NO.count()
    Mobile_trend=txn_df[txn_df.CHANNEL_ID=='G'].groupby('TXN_DATE').ACCOUNT_NO.count()            
    ussd_trend=txn_df[txn_df.CHANNEL_ID=='U'].groupby('TXN_DATE').ACCOUNT_NO.count()


#############################################channel amount##########################################
    iclick=txn_df[txn_df.CHANNEL_ID=='I'].groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.sum()
    Mobile=txn_df[txn_df.CHANNEL_ID=='G'].groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.sum()            
    ussd=txn_df[txn_df.CHANNEL_ID=='U'].groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.sum()
    
    iclick_tran_num=txn_df[txn_df.CHANNEL_ID=='I'].groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.count()
    Mobile_tran_num=txn_df[txn_df.CHANNEL_ID=='G'].groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.count()            
    ussd_tran_num=txn_df[txn_df.CHANNEL_ID=='U'].groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.count()
    
    iclick_cust=txn_df[txn_df.CHANNEL_ID=='I'].groupby('TXN_TYPE').ACCOUNT_NO.nunique()
    Mobile_cust=txn_df[txn_df.CHANNEL_ID=='G'].groupby('TXN_TYPE').ACCOUNT_NO.nunique()           
    ussd_cust=txn_df[txn_df.CHANNEL_ID=='U'].groupby('TXN_TYPE').ACCOUNT_NO.nunique()  
######################################age############################################################ 
# txn_df['DATE_OF_BIRTH']=datetime.datetime.strptime(txn_df['DATE_OF_BIRTH'],'%m-%d-%Y').date()
# txn_df['DATE_OF_BIRTH'].strftime('%Y-%m-%d %H:%M:%S.%f%z')
    txn_df['DATE_OF_BIRTH']=txn_df['DATE_OF_BIRTH'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# train['ID'].apply(lambda x: datetime.strptime(x, '%Y%m%d%H'))
# birthdate = datetime.datetime.strptime(birthday,'%m/%d/%Y')
    currentDate = datetime.now()
    txn_df['years']= (txn_df.DATE_OF_BIRTH.apply(lambda x:(currentDate-x) // timedelta(days=365.2425))).fillna(0).astype(int)
#     txn_df['years']= (txn_df.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
    bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
    Labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]

    dF = txn_df[(txn_df.CHANNEL_ID=='I')&(txn_df.CUSTOMER_SEX=='M')]
    ICLICK_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    dF = txn_df[(txn_df.CHANNEL_ID=='I')&(txn_df.CUSTOMER_SEX=='F')]
    iclick_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()

    dF = txn_df[(txn_df.CHANNEL_ID=='U')&(txn_df.CUSTOMER_SEX=='M')]
    ussd_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    dF = txn_df[(txn_df.CHANNEL_ID=='U')&(txn_df.CUSTOMER_SEX=='F')]
    ussd_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()    

    dF = txn_df[(txn_df.CHANNEL_ID=='G')&(txn_df.CUSTOMER_SEX=='M')]
    mobile_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    dF = txn_df[(txn_df.CHANNEL_ID=='G')&(txn_df.CUSTOMER_SEX=='F')]
    mobile_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()    

#######################Age vs transactions#############################
    dF = txn_df[(txn_df.CHANNEL_ID=='I')&(txn_df.CUSTOMER_SEX=='M')]
    ICLICK_male_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.count()
    dF = txn_df[(txn_df.CHANNEL_ID=='I')&(txn_df.CUSTOMER_SEX=='F')]
    iclick_female_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.count()

    dF = txn_df[(txn_df.CHANNEL_ID=='U')&(txn_df.CUSTOMER_SEX=='M')]
    ussd_male_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.count()
    dF = txn_df[(txn_df.CHANNEL_ID=='U')&(txn_df.CUSTOMER_SEX=='F')]
    ussd_female_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.count()    

    dF = txn_df[(txn_df.CHANNEL_ID=='G')&(txn_df.CUSTOMER_SEX=='M')]
    mobile_male_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.count()
    dF = txn_df[(txn_df.CHANNEL_ID=='G')&(txn_df.CUSTOMER_SEX=='F')]
    mobile_female_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.count()    
        
#     forex2 = txn_df.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\txn_df.csv', index=None, header=True) 
    return (txn_df,iclick_am,Mobile_am,ussd_am,iclick_tran,Mobile_tran,ussd_tran,
            iclick_cus,Mobile_cus,ussd_cus,iclick_cus,
            Mobile_cus,ussd_cus,iclick_trend,Mobile_trend,ussd_trend,iclick,Mobile,
            ussd,iclick_tran_num,Mobile_tran_num,ussd_tran_num,iclick_cust,
            Mobile_cust,ussd_cust,mobile_female_num,mobile_male_num,ussd_female_num,ussd_male_num,
            iclick_female_num,ICLICK_male_num,mobile_female,mobile_male,
            ussd_female,ussd_male,iclick_female,ICLICK_male)

@cache1.memoize(timeout=TIMEOUT)
def get_transact_summary_table(session_id, channel_id, txn_df, start, end,selected_channel):
    txn_df['TXN_DATE']=pd.to_datetime(txn_df['TXN_DATE'],format='%Y/%m/%d')
    data= txn_df.set_index('TXN_DATE').loc[start:end, ['TXN_TYPE','TOTAL_TXN_AMT_IN_HOMECRN','CHANNEL_ID','CP_ACCT_CRN','ACCOUNT_NO']]
    data['TXN_TYPE']= data['TXN_TYPE'].replace(tran_type_descr)
    df= data[data.CHANNEL_ID== channel_id]

    transactions__df= df.loc[:,['TXN_TYPE','TOTAL_TXN_AMT_IN_HOMECRN','ACCOUNT_NO']].groupby(['TXN_TYPE']).agg(["count", "sum",]).reset_index()
    transactions__df.columns= ['_'.join(col).strip() for col in transactions__df.columns.values]
    transactions__df= transactions__df.rename(
        columns={
            'TOTAL_TXN_AMT_IN_HOMECRN_sum': 'total_value', 
            'TOTAL_TXN_AMT_IN_HOMECRN_count': 'total_trans',
            'TXN_TYPE_': 'trans_type',
            'ACCOUNT_NO_count':'Users',
        })
    
    intra__transactions__df= df.query("CP_ACCT_CRN=='RWF'").loc[:,['TXN_TYPE', 'TOTAL_TXN_AMT_IN_HOMECRN','ACCOUNT_NO']].groupby(['TXN_TYPE']).agg(["count", "sum",]).reset_index()
    intra__transactions__df.columns= ['_'.join(col).strip() for col in intra__transactions__df.columns.values]
    intra__transactions__df= intra__transactions__df.rename(
        columns={
            'TOTAL_TXN_AMT_IN_HOMECRN_sum': 'total_value', 
            'TOTAL_TXN_AMT_IN_HOMECRN_count': 'total_trans',
            'TXN_TYPE_': 'trans_type', 
            'ACCOUNT_NO_count':'Users',            
        })

    inter__transactions__df= df.query("CP_ACCT_CRN!='RWF'").loc[:,['TXN_TYPE', 'TOTAL_TXN_AMT_IN_HOMECRN','ACCOUNT_NO']].groupby(['TXN_TYPE']).agg(["count", "sum",]).reset_index()
    inter__transactions__df.columns= ['_'.join(col).strip() for col in inter__transactions__df.columns.values]
    inter__transactions__df= inter__transactions__df.rename(
        columns={
            'TOTAL_TXN_AMT_IN_HOMECRN_sum': 'total_value', 
            'TOTAL_TXN_AMT_IN_HOMECRN_count': 'total_trans',
            'TXN_TYPE_': 'trans_type',
            'ACCOUNT_NO_count':'Users',            
        })

    intra_inter_trans= intra__transactions__df.merge(inter__transactions__df, on='trans_type', suffixes=['_intra', '_inter'], how='left')
    transact__df= transactions__df.merge(intra_inter_trans, on='trans_type', how='left')
    transact__df= transact__df.fillna(0)
#     return transact__df

    Trans_Type= transact__df.trans_type.values
    Total_Trans= transact__df.total_trans.values
    Total_Value= transact__df.total_value.values
    Total_users= transact__df.Users.values
    National_Trans= transact__df.total_trans_intra.values
    National_Value= transact__df.total_value_intra.values
#     National_User= transact__df.Users_intra.values    

    Inter_Trans= transact__df.total_trans_inter.values
    Inter_Value= transact__df.total_value_inter.values
    
    intra_cust=transact__df.Users_intra.values
    inter_cust=transact__df.Users_inter.values
    
    
    return Trans_Type, Total_Trans, Total_Value, National_Trans, National_Value, Inter_Trans, Inter_Value,intra_cust,inter_cust,Total_users

@cache1.memoize(timeout=TIMEOUT)
def get_push_and_pull_data(session_id,start, end,selected_channel):
#     query_reg = """
#     SELECT SP, SERVICE, MSISDN, FINACLE_ACCT, ACTIVE, ENTRY_DATE, APPROVAL_DATE, CLOSED_DATE
#     FROM MTNUSER.MM_REG
#     """

# #     df_mm_reg = pd.read_sql(query_reg, con=get_connection(userid_fiorano, password_fiorano, host_fiorano, port_fiorano, SID_fiorano))
# #     df_mm_reg = df_mm_reg[df_mm_reg["FINACLE_ACCT"]!= 'NA']
#     query_tran = """
#     SELECT SP, SERVICE, MSISDN, TRAN_TYPE, REQ_REF, TRAN_AMT, 
#         CBS_STATUS, to_char(MTNUSER.MM_TRAN.entry_date,'yyyy-mm-dd')as ENTRY_DATE
#     FROM MTNUSER.MM_TRAN
#     """
# #     df_mm_tran = pd.read_sql(query_tran, con=get_connection(userid_fiorano, password_fiorano, host_fiorano, port_fiorano, SID_fiorano))
# #     df_tran = df_mm_tran.merge(df_mm_reg, on=["MSISDN", "SP", "SERVICE"], suffixes=["","_REG"], how="left")
    
#     query1 = """SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
# VISIONRW.ACCOUNTS.SCHEME_CODE
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON 
# VISIONRW.CUSTOMERS.CUSTOMER_ID = VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000'
# """
#     customer_details = pd.read_sql(query1, con=get_connection())    
#     df= pd.merge(df_tran, customer_details, left_on="FINACLE_ACCT", right_on="ACCOUNT_NO").drop('ACCOUNT_NO', axis=1)
    df= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\push_pull.csv')    
#     push_pull_date = df.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\push_pull.csv', index=None, header=True)    
    df.ENTRY_DATE = pd.to_datetime(df.ENTRY_DATE,errors='coerce')
#     df['ENTRY_DATE']=df.ENTRY_DATE.dt.to_period('d').dt.strftime('%Y%M%D')    
#     df['ENTRY_DATE']=pd.PeriodIndex(df.ENTRY_DATE, freq='d') 
#     df['ENTRY_DATE']=df.ENTRY_DATE.dt.day

    df['TRAN_TYPE']= df['TRAN_TYPE'].replace(push_MAPPING)
    df= df.set_index('ENTRY_DATE').loc[start:end, ['TRAN_TYPE', 'TRAN_AMT','FINACLE_ACCT','DATE_OF_BIRTH','CUSTOMER_SEX','VISION_SBU']]    
    if selected_channel=="All":
        pass
    else:
        df=df[df.VISION_SBU==selected_channel]
    MTN_cus=df.FINACLE_ACCT.nunique()
    MTN_am=df.TRAN_AMT.sum()
    MTN_tran= df.TRAN_AMT.count()
    MTN_tran_numb=df.TRAN_AMT.count()    
    MTN_trend=df.groupby('ENTRY_DATE').FINACLE_ACCT.count()
    MTN=df.groupby('TRAN_TYPE').TRAN_AMT.sum()
    MTN_tran_num=df.groupby('TRAN_TYPE').TRAN_AMT.count()
    MTN_cust=df.groupby('TRAN_TYPE').FINACLE_ACCT.count()
###############################################################################################################################    
    df['DATE_OF_BIRTH']=df['DATE_OF_BIRTH'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# train['ID'].apply(lambda x: datetime.strptime(x, '%Y%m%d%H'))
# birthdate = datetime.datetime.strptime(birthday,'%m/%d/%Y')
    currentDate = datetime.now()
    df['years']= (df.DATE_OF_BIRTH.apply(lambda x:(currentDate-x) // timedelta(days=365.2425))).fillna(0).astype(int)    
#     df['years']= (df.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
    bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
    Labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]
    
    dF = df[df.CUSTOMER_SEX=='M']
    mtn_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()
    dF = df[df.CUSTOMER_SEX=='F']
    mtn_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()

    dF = df[df.CUSTOMER_SEX=='M']
    mtn_male_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.count()
    dF = df[df.CUSTOMER_SEX=='F']
    mtn_female_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.count()
#############################################################################################################################
#     forex2 = df.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\txn_df_1.csv', index=None, header=True)
    return (df,MTN_cus,MTN_am,MTN_tran, MTN_trend,MTN,MTN_tran_num,MTN_cust,mtn_male,
     mtn_female,mtn_male_num,mtn_female_num,MTN_tran_numb)
#     (df,MTN_cus,MTN_am,MTN_tran, MTN_trend,MTN,MTN_tran_num,MTN_cust,mtn_male,
#      mtn_female,mtn_male_num,mtn_female_num,MTN_tran_numb)
## Push & Pull
@cache1.memoize(timeout=TIMEOUT)
def get_transact_summary_table_push_pull(session_id, df, start, end, selected_channel):
#     data= df.set_index('ENTRY_DATE').loc[start:end, ['TRAN_TYPE', 'TRAN_AMT']]
    
    transactions__push_pull= df.groupby(['TRAN_TYPE']).agg(["count", "sum",]).reset_index()
    transactions__push_pull.columns= ['_'.join(col).strip() for col in transactions__push_pull.columns.values]
    transactions__push_pull= transactions__push_pull.rename(
        columns={
            'TRAN_AMT_sum': 'total_value', 
            'TRAN_AMT_count': 'total_trans',
            'TRAN_TYPE_': 'trans_type',
            'FINACLE_ACCT_count':'users',
        })

    Trans_Type__push_pull= transactions__push_pull.trans_type.values

    Total_Trans__push_pull= transactions__push_pull.total_trans.values
    Total_Value__push_pull= transactions__push_pull.total_value.values
    Total_users=transactions__push_pull.users.values

    National_Trans__push_pull= transactions__push_pull.total_trans.values
    National_Value__push_pull= transactions__push_pull.total_value.values

    Inter_Trans__push_pull= [0 for _ in range(transactions__push_pull.shape[0])]
    Inter_Value__push_pull= [0 for _ in range(transactions__push_pull.shape[0])]
    
    return (
        Trans_Type__push_pull, Total_Trans__push_pull, Total_Value__push_pull, National_Trans__push_pull, 
        National_Value__push_pull, Inter_Trans__push_pull, Inter_Value__push_pull,Total_users
    )
  
########################Channel#######################################################################################

@cache1.memoize(timeout=TIMEOUT)
def get_MTN_USER(session_id,cust_type):
#     query_mtn="""
# SELECT MTNUSER.MM_TRAN.tran_id,MTNUSER.MM_REG.msisdn,MTNUSER.MM_REG.finacle_acct,MTNUSER.MM_REG.sp,
# MTNUSER.MM_REG.active,MTNUSER.MM_TRAN.tran_type,to_char(MTNUSER.MM_TRAN.entry_date,'yyyy-mm-dd')as ENTRY_DATE,
# MTNUSER.MM_TRAN.tran_amt,
# MTNUSER.MM_TRAN.cbs_status
# FROM MTNUSER.MM_REG, MTNUSER.MM_TRAN
# where MTNUSER.MM_REG.msisdn= MTNUSER.MM_TRAN.msisdn
# """
    
# # AND MTNUSER.MM_TRAN.entry_date >=TO_DATE('2019-01-01', 'yyyy/mm/dd')    
# #     push_pull = pd.read_sql(query_mtn, con=get_connection_fiar())
# # AND EXTRACT( YEAR FROM MTNUSER.MM_TRAN.entry_date) = EXTRACT(YEAR FROM sysdate)

#     query1 = """SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
# VISIONRW.ACCOUNTS.SCHEME_CODE
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON 
# VISIONRW.CUSTOMERS.CUSTOMER_ID = VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000' 
# """
# # to_char(C.RECEIPTDATE,'DD/MM/YYYY'),    
#     customer_details = pd.read_sql(query1, con=get_connection())
    start = time.time()    
#     MTN_TIGO= pd.merge(push_pull, customer_details, left_on="FINACLE_ACCT", right_on="ACCOUNT_NO").drop('ACCOUNT_NO', axis=1)
    MTN_TIGO= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\push_pull.csv')    
#     MTN_TIGO= MTN_TIGO.drop_duplicates(subset='TRAN_ID')
#     forex2 = MTN_TIGO.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\MTN_TIGO.csv', index=None, header=True)
    if cust_type=="All":
        pass
    else:
        MTN_TIGO=MTN_TIGO[MTN_TIGO.VISION_SBU==cust_type]  
    
    #####################################Age###########################################################
    MTN_TIGO['DATE_OF_BIRTH']=MTN_TIGO['DATE_OF_BIRTH'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# train['ID'].apply(lambda x: datetime.strptime(x, '%Y%m%d%H'))
# birthdate = datetime.datetime.strptime(birthday,'%m/%d/%Y')
    currentDate = datetime.now()
    MTN_TIGO['years']= (MTN_TIGO.DATE_OF_BIRTH.apply(lambda x:(currentDate-x) // timedelta(days=365.2425))).fillna(0).astype(int)        
#     MTN_TIGO['years']= (MTN_TIGO.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
    bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
    Labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]
    
    dF = MTN_TIGO[(MTN_TIGO.ACTIVE=='Y')&(MTN_TIGO.CUSTOMER_SEX=='M')]
    age_active_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()
    dF = MTN_TIGO[(MTN_TIGO.ACTIVE=='Y')&(MTN_TIGO.CUSTOMER_SEX=='F')]
    age_active_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()
    
    dF = MTN_TIGO[(MTN_TIGO.ACTIVE=='N')&(MTN_TIGO.CUSTOMER_SEX=='M')]
    age_inactive_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()
    dF = MTN_TIGO[(MTN_TIGO.ACTIVE=='N')&(MTN_TIGO.CUSTOMER_SEX=='F')]
    age_inactive_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()    

    dF = MTN_TIGO[(MTN_TIGO.ACTIVE=='Y')&(MTN_TIGO.CUSTOMER_SEX=='M')]
    age_active_male_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.count()
    dF = MTN_TIGO[(MTN_TIGO.ACTIVE=='Y')&(MTN_TIGO.CUSTOMER_SEX=='F')]
    age_active_female_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.count()
    
    dF = MTN_TIGO[(MTN_TIGO.ACTIVE=='N')&(MTN_TIGO.CUSTOMER_SEX=='M')]
    age_inactive_male_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.count()
    dF = MTN_TIGO[(MTN_TIGO.ACTIVE=='N')&(MTN_TIGO.CUSTOMER_SEX=='F')]
    age_inactive_female_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.count()
#     #########################################Customer trend########################################################
#     MTN_TIGO.ENTRY_DATE = pd.to_datetime(MTN_TIGO.ENTRY_DATE,errors='ignore')    
#     MTN_TIGO['ENTRY_DATE']=MTN_TIGO.ENTRY_DATE.dt.to_period('d').dt.strftime('%Y%M%D')    
#     MTN_TIGO['ENTRY_DATE']=MTN_TIGO.ENTRY_DATE.dt.day
#     MTN_TIGO['ENTRY_DATE'] = pd.PeriodIndex(MTN_TIGO.ENTRY_DATE, freq='Q')
#     MTN_TIGO['ENTRY_DATE']=pd.PeriodIndex(MTN_TIGO['ENTRY_DATE'], freq='d') 
    Active_Male= MTN_TIGO[(MTN_TIGO.CUSTOMER_SEX=='M')&(MTN_TIGO.ACTIVE=='Y')].groupby('ENTRY_DATE').FINACLE_ACCT.count()
    Active_Female=MTN_TIGO[(MTN_TIGO.CUSTOMER_SEX=='F')&(MTN_TIGO.ACTIVE=='Y')].groupby('ENTRY_DATE').FINACLE_ACCT.count()
    
    Inactive_Male= MTN_TIGO[(MTN_TIGO.CUSTOMER_SEX=='M')&(MTN_TIGO.ACTIVE=='N')].groupby('ENTRY_DATE').FINACLE_ACCT.count()
    Inactive_Female=MTN_TIGO[(MTN_TIGO.CUSTOMER_SEX=='F')&(MTN_TIGO.ACTIVE=='N')].groupby('ENTRY_DATE').FINACLE_ACCT.count()
    
    return (Inactive_Female,Inactive_Male,Active_Female,Active_Male,age_inactive_female_tr,
            age_inactive_male_tr,age_active_female_tr,age_active_male_tr,
            age_inactive_female,age_inactive_male,age_active_female,age_active_male)

    end = time.time()     
    print("one", end - start) 
    
@cache1.memoize(timeout=TIMEOUT)
def get_MTN_info(session_id,cust_type):
#     query_mtn="""
# SELECT MTNUSER.MM_TRAN.tran_id,MTNUSER.MM_REG.msisdn,MTNUSER.MM_REG.finacle_acct,MTNUSER.MM_REG.sp,
# MTNUSER.MM_REG.active,MTNUSER.MM_TRAN.tran_type,to_char(MTNUSER.MM_TRAN.entry_date,'yyyy-mm-dd')as ENTRY_DATE,
# MTNUSER.MM_TRAN.tran_amt,
# MTNUSER.MM_TRAN.cbs_status
# FROM MTNUSER.MM_REG, MTNUSER.MM_TRAN
# WHERE MTNUSER.MM_REG.msisdn= MTNUSER.MM_TRAN.msisdn
# """
# # AND MTNUSER.MM_TRAN.entry_date >=TO_DATE('2019-01-01', 'yyyy/mm/dd')    
# #     push_pull = pd.read_sql(query_mtn, con=get_connection_fiar())
# # AND EXTRACT( YEAR FROM MTNUSER.MM_TRAN.entry_date) = EXTRACT(YEAR FROM sysdate)    
#     query1 = """SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.ACCOUNTS.SECTOR_CODE,
# VISIONRW.ACCOUNTS.SCHEME_CODE
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000'
# """
    
#  to_char(C.RECEIPTDATE,'DD/MM/YYYY'),   
#     customer_details = pd.read_sql(query1, con=get_connection()) 
#     MTN_TIGO= pd.merge(push_pull, customer_details, left_on="FINACLE_ACCT", right_on="ACCOUNT_NO").drop('ACCOUNT_NO', axis=1)
    MTN_TIGO= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\push_pull.csv')    
#     MTN_TIGO= MTN_TIGO.drop_duplicates(subset='TRAN_ID')    
    if cust_type=="All":
        pass
    else:
        MTN_TIGO=MTN_TIGO[MTN_TIGO.VISION_SBU==cust_type]
        customer_details=customer_details[customer_details.VISION_SBU==cust_type]
    customer= customer_details.CUSTOMER_ID.nunique()    
    ######################VISION_SBU################################################################################
    MTN_TIGO_cat_act=MTN_TIGO.groupby('VISION_SBU').FINACLE_ACCT.count()
    MTN_TIGO_cat_inac=MTN_TIGO.groupby('CUSTOMER_SEX').FINACLE_ACCT.count() 
        
    MTN_TIGO_cat_act_am=MTN_TIGO.groupby('VISION_SBU').TRAN_AMT.sum() 
#
    MTN_TIGO_cat_act_num=MTN_TIGO.groupby('VISION_SBU').TRAN_AMT.count() 

    ###########################Active################################################################################
    MTN_TIGO_act= MTN_TIGO[MTN_TIGO.ACTIVE=='Y'].FINACLE_ACCT.nunique()
    MTN_TIGO_inact= MTN_TIGO[MTN_TIGO.ACTIVE=='N'].FINACLE_ACCT.nunique()
    
    MTN_TIGO_cat_act=MTN_TIGO.groupby('VISION_SBU').FINACLE_ACCT.nunique()
    MTN_TIGO_cat_inac=MTN_TIGO[MTN_TIGO.CUSTOMER_SEX!='NA'].groupby('CUSTOMER_SEX').FINACLE_ACCT.nunique()
    ################################################Amount&customers##############################################
    Customers_reg=MTN_TIGO.FINACLE_ACCT.nunique()
    MTN_TIGO_act= MTN_TIGO[MTN_TIGO.ACTIVE=='Y'].FINACLE_ACCT.nunique()
    male_active=MTN_TIGO[(MTN_TIGO.ACTIVE=='Y')&(MTN_TIGO.CUSTOMER_SEX=='M')].groupby('CUSTOMER_SEX').FINACLE_ACCT.nunique()
    female_active=MTN_TIGO[(MTN_TIGO.ACTIVE=='Y')&(MTN_TIGO.CUSTOMER_SEX=='F')].groupby('CUSTOMER_SEX').FINACLE_ACCT.nunique()    
    MTN_TIGO_inact= MTN_TIGO[MTN_TIGO.ACTIVE=='N'].FINACLE_ACCT.nunique()
    male_inactive=MTN_TIGO[(MTN_TIGO.ACTIVE=='N')&(MTN_TIGO.CUSTOMER_SEX=='M')].groupby('CUSTOMER_SEX').FINACLE_ACCT.nunique()
    female_inactive=MTN_TIGO[(MTN_TIGO.ACTIVE=='N')&(MTN_TIGO.CUSTOMER_SEX=='F')].groupby('CUSTOMER_SEX').FINACLE_ACCT.nunique()    
    Amount_pl= MTN_TIGO.TRAN_AMT.sum()
    Number_pl= MTN_TIGO.TRAN_AMT.count()

    ##############################################tran_type vs transaction amount#######################################################Bank_to_wallet,Wallet_to_Bank,Bank_to_wallet_num
    Bank_to_wallet= MTN_TIGO.groupby("TRAN_TYPE").TRAN_AMT.sum()
    Bank_to_wallet_num= MTN_TIGO.groupby("TRAN_TYPE").TRAN_AMT.count()
    
    MTN_TIGO_trans_cust=MTN_TIGO.groupby('TRAN_TYPE').FINACLE_ACCT.nunique()
#     sector_numb=MTN_TIGO.groupby('SECTOR_CODE').TRAN_ID.nunique()
    
    return(Bank_to_wallet_num,Bank_to_wallet,Number_pl,Amount_pl,MTN_TIGO_inact,
           MTN_TIGO_act,Customers_reg,MTN_TIGO_cat_inac,MTN_TIGO_cat_act,MTN_TIGO_inact,
           MTN_TIGO_act,MTN_TIGO_cat_act_num,MTN_TIGO_cat_act_am,MTN_TIGO_cat_inac,
           MTN_TIGO_cat_act,MTN_TIGO_trans_cust,customer,male_active,female_active,male_inactive,female_inactive)        
    
@cache1.memoize(timeout=TIMEOUT)
def get_ussd_data(session_id,cust_type):
#     query_och = """SELECT
#   ECECUSER.TXND.bank_id,
#   ECECUSER.TXND.channel_id,
#   ECECUSER.TXND.txn_entry_status,
#   ECECUSER.TXND.tran_act_entity_id AS ACCOUNT_NO,
#   ECECUSER.TXNH.total_txn_amt_in_homecrn,
#   ECECUSER.TXNH.txn_type,
#   ECECUSER.TXNH.txn_id,
#   ECECUSER.TXNH.txn_date,
#   ECECUSER.TXNH.user_input_date
# FROM
#   ECECUSER.TXNH
#   LEFT JOIN ECECUSER.TXND ON ECECUSER.TXNH.txn_id = ECECUSER.TXND.txn_id
# WHERE
#  ECECUSER.TXND.bank_id = 'RW'
#  and ECECUSER.TXNH.bank_id = 'RW' 
#  and ECECUSER.TXND.channel_id='U'
# """
# #      AND EXTRACT( YEAR FROM ECECUSER.TRANSACTION_HEADER.user_input_date) = EXTRACT(YEAR FROM sysdate)
# #  AND ECECUSER.TXNH.txn_date >=TO_DATE('2019-01-01', 'yyyy/mm/dd')

# #     OCH = pd.read_sql(query_och, con=get_connection_och())
    
#     query1 = """SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
# VISIONRW.ACCOUNTS.SCHEME_CODE
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON 
# VISIONRW.CUSTOMERS.CUSTOMER_ID = VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000' 
# """
    
#     customer_details = pd.read_sql(query1, con=get_connection())    
#     ussd= OCH.merge(customer_details, on='ACCOUNT_NO')
    ussd= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\och_channels.csv')
    ussd=ussd[ussd.CHANNEL_ID=='U']    
#     df1=OCH_details[(OCH_details.TXN_ENTRY_STATUS=='SUS')&(OCH_details.CHARGE_CRN!='RWF')]
# #     df2 = OCH_details[(OCH_details.TXN_ENTRY_STATUS=='SUC')]
#     OCH_details = pd.concat([df1,df2])
#     ussd=ussd_details.drop_duplicates(subset='TXN_ID', keep='last')
#     forex2 = OCH_details.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\OCH_details.csv', index=None, header=True)
    if cust_type=="All":
        pass
    else:
        ussd=ussd[ussd.VISION_SBU==cust_type]
    start = time.time()

    #######################################Customer age groups###########################################################
    ussd['DATE_OF_BIRTH']=ussd['DATE_OF_BIRTH'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# train['ID'].apply(lambda x: datetime.strptime(x, '%Y%m%d%H'))
# birthdate = datetime.datetime.strptime(birthday,'%m/%d/%Y')
    currentDate = datetime.now()
    ussd['years']= (ussd.DATE_OF_BIRTH.apply(lambda x:(currentDate-x) // timedelta(days=365.2425))).fillna(0).astype(int)    
#     ussd['years']= (ussd.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
    bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
    Labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]
                          #ussd
    dF = ussd[ussd.CUSTOMER_SEX=='M']
    ussd_age_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    dF = ussd[ussd.CUSTOMER_SEX=='F']
    ussd_age_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    
    dF = ussd[ussd.CUSTOMER_SEX=='M']
    ussd_age_male_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TXN_ID.count()
    dF = ussd[ussd.CUSTOMER_SEX=='F']
    ussd_age_female_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TXN_ID.count()    
    #########################################Customer trend overtime########################################################
#     ussd['USER_INPUT_DATE']=ussd.USER_INPUT_DATE.dt.to_period('Q').dt.strftime('%YQ%q')     
#     ussd['USER_INPUT_DATE']=ussd.USER_INPUT_DATE.dt.quarter
#     ussd['USER_INPUT_DATE']= pd.PeriodIndex(ussd.USER_INPUT_DATE, freq='Q')     
    ussd_Male_overtime=ussd[ussd.CUSTOMER_SEX=='M'].groupby('USER_INPUT_DATE').ACCOUNT_NO.count()
    ussd_Female_overtime=ussd[ussd.CUSTOMER_SEX=='F'].groupby('USER_INPUT_DATE').ACCOUNT_NO.count()   
    end = time.time()     
    print("one", end - start)         
    return (ussd_Female_overtime,ussd_Male_overtime,ussd_age_female_tr,ussd_age_male_tr,ussd_age_female,ussd_age_male)

@cache1.memoize(timeout=TIMEOUT)
def get_ussd_user(session_id,cust_type):
#     query_och = """SELECT
#   ECECUSER.TXND.bank_id,
#   ECECUSER.TXND.channel_id,
#   ECECUSER.TXND.txn_entry_status,
#   ECECUSER.TXND.tran_act_entity_id AS ACCOUNT_NO,
#   ECECUSER.TXNH.total_txn_amt_in_homecrn,
#   ECECUSER.TXNH.txn_type,
#   ECECUSER.TXNH.txn_id,
#   ECECUSER.TXNH.txn_date,
#   ECECUSER.TXNH.user_input_date
# FROM
#   ECECUSER.TXNH
#   LEFT JOIN ECECUSER.TXND ON ECECUSER.TXNH.txn_id = ECECUSER.TXND.txn_id
# WHERE
#  ECECUSER.TXND.bank_id = 'RW'
#  and ECECUSER.TXNH.bank_id = 'RW' 
#  and ECECUSER.TXND.channel_id='U'
# """
# #     AND EXTRACT( YEAR FROM ECECUSER.TRANSACTION_HEADER.user_input_date) = EXTRACT(YEAR FROM sysdate)
# #  AND ECECUSER.TXNH.txn_date >=T O_DATE('2019-01-01', 'yyyy/mm/dd')
# #     OCH = pd.read_sql(query_och, con=get_connection_och())
    
#     query1 = """SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.ACCOUNTS.SECTOR_CODE,
# VISIONRW.ACCOUNTS.SCHEME_CODE 
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000' 
# """
    
#     customer_details = pd.read_sql(query1, con=get_connection())    
#     ussd= OCH.merge(customer_details, on='ACCOUNT_NO')
    ussd= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\och_channels.csv')
    ussd=ussd[ussd.CHANNEL_ID=='U']    
    
#     df1=OCH_details[(OCH_details.TXN_ENTRY_STATUS=='SUS')&(OCH_details.CHARGE_CRN!='RWF')]
# #     df2 = OCH_details[(OCH_details.TXN_ENTRY_STATUS=='SUC')]
# #     OCH_details = pd.concat([df1,df2])
#     ussd=ussd_details.drop_duplicates(subset='TXN_ID', keep='last')
#     forex2 = OCH_details.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\OCH_details.csv', index=None, header=True)
    if cust_type=="All":
        pass
    else:
        ussd=ussd[ussd.VISION_SBU==cust_type]
        customer_details=customer_details[customer_details.VISION_SBU==cust_type]
    customer= customer_details.CUSTOMER_ID.nunique()   
    ussd_amt= ussd.TOTAL_TXN_AMT_IN_HOMECRN.sum() #Total amount
    ussd_numb= ussd.TXN_ID.count()# Number of transaction   
    ussd_cust= ussd.ACCOUNT_NO.nunique() # ussd
    
                         #ACCOUNT STATUS(active and inactive)
    
    ussd_cat_ACT=ussd.groupby('VISION_SBU').ACCOUNT_NO.nunique()
    ussd_cat_INACT=ussd[ussd.CUSTOMER_SEX!='NA'].groupby('CUSTOMER_SEX').ACCOUNT_NO.nunique()
                                 #AMOUNT    
#     ussd_cat_am=ussd.groupby('VISION_SBU').TOTAL_TXN_AMT_IN_HOMECRN.sum()
#                               #NUMBER OF TRANSACTIONS
#     ussd_cat_num=ussd.groupby('VISION_SBU').TXN_ID.nunique()
    
    ##############################################tran_type#######################################################
                     # Amount
    ussd_trans_amt=ussd.groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.sum()
                   #Number of transaction
    ussd_trans_numb=ussd.groupby('TXN_TYPE').TXN_ID.count() 
    
    ussd_trans_cust=ussd.groupby('TXN_TYPE').ACCOUNT_NO.nunique()
#     sector_numb=ussd.groupby('SECTOR_CODE').TXN_ID.nunique()   
    
    return (ussd_trans_numb,ussd_trans_amt,ussd_cat_INACT,ussd_cat_ACT,ussd_cust,ussd_numb,ussd_amt,ussd_trans_cust,customer)
    

@cache1.memoize(timeout=TIMEOUT)
def get_iclick_data(session_id,cust_type):
#     query_och = """SELECT
#   ECECUSER.TXND.bank_id,
#   ECECUSER.TXND.channel_id,
#   ECECUSER.TXND.txn_entry_status,
#   ECECUSER.TXND.tran_act_entity_id AS ACCOUNT_NO,
#   ECECUSER.TXNH.total_txn_amt_in_homecrn,
#   ECECUSER.TXNH.txn_type,
#   ECECUSER.TXNH.txn_id,
#   ECECUSER.TXNH.txn_date,
#   ECECUSER.TXNH.user_input_date
# FROM
#   ECECUSER.TXNH
#   LEFT JOIN ECECUSER.TXND ON ECECUSER.TXNH.txn_id = ECECUSER.TXND.txn_id
# WHERE
#  ECECUSER.TXND.bank_id = 'RW'
#  and ECECUSER.TXNH.bank_id = 'RW' 
#  and ECECUSER.TXND.channel_id='I'
# """
# #  AND ECECUSER.TXNH.txn_date >=TO_DATE('2019-01-01', 'yyyy/mm/dd')    
# #     OCH = pd.read_sql(query_och, con=get_connection_och())
# #  AND EXTRACT( YEAR FROM ECECUSER.TRANSACTION_HEADER.user_input_date) = EXTRACT(YEAR FROM sysdate)    
#     query1 = """SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
# VISIONRW.ACCOUNTS.SCHEME_CODE
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON 
# VISIONRW.CUSTOMERS.CUSTOMER_ID = VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000' 
# """
    start=time.time()
#     customer_details = pd.read_sql(query1, con=get_connection())    
#     i_click= OCH.merge(customer_details, on='ACCOUNT_NO')
    i_click= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\och_channels.csv')
    i_click=i_click[i_click.CHANNEL_ID=='I']    
    

#     i_click=iclick_details.drop_duplicates(subset='TXN_ID', keep='last')
#     forex2 = OCH_details.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\OCH_details.csv', index=None, header=True)
    if cust_type=="All":
        pass
    else:
        i_click=i_click[i_click.VISION_SBU==cust_type]
        customer_details=customer_details[customer_details.VISION_SBU==cust_type]
    customer=customer_details.CUSTOMER_ID.nunique()    
    #####################################Age###########################################################
    i_click['DATE_OF_BIRTH']=i_click['DATE_OF_BIRTH'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# train['ID'].apply(lambda x: datetime.strptime(x, '%Y%m%d%H'))
# birthdate = datetime.datetime.strptime(birthday,'%m/%d/%Y')
    currentDate = datetime.now()
    i_click['years']= (i_click.DATE_OF_BIRTH.apply(lambda x:(currentDate-x) // timedelta(days=365.2425))).fillna(0).astype(int)        
#     i_click['years']= (i_click.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
    bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
    Labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]
                              # iclick
    
    dF =i_click[i_click.CUSTOMER_SEX=='M']
    i_click_age_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    dF = i_click[i_click.CUSTOMER_SEX=='F']
    i_click_age_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    
    dF =i_click[i_click.CUSTOMER_SEX=='M']
    i_click_age_male_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TXN_ID.count()
    dF = i_click[i_click.CUSTOMER_SEX=='F']
    i_click_age_female_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TXN_ID.count()

    #########################################Customer trend overtime########################################################

     #Iclick
#     i_click['USER_INPUT_DATE']=i_click.USER_INPUT_DATE.dt.to_period('Q').dt.strftime('%YQ%q')         
#     i_click['USER_INPUT_DATE']=i_click.USER_INPUT_DATE.dt.quarter
#     i_click['USER_INPUT_DATE']= pd.PeriodIndex(i_click.USER_INPUT_DATE, freq='Q')     
    i_click_Male_overtime=i_click[i_click.CUSTOMER_SEX=='M'].groupby('USER_INPUT_DATE').ACCOUNT_NO.count()
    i_click_Female_overtime=i_click[i_click.CUSTOMER_SEX=='F'].groupby('USER_INPUT_DATE').ACCOUNT_NO.count()
    
    end = time.time()     
    print("onec", end - start) 
            
    return (i_click_Female_overtime,i_click_Male_overtime,i_click_age_female_tr,
            i_click_age_male_tr,i_click_age_female,i_click_age_male)

@cache1.memoize(timeout=TIMEOUT)
def get_iclick_user(session_id,cust_type):
#     query_och = """
#     SELECT
#   ECECUSER.TXND.bank_id,
#   ECECUSER.TXND.channel_id,
#   ECECUSER.TXND.txn_entry_status,
#   ECECUSER.TXND.tran_act_entity_id AS ACCOUNT_NO,
#   ECECUSER.TXNH.total_txn_amt_in_homecrn,
#   ECECUSER.TXNH.txn_type,
#   ECECUSER.TXNH.txn_id,
#   ECECUSER.TXNH.txn_date,
#   ECECUSER.TXNH.user_input_date
# FROM
#   ECECUSER.TXNH
#   LEFT JOIN ECECUSER.TXND ON ECECUSER.TXNH.txn_id = ECECUSER.TXND.txn_id
# WHERE
#  ECECUSER.TXND.bank_id = 'RW'
#  and ECECUSER.TXNH.bank_id = 'RW' 
#  and ECECUSER.TXND.channel_id='I'
# """
# #  AND ECECUSER.TXNH.txn_date >=TO_DATE('2019-01-01', 'yyyy/mm/dd')     
# #     OCH = pd.read_sql(query_och, con=get_connection_och())
# #  AND EXTRACT( YEAR FROM ECECUSER.TRANSACTION_HEADER.user_input_date) = EXTRACT(YEAR FROM sysdate)    
#     query1 = """
#     SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.ACCOUNTS.SECTOR_CODE,
# VISIONRW.ACCOUNTS.SCHEME_CODE
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000'
# """
    start=time.time()
#     customer_details = pd.read_sql(query1, con=get_connection())    
#     i_click= OCH.merge(customer_details, on='ACCOUNT_NO') 
    df= pd.read_csv(r'C:\Users\Administrator\Desktop\newdata\och_channels.csv')
    i_click=df[df.CHANNEL_ID=='I']    

#     i_click=iclick_details.drop_duplicates(subset='TXN_ID', keep='last')
#     forex2 = OCH_details.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\OCH_details.csv', index=None, header=True)
    if cust_type=="All":
        pass
    else:
        i_click=i_click[i_click.VISION_SBU==cust_type]
        customer_details=customer_details[customer_details.VISION_SBU==cust_type]
    customer=customer_details.CUSTOMER_ID.nunique()                          #ACCOUNT STATUS(active and inactive)
    
    i_click_cat_ACT=i_click.groupby('VISION_SBU').ACCOUNT_NO.nunique()
    i_click_cat_INACT=i_click[i_click.CUSTOMER_SEX!='NA'].groupby('CUSTOMER_SEX').ACCOUNT_NO.nunique()
       
                                  #AMOUNT
    
    ################################################Amount&customers##############################################    
    i_click_amt= i_click.TOTAL_TXN_AMT_IN_HOMECRN.sum() #Total amount
    i_click_numb= i_click.TXN_ID.count()# Number of transaction
    
    iclick_cust= i_click.ACCOUNT_NO.nunique() # iclick number of customers users.

    ##############################################tran_type#######################################################
                     # Amount
    i_click_trans_amt=i_click.groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.sum() # Iclick transaction amount

                   #Number of transaction
    i_click_trans_numb=i_click.groupby('TXN_TYPE').TXN_ID.count() #iclick transaction id.
                                                                            
    i_click_trans_cust=i_click.groupby('TXN_TYPE').ACCOUNT_NO.nunique()
#     sector_numb=i_click.groupby('SECTOR_CODE').TXN_ID.nunique()     
    
    return (i_click_trans_numb,i_click_trans_amt,iclick_cust,i_click_numb,
           i_click_amt,i_click_cat_INACT,i_click_cat_ACT,i_click_trans_cust,customer) 

@cache1.memoize(timeout=TIMEOUT)
def get_mobile_data(session_id,cust_type):
#     query_och = """
#     SELECT
#   ECECUSER.TXND.bank_id,
#   ECECUSER.TXND.channel_id,
#   ECECUSER.TXND.txn_entry_status,
#   ECECUSER.TXND.tran_act_entity_id AS ACCOUNT_NO,
#   ECECUSER.TXNH.total_txn_amt_in_homecrn,
#   ECECUSER.TXNH.txn_type,
#   ECECUSER.TXNH.txn_id,
#   ECECUSER.TXNH.txn_date,
#   ECECUSER.TXNH.user_input_date
# FROM
#   ECECUSER.TXNH
#   LEFT JOIN ECECUSER.TXND ON ECECUSER.TXNH.txn_id = ECECUSER.TXND.txn_id
# WHERE
#  ECECUSER.TXND.bank_id = 'RW'
#  and ECECUSER.TXNH.bank_id = 'RW' 
#  and ECECUSER.TXND.channel_id='G'
# """
# #  AND ECECUSER.TXNH.txn_date >=TO_DATE('2019-01-01', 'yyyy/mm/dd')     
# #     OCH = pd.read_sql(query_och, con=get_connection_och())
# #  AND EXTRACT( YEAR FROM ECECUSER.TRANSACTION_HEADER.user_input_date) = EXTRACT(YEAR FROM sysdate)    
#     query1 = """
#     SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
# VISIONRW.ACCOUNTS.SCHEME_CODE, 
# VISIONRW.ACCOUNTS.ACCOUNT_STATUS
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON 
# VISIONRW.CUSTOMERS.CUSTOMER_ID = VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000'
# """
    
#     customer_details = pd.read_sql(query1, con=get_connection())    
#     Mobile_APP= OCH.merge(customer_details, on='ACCOUNT_NO') 
    Mobile_APP= pd.read_csv(r'C:\Users\Administrator\Desktop\newdata\och_channels.csv')
    Mobile_APP=Mobile_APP[Mobile_APP.CHANNEL_ID=='G']    

#     df1=OCH_details[(OCH_details.TXN_ENTRY_STATUS=='SUS')&(OCH_details.CHARGE_CRN!='RWF')]
# #     df2 = OCH_details[(OCH_details.TXN_ENTRY_STATUS=='SUC')]
#     OCH_details = pd.concat([df1,df2])
#     Mobile_APP=mobile_details.drop_duplicates(subset='TXN_ID', keep='last')
#     forex2 = OCH_details.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\OCH_details.csv', index=None, header=True)
    if cust_type=="All":
        pass
    else:
        Mobile_APP=Mobile_APP[Mobile_APP.VISION_SBU==cust_type]
  
    #####################################Age########################################################################
    Mobile_APP['DATE_OF_BIRTH']=Mobile_APP['DATE_OF_BIRTH'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# train['ID'].apply(lambda x: datetime.strptime(x, '%Y%m%d%H'))
# birthdate = datetime.datetime.strptime(birthday,'%m/%d/%Y')
    currentDate = datetime.now()
    Mobile_APP['years']= (Mobile_APP.DATE_OF_BIRTH.apply(lambda x:(currentDate-x) // timedelta(days=365.2425))).fillna(0).astype(int)            
#     Mobile_APP['years']= (Mobile_APP.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
    bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
    Labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]

    dF = Mobile_APP[Mobile_APP.CUSTOMER_SEX=='M']
    Mobile_APP_age_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    dF = Mobile_APP[Mobile_APP.CUSTOMER_SEX=='F']
    Mobile_APP_age_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TOTAL_TXN_AMT_IN_HOMECRN.sum()
    
    dF = Mobile_APP[Mobile_APP.CUSTOMER_SEX=='M']
    Mobile_APP_age_male_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TXN_ID.count()
    dF = Mobile_APP[Mobile_APP.CUSTOMER_SEX=='F']
    Mobile_APP_age_female_tr = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TXN_ID.count()    

    #########################################Customer trend overtime########################################################
    ########################################################################################################################
    ### Mobile_APP=Mobile_APP.USER_INPUT_DATE.dt.to_period('Q').dt.strftime('%YM%m')     
#     Mobile_APP['USER_INPUT_DATE']=Mobile_APP.USER_INPUT_DATE.dt.to_period('Q').dt.strftime('%YQ%q')    
#     Mobile_APP['USER_INPUT_DATE']=Mobile_APP.USER_INPUT_DATE.dt.quarter  
#     Mobile_APP['USER_INPUT_DATE']= pd.PeriodIndex(Mobile_APP.USER_INPUT_DATE, freq='Q')     
    Mobile_Male_overtime=Mobile_APP[Mobile_APP.CUSTOMER_SEX=='M'].groupby('USER_INPUT_DATE').ACCOUNT_NO.count()
    Mobile_Female_overtime=Mobile_APP[Mobile_APP.CUSTOMER_SEX=='F'].groupby('USER_INPUT_DATE').ACCOUNT_NO.count()    
        
    return (Mobile_Female_overtime,Mobile_Male_overtime,Mobile_APP_age_female_tr,
            Mobile_APP_age_male_tr,Mobile_APP_age_female,Mobile_APP_age_male)

@cache1.memoize(timeout=TIMEOUT)
def get_mobile_user(session_id,cust_type):
#     query_och = """SELECT
#   ECECUSER.TXND.bank_id,
#   ECECUSER.TXND.channel_id,
#   ECECUSER.TXND.txn_entry_status,
#   ECECUSER.TXND.tran_act_entity_id AS ACCOUNT_NO,
#   ECECUSER.TXNH.total_txn_amt_in_homecrn,
#   ECECUSER.TXNH.txn_type,
#   ECECUSER.TXNH.txn_id,
#   ECECUSER.TXNH.txn_date,
#   ECECUSER.TXNH.user_input_date
# FROM
#   ECECUSER.TXNH
#   LEFT JOIN ECECUSER.TXND ON ECECUSER.TXNH.txn_id = ECECUSER.TXND.txn_id
# WHERE
#  ECECUSER.TXND.bank_id = 'RW'
#  and ECECUSER.TXNH.bank_id = 'RW' 
#  and ECECUSER.TXND.channel_id='G'
# """
# # AND ECECUSER.TRANSACTION_HEADER.txn_date >=TO_DATE('2019-01-01', 'yyyy/mm/dd')    
# #     OCH = pd.read_sql(query_och, con=get_connection_och())
# #  AND EXTRACT( YEAR FROM ECECUSER.TRANSACTION_HEADER.user_input_date) = EXTRACT(YEAR FROM sysdate)    
#     query1 = """SELECT VISIONRW.CUSTOMERS.CUSTOMER_ID,
# VISIONRW.ACCOUNTS.ACCOUNT_NO,
# VISIONRW.CUSTOMERS.CUSTOMER_SEX,
# VISIONRW.ACCOUNTS.VISION_SBU,
# VISIONRW.ACCOUNTS.SECTOR_CODE,
# VISIONRW.ACCOUNTS.SCHEME_CODE 
# FROM VISIONRW.CUSTOMERS
# LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON 
# VISIONRW.CUSTOMERS.CUSTOMER_ID = VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID
# LEFT JOIN VISIONRW.ACCOUNTS ON
# VISIONRW.ACCOUNTS.CUSTOMER_ID = VISIONRW.CUSTOMERS.CUSTOMER_ID
# WHERE VISIONRW.ACCOUNTS.SCHEME_CODE NOT IN ( 'CAF08', 'CAL08', 'LAL26' )
# and VISIONRW.CUSTOMERS.CUSTOMER_ID<>'D000' 
# """
    
#     customer_details = pd.read_sql(query1, con=get_connection())    
#     Mobile_APP= OCH.merge(customer_details, on='ACCOUNT_NO')
    Mobile_APP= pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\och_channels.csv')
    Mobile_APP=Mobile_APP[Mobile_APP.CHANNEL_ID=='G']        
#     df1=OCH_details[(OCH_details.TXN_ENTRY_STATUS=='SUS')&(OCH_details.CHARGE_CRN!='RWF')]
# #     df2 = OCH_details[(OCH_details.TXN_ENTRY_STATUS=='SUC')]
#     OCH_details = pd.concat([df1,df2])
#     Mobile_APP=mobile_details.drop_duplicates(subset='TXN_ID', keep='last')
#     forex2 = OCH_details.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\OCH_details.csv', index=None, header=True)
    if cust_type=="All":
        pass
    else: 
        Mobile_APP=Mobile_APP[Mobile_APP.VISION_SBU==cust_type]
        customer_details=customer_details[customer_details.VISION_SBU==cust_type]
    customer=customer_details.CUSTOMER_ID.nunique()    
    Mobile_APP_cat_ACT=Mobile_APP.groupby('VISION_SBU').ACCOUNT_NO.nunique()
    Mobile_APP_cat_INACT=Mobile_APP[Mobile_APP.CUSTOMER_SEX!='NA'].groupby('CUSTOMER_SEX').ACCOUNT_NO.nunique()
                                 #AMOUNT

    Mobile_APP_cat_am=Mobile_APP.groupby('VISION_SBU').TOTAL_TXN_AMT_IN_HOMECRN.sum()

                              #NUMBER OF TRANSACTIONS
    
    ################################################Amount&customers##############################################       
    Mobile_APP_amt= Mobile_APP.TOTAL_TXN_AMT_IN_HOMECRN.sum() #Total amount
    Mobile_APP_numb= Mobile_APP.TXN_ID.count()# Number of transaction 
    Mobile_APP_cust= Mobile_APP.ACCOUNT_NO.nunique() # Mobile app

    ##############################################tran_type#######################################################
                     # Amount
    Mobile_APP_trans_amt=Mobile_APP.groupby('TXN_TYPE').TOTAL_TXN_AMT_IN_HOMECRN.sum()

                   #Number of transaction
    Mobile_APP_trans_numb=Mobile_APP.groupby('TXN_TYPE').TXN_ID.count()
    
    Mobile_APP_trans_cust=Mobile_APP.groupby('TXN_TYPE').ACCOUNT_NO.nunique()
    
#     sector=Mobile_APP.groupby('SECTOR_CODE').TOTAL_TXN_AMT_IN_HOMECRN.sum()
#     sector_numb=Mobile_APP.groupby('SECTOR_CODE').TXN_ID.nunique()     
    
    return (Mobile_APP_trans_numb,Mobile_APP_trans_amt,Mobile_APP_cust,
            Mobile_APP_numb,Mobile_APP_amt,Mobile_APP_cat_am,
            Mobile_APP_cat_INACT,Mobile_APP_cat_ACT,Mobile_APP_trans_cust,customer)  

#################################################CARDS DETAILS AND TRANSACTIONS#################################################################################################################################
@cache1.memoize(timeout=TIMEOUT)
def get_och_registered(session_id):
    och=pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\och_registered.csv')
    users=och.groupby('SERVICE').NUMBER.sum()
    return users
@cache1.memoize(timeout=TIMEOUT)
def get_cards_details(session_id,card=None):
#     query = """SELECT PAN, INTERNALACCOUNTNO,CARDPRODUCT,CARDONLINESTATUS,CARDBRANCHNAME,
#                CARDTWCMSSTATE,PRIMARYSUPPLEMENTARYFLAG,ACCOUNTBALANCE,
#                CREATEDATE,MODIFYDATE,BUSINESS_DATE FROM VISIONRW.FINACLE_FCLIENTS
#                WHERE CARDPRODUCT NOT IN ('IM Customer','IM Merchant','IM Agent','IM Super','IM Business')
#                """
#     cards_details = pd.read_sql(query, con=get_connection()) 
#     cards_csv = cards_details.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\card_details.csv', index=None, header=True)
    cards_details=pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\card_details.csv')
    cards_details=cards_details.drop_duplicates(subset='PAN')
#     cards_details= cards_details.set_index('BUSINESS_DATE').loc[start:end, ['CARDPRODUCT','CARDONLINESTATUS','CARDTWCMSSTATE','PRIMARYSUPPLEMENTARYFLAG','CARDBRANCHNAME','PAN','INTERNALACCOUNTNO','MODIFYDATE']]    
    
    if card is None:
        pass
    else:
        cards_details=cards_details[cards_details.CARDPRODUCT==card]    
    ####################Customers and cards number####################
    cards_numb= cards_details.PAN.nunique()
    customers= cards_details.INTERNALACCOUNTNO.nunique()
    card_product=cards_details.CARDPRODUCT.unique()
    #########################status#############################################################################
    card_status= cards_details.groupby('CARDONLINESTATUS').PAN.nunique()
    card_branch= cards_details.groupby('CARDBRANCHNAME').PAN.nunique()
    card_primary_supp= cards_details.groupby('PRIMARYSUPPLEMENTARYFLAG').PAN.nunique()
    
    Open_card_branch=cards_details[cards_details.CARDONLINESTATUS=='Opened'].groupby('CARDBRANCHNAME').PAN.nunique()
    decl_card_branch=cards_details[cards_details.CARDONLINESTATUS=='Declared'].groupby('CARDBRANCHNAME').PAN.nunique()
    clos_card_branch=cards_details[cards_details.CARDONLINESTATUS=='Closed'].groupby('CARDBRANCHNAME').PAN.nunique()
    Lost_card_branch=cards_details[cards_details.CARDONLINESTATUS=='Lost'].groupby('CARDBRANCHNAME').PAN.nunique()
    Stol_card_branch=cards_details[cards_details.CARDONLINESTATUS=='Stolen'].groupby('CARDBRANCHNAME').PAN.nunique()
    compr_card_branch=cards_details[cards_details.CARDONLINESTATUS=='Compromised'].groupby('CARDBRANCHNAME').PAN.nunique()  
    
    classic_deb_branch=cards_details[cards_details.CARDPRODUCT=='Visa Classic Debit'].groupby('CARDBRANCHNAME').PAN.nunique()
    classic_pre_branch=cards_details[cards_details.CARDPRODUCT=='Visa Classic Prepaid'].groupby('CARDBRANCHNAME').PAN.nunique()
    gold_cre_branch=cards_details[cards_details.CARDPRODUCT=='Visa Gold Credit'].groupby('CARDBRANCHNAME').PAN.nunique()
    gold_deb_branch=cards_details[cards_details.CARDPRODUCT=='Visa Gold Debit'].groupby('CARDBRANCHNAME').PAN.nunique()
    
#     classic_deb_status=cards_details[cards_details.CARDPRODUCT=='Visa Classic Debit'].groupby('CARDONLINESTATUS').PAN.count()
#     classic_pre_status=cards_details[cards_details.CARDPRODUCT=='Visa Classic Prepaid'].groupby('CARDONLINESTATUS').PAN.count()
#     gold_cre_status=cards_details[cards_details.CARDPRODUCT=='Visa Gold Credit'].groupby('CARDONLINESTATUS').PAN.count()
#     gold_deb_status=cards_details[cards_details.CARDPRODUCT=='Visa Gold Debit'].groupby('CARDONLINESTATUS').PAN.count() 

######################################Card types##############################################################################    
    Open_card_status=cards_details[cards_details.CARDONLINESTATUS=='Opened'].groupby('CARDPRODUCT').PAN.nunique()
    decl_card_status=cards_details[cards_details.CARDONLINESTATUS=='Declared'].groupby('CARDPRODUCT').PAN.nunique()
    clos_card_status=cards_details[cards_details.CARDONLINESTATUS=='Closed'].groupby('CARDPRODUCT').PAN.nunique()
    Lost_card_status=cards_details[cards_details.CARDONLINESTATUS=='Lost'].groupby('CARDPRODUCT').PAN.nunique()
    Stol_card_status=cards_details[cards_details.CARDONLINESTATUS=='Stolen'].groupby('CARDPRODUCT').PAN.nunique()
    compr_card_status=cards_details[cards_details.CARDONLINESTATUS=='Compromised'].groupby('CARDPRODUCT').PAN.nunique()
    
##############################################################################################################################
    Card_type=cards_details.groupby('CARDPRODUCT').PAN.nunique()
###############################################################################################################################    
    Open_card=cards_details[cards_details.CARDONLINESTATUS=='Opened'].groupby('MODIFYDATE').PAN.nunique()
    decl_card=cards_details[cards_details.CARDONLINESTATUS=='Declared'].groupby('MODIFYDATE').PAN.nunique()
    clos_card=cards_details[cards_details.CARDONLINESTATUS=='Closed'].groupby('MODIFYDATE').PAN.nunique()
    Lost_card=cards_details[cards_details.CARDONLINESTATUS=='Lost'].groupby('MODIFYDATE').PAN.nunique()
    Stol_card=cards_details[cards_details.CARDONLINESTATUS=='Stolen'].groupby('MODIFYDATE').PAN.nunique()
    compr_card=cards_details[cards_details.CARDONLINESTATUS=='Compromised'].groupby('MODIFYDATE').PAN.nunique()
    
    primary=cards_details[cards_details.PRIMARYSUPPLEMENTARYFLAG=='P'].groupby('MODIFYDATE').PAN.nunique()
    supply=cards_details[cards_details.PRIMARYSUPPLEMENTARYFLAG=='S'].groupby('MODIFYDATE').PAN.nunique()
    
    classic_deb_state=cards_details[cards_details.CARDPRODUCT=='Visa Classic Debit'].groupby('CARDTWCMSSTATE').PAN.nunique()
    classic_pre_state=cards_details[cards_details.CARDPRODUCT=='Visa Classic Prepaid'].groupby('CARDTWCMSSTATE').PAN.nunique()
    gold_cre_state=cards_details[cards_details.CARDPRODUCT=='Visa Gold Credit'].groupby('CARDTWCMSSTATE').PAN.nunique()
    gold_deb_state=cards_details[cards_details.CARDPRODUCT=='Visa Gold Debit'].groupby('CARDTWCMSSTATE').PAN.nunique()
    
    return (card_primary_supp,card_branch,card_status,customers,cards_numb,
            card_product,supply,primary,compr_card,Stol_card,Lost_card,clos_card,decl_card,Open_card,
            Open_card_status,decl_card_status,clos_card_status,Lost_card_status,Stol_card_status,compr_card_status,
            Open_card_branch,decl_card_branch,clos_card_branch,Lost_card_branch,Stol_card_branch,compr_card_branch,
            classic_deb_branch,classic_pre_branch,gold_cre_branch,gold_deb_branch,
            classic_deb_state,classic_pre_state,gold_cre_state,gold_deb_state,Card_type)  

@cache1.memoize(timeout=TIMEOUT)
def get_cards_transactions(session_id,start_date, end_date):
#     query = """SELECT DISTINCT(VISIONRW.TRANS_COUNT_FEED_STG.TRAN_ID),
#     VISIONRW.TRANS_COUNT_FEED_STG.CUSTOMER_ID,
#     VISIONRW.TRANS_COUNT_FEED_STG.TRANSACTION_CHANNEL, 
#     VISIONRW.TRANS_COUNT_FEED_STG.TRAN_AMT,
#     VISIONRW.TRANS_COUNT_FEED_STG.TRAN_DATE, 
#     VISIONRW.CUSTOMER_EXTRAS.DATE_OF_BIRTH,
#     VISIONRW.CUSTOMERs_DLY.CUSTOMER_SEX,
#     VISIONRW.CUSTOMERs_DLY.VISION_SBU
#     FROM VISIONRW.TRANS_COUNT_FEED_STG
#     LEFT JOIN VISIONRW.CUSTOMER_EXTRAS ON
#     VISIONRW.TRANS_COUNT_FEED_STG.CUSTOMER_ID =VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID 
#     LEFT JOIN VISIONRW.CUSTOMERS_DLY ON
#     VISIONRW.CUSTOMER_EXTRAS.CUSTOMER_ID = VISIONRW.CUSTOMERS_DLY.CUSTOMER_ID 
#     WHERE VISIONRW.TRANS_COUNT_FEED_STG.TRANSACTION_CHANNEL IN ('ATM','POS')
#     """

#     card_tran = pd.read_sql(query, con=get_connection())
    
    card_tran=pd.read_csv(r'C:\Users\Administrator\Downloads\imdas_new\Data_im\atm.csv') 
    card_tran=card_tran[(card_tran.TRAN_DATE>=start_date)&(card_tran.TRAN_DATE<=end_date)]
#     card_tran_csv = card_tran.to_csv(r'C:\Users\clement nshimiyima\Desktop\dt\card_tran.csv', index=None, header=True)
    card_tran=card_tran.drop_duplicates(subset='TRAN_ID')
#     card_tran= card_tran.set_index('TRAN_DATE').loc[start:end, ['TRANSACTION_CHANNEL','TRAN_AMT','DATE_OF_BIRTH','CUSTOMER_SEX','VISION_SBU','TRAN_ID']]    

#################################transaction overtime#################################################################
#     card_tran['DATE_OF_BIRTH']=pd.to_datetime(card_tran.DATE_OF_BIRTH, errors='coerce')
#     card_tran['DATE_OF_BIRTH']=card_tran['DATE_OF_BIRTH'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
#     card_tran['DATE_OF_BIRTH']=card_tran['DATE_OF_BIRTH'].astype(str)   
#     card_tran['TRAN_DATE']=card_tran.TRAN_DATE.dt.to_period('m').dt.strftime('%Y%b')
#     card_tran['TRAN_DATE']=card_tran.TRAN_DATE.dt.quarter
#     card_tran['TRAN_DATE']= pd.PeriodIndex(card_tran.TRAN_DATE, freq='Q')     
    atm_male_overtime= card_tran[(card_tran.TRANSACTION_CHANNEL=='ATM')&(card_tran.CUSTOMER_SEX=='M')].groupby('TRAN_DATE').CUSTOMER_ID.count()
    
    atm_female_overtime= card_tran[(card_tran.TRANSACTION_CHANNEL=='ATM')&(card_tran.CUSTOMER_SEX=='F')].groupby('TRAN_DATE').CUSTOMER_ID.count()
    
    pos_male_overtime= card_tran[(card_tran.TRANSACTION_CHANNEL=='POS')&(card_tran.CUSTOMER_SEX=='M')].groupby('TRAN_DATE').CUSTOMER_ID.count()
    
    pos_female_overtime= card_tran[(card_tran.TRANSACTION_CHANNEL=='POS')&(card_tran.CUSTOMER_SEX=='F')].groupby('TRAN_DATE').CUSTOMER_ID.count()
##############################################Total Transactions#######################################################
    POS_tran=card_tran[card_tran.TRANSACTION_CHANNEL=='POS'].TRAN_ID.count()
    POS_AM=card_tran[card_tran.TRANSACTION_CHANNEL=='POS'].TRAN_AMT.sum()
    ATM_tran=card_tran[card_tran.TRANSACTION_CHANNEL=='ATM'].TRAN_ID.count()
    ATM_AM=card_tran[card_tran.TRANSACTION_CHANNEL=='ATM'].TRAN_AMT.sum()
    POS_trend=card_tran[card_tran.TRANSACTION_CHANNEL=='POS'].groupby('TRAN_DATE').TRAN_ID.count()
    ATM_trend=card_tran[card_tran.TRANSACTION_CHANNEL=='ATM'].groupby('TRAN_DATE').TRAN_ID.count()   
#############################################CUSTOMER AGE#################################################################
#     dt.today().strftime('%Y-%m-%d')
#     card_tran['years']= (card_tran.DATE_OF_BIRTH.apply(lambda x:(dt.today()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
#     bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
#     Labels = ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-60",">60"]
    
#     dF = card_tran[(card_tran.CUSTOMER_SEX=='M')&(card_tran.TRANSACTION_CHANNEL=='ATM')]
#     atm_age_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()
#     dF = card_tran[(card_tran.CUSTOMER_SEX=='F')&(card_tran.TRANSACTION_CHANNEL=='ATM')]
#     atm_age_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()

#     dF = card_tran[(card_tran.CUSTOMER_SEX=='M')&(card_tran.TRANSACTION_CHANNEL=='ATM')]
#     atm_age_male_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_ID.count()
#     dF = card_tran[(card_tran.CUSTOMER_SEX=='F')&(card_tran.TRANSACTION_CHANNEL=='ATM')]
#     atm_age_female_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_ID.count()
    
#     dF = card_tran[(card_tran.CUSTOMER_SEX=='M')&(card_tran.TRANSACTION_CHANNEL=='POS')]
#     pos_age_male = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()
#     dF = card_tran[(card_tran.CUSTOMER_SEX=='F')&(card_tran.TRANSACTION_CHANNEL=='POS')]
#     pos_age_female = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_AMT.sum()

#     dF = card_tran[(card_tran.CUSTOMER_SEX=='M')&(card_tran.TRANSACTION_CHANNEL=='POS')]
#     pos_age_male_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_ID.count()
#     dF = card_tran[(card_tran.CUSTOMER_SEX=='F')&(card_tran.TRANSACTION_CHANNEL=='POS')]
#     pos_age_female_num = dF.groupby(pd.cut(dF['years'], bins, include_lowest=True, right = False, labels=Labels)).TRAN_ID.count()
    
    return (pos_female_overtime,pos_male_overtime,atm_female_overtime,
            atm_male_overtime,POS_tran,POS_AM,ATM_tran,ATM_AM,POS_trend,ATM_trend)  

# @cache1.memoize(timeout=TIMEOUT)
# def get_p&l(session_id, cust_type='All'):
#     query="""
#     with dates as (
#     --  select LPAD(extract(day from to_date('20200131','yyyymmdd')), 2, '0') as day,TO_CHAR(to_date('20200131','yyyymmdd'), 'YYYYMM') as year_month from dual
#     select LPAD(extract(day from to_date(sysdate-1)), 2, '0') as day,TO_CHAR(to_date(sysdate-1), 'YYYYMM') as year_month , TO_CHAR(to_date(sysdate-1), 'MM') as current_month,
#     TO_CHAR(to_date(sysdate-1), 'YYYY') as current_year from dual
#     ),

#     day_balance as (
#     select year_month,country,le_book,Sequence_FD,balance as balance,column_,dr_cr_bal_ind,bal_type
#         from VISIONRW.Fin_Dly_Balances 
#         unpivot ( 
#             balance for column_
#             in (balance_01, balance_02, balance_03, balance_04, balance_05, balance_06, balance_07, balance_08, balance_09, balance_10, balance_11, balance_12, balance_13, balance_14, balance_15, balance_16, balance_17, balance_18, balance_19, balance_20, balance_21, balance_22, balance_23, balance_24, balance_25, balance_26, balance_27, balance_28, balance_29, balance_30, balance_31)
#             ) balance_unpivot 

#            where year_month between '201912' and  (select year_month from dates fetch next 1 row only) 
#     ),

#     default_pl as (SELECT
#         fin_dly_headers.year_month             AS year_month,
#         frl_lines_pl.frl_attribute_04          AS frl_attribute_04,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 4
#                 AND frl_lines_pl.frl_attribute_04 = frl_attribute
#         ) ) AS frl_att_04_description,
#         frl_lines_pl.frl_attribute_02          AS frl_attribute_02,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 2
#                 AND frl_lines_pl.frl_attribute_02 = frl_attribute
#         ) ) AS frl_att_02_description,
#         frl_lines_pl.frl_attribute_06          AS frl_attribute_06,
#         ( (
#             SELECT
#                 frl_attribute_description
#             FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 6
#                 AND frl_lines_pl.frl_attribute_06 = frl_attribute
#         ) ) AS frl_att_06_description,
#         frl_lines_bs.frl_attribute_01          AS frl_attribute_01,
#         ( (
#             SELECT
#                 frl_attribute_description
#            FROM
#                 visionrw.frl_attributes
#             WHERE
#                 frl_attribute_level = 1
#                 AND frl_lines_bs.frl_attribute_01 = frl_attribute
#         ) ) AS frl_att_01_description,
#         product_expanded.product_description   AS product_description,
#         frl_lines_bs.source_type               AS source_type,
#         fin_dly_headers.office_account         AS office_account,
#         ouc_expanded.ouc_description           AS ouc_description,
#         fin_dly_headers.customer_id            AS customer_id,
#         fin_dly_headers.contract_id            AS contract_id,
#         customers_dly_expanded.customer_name   AS customer_name,
#         fin_dly_headers.bs_gl                  AS bs_gl,
#         fin_dly_headers.pl_gl                  AS pl_gl,
#         fin_dly_headers.vision_ouc             AS vision_ouc,
#         fin_dly_headers.vision_sbu             AS vision_sbu,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 3
#                 AND alpha_sub_tab = fin_dly_headers.vision_sbu
#         ) AS vision_sbu_desc,
#         fin_dly_headers.currency               AS currency,
#             accounts_dly.ACCOUNT_TYPE               AS ACCOUNT_TYPE,    
#             accounts_dly.scheme_code               AS scheme_code,
#         (
#             SELECT
#                alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 171
#                 AND alpha_sub_tab = accounts_dly.scheme_code
#         ) AS scheme_code_desc,
#         accounts_dly.sector_code               AS sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 59
#                 AND alpha_sub_tab = accounts_dly.sector_code
#         ) AS sector_code_desc,
#         accounts_dly.sub_sector_code           AS sub_sector_code,
#         (
#             SELECT
#                 alpha_subtab_description
#             FROM
#                 visionrw.alpha_sub_tab
#             WHERE
#                 alpha_tab = 60
#                 AND alpha_sub_tab = accounts_dly.sub_sector_code
#         ) AS sub_sector_code_desc,
#         fin_dly_headers.record_type            AS record_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 22
#                 AND num_sub_tab = fin_dly_headers.record_type
#         ) AS record_type_desc,
#         fin_dly_balances.bal_type              AS bal_type,
#         (
#             SELECT
#                 num_subtab_description
#             FROM
#                 visionrw.num_sub_tab
#             WHERE
#                 num_tab = 24
#                 AND num_sub_tab = fin_dly_balances.bal_type
#         ) AS bal_type_desc,
#         to_number(SUM(fin_dly_balances.balance)) AS balance

#     FROM
#         visionrw.fin_dly_headers             fin_dly_headers
#         JOIN day_balance            fin_dly_balances ON fin_dly_headers.country = fin_dly_balances.country
#                                                   AND fin_dly_headers.le_book = fin_dly_balances.le_book
#                                                   AND fin_dly_headers.year_month = fin_dly_balances.year_month
#                                                   AND fin_dly_headers.sequence_fd = fin_dly_balances.sequence_fd
#                                                   AND fin_dly_headers.record_type != 9999
#             LEFT JOIN visionrw.accounts_dly_view           accounts_dly ON fin_dly_headers.country = accounts_dly.country
#                                                     AND fin_dly_headers.le_book = accounts_dly.le_book
#                                                     AND (
#             CASE
#                 WHEN fin_dly_headers.contract_id = '0' THEN
#                     fin_dly_headers.office_account
#                 ELSE
#                     fin_dly_headers.contract_id
#             END
#         ) = accounts_dly.account_no
#                                                     AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.ouc_expanded                ouc_expanded ON ouc_expanded.vision_ouc = fin_dly_headers.vision_ouc
#                                                AND fin_dly_headers.record_type != 9999
#         LEFT JOIN visionrw.vw_customers_dly_expanded   customers_dly_expanded ON customers_dly_expanded.country = fin_dly_headers.country
#                                                                       AND customers_dly_expanded.le_book = fin_dly_headers.le_book
#                                                                       AND customers_dly_expanded.customer_id = fin_dly_headers.customer_id
#                                                                       AND fin_dly_headers.record_type != 9999
#         JOIN visionrw.fin_dly_mappings            fin_dly_mappings ON fin_dly_balances.country = fin_dly_mappings.country
#                                                   AND fin_dly_balances.le_book = fin_dly_mappings.le_book
#                                                   AND fin_dly_balances.year_month = fin_dly_mappings.year_month
#                                                   AND fin_dly_balances.sequence_fd = fin_dly_mappings.sequence_fd
#                                                   AND fin_dly_balances.dr_cr_bal_ind = fin_dly_mappings.dr_cr_bal_ind
#         JOIN visionrw.product_expanded            product_expanded ON product_expanded.product = fin_dly_mappings.product
#         JOIN visionrw.frl_lines                   frl_lines_bs ON fin_dly_mappings.frl_line_bs = frl_lines_bs.frl_line
#         JOIN visionrw.frl_lines                   frl_lines_pl ON fin_dly_mappings.frl_line_pl = frl_lines_pl.frl_line
#     WHERE
#         fin_dly_headers.year_month between '201912' and  (select year_month from dates fetch next 1 row only)
#         AND frl_lines_bs.source_type = '0'
#         AND fin_dly_headers.record_type NOT IN (
#             '9999'
#         )
#         AND fin_dly_balances.bal_type = '54'
#     GROUP BY
#         fin_dly_headers.year_month,
#         frl_lines_pl.frl_attribute_04,
#         frl_lines_pl.frl_attribute_02,
#         frl_lines_pl.frl_attribute_06,
#         frl_lines_bs.frl_attribute_01,
#         product_expanded.product_description,
#         frl_lines_bs.source_type,
#         fin_dly_headers.office_account,
#         ouc_expanded.ouc_description,
#         fin_dly_headers.customer_id,
#         fin_dly_headers.contract_id,
#         customers_dly_expanded.customer_name,
#         fin_dly_headers.bs_gl,
#         fin_dly_headers.pl_gl,
#         fin_dly_headers.vision_ouc,
#         fin_dly_headers.vision_sbu,
#         fin_dly_headers.currency,
#         accounts_dly.ACCOUNT_TYPE,
#         accounts_dly.scheme_code,
#         accounts_dly.sector_code,
#         accounts_dly.sub_sector_code,
#         fin_dly_headers.record_type,
#         fin_dly_balances.bal_type)
#         select * from default_pl
#     """
#     pls = pd.read_sql(query, con=conn)    
#     if cust_type=="All":
#         pass
#     else: 
#         pls=pls[pls.VISION_SBU==cust_type]
#     Loan=pls[pls.ACCOUNT_TYPE=='LAA']
#     Overdraft=pls[pls.ACCOUNT_TYPE=='ODA']
#     Current=pls[pls.ACCOUNT_TYPE=='CAA']
#     Saving=pls[pls.ACCOUNT_TYPE=='SBA']
#     Term_Dep=pls[pls.ACCOUNT_TYPE=='TDA']
    
#     Income=pls[pls.FRL_ATTRIBUTE_04=='FA040100'].BALANCE.sum()
#     Expenses=pls[pls.FRL_ATTRIBUTE_04=='FA040200'].BALANCE.sum()
#     FC=pls[pls.FRL_ATTRIBUTE_04=='FA040300'].BALANCE.sum()    
#     return (pos_female_overtime,pos_male_overtime,atm_female_overtime,atm_male_overtime)

