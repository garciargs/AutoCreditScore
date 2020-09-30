# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
# import numpy as np
from prediction import classify
import variaveis
import plots


external_stylesheets = ['assets/css.css', dbc.themes.MATERIA]

app = dash.Dash(__name__
                , external_stylesheets=external_stylesheets
                , suppress_callback_exceptions=True)

server = app.server

def suspended_list_val(group):
    return [{'label': x, 'value': x} for x in variaveis.transform[group].values()]


app.layout = html.Div(className="container", 
                      style={'width': '100%'}
                      , children=[
    dcc.Store(id='memory')
    , html.Div(                      
        html.H1(children='Crédito Automático'
                , style={'backgroundColor': 'blue'
                          , 'textAlign': 'center'
                          , 'color': 'white'
                          }
                )
        )
        , html.Div(
                        children=[html.H2(children=['Preencha os dados abaixo'])]
                        # , className='four.columns'
                        , style={
                            'textAlign':'left'
                            , 'padding-left': '2rem'
                            }
                        )
    , html.Div(
        className='row'
        , style={
            'height': '45rem'
            }
        , children=[
            html.Div(
                className='six columns'
                , style={
                    'padding': '0 2.5%'
                    , 'width': '30%'
                    }
                , children=[
                    html.Div(
                        style={
                            'textAlign': 'left'
                            , 'width': '100%'
                            , 'padding': '0.35rem 0'
                            }
                        , children=[
                            html.H5(
                                style={
                                    'margin': '0 0 -0.5rem 0'
                                    }
                                , children=['Sexo']
                                )
                            , dcc.Dropdown(
                                id='list-sexo'
                                , options=suspended_list_val('SEX')
                                , value=''
                                , style={
                                    'height': '4rem'
                                    # , 'margin': '1.75rem 0'
                                    }
                            )
                            ]
                        )
                    , html.Div(
                        style={
                            'textAlign': 'left'
                            , 'width': '100%'
                            , 'padding': '0.35rem 0'
                            }
                        , children=[
                            html.H5(
                                style={
                                    'margin': '0 0 -0.5rem 0'
                                    }
                                , children=['Nível de ensino']
                                )
                            , dcc.Dropdown(
                                id='list-educ'
                                , options=suspended_list_val('EDUCATION')
                                , value=''
                                , style={
                                    'height': '4rem'
                                    # , 'margin': '1.75rem 0'
                                    }
                            )
                            ]
                        )
                    , html.Div(
                        style={
                            'textAlign': 'left'
                            , 'width': '100%'
                            , 'padding': '0.35rem 0'
                            }
                        , children=[
                            html.H5(
                                style={
                                    'margin': '0 0 -0.5rem 0'
                                    }
                                , children=['Estado civil']
                                )
                            , dcc.Dropdown(
                                id='list-status-civil'
                                , options=suspended_list_val('MARRIAGE')
                                , value=''
                                , style={
                                    'height': '4rem'
                                    # , 'margin': '1.75rem 0'
                                    }
                            )
                            ]
                        )
                    , html.Div(
                        style={
                            'padding': '0.35rem 0'
                            }
                        , children=[
                            html.H5(
                                style={
                                    'margin': '0 0 -0.5rem 0'
                                    }
                                , children=['Idade']
                                )
                            , dcc.Input(
                                id='input-idade'
                                , type='number'
                                , style={
                                    'textAlign': 'center'
                                    , 'width': '100%'
                                    , 'height': '4rem'
                                    # , 'margin': '1.75rem 0'
                                    }
                                )
                            ]
                        )
                    , html.Div(
                        children=[
                            dbc.Button('Enviar', id='submit-val'
                                        , n_clicks=0
                                        , className='mr-1'
                                        , color='success'
                                        , style={
                                            'width':'100%'
                                            , 'height': '4rem'
                                            , 'margin': '1.75rem 0'
                                            , 'font-size': '1.5rem'
                                            }
                                  )
                            ]
                        )
                    , html.Div(
                        children=[
                            dbc.Button('Restart', id='reset-val'
                                        , n_clicks=0
                                        , className='mr-1'
                                        , color='secondary'
                                        , style={
                                            'width':'100%'
                                            , 'height': '4rem'
                                            , 'margin': '1.75rem 0'
                                            , 'font-size': '1.5rem'
                                            }
                                  )
                            ]
                        )
                    ]
                )
            
            , html.Div(className='six columns'
                        , style={
                            'textAlign':'center'
                            , 'width': '70%'
                            }
                        , id='pass-not-pass'
                        )
            ]
        )
    , html.Div(
        className='row'
        , id='show-details'
        , style={'width': '50%', 'margin-left': '25%'}
        # , children=[
        #     dbc.Button(
        #         'Detalhes'
        #         , id='button-show-details'
        #         , n_clicks=0
        #         , className='mr-1'
        #         , color='info'
        #         , style={
        #             'width':'100%'
        #             , 'height': '4rem'
        #             , 'margin': '1.75rem 0'
        #             , 'font-size': '1.5rem'
        #             }
        #         )
        #     ]
        )
    
    , html.Div(
        className='row'
        , id='details'
        )
    , html.Div(id='risco-val', style={'display': 'none'})
    ])


#-------Pega os dados de entrada do usuário e determina a classificação
@app.callback(
    [Output('memory', 'data')
     , Output('pass-not-pass', 'children')
     , Output('show-details', 'children')
     , Output('submit-val', 'disabled')],
    [Input('submit-val', 'n_clicks')
     , Input('reset-val','n_clicks')
      , State('input-idade', 'value')
      , State('list-sexo', 'value')
      , State('list-educ', 'value')
      , State('list-status-civil', 'value')])
def predict(n_clicks, reset, idade, sexo, educ, civil):
    
    ctx = dash.callback_context
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id=='reset-val':
        n_clicks = 0
        return '', '', '', False
    
    if n_clicks>0:
        aprova, risco = classify(idade, sexo, educ, civil)
        if aprova==1:
            img='ok_icon.gif'
        else:
            img='x_icon.gif'
        return (
            {'risco': risco}
            , html.Img(src=app.get_asset_url(img)
                        , style={
                            'height':'35rem'
                            , 'margin': '5rem 0'
                            }
                        )
            , dbc.Button(
                'Detalhes'
                , id='button-show-details'
                , n_clicks=0
                , className='mr-1'
                , color='info'
                , style={
                    'width':'100%'
                    , 'height': '4rem'
                    , 'margin': '1.75rem 0'
                    , 'font-size': '1.5rem'
                    }
                )
            , True
            )
    else:
        raise PreventUpdate
               


#--------Reseta os parâmetros
@app.callback([Output('input-idade', 'value')
               , Output('list-sexo', 'value')
               , Output('list-educ', 'value')
               , Output('list-status-civil', 'value')]
              , [Input('reset-val','n_clicks')])
def reset(reset):
    return '', '', '', ''


#-------Exibe os detalhes dos grupos
@app.callback(
    [Output('details', 'children')
     , Output('details', 'style')]
    , [Input('button-show-details', 'n_clicks')
        , Input('reset-val','n_clicks')
        , State('memory', 'data')])
def show_details(n_clicks, reset, risco):
    ctx = dash.callback_context
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    risco_val = risco.get('risco', 0)
    
    if button_id=='reset-val':
        return html.Div(), {'width': '100%'}
    else:
        if n_clicks>0:
            table = plots.table(risco_val)
            
            return (html.Div(
                children=[
                    dcc.Graph(
                        figure=table
                        )
                    ]
                )
                , {'width': '150%', 'height': '50rem', 'margin-left': '-25%'}
                )
        else:
            raise PreventUpdate




if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)