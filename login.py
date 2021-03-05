import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

import warnings
warnings.filterwarnings("ignore")

## For session and enhance performance
from werkzeug.security import check_password_hash
from flask_login import login_user
from assets import *

from app import User, app

layout = html.Div(
    children=[
        html.Div(
            className="container",
            children=[
                dcc.Location(id='url_login', refresh=True),
                html.Div(html.H4('Welcome to the dashboard'), id='h1', style={"margin": "15px 0px 15px 50px","family": "family: 'Calibri, monospace",}),
                html.Div(
                    # method='Post', 
                    children=[
                        dcc.Input(
                            placeholder='Enter your username',
                            type='text',
                            id='uname-box',
                            style={"margin": "250px 0px 0px 100px"},
                        ),
                        html.Br(),
                        dcc.Input(
                            placeholder='Enter your password',
                            type='password',
                            id='pwd-box',
                            style={"margin": "30px 0px 0px 100px"},
                        ),
                        html.Br(),
                        html.Button(
                            children='Login',
                            n_clicks=0,
                            type='submit',
                            id='login-button',
                            style={"margin": "30px 0px 0px 100px"},
                        ),
                        html.Div(children='', id='output-state')
#                     ],style={'background-image': 'url(https://html1-f.scribdassets.com/5b6ivtv20w5q554t/images/1-8beea4ea85.jpg',"opacity": 1, "height":1000,},
                    ],style={'background-image': 'url(/assets/Building_portrait.jpg)',"opacity": 2, "height":1685,'position':'center',},                    
                ),
            ]
        )
    ]
)

@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, input1, input2):
    user = User.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/Overview'
        else:
            pass
    else:
        pass
    
@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = User.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''    