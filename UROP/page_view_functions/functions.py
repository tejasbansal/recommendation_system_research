import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.ticker import AutoMinorLocator
import datetime as dt
import numpy as np
import gc
from sklearn import svm, preprocessing

def daily_breakdown(filename): # for the user movie view file
    try: 
        df = pd.read_csv(filename)
        df['tstamp'] = df['tstamp'].apply(lambda x: dt.datetime.strptime(x,'%d-%m-%Y %H:%M'))
        start = df['tstamp'].min()
        end = df['tstamp'].max()
        new_df = pd.DataFrame(columns=['timestamp','pg_views'])
        delta = dt.timedelta(days=1) 
        i = 0
        e = start
        print(start)
        print(end)
        while start <= end:
            count = 0
            e = start+delta
            for t in df.tstamp:
                if start<=t<e:
                    count +=1
            new_df.loc[i] = [start,count]
            i+=1
            start = e
        new_df['rolling_avg'] = new_df['pg_views'].rolling(window=14).mean()
        new_df.to_csv("daily_breakdown_try.csv")
        return new_df
    except FileNotFoundError:
        print("File not found")

def pg_views_for_a_tag(pg_view,tag):
    df = pd.read_csv('user_movie_view.csv')
    df['tstamp'] = df['tstamp'].apply(lambda x: dt.datetime.strptime(x,'%d-%m-%Y %H:%M'))
    del df["userId"]
    df2 = pd.read_csv('tags.csv')
    del df2['timestampForTag']
    del df2['userId']
    t = tag
    df2.drop(df2[df2['tag'] !=t.casefold()].index, inplace=True)
    df2 = df2.movieId.unique()
    df2 = pd.DataFrame({'movieId':df2})
    df3 = pd.merge(df2,df,on='movieId')
    #df3['tstamp'] = df3['tstamp'].apply(lambda x: dt.datetime.strptime(x,'%d-%m-%Y %H:%M'))
    start = df['tstamp'].min()
    end = df['tstamp'].max()
    df5 = pd.DataFrame(columns=['timestamp','pg_view'])
    delta = dt.timedelta(days=1)
    i = 0
    e = start
    print(start)
    print(end)
    while start <= end:
        count = 0
        e = start+delta
        for t in df3.tstamp:
            if start<=t<e:
                count +=1
        df5.loc[i] = [start,count]
        i+=1
        start = e
    return df5

def tag_perc(df_tag,tag):
    df_perc = pd.DataFrame(columns=['timestamp','perc'])
    pg_view = pd.read_csv('pg_view_1.csv')
    df_perc['timestamp'] = pg_view['timestamp']
    df_perc['perc'] = df_tag['pg_view']/(pg_view['pg_views']+1) * 100
    return df_perc

def tag_overall_sub_avg_perc(df_perc):
    avg = df_perc['perc'].sum()/(df_perc[0]+1)
    df_sub = df_perc['perc'] - avg
    return df_sub

def tag_daily_avg_over_years (df,tag):
    # df5 = pd.DataFrame(columns=['timestamp','pg_view'])
    df['timestamp'] = df['timestamp'].apply(lambda x: dt.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    df['mth_day'] = df['timestamp'].map(lambda x: x.strftime("%m-%d"))
    df.sort_values('mth_day',inplace = True)
    df = df.reset_index(drop=True)
    df['perc'] = df['perc'].rolling(window=7,center=True).mean() 
    
    date = pd.date_range(start='2016-01-01',end='2016-12-31')
    df_avg = pd.DataFrame({'dates':date})
    df_avg["mth_day"] = df_avg['dates'].map(lambda x: x.strftime("%m-%d"))
    df_avg[tag]=0
    del df_avg['dates']
    i = 0
    count = 0
    total = 0
    for t in df_avg.mth_day:
        count = 0
        total = 0
        j = 0
        for s in df.mth_day:
            if t == s and j<len(df.index):
                total+=df['perc'].loc[j]
                count+=1
            j+=1
        if(count == 0):
            count = 1
        #print(count)
        df_avg.loc[i] = [t,(total/count)]
        i+=1
   
    X = np.array(df_avg[tag].values)#.tolist()
    X = preprocessing.scale(X)
    df_avg[tag+'_norm'] = X
    df_avg[tag+'_ravg'] = df_avg[tag+'_norm'].rolling(window=6,center=True).mean()
    return df_avg
    
def print_df(df,tag):
    fig = df.plot(x='mth_day',y=tag+'_norm',figsize = (15,8))
    fig.figure.savefig('graphs/daily_avg_over_yrs/'+ tag+'.pdf')
    fig1 = df.plot(x='mth_day',y= tag+'_ravg',figsize = (15,8))
    fig1.figure.savefig('graphs/daily_avg_over_yrs/rolling_avg/'+ tag+'_ravg.pdf')
    return 

def unique_tags():
    df = pd.read_csv('tags.csv')
    tag_array = df['tag'].unique()
    return tag_array

# def roll_avg_of_norm_val (tag_array):
#     from pathlib import Path
#     import pandas as pd
#     root = Path('dataframe', 'daily_avg_over_yrs')
#     for tag in tag_array:
#         tagn = tag+'.csv'
#         df = pd.read_csv(root / tagn)
#         df[tag+'_ravg'] = df[tag+'_norm'].rolling(window=6,center=True).mean()
#         fig = df.plot(x='mth_day',y= tag+'_ravg',figsize = (15,8))
#         fig.figure.savefig('graphs/daily_avg_over_yrs/rolling_avg/'+ tag+'_ravg.pdf')
    #     df_daily_avg.to_csv('dataframe/daily_avg_over_yrs/'+ tag +'.csv')

#     return df
        

def best_date_of_tag (tag_array):
    from pathlib import Path
    import pandas as pd
    root = Path('dataframe', 'daily_avg_over_yrs_1')
    i = 0
    df2 = pd.DataFrame(columns=['tag','date','ravg_value'])
    for tag in tag_array:
        tagn = tag+'.csv'
        df = pd.read_csv(root / tagn)
        date = df.loc[df[tag+'_ravg'].idxmax()]['mth_day']
        ravg_value = df.loc[df[tag+'_ravg'].idxmax()][tag+'_ravg']
        df2.loc[i] = [tag,date,ravg_value]
        i +=1
    return df2

# FUNCTION TO CONVERT THE DATAFRAME'S HEADERS TO LOWERCASE
# import os
# import glob
# path = r"C:\Users\tejas\Desktop\recommendation_system_research\UROP\page_view_functions\dataframe\daily_avg_over_yrs_1\*.csv"
# for file in glob.glob(path):
#     #print(file)
#     df=pd.read_csv(file)
#     df.columns = df.columns.str.lower()
#     df.to_csv(file)
# df.head()