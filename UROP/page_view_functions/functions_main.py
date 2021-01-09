import pandas as pd
import functions as fn

def main():
    df1 = pd.read_csv("tags.csv")
    n = 10
    tag_array = df1['tag'].value_counts()[:n].index.tolist()
    # del tag_array[0:1]
    print(tag_array)
    #print(fn.best_date_of_tag(tag_array))
    df = pd.read_csv("pg_view_1.csv")     
    # i = 0
    # for tag in tag_array:  
    #     print(tag)
    #     print('\t')
    #     print(i)
    #     i+=1
    #     df_tag = fn.pg_views_for_a_tag(df,tag)
    #     df_perc = fn.tag_perc(df_tag,tag)
    #     df_daily_avg = fn.tag_daily_avg(df_perc,tag)
    #     df_daily_avg.columns = map(str.lower, df_daily_avg.columns)    
    #     df_daily_avg.to_csv('dataframe/daily_avg_over_yrs_1/'+ tag +'.csv')
    #     #fn.print_df(df_daily_avg,tag)


    # TEST FOR A SINGLE VALUE 
# =============================================================================
    tag = "christmas"
    df_tag = fn.pg_views_for_a_tag(df,tag)
    print(df_tag.head)
    df_perc = fn.tag_perc(df_tag,tag)
    print(df_perc)
    df_daily_avg = fn.tag_daily_avg(df_perc,tag)
    print(df_daily_avg.head)
    fn.print_df(df_daily_avg,tag)  
    # df_daily_avg.to_csv('dataframe/daily_avg_over_yrs/'+ tag +'.csv')
# 
# =============================================================================
    # END FUNCTION 
    
if __name__ == "__main__":
    main()

