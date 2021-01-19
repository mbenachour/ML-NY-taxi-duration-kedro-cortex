import datetime
import numpy as np
import pandas as pd
import haversine

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    df['hdistance'] = df.apply(lambda r: haversine.haversine((r['pickup_latitude'],r['pickup_longitude']),(r['dropoff_latitude'], r['dropoff_longitude'])), axis=1)
    df['distance'] = np.sqrt(np.power(df['dropoff_longitude'] - df['pickup_longitude'], 2) + np.power(df['dropoff_latitude'] - df['pickup_latitude'], 2))
    df['log_distance'] = np.log(df['distance'] + 1)
    df['month'] = df['pickup_datetime'].apply(lambda x: int(x.split(' ')[0].split('-')[1]))
    df['day'] = df['pickup_datetime'].apply(lambda x: int(x.split(' ')[0].split('-')[2]))
    df['hour'] = df['pickup_datetime'].apply(lambda x: int(x.split(' ')[1].split(':')[0]))
    df['minutes'] = df['pickup_datetime'].apply(lambda x: int(x.split(' ')[1].split(':')[1]))
    df['is_weekend'] = ((df.pickup_datetime.astype('datetime64[ns]').dt.dayofweek) // 4 == 1).astype(float)
    df['weekday'] = df.pickup_datetime.astype('datetime64[ns]').dt.dayofweek
    df['is_holyday'] = df.apply(lambda row: 1 if (row['month']==1 and row['day']==1) or (row['month']==7 and row['day']==4) or (row['month']==11 and row['day']==11) or (row['month']==12 and row['day']==25) or (row['month']==1 and row['day'] >= 15 and row['day'] <= 21 and row['weekday'] == 0) or (row['month']==2 and row['day'] >= 15 and row['day'] <= 21 and row['weekday'] == 0) or (row['month']==5 and row['day'] >= 25 and row['day'] <= 31 and row['weekday'] == 0) or (row['month']==9 and row['day'] >= 1 and row['day'] <= 7 and row['weekday'] == 0) or (row['month']==10 and row['day'] >= 8 and row['day'] <= 14 and row['weekday'] == 0) or (row['month']==11 and row['day'] >= 22 and row['day'] <= 28 and row['weekday'] == 3) else 0, axis=1)
    df['is_day_before_holyday'] = df.apply(lambda row: 1 if (row['month']==12 and row['day']==31) or (row['month']==7 and row['day']==3) or (row['month']==11 and row['day']==10) or (row['month']==12 and row['day']==24) or (row['month']==1 and row['day'] >= 14 and row['day'] <= 20 and row['weekday'] == 6) or (row['month']==2 and row['day'] >= 14 and row['day'] <= 20 and row['weekday'] == 6) or (row['month']==5 and row['day'] >= 24 and row['day'] <= 30 and row['weekday'] == 6) or ((row['month']==9 and row['day'] >= 1 and row['day'] <= 6) or (row['month']==8 and row['day'] == 31) and row['weekday'] == 6) or (row['month']==10 and row['day'] >= 7 and row['day'] <= 13 and row['weekday'] == 6) or (row['month']==11 and row['day'] >= 21 and row['day'] <= 27 and row['weekday'] == 2) else 0, axis=1)
    df['store_and_fwd_flag'] = df['store_and_fwd_flag'].map(lambda x: 0 if x =='N' else 1)
    df.drop('day', axis=1, inplace=True)
    return df