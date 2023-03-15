import requests
import pandas as pd
import datetime
from datetime import datetime
import time
import matplotlib.pyplot as plt
import streamlit as st


def round_off(underlaying_value):
    p = underlaying_value
    k = p - (p % 10)
    rounded = k % 100

    if 0 < rounded <= 40:
        rounded_new = k - (rounded)
    elif 50 < rounded <= 90:
        rounded_new = k - ((rounded) - 50)
    else:
        rounded_new = k

    return int(rounded_new)

def list_of_strike(price):
   strike_list = []
   strike_list.append(price)
   for i in range(1,7):
       strike_list.append(price + (50 * i))
       i=i+1
   strike_list_2=[]
   for i in range(1,7):
       strike_list_2.append(price - (50 * i))
       i=i+1

   final_strike_list=(strike_list_2+strike_list)
   return final_strike_list

def oi(Strike_List,LIST):
    oi = 0
    for i in LIST:
        if i['strikePrice'] in Strike_List:
            print(i)
            oi = oi + int(i['changeinOpenInterest'])

    return oi

def latest_time():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    list_time = current_time.split(':')
    time = list_time[0] + list_time[1]
    return str(time)

def signal_generator(call_oi,put_oi):
    diff=put_oi-call_oi
    if diff>0:
        signal='BUY'
    else:
        signal ='SELL'

    return diff,signal

def create_data_frame(data):
     df=pd.DataFrame(data,columns=['time','call_oi','put_oi','differance_oi','signal'])
     return df

def today_date():
    Current_Date = str(datetime.today())
    print(Current_Date)
    lt = Current_Date.split(' ')
    return lt[0]

data_frame_list=[]


while True:

    url='https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    header={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
         'accept-encoding': 'gzip, deflate, br',
         'accept-language': 'en-US,en;q=0.9'
    }
    session=requests.Session()
    request=session.get(url,headers=header)
    cokies=dict(request.cookies)
    response=session.get(url,headers=header,cookies=cokies).json()
    df= pd.DataFrame(response)
    data=(pd.DataFrame(df['filtered']['data']))
    CE_LIST=list(data['CE'])
    PE_LIST=list(data['PE'])



    ATM_Strike=round_off(CE_LIST[0]['underlyingValue'])
    Strike_List=list_of_strike(ATM_Strike)


    call_oi =oi(Strike_List,CE_LIST)
    put_oi=oi(Strike_List,PE_LIST)
    current_time=latest_time()
    differance_oi,signal=signal_generator(call_oi,put_oi)
    row=[current_time,call_oi,put_oi,differance_oi,signal]
    data_frame_list.append(row)
    df=create_data_frame(data_frame_list)
    df = df.astype({'time': 'string'})


    df_new=df[['time','differance_oi']]
    name_of_file="Option_Data_"+today_date()+".csv"
    df.to_csv(name_of_file)
    placeholder=st.empty()
    placeholder.dataframe(df)
    placeholder_graph=st.empty()
    placeholder_graph.line_chart(df,y='differance_oi')

    time.sleep(900)
    placeholder.empty()
    placeholder_graph.empty()

