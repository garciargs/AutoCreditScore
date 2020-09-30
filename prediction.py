# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 18:48:46 2020

@author: ricar
"""
import joblib
import numpy as np


def classify(age, sex, education, marriage):
    
    encoder_file = 'encoder.save'
    kmeans_file = 'kmeans_model.save'
    grupos_risco = 'grupos.save'
    
    one_hot_enc = joblib.load(encoder_file)
    kmeans = joblib.load(kmeans_file)
    df_risco = joblib.load(grupos_risco)
    
    user = np.array([sex, education, marriage]).reshape(1, -1)
    user_enc = one_hot_enc.transform(user).toarray()
    user_enc = np.append(user_enc, age).reshape(1, -1)
    
    prediction = kmeans.predict(user_enc)[0]
    
    risco = (
        df_risco['Risco']
        .loc[df_risco['Cluster']==prediction]
        .values[0]
        )
    
    if risco < 4:
        aprova = 1
    else:
        aprova = 0
    
    return aprova, risco