from plotly.subplots import make_subplots
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly import tools
from plotly.subplots import make_subplots  
import plotly.io as pio
import warnings
warnings.filterwarnings("ignore")

import numpy as np

from app import app, session_id
from components import *
from config import * 

pio.templates.default = "plotly_white"
(customer_Opening,account_Opening,customer_open,account_open,active_cust,inactive_cust,active,inactive,dormant,active_cust,inactive_cust,dormant_cust) = get_customer_account_trend_data(session_id)

layout = html.Div(
	[	        
		html.H1("Overview",id="general_overview"),
		html.Hr(),        
#     html.P('This section is a general overview of customers and accounts including customer trends, accounts status, age and gender segmentation at I&M bank. To view information based on business category, choose one of the radio buttons i.e. ALL, RETAIL, SME, CORPORATE. For graphs showing trends overtime, buttons 1 MONTH, 3 MONTHS, 6 MONTHS, 1 YEAR and ALL allow one to see trends over one month, three months and so on. In addition, for each graph you can choose one field you want to see clearly by disabling others i.e. click on an item in the legend to disable it.'),  
# 		html.Hr(),
		dbc.Row([
			dbc.Col([
				dcc.RadioItems(
					id= "select-cust_type",
					options=[
					    {'label': 'ALL', 'value': 'ALL'},
					    {'label': 'RETAIL', 'value': 'R'},
					    {'label': 'CORPORATE', 'value': 'C'},
					    {'label': 'MSME', 'value': 'S'},
					],
					value='ALL',
					labelStyle={'display': 'inline-block', 'margin':'10px 10px 10px 10px', 'font-size':20, 'font-style': 'italic'}
				),
			]),            
		]),
        html.Div([]),
#         html.H5("{}".format(customer_Opening.index[-1].strftime("%b %d (%a), %Y")),style={"color":"#004206"}),
        html.Div([]),        
		html.Div([
			html.Div(id="overview_info"),
			dcc.Interval(id="update-overview_info", interval=1000*60*60*2, n_intervals=0),
		]),

		html.Div([
			html.Div(id="new_opening_trend-line"),
			dcc.Interval(id="update-new_opening_trend", interval=1000*60*60*2, n_intervals=0),
		]),
		html.Div([
			html.Div(id="num_accounts"),
			dcc.Interval(id="update-num_accounts", interval=1000*60*60*2, n_intervals=0),
		]),         
		html.Div([
			html.Div(id="overview_graph"),
			dcc.Interval(id="update-overview_graph", interval=1000*60*60*2, n_intervals=0),
		]),                    

	],
)
#################################################################################################################
###################### layout callback ###########################################################################
##################################################################################################################

############################################Customer and accounts trend#################################################
@app.callback(
    Output("new_opening_trend-line","children"),
    [
    	Input('update-new_opening_trend', 'n_intervals'),
    	Input("select-cust_type", "value"),
    ]
)
def update_new_opening_trend_graph(n, cust_type):

	(customer_Opening,account_Opening,customer_open,account_open,active_cust,inactive_cust,active,inactive,dormant,active_cust,inactive_cust,dormant_cust) = get_customer_account_trend_data(session_id, cust_type)
    
	output = html.Div([
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([       
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Scatter(
                                        x= customer_open.index, 
                                        y= customer_open.values,
                                        name='New Customers',
                                        mode= "lines",
                #                         hoverinfo = 'text',
                                        fill="tonexty",
                                        marker=go.scatter.Marker(
                                            color='#000080'
                                        )
                                    ),
                	                go.Scatter(
                	                    x= account_open.index, 
                	                    y= account_open.values,
                	                    name='New Accounts',
                #                         hoverinfo = 'text',
                	                    mode= "lines",
                                        fill='tonexty',
                                        visible='legendonly',
                	                    marker=go.scatter.Marker(
                	                        color='#494c53'
                	                    )
                	                ),
                                ],
                                layout=go.Layout(
                                    showlegend=True,
                                    autosize=True,
                #                     type='aggregate',
                #                     groups=account_open.index, 
                #                     target='y', 
                #                     func='sum',
                #                     enabled=True,
                # 	                xaxis_rangeslider_visible=True,
                                    legend=go.layout.Legend(x=0.8,y=1.0),
                                    margin=go.layout.Margin(l=10, r=10, t=60, b=10),
                                    title=go.layout.Title(
                                        text="New Customers over time[{}]".format(cust_type),
                                    # 	xref="paper",
                # 						x=0,
                #                         y=0.99,
                                    ),
                                    xaxis=go.layout.XAxis(
                                        rangeselector=dict(
                                            buttons=list([
                                                dict(count=1,
                                                     label="1 MONTH",
                                                     step="month",
                                                     stepmode="backward"),
                                                dict(count=3,
                                                     label="3 MONTHS",
                                                     step="month",
                                                     stepmode="backward"),                                
                                                dict(count=6,
                                                     label="6 MONTHS",
                                                     step="month",
                                                     stepmode="backward"),
                                                dict(count=1,
                                                     label="1YEAR",
                                                     step="year",
                                                     stepmode="backward"),
                                                dict(step="all")
                                            ])
                                        ),
                                        rangeslider=dict(
                                            visible=True
                                        ),
                                        type="date"

                                    ),
                					yaxis=go.layout.YAxis(
                                        mirror="ticks",
                						title=go.layout.yaxis.Title(
                							text="New Customers/New Accounts",
                							# font=dict(
                							#     family="Courier New, monospace",
                							#     size=18,
                							#     color="#7f7f7f"
                							# )
                						)
                					)
                                )
                            ),

                	    ),
                    ],style={'padding': 10})
                ],
                body=True,
                style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},                
            ),
        ]),
# 		dbc.CardGroup([
# 			dbc.Card(
#                 [
#                     html.Div([       
#                         dcc.Graph(
#                             figure=go.Figure(
#                                 data=[
#                                     go.Scatter(
#                                         x= customer_Opening.index, 
#                                         y= np.cumsum(customer_Opening.values),
#                                         name='Customers',
#                                         text=customer_Opening.pct_change().round(1),
#                                         mode="lines",
#                 #                         fill="toself",tonexty
#                                         fill="tozeroy",
#                                         marker=go.scatter.Marker(
#                                             color='#000080'
#                                         )
#                                     ),
#                 	                go.Scatter(
#                 	                    x= account_Opening.index, 
#                 	                    y= np.cumsum(account_Opening),
#                                         text=account_Opening.pct_change().round(1),
#                 	                    name='Accounts',
#                 	                    mode= "lines",
#                                         fill="tonexty",
# #                                         visible='legendonly',
#                 	                    marker=go.scatter.Marker(
#                 	                        color='#494c53'
#                 	                    )
#                 	                ),
#                                 ],
#                                 layout=go.Layout(
#                                     showlegend=True,
#                 #                     annotations=[
#                 #                         dict(
#                 #                             x=0,
#                 #                             y=0,
#                 #                             xref="x",
#                 #                             yref="y",
#                 #                             text="initial",
#                 #                             showarrow=True,
#                 #                             arrowhead=7,
#                 #                             ax=0,
#                 #                             ay=-40
#                 #                         )
#                 #                     ],                      
#                                     xaxis_rangeslider_visible= True,
#                                     legend=go.layout.Legend(
#                                         x=0,
#                                         y=1.0
#                                     ),
#                                     margin=go.layout.Margin(l=10, r=10, t=60, b=10),

#                                     title=go.layout.Title(
#                                         text="Customers Over Time[{}]".format(cust_type),
#                                     # 	xref="paper",
#                 # 						x=0,
#                 #                         y=0.99
#                                     ),
#                                     xaxis=go.layout.XAxis(
# #                                         nticks=24,
# #                                         type="date"
# #                                         ),                                                     
#                 # 	                	tickmode= "auto",
#                 						title=go.layout.xaxis.Title(
#                 							text="Years",
#                 							# font=dict(
#                 							#     family="Courier New, monospace",
#                 							#     size=18,
#                 							#     color="#7f7f7f"
#                 							# )
#                 						)
#                                     ),
#                 					yaxis=go.layout.YAxis(
#                                         mirror=True,
#                 						title=go.layout.yaxis.Title(
#                 							text="Customers/Accounts", 
#                 							# font=dict(
#                 							#     family="Courier New, monospace",
#                 							#     size=18,
#                 							#     color="#7f7f7f"
#                 							# )
#                 						)
#                 					)
#                                 )

#                             ),

#                 	    ),
#                     ],style={'padding': 10})
#                 ],
#                 body=True,
#                 style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},                  
#             ),
#         ]),               
    ])
	return output

@app.callback(
	[
		Output("overview_info","children"),
	],
	[
		Input("update-overview_info", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)                                          
def update_overview_info(n, cust_type):
    (customer_Opening,account_Opening,customer_open,account_open,active_cust,inactive_cust,active,inactive,dormant,active_cust,inactive_cust,dormant_cust) = get_customer_account_trend_data(session_id, cust_type)

    positive_amt, negative_amt = get_account_cleared_balance_lcy(session_id, cust_type)
    
#     PL=get_deposit_loans(session_id, cust_type)
    loan_depos=get_loan_dep_trend(session_id, cust_type)    
#     Deposits=PL[PL.FRL_ATTRIBUTE_05=='FA052010'].BALANCE_LCY.sum()# Total deposits.
#     Loans=-1*PL[PL.FRL_ATTRIBUTE_05=='FA051050'].BALANCE_LCY.sum() # Total loans.   
    Deposits=loan_depos[(loan_depos.FRL_ATTRIBUTE_05=='FA052010')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()# Total deposits.
    Loans=-1*loan_depos[(loan_depos.FRL_ATTRIBUTE_05=='FA051050')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum() # Total loans.        

    return [dbc.CardDeck(
			[
                                                          
                dbc.Card(
                    [                        

                        html.H5("Total number of Customers"),                        
                        html.H2("{:,.0f}".format(customer_Opening.sum())),
#                         html.H6("Total number of Customers"), 
                        html.H5("New Customers"),                        
                        html.H3(" {:,.0f}".format(customer_open[-1]), style={"color":"#004206"}),
                       
                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
                ), 
                dbc.Card(
                    [
#                         html.H3("{}".format(account_Opening.index[-1].strftime("%b %d (%a), %Y"))),
                        html.Div([]),                        
                        html.H5("Total number of Accounts"),                        
                        html.H2("{:,.0f}".format(account_Opening.sum())),
#                         html.H6("Total number of Accounts"),
                        html.H5("New Accounts"),                        
                        html.H3(" {:,.0f}".format(account_open[-1]), style={"color":"#004206"}),
                      
                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.Div([]),                        
                        html.H5("Total Deposit Amount"),                                             
                        html.H3("Rwf {:,.0f}".format(Deposits), style={"color":"#000080"}),#positive_amt
#                         html.H6("Total Deposit Amount in million"),
                        html.H5("Total Loan Amount"),                        
                        html.H3("Rwf {:,.0f}".format(Loans), style={"color":"blueviolet"}),#-1*negative_amt
#                         html.H6("Total Overdraft Amount in million"),
                        html.H5("Loans to deposits ratio(LTD)"),                        
                        html.H3("{:,.0f} %".format((Loans/Deposits)*100), style={"color":"blue"}),                        
                    ],
                    body=True,
                ),
			],
			
		), 
    ]


###################################################################################################
@app.callback(
	Output("num_accounts","children"),
	[
		Input("update-num_accounts", "n_intervals"),
		Input("select-cust_type", "value"),
#         Input("year_range","value"),        
	]
)

def update_num_accounts_graph(n, cust_type):

	customers, num_accounts= get_customer_sbu_gender_age_segment(session_id, cust_type)    
	loan_depos=get_loan_dep_trend(session_id, cust_type)
# 	customers, num_accounts,active_num,inactive_num,dorm_num,clos_num = get_customer_sbu_gender_age_segment(session_id, cust_type)
	loan_depos["VALUE_DATE"]=pd.to_datetime(loan_depos.VALUE_DATE,errors="coerce")      
	loan_overtime=-1*loan_depos[(loan_depos.FRL_ATTRIBUTE_05=='FA051050')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()
	depo_overtime=loan_depos[(loan_depos.FRL_ATTRIBUTE_05=='FA052010')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()
	income_overtime,income_trend=get_income_trend(session_id, cust_type)
	fees_overtime,fees_trend=get_fees_trend(session_id, cust_type)
	custom=customers[customers.CUSTOMER_OPEN_DATE>='2020-03-01'].groupby('CUSTOMER_OPEN_DATE').CUSTOMER_ID.nunique()
	account=customers[customers.CUSTOMER_OPEN_DATE>='2020-03-01'].groupby('CUSTOMER_OPEN_DATE').ACCOUNT_NO.nunique() 


	fig=make_subplots(rows=3,
                     cols=1,
                     shared_xaxes=True,
                     vertical_spacing=0.005)
	fig.add_trace(
        go.Scatter(
        x=loan_overtime.index,
        y=loan_overtime,
        name='Loans amount(Billion rwf)',
        mode='lines',
        marker=go.scatter.Marker(
            color='#000080'
        )
        ),
        2,
        1
	)

	fig.add_trace(
        go.Scatter(
        x=depo_overtime.index,
        y=depo_overtime,
        name='Deposits amount(Billion rwf)',
        mode='lines',
        marker=go.scatter.Marker(
            color='#45b6fe'
        )
        ),
        1,
        1
	)
# 	fig.add_trace(
#         go.Scatter(
#         x=(income_trend+fees_trend).index,
#         y=(income_trend+fees_trend),
#         name='Revenue(Billion rwf)',
#         mode='lines',
#         connectgaps=True,    
#         marker=go.scatter.Marker(
#             color='darkgreen'
#         )
#         ),
#         3,
#         1
# 	)    

	fig.add_trace(
        go.Scatter(
        x=custom.index,
        y=custom,
        name='Customers',
        mode='lines',
        marker=go.scatter.Marker(
            color='#8c6464'
        )
        ),
        3,
        1
	)

	fig.add_trace(
        go.Scatter(
        x=account.index,
        y=account,
        name='Accounts',
        mode='lines',
        marker=go.scatter.Marker(
            color='grey'
        )
        ),
        3,
        1
	)

	fig.layout.update(title="Performance trend[{}]".format(cust_type),
                        showlegend=True,
                        legend_orientation="h",
                        height=700,
#                         xaxis_rangeslider_visible= True,
#                         legend=go.layout.Legend(
#                             x=0,
#                             y=0.95
#                         ),
                        margin=go.layout.Margin(l=10, r=10, t=60, b=10),
#                         xaxis=go.layout.XAxis(
#                             type="category",
#                             categoryorder='category ascending',
#                         ),
#                         type="category",
#                         categoryorder='category ascending',                       
#                         xaxis=go.layout.XAxis(
#                             rangeselector=dict(
#                                 buttons=list([
#                                     dict(count=1,
#                                          label="1 MONTH",
#                                          step="month",
#                                          stepmode="backward"),
#                                     dict(count=3,
#                                          label="3 MONTHS",
#                                          step="month",
#                                          stepmode="backward"),                                
#                                     dict(count=6,
#                                          label="6 MONTHS",
#                                          step="month",
#                                          stepmode="backward"),
#                                     dict(count=1,
#                                          label="1YEAR",
#                                          step="year",
#                                          stepmode="backward"),
#                                     dict(step="all")
#                                 ])
#                             ),
#                             rangeslider=dict(
#                                 visible=True
#                             ),
#                             type="date"

#                         ),                      
                     )

	output =  html.Div([
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([       
                        dcc.Graph(
                            figure=fig
#                             figure=go.Figure(
#                                 data=[
#                                     go.Scatter(
#                                         x= depo_overtime.index, 
#                                         y= depo_overtime//1e10,
#                                         text=depo_overtime.round(),
#                                         name='Deposits amount(10Billion Rwf)',
# #                                         text=customer_Opening.pct_change(),
#                                         mode="lines",
#                 #                         fill="toself",tonexty
# #                                         fill="tozeroy",
#                                         marker=go.scatter.Marker(
#                                             color='#45b6fe'
#                                         )
#                                     ),
#                                     go.Scatter(
#                                         x=loan_overtime.index,
#                                         y=loan_overtime//1e10,
#                                         text=loan_overtime.round(),
#                                         name='Loans amount(10Billion Rwf)',
#                                         mode='lines',
#                                         marker=go.scatter.Marker(
#                                             color='#000080'
#                                         )
#                                     ),                                    
#                 	                go.Scatter(
#                 	                    x= (income_trend+fees_trend).index, 
#                 	                    y= (income_trend+fees_trend)//1e9,
#                                         text=(income_trend+fees_trend).round(),
#                                         connectgaps=True,
#                 	                    name='Revenues(Billion Rwf)',
#                 	                    mode= "lines",
# #                                         fill="tonexty",
# #                                         visible='legendonly',
#                 	                    marker=go.scatter.Marker(
#                 	                        color='darkgreen'
#                 	                    )
#                 	                ),                            
#                                     go.Scatter(
#                                         x= custom.index, 
#                                         y= custom,
#                                         text=custom,
#                                         name='Customers',
#                                         mode= "lines",
#                         #                 row=1,
#                         #                 col=1,                
#                         #                 fill="tonexty",
#                         #                 visible='legendonly',
#                                         marker=go.scatter.Marker(
#                                             color='#8c6464'
#                                         )
#                                     ),
#                         #             secondary_y=True,
#                                     go.Scatter(
#                                         x= account.index, 
#                                         y= account,
#                                         name='Accounts',
#                                         mode= "lines",
#                         #                 row=1,
#                         #                 col=1,             
#                         #                 fill="tonexty",
#                         #                 visible='legendonly',
#                                         marker=go.scatter.Marker(
#                                             color='grey'
#                                         )
#                                     ),                                    
#                                 ],
#                                 layout=go.Layout(
#                                     showlegend=True,
# #                                     height=800,
#                                     legend_orientation="h",
#                 #                     annotations=[
#                 #                         dict(
#                 #                             x=0,
#                 #                             y=0,
#                 #                             xref="x",
#                 #                             yref="y",
#                 #                             text="initial",
#                 #                             showarrow=True,
#                 #                             arrowhead=7,
#                 #                             ax=0,
#                 #                             ay=-40
#                 #                         )
#                 #                     ],                      
#                                     xaxis_rangeslider_visible= True,
#                                     legend=go.layout.Legend(
#                                         x=0,
#                                         y=0.95
#                                     ),
#                                     margin=go.layout.Margin(l=10, r=10, t=60, b=10),

#                                     title=go.layout.Title(
#                                         text="Performance trend[{}]".format(cust_type),
#                                     # 	xref="paper",
#                 # 						x=0,
#                 #                         y=0.99
#                                     ),
#                                     xaxis=go.layout.XAxis(
#                                         rangeselector=dict(
#                                             buttons=list([
#                                                 dict(count=1,
#                                                      label="1 MONTH",
#                                                      step="month",
#                                                      stepmode="backward"),
#                                                 dict(count=3,
#                                                      label="3 MONTHS",
#                                                      step="month",
#                                                      stepmode="backward"),                                
#                                                 dict(count=6,
#                                                      label="6 MONTHS",
#                                                      step="month",
#                                                      stepmode="backward"),
#                                                 dict(count=1,
#                                                      label="1YEAR",
#                                                      step="year",
#                                                      stepmode="backward"),
#                                                 dict(step="all")
#                                             ])
#                                         ),
#                                         rangeslider=dict(
#                                             visible=True
#                                         ),
#                                         type="date"

#                                     ),
#                 					yaxis=go.layout.YAxis(
#                                         mirror=True,
# #                 						title=go.layout.yaxis.Title(
# #                 							text="Deposits/Loans", 
# #                 							# font=dict(
# #                 							#     family="Courier New, monospace",
# #                 							#     size=18,
# #                 							#     color="#7f7f7f"
# #                 							# )
# #                 						)
#                 					)
#                                 )

#                             ),
# #                     #             style={'height': 300, "top":30},
# #                 # 	        id="trend-graph-2",
# #                 # 	        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
                	    ),
                    ],style={'padding': 10})
                ],
                body=True,
                style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},                  
            ),
        ]),##################################################
	])

	return output


###################################################################################################
@app.callback(
	Output("overview_graph","children"),
	[
		Input("update-overview_graph", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_graph(n, cust_type):

	colors_sbu=['#45b6fe', '#000080', 'blueviolet']
	colors_gender=['#45b6fe', '#000080', 'violet']
# 	colors_acc=['#45b6fe','#000080','blueviolet', '#494c53']    
	colors_acc=['#45b6fe','#000080','#494c53']    

	positive_amt, negative_amt =get_account_cleared_balance_lcy(session_id, cust_type)

    
# 	colors_interest=['grey','darkred']    
	colors_overd = ["#000080","#45b6fe"]
	(card_primary_supp,card_branch,card_status,customers,cards_numb,
     card_product,supply,primary,compr_card,Stol_card,Lost_card,clos_card,decl_card,Open_card,
     Open_card_status,decl_card_status,clos_card_status,Lost_card_status,Stol_card_status,compr_card_status,
     Open_card_branch,decl_card_branch,clos_card_branch,Lost_card_branch,Stol_card_branch,compr_card_branch,
     classic_deb_branch,classic_pre_branch,gold_cre_branch,gold_deb_branch,
     classic_deb_state,classic_pre_state,gold_cre_state,gold_deb_state,Card_type)=get_cards_details(session_id)
    
	users=get_och_registered(session_id)

	if cust_type == 'R':
		sbu_output= dbc.CardGroup(
			[

            ],
        )

		gender_output= dbc.CardGroup(
			[
            
            ],
        )
		gender_output1= dbc.CardGroup(
            [            
            ],
        )    
	elif cust_type == 'ALL':
		sbu_output= dbc.CardGroup(
			[
            ]
        )
		html.Div([]),        
		html.Div([html.H3(['Cards & Channels'])]),
		html.Div([])         
		gender_output=dbc.CardGroup([
                dbc.Card(
                    [
                        html.Div([
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Bar(
                                            x=Card_type.index,
                                            y=Card_type,
                                            name='Cards',
                                            text=Card_type,
                                            textposition='outside',
              #   							base=0,
              #   							width = 0.4,
                                            # offset = -0.4,
                                            marker=go.bar.Marker(
                                                color="#45b6fe"
                                            )
                                        ),
                                    ],
                                    layout=go.Layout(
                                        # barmode="stack",
                                        showlegend=False,
                                        legend=go.layout.Legend(
                                            x=1.0,
                                            y=1.0,
                                            xanchor="center",
                                            yanchor="top",
                                        ),
                                        margin=go.layout.Margin(l=40, r=0, t=40, b=30),
    # 						            barmode="stack",                                    
                                        title=go.layout.Title(
                                            text="Card types",
                                        # 	xref="paper",
    # 										x=0.5
                                        ),
                                        xaxis=go.layout.XAxis(
                                            title=go.layout.xaxis.Title(
                                                text="Card",
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
                                        )
                                    )
                                ),
                                # style={'height': 400,},
#                                 id='my-graph_1',
#                                 config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Customers at Branch level" )}),
                            ),
                            ], 
                            id="loan",
                            # style={'width': 700,},
                        ),
                    ],
                    body=True,
                    style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
                ),
                dbc.Card(
                    [
                        html.Div([
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Bar(
                                            x=users.index,
                                            y=users,
                                            name='Channels',
                                            text=users,
                                            textposition='outside',
              #   							base=0,
              #   							width = 0.4,
                                            # offset = -0.4,
                                            marker=go.bar.Marker(
                                                color="#45b6fe"
                                            )
                                        ),
                                    ],
                                    layout=go.Layout(
                                        # barmode="stack",
                                        showlegend=False,
                                        legend=go.layout.Legend(
                                            x=1.0,
                                            y=1.0,
                                            xanchor="center",
                                            yanchor="top",
                                        ),
                                        margin=go.layout.Margin(l=40, r=0, t=40, b=30),
    # 						            barmode="stack",                                    
                                        title=go.layout.Title(
                                            text="Total registered on each channel",
                                        # 	xref="paper",
    # 										x=0.5
                                        ),
                                        xaxis=go.layout.XAxis(
                                            title=go.layout.xaxis.Title(
                                                text="Channel",
                                                # font=dict(
                                                #     family="Courier New, monospace",
                                                #     size=18,
                                                #     color="#7f7f7f"
                                                # )
                                            )
                                        ),
                                        yaxis=go.layout.YAxis(
                                            title=go.layout.yaxis.Title(
                                                text="Number of registered",
                                                # font=dict(
                                                #     family="Courier New, monospace",
                                                #     size=18,
                                                #     color="#7f7f7f"
                                                # )
                                            )
                                        )
                                    )
                                ),
                                # style={'height': 400,},
#                                 id='my-graph_1',
#                                 config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Customers at Branch level" )}),
                            ),
                            ], 
                            id="loan",
                            # style={'width': 700,},
                        ),
                    ],
                    body=True,
                    style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
                ),            
            
            ])        

		gender_output1= dbc.CardGroup(
            [           
            ],
        )    
	else:
		sbu_output= dbc.CardGroup([])
		gender_output= dbc.CardGroup([])
		gender_output1= dbc.CardGroup([])               
    
	if cust_type == 'All':        
		deposit_output= dbc.CardGroup(
			[                
        ])                
                    
	else:
		deposit_output=dbc.CardGroup([])
        
	output =  html.Div([
		sbu_output,
        html.Div([]),        
        html.Div([html.H3(['Cards&Channels'])]),
        html.Div([]),         
		######################################################         
		gender_output,
		gender_output1,
#         html.Div([]),        
#         html.Div([html.H3(['Deposits vs Loans'])]),
#         html.Div([]),            
        deposit_output,        
		##############################################################
#         fig = make_subplots(
#     rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02
# )
# 		dbc.CardGroup([
# 			dbc.Card(
#                 [
#                     html.Div([
#                     	dcc.Graph(
# 						    figure=go.Figure(                 
# #                                 make_subplots(
# # #                                     rows=2,
# # #                                     cols=1,
# # #                                     specs=xy,
# #                                     shared_xaxes=True,
# #                                     shared_yaxes=True, 
# #                                     vertical_spacing=0.001,
# #                                 ),
# 						        data=[
# 						            go.Bar(
# 						                x=deposit_branch.rename(index=branch_name_mapping).index,
# 						                y=(deposit_branch/1e9).round(),
# 						                name='Deposit amount-other branches',
# 						                text=(deposit_branch/1e9).round(),
#             							textposition='outside',
# #                                         row=1,
# #                                         col=1,
#           #   							base=0,
#           #   							width = 0.4,
# 										# offset = -0.4,
# 						                marker=go.bar.Marker(
# 						                    color="#45b6fe"
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=overdraft_branch.rename(index=branch_name_mapping).index,
# 						                y=(overdraft_branch/1e9).round(),
# 						                name='Loan amount-other branches',
# 						                text=(overdraft_branch/1e9).round(),
#             							textposition='outside',
# #                                         row=1,
# #                                         col=1,
#           #   							base=0,
#           #   							width = 0.4,
# 										# offset = -0.4,
# 						                marker=go.bar.Marker(
# 						                    color='#000080'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=deposit_branch_main.rename(index=branch_name_mapping).index,
# 						                y=(deposit_branch_main/1e9).round(),
# 						                name='Deposit amount-Main branch',
# 						                text=(deposit_branch_main/1e9).round(),
#             							textposition='outside',
#                                         visible='legendonly', 
# #                                         row=1,
# #                                         col=1,
#           #   							base=0,
#           #   							width = 0.4,
# 										# offset = -0.4,
# 						                marker=go.bar.Marker(
# 						                    color="#45b6fe"
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=overdraft_branch_main.rename(index=branch_name_mapping).index,
# 						                y=overdraft_branch_main/1e9,
# 						                name='Loan amount-Main branch',
# 						                text=overdraft_branch_main/1e9,
#             							textposition='outside',
#                                         visible='legendonly',
# #                                         row=1,
# #                                         col=1,
#           #   							base=0,
#           #   							width = 0.4,
# 										# offset = -0.4,
# 						                marker=go.bar.Marker(
# 						                    color='#000080'
# 						                )
# 						            ),                                    
# 						        ],
# 						        layout=go.Layout(
# #                                     width=1000,
# #                                     height=600,
# # 						            barmode="stack",
# 						            showlegend=True,
# 						            legend=go.layout.Legend(
# 						                x=1.0,
# 						                y=1.0,
# 						                xanchor="center",
#     									yanchor="top",
# 						            ),
# 						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
# # 						            barmode="stack",                                    
# 						            title=go.layout.Title(
# 										text="Deposits vs loans at Branch level(Billions Rwf)[{}]".format(cust_type),
# 									# 	xref="paper",
# # 										x=0.5 
# 									),
# 									xaxis=go.layout.XAxis(
# #                                         row=2,
# #                                         col=1,
# 										title=go.layout.xaxis.Title(
# 											text="Branch name",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									),
# 									yaxis=go.layout.YAxis(
# #                                         row=1,
# #                                         col=1,
# 										title=go.layout.yaxis.Title(
# 											text="Amount(Billions Rwf)",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									)
# 						        )
# 						    ),
# 						    # style={'height': 400,},
# 						    id='my-graph_1',
# 						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Deposit and overdraft at Branch level" )}),
# 						),
#                     	], 
#                     	id="loan",
#                     	# style={'width': 700,},
#                     ),
#                 ],
#                 body=True,
#                 style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
#             ),            
         
# 		]),
        
	])

	return output
