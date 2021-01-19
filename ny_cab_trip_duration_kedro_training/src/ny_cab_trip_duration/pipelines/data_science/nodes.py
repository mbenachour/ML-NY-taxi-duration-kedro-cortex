import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from kedro.config import ConfigLoader
import logging
from typing import Dict, List

# conf_paths = ["conf/base", "conf/local"]
# conf_loader = ConfigLoader(conf_paths)
# parameters = conf_loader.get("parameters*", "parameters*/**")



def split_data(data: pd.DataFrame, parameters: Dict) -> List:
    """Splits data into training and test sets.

        Args:
            data: Source data.
            parameters: Parameters defined in parameters.yml.

        Returns:
            A list containing split data.

    """
    X = data[
        [
           "id",
           "vendor_id",
           "pickup_datetime",
           "dropoff_datetime",
           "passenger_count",
           "pickup_longitude",
           "pickup_latitude",
           "dropoff_longitude",
           "dropoff_latitude",
           "store_and_fwd_flag",
           "hdistance",
           "distance",
           "log_distance",
           "month",
           "hour",
           "minutes",
           "is_weekend",
           "weekday",
           "is_holyday",
           "is_day_before_holyday"

        ]
    ].values
    y = data["trip_duration"].values

    X = np.array(data.drop(['id', 'pickup_datetime', 'dropoff_datetime', 'store_and_fwd_flag', 'trip_duration'], axis=1))
    y = np.log(data['trip_duration'].values)
    #median_trip_duration = np.median(train['trip_duration'].values) 

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )

    return [X_train, X_test, y_train, y_test]

def train_model(X_train: np.ndarray, y_train: np.ndarray, parameters: Dict) -> lgb:
    """Train the linear regression model.

        Args:
            X_train: Training data of independent features.
            y_train: Training data for price.

        Returns:
            Trained model.

    """
    


    d_train = lgb.Dataset(X_train, label=y_train)


    boosting_type = parameters["boosting_type"]
    objective  = parameters["objective"]
    metric = parameters["metric"]
    max_depth = parameters["max_depth"]
    learning_rate = parameters["learning_rate"]
    verbose = parameters["verbose"]
    early_stopping_round  = parameters["early_stopping_round"]
    n_estimators = parameters["n_estimators"]


    params = {
    'boosting_type': boosting_type,
    'objective': objective,
    'metric': metric,
    'max_depth': max_depth, 
    'learning_rate': learning_rate,
    'verbose': verbose, 
    #'early_stopping_round': early_stopping_round
    }

    model = lgb.train(params=params, train_set=d_train, valid_sets=None, verbose_eval=1)

    return model





def evaluate_model(model: lgb, X_test: np.ndarray, y_test: np.ndarray) -> pd.DataFrame:
    """Calculate the coefficient of determination and log the result.

        Args:
            regressor: Trained model.
            X_test: Testing data of independent features.
            y_test: Testing data for price.

    """
    y_pred = model.predict(X_test)

    results = pd.concat([pd.DataFrame(X_test),pd.DataFrame(y_test) ,pd.DataFrame(y_pred)], axis=1)

    return results