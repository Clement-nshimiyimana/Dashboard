import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly import tools
import time
import warnings
warnings.filterwarnings("ignore")

from app import cache1, TIMEOUT, app, session_id
from components import *
from config import *
# import datetime as dt
import pandas as pd


min_date_allow= '2020-01-01'
init_start_date= str(dt.today().year)+'-'+str(dt.today().month)+'-01'
init_end_date= str(dt.today().year)+'-'+str(dt.today().month)+'-'+str(dt.today().day)

    
(card_primary_supp,card_branch,card_status,customers,cards_numb,
 card_product,supply,primary,compr_card,Stol_card,
 Lost_card,clos_card,decl_card,Open_card,Open_card_status,decl_card_status,clos_card_status,
 Lost_card_status,Stol_card_status,compr_card_status,Open_card_branch,decl_card_branch,
 clos_card_branch,Lost_card_branch,Stol_card_branch,compr_card_branch,
 classic_deb_branch,classic_pre_branch,gold_cre_branch,gold_deb_branch,
 classic_deb_state,classic_pre_state,gold_cre_state,gold_deb_state,Card_type)=get_cards_details(session_id)
card_common_layout = html.Div(
	[       
		html.Div(id="card_overview", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
		html.Div([
			html.Div(id="card_info"),
			dcc.Interval(id="update-card_overview", interval=1000*60*60*2, n_intervals=0),
		]),
	],
)

layout= html.Div([
    html.H1('Cards Details'),
    html.Hr(),
#     html.P('This section contains cards details and cards transactions. For cards details, we have a number of all cards and the customers, cards status(opened, declared, lost,...) the number of primary and supplementary cards for all cards types(debit, credit and prepaid). For transactions, we have ATM and POS transactions. Notice:for graphs showing trend overtime, there are buttons 1MONTH, 3MONTH,1YEAR which allows to see the situation in one month, three months ago and so on. In addition,for each graph you can choose one field you want see clearly by double clicking it on legend to disable others.'),
#     html.Hr(), 
	html.Div([
        dcc.DatePickerSingle(
            id='my-date-picker-single',
#                 min_date_allowed=dt(1995, 8, 5),
#                 max_date_allowed=dt(2017, 9, 19),
            initial_visible_month=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'),
            date=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        ),
        html.Div(id='output-container-date-picker-single')
	]),     
    html.H3('Select cards type:'),    
	dbc.Row([
		dbc.Col([
			dcc.Dropdown(
				id= "MOB_CAT",
		        placeholder="Select card type",                
				options=[{'label': i, 'value': i} for i in card_product
				],
# 				value=card_product[0],#cards_details.CARDPRODUCT.unique[0],card_product[0]
                className='three columns'  
# 				style={'display': 'inline-block', 'margin':'10px 10px 10px 10px', 'font-size':20, 'font-style': 'italic'}
			),          
		]),
	]),   
	card_common_layout,
])


@app.callback(
	Output("card_info","children"),
	[
    Input("update-card_overview", "n_intervals"),       
    Input("MOB_CAT", "value"),
	]
)
def card_infos(n,card):
    (card_primary_supp,card_branch,card_status,customers,cards_numb,
     card_product,supply,primary,compr_card,Stol_card,
     Lost_card,clos_card,decl_card,Open_card,Open_card_status,decl_card_status,
     clos_card_status,Lost_card_status,Stol_card_status,compr_card_status,
     Open_card_branch,decl_card_branch,clos_card_branch,Lost_card_branch,
     Stol_card_branch,compr_card_branch,classic_deb_branch,classic_pre_branch,
     gold_cre_branch,gold_deb_branch,classic_deb_state,classic_pre_state,
     gold_cre_state,gold_deb_state,Card_type)=get_cards_details(session_id,card)
    
    colors_primary=['darkblue','lightblue']
    cards=Open_card_status+decl_card_status+Lost_card_status+clos_card_status+Stol_card_status+compr_card_status
    branch=Open_card_branch+decl_card_branch+Lost_card_branch+clos_card_branch+Stol_card_branch+compr_card_branch
    Type=classic_deb_branch+classic_pre_branch+gold_cre_branch+gold_deb_branch
    output= [
		html.Div([]),
        dbc.CardDeck(
            [
                dbc.Card(
                    [
                        html.H6("User customers"),                         
                        html.H3("{:,.0f}".format(customers), style={"color":"DarkBlue"}),
                 
                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
                ),
                dbc.Card(
                    [
                        html.H6("Total number of cards"),                        
                        html.H2("{:,.0f}".format(cards_numb), style={"color":"LightBlue"}),

                    ],
                    body=True,
	            ),
			],
		),

    html.Div([        
    dbc.CardGroup([
        dbc.Card(
            [
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x= Open_card_status.index, 
                                y= Open_card_status,
                                text=get_percentage_label((Open_card_status*100/(cards)).round(2)),
                                name='Opened cards',
                                textposition='auto',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='LightBlue'
                                )
                            ),
                            go.Bar(
                                x= decl_card_status.index, 
                                y= decl_card_status,
                                text=get_percentage_label((decl_card_status*100/(cards)).round(2)),
                                textposition='auto',
                                name='Declared cards',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='darkblue'
                                )
                            ),
                            go.Bar(
                                x= Lost_card_status.index, 
                                y= Lost_card_status,
                                name='Lost cards',
                                text=get_percentage_label((Lost_card_status*100/(cards)).round(2)),
                                textposition='auto',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='#F5D3C7'
                                )
                            ),
                            go.Bar(
                                x= clos_card_status.index, 
                                y= clos_card_status,
                                name='Closed cards',
                                text=get_percentage_label((clos_card_status*100/(cards)).round(2)),
                                textposition='auto',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='darkred'
                                )
                            ),
                            go.Bar(
                                x= Stol_card_status.index, 
                                y= Stol_card_status,
                                text=get_percentage_label((Stol_card_status*100/(cards)).round(2)),
                                textposition='auto',
                                name='Stolen cards',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='grey'
                                )
                            ),
                            go.Bar(
                                x= compr_card_status.index, 
                                y= compr_card_status,
                                text=get_percentage_label((compr_card_status*100/(cards)).round(2)),
                                textposition='auto',
                                name='Compromised cards',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='green'
                                )
                            ),        
                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text="Cards status",
                            # 	xref="paper",
                            # 	x=0
                            ),
#                             orientation='h',
                            xaxis=go.layout.XAxis(
                                title=go.layout.xaxis.Title(
                                    text="Card types",
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=18,
                                    #     color="#7f7f7f"
                                    # )
                                )
                            ),
                            yaxis=go.layout.YAxis(
                                title=go.layout.yaxis.Title(
                                    text="Number of cards",
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=18,
                                    #     color="#7f7f7f"
                                    # )
                                )
                            ), 
                            barmode="stack",
                            showlegend=True,
                            legend=go.layout.Legend(
                                x=0.9,
                                y=1.0,
                                xanchor="center",
                                yanchor="top",
                            ),
                            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                        )
                    ),
                    # style={'height': 400,},
                    id='Transaction_amt_icl',
                ),

                ]),
            ],
            body=True,
            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
        ),        
        dbc.Card(
            [
                html.Div([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Pie(
                                    labels=card_primary_supp.rename(index=card_mapping).index, 
                                    values=card_primary_supp,
                                    text = card_primary_supp,
                                    hoverinfo= "label+percent+text",
                                    hole=0.5,
                                    marker=go.pie.Marker(
                                        colors= colors_primary,
                                        # line=dict(color='#000000', width=1),
                                    ),	
                                    # hoverinfo='label+value',
                                ),
                            ],
                            layout=go.Layout(
                                title="Rate of primary cards vs supplementary",
                                showlegend=True,
                                legend=go.layout.Legend(
                                    x=1.0,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=5, r=5, t=70, b=5),
                            ),
                        ),
#                             style={'height': 300, "top":30},
                        id="customer_cat_pie_icl",
                    )
                ]),
            ],
            body=True,
            style={"padding":"5px 5px 5px 5px", },
        ),
    ]),        
]),

    dbc.CardGroup([
        dbc.Card(
            [
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x= classic_deb_state.index, 
                                y= classic_deb_state,
                                text=classic_deb_state,
#                                 text=get_percentage_label((classic_deb_branch*100/(Type)).round(3)),
                                name='Visa Classic Debit',
                                textposition='auto',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='LightBlue'
                                )
                            ),
                            go.Bar(
                                x= classic_pre_state.index, 
                                y= classic_pre_state,
                                text=classic_pre_state,
#                                 text=get_percentage_label((classic_pre_branch*100/(Type)).round(3)),
                                textposition='auto',
                                name='Visa Classic Prepaid',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='darkblue'
                                )
                            ),
                            go.Bar(
                                x= gold_cre_state.index, 
                                y= gold_cre_state,
                                text=gold_cre_state,
                                name='Visa Gold credit',
#                                 text=get_percentage_label((gold_cre_branch*100/(Type)).round(3)),
                                textposition='auto',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='#F5D3C7'
                                )
                            ),
                            go.Bar(
                                x= gold_deb_state.index, 
                                y= gold_deb_state,
                                text=gold_deb_state,
                                name='Visa Gold debit',
#                                 text=get_percentage_label((gold_deb_branch*100/(Type)).round(2)),
                                textposition='auto',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='darkred'
                                )
                            ),        
                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text="Cards states",
                            # 	xref="paper",
                            # 	x=0
                            ),
                            barmode='relative',
                            xaxis=go.layout.XAxis(
                                title=go.layout.xaxis.Title(
                                    text="State",
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=18,
                                    #     color="#7f7f7f"
                                    # )
                                )
                            ),
                            yaxis=go.layout.YAxis(
                                title=go.layout.yaxis.Title(
                                    text="Number of cards",
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=18,
                                    #     color="#7f7f7f"
                                    # )
                                )
                            ), 
                            # barmode="stack",
                            showlegend=True,
                            legend=go.layout.Legend(
                                x=0.9,
                                y=1.0,
                                xanchor="center",
                                yanchor="top",
                            ),
                            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                        )
                    ),
                    # style={'height': 400,},
                    id='Transaction_amt_icl',
                    animate = True,
#                    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Channel usage based on customers age" )}),
                ),

                ]),
            ],
            body=True,
            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
        ),
    ]),        
        
    dbc.CardGroup([
        dbc.Card(
            [
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x= Open_card_branch.index, 
                                y= Open_card_branch,
                                text=Open_card_branch,
#                                 text=get_percentage_label((Open_card_branch*100/(branch)).round(3)),
                                name='Opened cards',
                                textposition='auto',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='LightBlue'
                                )
                            ),
                            go.Bar(
                                x= decl_card_branch.index, 
                                y= decl_card_branch,
                                text=decl_card_branch,
#                                 text=get_percentage_label((decl_card_branch*100/(branch)).round(3)),
                                textposition='auto',
                                name='Declared cards',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='darkblue'
                                )
                            ),
                            go.Bar(
                                x= Lost_card_branch.index, 
                                y= Lost_card_branch,
                                text=Lost_card_branch,
                                name='Lost cards',
#                                 text=get_percentage_label((Lost_card_branch*100/(branch)).round(3)),
                                textposition='auto',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='#F5D3C7'
                                )
                            ),
                            go.Bar(
                                x= clos_card_branch.index, 
                                y= clos_card_branch,
                                text=clos_card_branch,
                                name='Closed cards',
#                                 text=get_percentage_label((clos_card_branch*100/(branch)).round(3)),
                                textposition='auto',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='darkred'
                                )
                            ),
                            go.Bar(
                                x= Stol_card_branch.index, 
                                y= Stol_card_branch,
                                text=Stol_card_branch,
#                                 text=get_percentage_label((Stol_card_branch*100/(branch)).round(3)),
                                textposition='auto',
                                name='Stolen cards',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='grey'
                                )
                            ),
                            go.Bar(
                                x= compr_card_branch.index, 
                                y= compr_card_branch,
                                text=compr_card_branch,
#                                 text=get_percentage_label((compr_card_branch*100/(branch)).round(3)),
                                textposition='auto',
                                name='Compromised cards',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='green'
                                )
                            ),        
                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text="Cards status on bank's branch level",
                            # 	xref="paper",
                            # 	x=0
                            ),
                            barmode='relative',
                            xaxis=go.layout.XAxis(
                                title=go.layout.xaxis.Title(
                                    text="Branch name",
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=18,
                                    #     color="#7f7f7f"
                                    # )
                                )
                            ),
                            yaxis=go.layout.YAxis(
                                title=go.layout.yaxis.Title(
                                    text="Number of cards",
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=18,
                                    #     color="#7f7f7f"
                                    # )
                                )
                            ), 
                            # barmode="stack",
                            showlegend=True,
                            legend=go.layout.Legend(
                                x=0.9,
                                y=1.0,
                                xanchor="center",
                                yanchor="top",
                            ),
                            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                        )
                    ),
                    # style={'height': 400,},
                    id='Transaction_amt_icl',
                    animate = True,
#                    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Channel usage based on customers age" )}),
                ),

                ]),
            ],
            body=True,
            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
        ),
    ]),
    dbc.CardGroup([
        dbc.Card(
            [
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x= classic_deb_branch.index, 
                                y= classic_deb_branch,
                                text=classic_deb_branch,
#                                 text=get_percentage_label((classic_deb_branch*100/(Type)).round(3)),
                                name='Visa Classic Debit',
                                textposition='auto',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='LightBlue'
                                )
                            ),
                            go.Bar(
                                x= classic_pre_branch.index, 
                                y= classic_pre_branch,
                                text=classic_pre_branch,
#                                 text=get_percentage_label((classic_pre_branch*100/(Type)).round(3)),
                                textposition='auto',
                                name='Visa Classic Prepaid',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='darkblue'
                                )
                            ),
                            go.Bar(
                                x= gold_cre_branch.index, 
                                y= gold_cre_branch,
                                text=gold_cre_branch,
                                name='Visa Gold credit',
#                                 text=get_percentage_label((gold_cre_branch*100/(Type)).round(3)),
                                textposition='auto',
                                visible='legendonly',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='#F5D3C7'
                                )
                            ),
                            go.Bar(
                                x= gold_deb_branch.index, 
                                y= gold_deb_branch,
                                text=gold_deb_branch,
                                name='Visa Gold debit',
#                                 text=get_percentage_label((gold_deb_branch*100/(Type)).round(2)),
                                textposition='auto',
    # 			                    mode= "lines",
                                marker=go.bar.Marker(
                                    color='darkred'
                                )
                            ),        
                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text="Number of cards issued on bank's branch level",
                            # 	xref="paper",
                            # 	x=0
                            ),
                            barmode='relative',
                            xaxis=go.layout.XAxis(
                                title=go.layout.xaxis.Title(
                                    text="Branch name",
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=18,
                                    #     color="#7f7f7f"
                                    # )
                                )
                            ),
                            yaxis=go.layout.YAxis(
                                title=go.layout.yaxis.Title(
                                    text="Number of cards",
                                    # font=dict(
                                    #     family="Courier New, monospace",
                                    #     size=18,
                                    #     color="#7f7f7f"
                                    # )
                                )
                            ), 
                            # barmode="stack",
                            showlegend=True,
                            legend=go.layout.Legend(
                                x=0.9,
                                y=1.0,
                                xanchor="center",
                                yanchor="top",
                            ),
                            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                        )
                    ),
                    # style={'height': 400,},
                    id='Transaction_amt_icl',
                    animate = True,
#                    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Channel usage based on customers age" )}),
                ),

                ]),
            ],
            body=True,
            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
        ),
    ]),        
        
# ]),
# ]),  
#     end = time.time()     
#     print("fivec", end - start) 
                   

 ############################## customer's category###################################################################

]        
#     end = time.time()
#     print("sixc", end - start)
    return output