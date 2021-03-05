import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import visdcc
from dash.dependencies import Input, Output, State
from app import app, server, session_id

import pandas as pd
import io

from components import get_navbar, get_sidebar, parse_query_params, session_id

from flask_login import logout_user, current_user

from views import dash, loans,Channel,login, logout, i_click, Mobile, MTN, ussd, card, card_transactions, Customers, Profitability, Accounts_own, Accounts_stat, Deposits 

def get_page_layout(session_id):
    
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(session_id, id='session-id', style={'display': 'none'}),
            dbc.Row(id="navbar"),
            dbc.Row([
                # dbc.Col(id="sidebar", get_sidebar(), width={"size": 2,}, className="box"),
                dbc.Col(id="sidebar", width={"size": 2,}, className="box"),
                dbc.Col(
                    html.Div(id="page-content"),
                    width={"size": 10,}, className="box"
                ), 
            ], 
                no_gutters=False,
        #         form=True
            ),
#             dbc.Nav(submenu_1,  vertical=True),
            # html.Hr(),
            dbc.Button("Top",id="top", className="float-right", 
                style={
                    "position": "fixed",
                    # "overflow": "auto",
                    # "display":"none",
                    "background-color": "#f44336",
                    "color": "white",
                    "padding": "15px 25px",
                    "top":"80%",
                    "right":"10%",
                    "text-align": "center",
                    "text-decoration": "none",
                    "display": "inline-block",
                    "opacity": 0.2,
                }
            ), 
            visdcc.Run_js(id = 'hideButton'),
            visdcc.Run_js(id = 'showHideButton'),
            visdcc.Run_js(id = 'backToTop'),
        ],

        className="container-fluid",
    )

app.layout = get_page_layout(session_id)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
    [State("url", "search")],
)
def render_page_content(pathname, search):
    ## Set page-content based on url

    if pathname in ["/", "/login"]:
        return login.layout

    elif pathname == "/Overview":
        if search:
            query_params = parse_query_params(search)
        else:
            query_params = None
        return dash.layout
    
    elif pathname == "/Customers":
        return Customers.layout
    elif pathname == "/Accounts_own":
        return Accounts_own.layout
    elif pathname == "/Accounts_stat":
        return Accounts_stat.layout     
    
    elif pathname == "/loans":
        return loans.layout
    elif pathname == "/Deposits":
        return Deposits.layout        
    
#     elif pathname == "/Channel":
#         return html.H1("Channel")
    
    elif pathname == "/channels":
        return Channel.layout
    
    elif pathname == "/I_click":
        return i_click.layout
    
    elif pathname == "/Mobile":
        return Mobile.layout
    
    elif pathname == "/Ussd":
        return ussd.layout
    
    elif pathname == "/MTN":
        return MTN.layout
        
    elif pathname == "/card":
        return card.layout
    elif pathname == "/card_transactions":
        return card_transactions.layout    
    
    elif pathname == "/Profitability":
        return Profitability.layout    

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout

    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

########################################################################################
@app.callback(
    [
        Output("navbar", "children"), 
        Output("sidebar", "children"),
    ],
    [Input("url", "pathname")],
)
def set_app_layout(pathname):
    if pathname in ["/", "/login", '/logout']:
        return [dbc.Col(get_navbar(login=False)),'']
    else :
        return [
            dbc.Col(get_navbar()), 
            get_sidebar()
        ]

@app.callback(
    [
        Output("dash", "active"),
        Output("Customers", "active"),
        Output("Accounts_own", "active"),
        Output("Accounts_stat", "active"),        
        Output("loans", "active"),
        Output("Deposits", "active"),        
        Output("Channel", "active"),
#         Output("Channels", "active"),
        Output("I_click", "active"),
        Output("Mobile", "active"),
        Output("Ussd", "active"),
        Output("MTN", "active"),
#         Output("TIGO", "active"),
        Output("card", "active"),
        Output("card_transactions", "active"),        
        Output("Profitability", "active"),        
    ],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    return pathname == "/Overview",pathname == "/Customers",pathname == "/Accounts_own",pathname == "/Accounts_stat", pathname == "/loans",pathname == "/Deposits",pathname == "/Channel",pathname == "/I_click",pathname == "/Mobile",pathname == "/Ussd",pathname == "/MTN",pathname == "/card",pathname == "/card_transactions",pathname == "/Profitability"

#pathname == "/TIGO",
@app.callback(
    Output('backToTop', 'run'),
    [Input("top", "n_clicks")]
)
def scroll_top(n_clicks):
    if n_clicks: 
        return "document.documentElement.scrollTop = 0"
    return ""


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout',style={"color":"white"})
    else:
        return ''

#########################################################################################################
if __name__ == "__main__":
    app.server.run(debug=True)