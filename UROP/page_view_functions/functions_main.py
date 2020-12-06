import pandas as pd
import functions as fn

def main():
    df1 = pd.read_csv("tags.csv")
    n = 1000
    tag_array = df1['tag'].value_counts()[:n].index.tolist()
    del tag_array[0:50]
    print(tag_array)
    #print(fn.best_date_of_tag(tag_array))
    df = pd.read_csv("pg_view_1.csv")     
    for tag in tag_array:  
        print(tag)
        df_tag = fn.pg_views_for_a_tag(df,tag)
        df_perc = fn.tag_perc(df_tag,tag)
        df_daily_avg = fn.tag_daily_avg(df_perc,tag)
        fn.roll_avg_of_norm_val(df_daily_avg,tag)       
        df_daily_avg.to_csv('dataframe/daily_avg_over_yrs/'+ tag +'.csv')
        fn.print_df(df_daily_avg,tag)


    # TEST FOR A SINGLE VALUE 
# =============================================================================
#     tag = "halloween"
#     df_tag = fn.pg_views_for_a_tag(df,tag)
#     print(df_tag.head)
#     df_perc = fn.tag_perc(df_tag,tag)
#     print(df_perc)
#     df_daily_avg = fn.tag_daily_avg(df_perc,tag)
#     print(df_daily_avg.head)
#     fn.print_df(df_daily_avg,tag)
#     fn.roll_avg_of_norm_val(df_daily_avg,tag)       
#     df_daily_avg.to_csv('dataframe/daily_avg_over_yrs/'+ tag +'.csv')
# 
# =============================================================================
    # END FUNCTION 
    
if __name__ == "__main__":
    main()

