# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:47:05 2020

@author: ricar
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib

df = joblib.load('grupos.save')

df = df.drop(columns=['Cluster', 'default'])
df.rename(columns={
    'x1_Outros': 'Ensino Outros'
    , 'x2_Outros': 'Estado Civil Outros'
    }
    , inplace=True)

columns = df.columns
columns = [x.split('_', 1)[1] if '_' in x else x for x in columns]
df.columns = columns

df['Idade'] = np.round(df['AGE'], 1)

def table(risco):

    df_format=pd.DataFrame()

    for x in columns[:-2]:
        df_format[x] = ['{:.1%}'.format(y) for y in df[x]]
    
    df_format[['Risco', 'Idade']] = df[['Risco', 'Idade']]
    
    df_format = df_format[list(df_format.columns[-2:])
                          +list(df_format.columns[:-2])]
    
       
    df_format['selection'] = 0
    df_format.drop(columns=['Desconhecido 1', 'Desconhecido 2', 'Ensino Outros', 'Estado Civil Outros'], inplace=True)
    
    df_format.at[risco-1, 'selection'] = 1
    
    font_color = [['rgb(150,150,150)' if x==0 else 'white' for x in df_format['selection']]]
    row_color = [['white' if x==0 else 'blue' for x in df_format['selection']]]
    
    df_format = df_format.astype(str)
    iat = risco-1
    for x in df_format.columns:
        df_format.at[iat, x] = '<b>'+str(df_format[x].iloc[iat])+'</b>'
    
    fig = go.Figure(
        go.Table(
            header=dict(
                values=['<b>'+x+'</b>' for x in df_format.iloc[:,:-1].columns]
                , fill_color='white'
                , align='left'
                , font=dict(color='rgb(150,150,150)', size=20)
                , height=50
                ),
            cells=dict(
                values=[df_format[x] for x in df_format.iloc[:,:-1].columns]
                , fill_color=row_color
                , align='left'
                , font=dict(
                    color=font_color
                    , size=20
                    )
                , height=40
                )
            )
        )
    fig.update_layout(height=700, width=1440)
    
    return fig