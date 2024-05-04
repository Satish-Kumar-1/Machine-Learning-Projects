# -*- coding: utf-8 -*-
"""EPS_Data_deployment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mQdwlDyRmbvrJJ4mdA7_UuI1eyzVlwjm
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score, accuracy_score, classification_report, precision_recall_curve, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error

b = pd.read_excel("/content/drive/MyDrive/EPS_Dataset.xlsx")

df = b.copy()

df.head()

df = df.drop(['Bank name'], axis=1)

df.head(10)

## Outliers detection


col_list = df.columns
for i in col_list:
    q1 = np.percentile(df[i], 25)
    q3 = np.percentile(df[i], 75)
    iqr = q3-q1
    lower_bound = q1 - (5*iqr)
    upper_bound = q3 + (5*iqr)

    df = df.loc[(df[i] >=lower_bound) & (df[i] <= upper_bound)]

df.columns

y = df['Basic EPS (Rs.)']
x = df.drop(['Basic EPS (Rs.)'], axis  = 1)

## VIF for numerical columns

from statsmodels.stats.outliers_influence import variance_inflation_factor

numeric_columns = x.columns
vif_data = x
total_columns = vif_data.shape[1]
columns_to_be_kept = []
column_index = 0

for i in range(0, total_columns):
    vif_value = variance_inflation_factor(vif_data, column_index)
    print(column_index, vif_value)

    if vif_value <= 200:
        columns_to_be_kept.append(numeric_columns[i])
        column_index = column_index + 1

    else:
        vif_data = vif_data.drop([numeric_columns[i]], axis=1)

x = x[columns_to_be_kept]

## Apply standard scaler
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
x = x_scaled

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)

param_grid = {
    'colsample_bytree' : [0.1, 0.3, 0.5, 0.7, 0.9],
    'learning_rate' : [0.001, 0.01, 0.1, 1],
    'max_depth' : [3, 5, 8, 10],
    'alpha' : [1, 10, 100],
    'n_estimators' : [10, 50, 100]
}

index = 0

answers_grid = {
    'combination' : [],
    'train_RMSE' : [],
    'test_RMSE' : [],
    'train_R2' : [],
    'test_R2' : [],
    'train_std_diff' : [],
    'test_std_diff' : [],
    'colsample_bytree' : [],
    'learning_rate' : [],
    'max_depth' : [],
    'alpha' : [],
    'n_estimators' : []
}

for colsample_bytree in param_grid['colsample_bytree']:
    for learning_rate in param_grid['learning_rate']:
        for max_depth in param_grid['max_depth']:
            for alpha in param_grid['alpha']:
                for n_estimators in param_grid['n_estimators']:

                    index = index + 1

                    model = xgb.XGBRegressor(objective = 'reg:squarederror',
                                             colsample_bytree = colsample_bytree,
                                             learning_rate = learning_rate,
                                             max_depth = max_depth,
                                             alpha = alpha,
                                             n_estimators = n_estimators)

                    model.fit(x_train, y_train)

                    y_pred_train = model.predict(x_train)
                    y_pred_test = model.predict(x_test)

                    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
                    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
                    train_r2 = r2_score(y_train, y_pred_train)
                    test_r2 = r2_score(y_train, y_pred_train)
                    train_std_diff = train_rmse / np.std(y_train)
                    test_std_diff = test_rmse / np.std(y_test)

                    answers_grid['combination'].append(index)
                    answers_grid['train_RMSE'].append(train_rmse)
                    answers_grid['test_RMSE'].append(test_rmse)
                    answers_grid['train_R2'].append(train_r2)
                    answers_grid['test_R2'].append(test_r2)
                    answers_grid['train_std_diff'].append(train_std_diff)
                    answers_grid['test_std_diff'].append(test_std_diff)
                    answers_grid['colsample_bytree'].append(colsample_bytree)
                    answers_grid['learning_rate'].append(learning_rate)
                    answers_grid['max_depth'].append(max_depth)
                    answers_grid['alpha'].append(alpha)
                    answers_grid['n_estimators'].append(n_estimators)

                    # print(f"Combination {index}")
                    # print(f"colsample_bytree: {colsample_bytree}, learning_rate: {learning_rate}, max_depth: {max_depth}, alpha: {alpha}, n_estimators: {n_estimators}")
                    # print(f"Train RMSE: {train_rmse:.2f}")
                    # print(f"Test RMSE : {test_rmse:.2f}")
                    # print(f"Train R2  : {train_r2:.2f}")
                    # print(f"Test R2   : {test_r2:.2f}")
                    # print(f"Train std_diff: {train_std_diff:.2f}")
                    # print(f"Test std_diff : {test_std_diff:.2f}")
                    # print("-" * 30)

answers_grid_df = pd.DataFrame(answers_grid)
answers_grid_df.toexcel('/content/sample_data/accuracy.xlsx', index = False)

"""answers_grid = {
    'combination' : [],
    'train_RMSE' : [],
    'test_RMSE' : [],
    'train_R2' : [],
    'test_R2' : [],
    'train_std_diff' : [],
    'test_std_diff' : [],
    'colsample_bytree' : [],
    'learning_rate' : [],
    'max_depth' : [],
    'alpha' : [],
    'n_estimators' : []              
}

"""

print(len(answers_grid['combination']), len(answers_grid['colsample_bytree']), len(answers_grid['train_RMSE']))

print(len(answers_grid['learning_rate']), len(answers_grid['test_RMSE']), len(answers_grid['n_estimators']))

l = ['combination',
    'train_RMSE',
    'test_RMSE',
    'train_R2',
    'test_R2',
    'train_std_diff',
    'test_std_diff',
    'colsample_bytree',
    'learning_rate',
    'max_depth',
    'alpha',
    'n_estimators']

for i in l:
    if len(answers_grid[i])==1440:
        print(i)

for i in l:
    if len(answers_grid[i]) == 1441:
        print(i)

