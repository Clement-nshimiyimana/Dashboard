import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import base64
from assets import *


IMBANK_LOGO = "http://seekvectorlogo.com/wp-content/uploads/2018/01/im-bank-limited-vector-logo-small.png"

def Header():
    return html.Div([
        get_header(),
        html.Br([]),
        get_menu()
    ])


def get_header():
    header = html.Div([
        html.I(className='fa fa-home', **{'aria-hidden': 'true'}, children=None),# Home icon
        html.Div([
            html.H5(
                'IM Bank Plc (Rwanda) ')
        ], className="banner"),

    ], className="row gs-header gs-text-header")
    return header

def get_sidebar(): #  THIS IS A SIDEBAR(OVERVIEW, CUSTOMER,...)
    
    sidebar = dbc.NavbarBrand(
        [
            dbc.NavLink("Overview",id="dash", href="/Overview", className="my-1"),
#             dbc.NavLink("Overview",id="dash", href="/Overview", className="fa fa-fw fa-home"><i class="fa fa-fw fa-home"></i> Overview</a>),
#             dbc.NavLink("Overview",id="dash", href="/Overview", className="fa fa-fw fa-home"),              
            dbc.NavLink("Customers",id="Customers", href="/Customers", className="my-1"),
            dbc.DropdownMenu(
            [dbc.NavLink("Accounts types",id="Accounts_own", href="/Accounts_own", className="caret"), dbc.NavLink("Accounts Status",id="Accounts_stat", href="/Accounts_stat", className="caret")],
            label="Accounts",
            nav=True,
        ),             
            dbc.NavLink("Loans", id="loans", href="/loans", className="my-1"),
            dbc.NavLink("Deposits", id="dash", href="/Deposits", className="my-1"),            
            dbc.DropdownMenu(
            [dbc.NavLink("Summary",id="channel", href="/channels", className="caret"),
             dbc.NavLink("I_click",id="I_click", href="/I_click", className="caret"), dbc.NavLink("Mobile App",id="Mobile", href="/Mobile", className="caret"),dbc.NavLink("USSD",id="Ussd", href="/Ussd", className="caret"),dbc.NavLink("Push& Pull",id="MTN", href="/MTN", className="caret")],
            label="Channels",
            nav=True,
        ), 
            dbc.DropdownMenu(
            [dbc.NavLink("card details",id="card", href="/card", className="caret"),
             dbc.NavLink("card transactions",id="card_transactions", href="/card_transactions", className="caret")],
            label="Cards",
            nav=True,
        ),            
            dbc.NavLink("Revenue&Expense", id="Profitability", href="/Profitability", className="my-1"),            

        ],
        id="sideNavBar",
        className="sidebar navbar-expand-lg navbar-light bg-light",          
#         className="sidebar navbar-expand-lg navbar-dark bg-green ",        
#         className="sidebar navbar-expand-lg navbar-dark bg-primary ",
        style={
            "list-style-type":"none",
#             "background-image":"url('images.jpg')",
#             "background-repeat": "no-repeat",
#             "background-position": "right top",
#             "background-size": "150px 150px",
            "background-size": "150px 150px",            
            "background-color": "#0074D9",              
            "overflow": "hidden",
            "position": "absolute",
            "top": "5px",
            "overflow-y": "scroll",
            "height":"auto",
        }
    )
    return sidebar


def get_navbar(login=True):
    if login:
        navbar = dbc.Navbar(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=IMBANK_LOGO, height="50px")),
                        ],
#                         align="center",
#                         no_gutters=True,
                    ),
                    # href="https://www.imbank.com/rwanda/",
                    href="#",
                ),
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link', style={"margin":"0px 0px 0px 70%",}),
            ],
            color="#0074D9", ##0000ae
#             dark=False,
            className="navbar navbar-expand navbar-dark flex-column flex-md-row bd-navbar",
            # style={
            #     "overflow": "hidden",
            #     "position": "fixed",
            # }
        )
        return navbar
    else:
        navbar = dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=IMBANK_LOGO, height="50px")),
                        ],
#                         align="center",
#                         no_gutters=True,
                    ),
                    # href="https://www.imbank.com/rwanda/",
                    href="#",
                ),

            ],
            color="#0074D9",
#             dark=False,
            className="navbar navbar-expand navbar-dark flex-column flex-md-row bd-navbar",
            # style={
            #     "overflow": "hidden",
            #     "position": "fixed",
            # }
        )
        return navbar

def get_menu():
    search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
    )
    get_navbar()
    get_sidebar()
    
