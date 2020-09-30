# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 11:06:42 2020

@author: ricar
"""


import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
import plotly.graph_objects as go
from plotly.offline import plot
import variaveis
import joblib

df = pd.read_csv('file/data.csv')
df = df[['SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 'default.payment.next.month']]

df1 = (df.loc[(df['EDUCATION']!=0) & (df['MARRIAGE']!=0)]
           .reset_index(drop=True)
           .copy())

bin_columns = ['SEX', 'EDUCATION', 'MARRIAGE']

for col in bin_columns:
    df1[col] = df1[col].apply(
        lambda x: variaveis.transform[col][x]
        )

X = df1.iloc[:,:-1]
y = df1.iloc[:, -1]


one_hot_enc = OneHotEncoder()

one_hot_enc.fit(X[bin_columns])

X_bin = pd.DataFrame(
    one_hot_enc.transform(X[bin_columns]).toarray()
    , columns=one_hot_enc.get_feature_names()
    )
X_bin['AGE'] = X['AGE']


custo = []

for i in range(2,20):
    kmeans = KMeans(n_clusters = i, random_state = 1)
    kmeans.fit(X_bin)
    custo.append((i, kmeans.inertia_))
    
df_custo = pd.DataFrame(np.array(custo), columns=['N', 'Inertia'])

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df_custo['N']
        , y=df_custo['Inertia']
        )
    )
plot(fig)


kmeans = KMeans(n_clusters=10)

df_final = X_bin.copy()
df_final['Cluster'] = kmeans.fit_predict(df_final)

df_final['default'] = y

df_risco = df_final.groupby('Cluster').mean().sort_values('default').reset_index()

df_risco['Risco'] = df_risco.index + 1

encoder_file = 'encoder.save'
kmeans_file = 'kmeans_model.save'
grupos_risco = 'grupos.save'

joblib.dump(one_hot_enc, encoder_file)
joblib.dump(kmeans, kmeans_file)
joblib.dump(df_risco, grupos_risco)