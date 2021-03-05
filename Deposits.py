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

layout = html.Div(
	[	        
		html.H1("Deposits",id="general_overview"),
		html.Hr(),        
#     html.P('This section is a general overview of customers and accounts including customer trends, accounts status, age and gender segmentation at I&M bank. To view information based on business category, choose one of the radio buttons i.e. ALL, RETAIL, SME, CORPORATE. For graphs showing trends overtime, buttons 1 MONTH, 3 MONTHS, 6 MONTHS, 1 YEAR and ALL allow one to see trends over one month, three months and so on. In addition, for each graph you can choose one field you want to see clearly by disabling others i.e. click on an item in the legend to disable it for example to view all accounts apart from active ones, double click on the active item in the legend.'),        
# 		html.Hr(),
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
		html.Div([
			html.Div(id="overview_infod"),
			dcc.Interval(id="update-overview_infod", interval=1000*60*60*2, n_intervals=0),
		]),        
		html.Div([
			html.Div(id="overview_d"),
			dcc.Interval(id="update-overview_d", interval=1000*60*60*2, n_intervals=0),
		]),        

#         html.Div([
#             html.Div(id="summary-channel"),
#             dcc.Interval(id="update-channels", interval=1000*60*60*2, n_intervals=0),
#         ]),        
		# html.Hr(),
		dbc.CardGroup([
    		dbc.Card([
    			html.Div(id="new_opening_trend-lined"),
    			dcc.Interval(id="update-new_opening_trendd", interval=1000*60*60*2, n_intervals=0),
    		]),
    		dbc.Card([
    			html.Div(id="trend-lined"),
    			dcc.Interval(id="update-trend_lined", interval=1000*60*60*2, n_intervals=0),
    		]),
    	]),
		html.Div([
			html.Div(id="overview_graphd"),
			dcc.Interval(id="update-overview_graphd", interval=1000*60*60*2, n_intervals=0),
		]),
# 		html.Div([
# 			html.Div(id="comparison"),
# 			dcc.Interval(id="update-comparison", interval=1000*60*60*2, n_intervals=0),
# 		]),         
    	# html.Hr(),
		dbc.CardGroup([
    		dbc.Card([
    			html.Div(id="num_accountsd"),
    			dcc.Interval(id="update-num_accountsd", interval=1000*60*60*2, n_intervals=0),
    		]),
    		# dbc.Card([
    		# 	html.Div(id=""),
    		# 	dcc.Interval(id="", interval=1000*60*60*12, n_intervals=0),
    		# ]),
    	]),
		# html.Hr(),
# 		html.Div([
# 			html.Div(id="overview_graph"),
# 			dcc.Interval(id="update-overview_graph", interval=1000*60*60*2, n_intervals=0),
# 		]),
		# html.Hr(),
# 		html.Div([
# 			html.Div(id="sbu_age_segmentation"),
# 			dcc.Interval(id="update-sbu_age_segmentation", interval=1000*60*60*2, n_intervals=0),
# 		]),
	],
)

#############################################################################################
###################### layout callback ######################################################
#############################################################################################
@app.callback(
	[
		Output("overview_infod","children"),
	],
	[
		Input("update-overview_infod", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_info(n, cust_type):
# 	(Current_lcy,Current_fcy,Saving_lcy,Saving_fcy,fix_depo_lcy,fix_depo_fcy,Margin,interest_pay)=get_deposit(session_id, cust_type)    
# 	PL=get_deposit_loans(session_id, cust_type)
	loan_depos=get_loan_dep_trend(session_id, cust_type)    
	Current_lcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Current Account - LCY')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()
	Current_fcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Current Account - FCY')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()
	Saving_lcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Savings - LCY')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()
	Saving_fcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Savings - FCY')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()    
	fix_depo_lcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Fixed Deposits - LCY')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()
	fix_depo_fcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Fixed Deposits - FCY')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()
	Margin=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Margin Deposits')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()
	interest_pay=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Interest Payable')&(loan_depos.VALUE_DATE==loan_depos.VALUE_DATE.max())].BALANCE.sum()     
	return [dbc.CardDeck(
			[
                dbc.Card(
                    [
                        html.H5("Demands"),                                             
                        html.H4("Rwf {:,.0f}".format(Current_lcy + Current_fcy), style={"color":"lightblue"}),
#                         html.H6("Total Deposit Amount in million"),
                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.H5("Savings"),                                             
                        html.H4("Rwf {:,.0f}".format(Saving_lcy + Saving_fcy), style={"color":"#494c53"}),
#                         html.H6("Total Overdraft Amount in million"),
                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.H5("Term deposits"),                                             
                        html.H4("Rwf {:,.0f}".format(fix_depo_lcy + fix_depo_fcy), style={"color":"#000080"}),

                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.H5("Margin deposits"),                                             
                        html.H4("Rwf {:,.0f}".format(Margin ), style={"color":"violet"}),
#                         html.H6("Total Deposit Amount in million"),
                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.H5("Interest payable"),                                             
                        html.H4("Rwf {:,.0f}".format(interest_pay), style={"color":"#004206"}),
#                         html.H6("Total Deposit Amount in million"),
                    ],
                    body=True,
                ),                 
			],
			
		),
    ]

@app.callback(
	Output("overview_d","children"),
	[
		Input("update-overview_d", "n_intervals"),
		Input("select-cust_type", "value"),
#         Input("year_range","value"),        
	]
)
def update_overview_trend(n, cust_type):

	loan_depos=get_loan_dep_trend(session_id, cust_type)
	loan_depos["VALUE_DATE"]=pd.to_datetime(loan_depos.VALUE_DATE,errors="coerce")   
	Current_lcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Current Account - LCY')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()
	Current_fcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Current Account - FCY')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()
	Saving_lcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Savings - LCY')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()
	Saving_fcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Savings - FCY')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()    
	fix_depo_lcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Fixed Deposits - LCY')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()
	fix_depo_fcy=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Fixed Deposits - FCY')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()
	Margin=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Margin Deposits')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()
	interest_pay=loan_depos[(loan_depos.FRL_ATT_01_DESCRIPTION=='Interest Payable')&(loan_depos.VALUE_DATE<date.today())].groupby('VALUE_DATE').BALANCE.sum()  
    
	Demands=Current_lcy + Current_fcy  
	Savings=Saving_lcy + Saving_fcy
	Fixed=fix_depo_lcy + fix_depo_fcy    
###################################################################################################
	fig=make_subplots(rows=3,
                     cols=1,
                     shared_xaxes=True,
                     vertical_spacing=0.005)
	fig.add_trace(
        go.Scatter(
            x=Demands.index,
            y=Demands,
            name='Demand deposits',
            marker=go.scatter.Marker(color='lightblue'),
        ),
        1,
        1
	)

	fig.add_trace(
        go.Scatter(
            x=Fixed.index,
            y=Fixed,
            name='Term deposits',
            connectgaps=True,
            marker=go.scatter.Marker(color='#000080'),
        ),
        3,
        1
	)

	fig.add_trace(
        go.Scatter(
            x=Savings.index,
            y=Savings,
            name='Saving deposits',
            marker=go.scatter.Marker(color='#494c53'),
        ),
        2,
        1
	)
# 	fig.add_trace(
#         go.Scatter(
#             x=Margin.index,
#             y=Margin,
#             name='Margin deposits',
#             marker=go.scatter.Marker(color='violet'),
#         ), 
#         4,
#         1
# 	)
# 	fig.add_trace(
#         go.Scatter(
#             x=interest_pay.index,
#             y=interest_pay,
#             name='Interest payable',
#             marker=go.scatter.Marker(color='#004206')
#         ),  
#         4,
#         1
# 	)    

	fig.layout.update(title="Deposits overtime(Rwf)[{}]".format(cust_type),
                        showlegend=True,
                        legend_orientation="h",
                        xaxis_tickmode="linear",
                        xaxis_tickformat='%Y%B%d',
                        height=700,
#                         xaxis=xaxis_update(showgrid=False),
#                         xaxis_rangeslider_visible= True,
#                         legend=(
#                             x=0,
#                             y=0.95
# #                         ),
#                         margin=go.layout.Margin(l=10, r=10, t=60, b=10),                      
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
# ################################################################################################### 
	if cust_type == 'ALL':
		output =  html.Div([
#             dbc.CardGroup([
#                 dbc.Card(
#                     [
#                         html.Div([
#                             dcc.Graph(
#                                 figure=go.Figure(
#                                     data=[
#                                         go.Scatter(
#                                             x=Demands.index,
#                                             y=Demands,
#                                             name='Demands',
#                                             marker=go.scatter.Marker(color='lightblue'),
#                                         ),
#                                         go.Scatter(
#                                             x=Savings.index,
#                                             y=Savings,
#                                             name='Savings',
#                                             marker=go.scatter.Marker(color='#494c53'),
#                                         ),
#                                         go.Scatter(
#                                             x=Fixed.index,
#                                             y=Fixed,
#                                             name='Term deposits',
#                                             marker=go.scatter.Marker(color='#000080'),
#                                         ),
# #                                         go.Scatter(
# #                                             x=Margin.index,
# #                                             y=Margin,
# #                                             name='Margin deposits',
# #                                             marker=go.scatter.Marker(color='violet'),
# #                                         ),                                    
# #                                         go.Scatter(
# #                                             x=interest_pay.index,
# #                                             y=interest_pay,
# #                                             name='Interest payable',
# #                                             marker=go.scatter.Marker(color='#004206')
# #                                         ),                                    
#                                     ],
#     #                                 data=[trace]
#                                     layout=go.Layout(
#     #                                     in_view=df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
#     #                                     fig.layout.yaxis.range=[in_view.High.min()-10,in_view.High.max()+10]                                    
#                                         # barmode="stack",
#                                         showlegend=True,
# #                                         height=700,
#                                         legend_orientation="h",
#                                         legend=go.layout.Legend(
#                                             x=0,
#                                             y=0.95,
#     # 						                xanchor="center",
#     #     									yanchor="top",
#                                         ),
#                                         margin=go.layout.Margin(l=10, r=10, t=60, b=10),
#     #                                     xaxis_rangeslider_visible=True,
#                                         title=go.layout.Title(
#                                             text="Deposits overtime(Rwf) [{}]".format(cust_type),
#     #                                         x=0.5, 
#     #                                         y=0.99
#                                         ),
#                                         xaxis=go.layout.XAxis(
#                                             showgrid=False,
#                                             rangeselector=dict(
#                                                 buttons=list([
#                                                     dict(count=1,
#                                                          label="1MONTH",
#                                                          step="month",
#                                                          stepmode="backward"),
#                                                     dict(count=3,
#                                                          label="3MONTHS",
#                                                          step="month",
#                                                          stepmode="backward"),                                                    
#                                                     dict(count=6,
#                                                          label="6MONTHS",
#                                                          step="month",
#                                                          stepmode="backward"),
#                                                     dict(count=1,
#                                                          label="1YEAR",
#                                                          step="year",
#                                                          stepmode="backward"),
#                                                     dict(step="all")
#                                                 ])
#                                             ),
#                                             rangeslider=dict(
#                                                 visible=True
#                                             ),                                            
#                                             type="date"
#                                             ),                                                                         
    
#                                         ),

#                                     )

#                                 ),

#                     ],style={'padding': 3})            
            dbc.CardGroup([
                dbc.Card(
                    [
                        html.Div([       
                            dcc.Graph(
                                figure=fig
    # #                             figure=go.Figure(
    # #                                 data=[
    # #                                     go.Scatter(
    # #                                         x= depo_overtime.index, 
    # #                                         y= depo_overtime/1e9,
    # #                                         name='Deposits amount(Billion rwf)',
    # # #                                         text=customer_Opening.pct_change(),
    # #                                         mode="lines",
    # #                 #                         fill="toself",tonexty
    # # #                                         fill="tozeroy",
    # #                                         marker=go.scatter.Marker(
    # #                                             color='#45b6fe'
    # #                                         )
    # #                                     ),
    # #                 	                go.Scatter(
    # #                 	                    x= loan_overtime.index, 
    # #                 	                    y= loan_overtime/1e9,
    # # #                                         text=account_Opening.pct_change(),
    # #                 	                    name='Loans amount(Billion rwf)',
    # #                 	                    mode= "lines",
    # # #                                         fill="tonexty",
    # # #                                         visible='legendonly',
    # #                 	                    marker=go.scatter.Marker(
    # #                 	                        color='#000080'
    # #                 	                    )
    # #                 	                ),
    # #                                     go.Scatter(
    # #                                         x= custom.index, 
    # #                                         y= custom,
    # #                                         name='Customers',
    # #                                         mode= "lines",
    # #                         #                 row=1,
    # #                         #                 col=1,                
    # #                         #                 fill="tonexty",
    # #                         #                 visible='legendonly',
    # #                                         marker=go.scatter.Marker(
    # #                                             color='#8c6464'
    # #                                         )
    # #                                     ),
    # #                         #             secondary_y=True,
    # #                                     go.Scatter(
    # #                                         x= account.index, 
    # #                                         y= account,
    # #                                         name='Accounts',
    # #                                         mode= "lines",
    # #                         #                 row=1,
    # #                         #                 col=1,             
    # #                         #                 fill="tonexty",
    # #                         #                 visible='legendonly',
    # #                                         marker=go.scatter.Marker(
    # #                                             color='grey'
    # #                                         )
    # #                                     ),                                    
    # #                                 ],
    # #                                 layout=go.Layout(
    # #                                     tickformat='%Y%B%d',
    # #                                     showlegend=True,
    # #                                     legend_orientation="h",
    # #                 #                     annotations=[
    # #                 #                         dict(
    # #                 #                             x=0,
    # #                 #                             y=0,
    # #                 #                             xref="x",
    # #                 #                             yref="y",
    # #                 #                             text="initial",
    # #                 #                             showarrow=True,
    # #                 #                             arrowhead=7,
    # #                 #                             ax=0,
    # #                 #                             ay=-40
    # #                 #                         )
    # #                 #                     ],                      
    # #                                     xaxis_rangeslider_visible= True,
    # #                                     legend=go.layout.Legend(
    # #                                         x=0,
    # #                                         y=0.95
    # #                                     ),
    # #                                     margin=go.layout.Margin(l=10, r=10, t=60, b=10),

    # #                                     title=go.layout.Title(
    # #                                         text="Performance trend[{}]".format(cust_type),
    # #                                     # 	xref="paper",
    # #                 # 						x=0,
    # #                 #                         y=0.99
    # #                                     ),
    # #                                     xaxis=go.layout.XAxis(
    # #                                         rangeselector=dict(
    # #                                             buttons=list([
    # #                                                 dict(count=1,
    # #                                                      label="1 MONTH",
    # #                                                      step="month",
    # #                                                      stepmode="backward"),
    # #                                                 dict(count=3,
    # #                                                      label="3 MONTHS",
    # #                                                      step="month",
    # #                                                      stepmode="backward"),                                
    # #                                                 dict(count=6,
    # #                                                      label="6 MONTHS",
    # #                                                      step="month",
    # #                                                      stepmode="backward"),
    # #                                                 dict(count=1,
    # #                                                      label="1YEAR",
    # #                                                      step="year",
    # #                                                      stepmode="backward"),
    # #                                                 dict(step="all")
    # #                                             ])
    # #                                         ),
    # #                                         rangeslider=dict(
    # #                                             visible=True
    # #                                         ),
    # #                                         type="date"

    # #                                     ),
    # #                 					yaxis=go.layout.YAxis(
    # #                                         mirror=True,
    # # #                 						title=go.layout.yaxis.Title(
    # # #                 							text="Deposits/Loans", 
    # # #                 							# font=dict(
    # # #                 							#     family="Courier New, monospace",
    # # #                 							#     size=18,
    # # #                 							#     color="#7f7f7f"
    # # #                 							# )
    # # #                 						)
    # #                 					)
    # #                                 )

    # #                             ),
    # #                     #             style={'height': 300, "top":30},
    # #                 # 	        id="trend-graph-2",
    # #                 # 	        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
                            ),
                        ],style={'padding': 10})
                    ],
                    body=True,
                    style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},                  
                ),
            ])##################################################
		])
	else:
		output =  html.Div([
            dbc.CardGroup([
                dbc.Card(
                    [
                        html.Div([
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Scatter(
                                            x=Demands.index,
                                            y=Demands,
                                            name='Demands',
                                            marker=go.scatter.Marker(color='lightblue'),
                                        ),
                                        go.Scatter(
                                            x=Savings.index,
                                            y=Savings,
                                            name='Savings',
                                            marker=go.scatter.Marker(color='#494c53'),
                                        ),
                                        go.Scatter(
                                            x=Fixed.index,
                                            y=Fixed,
                                            name='Fixed deposits',
                                            marker=go.scatter.Marker(color='#000080'),
                                        ),
#                                         go.Scatter(
#                                             x=Margin.index,
#                                             y=Margin,
#                                             name='Margin deposits',
#                                             marker=go.scatter.Marker(color='violet'),
#                                         ),                                    
#                                         go.Scatter(
#                                             x=interest_pay.index,
#                                             y=interest_pay,
#                                             name='Interest payable',
#                                             marker=go.scatter.Marker(color='#004206')
#                                         ),                                    
                                    ],
    #                                 data=[trace]
                                    layout=go.Layout(
    #                                     in_view=df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
    #                                     fig.layout.yaxis.range=[in_view.High.min()-10,in_view.High.max()+10]                                    
                                        # barmode="stack",
                                        showlegend=True,
                                        height=700,
                                        legend_orientation="h",
                                        legend=go.layout.Legend(
                                            x=0,
                                            y=0.95,
    # 						                xanchor="center",
    #     									yanchor="top",
                                        ),
                                        margin=go.layout.Margin(l=10, r=10, t=60, b=10),
    #                                     xaxis_rangeslider_visible=True,
                                        title=go.layout.Title(
                                            text="Deposits overtime(Rwf) [{}]".format(cust_type),
    #                                         x=0.5, 
    #                                         y=0.99
                                        ),
                                        xaxis=go.layout.XAxis(
                                            rangeselector=dict(
                                                buttons=list([
                                                    dict(count=1,
                                                         label="1MONTH",
                                                         step="month",
                                                         stepmode="backward"),
                                                    dict(count=3,
                                                         label="3MONTHS",
                                                         step="month",
                                                         stepmode="backward"),                                                    
                                                    dict(count=6,
                                                         label="6MONTHS",
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
    
                                        ),

                                    )

                                ),

                    ],style={'padding': 3})
                ],
                body=True, 
    #             style={"padding":"5px 5px 5px 5px", },                
            ),
    #             ),
        ]),##################################################
	])

	return output

@app.callback(
	Output("comparison","children"),
	[
		Input("update-comparison", "n_intervals"),
		Input("select-cust_type", "value"),
#         Input("year_range","value"),        
	]
)
def update_overview_comp(n, cust_type):

	(loan_overtime,depo_overtime,Current_lcy,Current_fcy,Saving_lcy,Saving_fcy,
     fix_depo_lcy,fix_depo_fcy,Margin,interest_pay)=get_loan_dep_trend(session_id, cust_type)    
# ###################################################################################################
	output =  html.Div([
	])

	return output




# @app.callback(
#     Output('my-graph', 'figure'),')])
#     [Input('selected-value', 'value'), Input('year-range', 'value
def update_num_accounts_graph(n, cust_type):

	output =  html.Div([
	])

	return output

###################################################################################################
@app.callback(
	Output("overview_graphd","children"),
	[
		Input("update-overview_graphd", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_graph(n, cust_type):

	colors_sbu=['#45b6fe', '#000080', 'blueviolet']
	colors_gender=['#45b6fe', '#000080', 'blueviolet']
# 	colors_acc=['#45b6fe','#000080','blueviolet', '#494c53']    
	colors_acc=['#45b6fe','#000080','#494c53']



	(positive_amt, negative_amt) =get_account_cleared_balance_lcy(session_id, cust_type)

   
	colors_overd = ["#000080","#45b6fe"]
# 	colors_sbu = ["#494c53","#000080","45b6fe"]              
    
	if cust_type == 'R':
		deposit_output= dbc.CardGroup(
			[
# 	            dbc.Card(

#                 [
#                     html.Div([
#                         dcc.Graph(
#                             figure=go.Figure(
#                                 data=[
#                                     go.Bar(
#                                         x=male_age_deposit.index,
#                                         y=(male_age_deposit/1e6).round(),
#                                         name='Male',
#                                         text=get_percentage_label((male_age_deposit*100/(male_age_deposit.sum())).round()),
#                                         textposition='outside',
#           #   							base=0,
#           #   							width = 0.4,
#                                         # offset = -0.4,
#                                         marker=go.bar.Marker(
#                                             color="#000080"
#                                         )
#                                     ),
#                                     go.Bar(
#                                         x=female_age_deposit.index,
#                                         y=(female_age_deposit/1e6).round(),
#                                         name='Female',
#                                         text=get_percentage_label((female_age_deposit*100/(female_age_deposit.sum())).round()),
#                                         textposition='outside',
#           #   							base=0,
#           #   							width = 0.4,
#                                         # offset = -0.4,
#                                         marker=go.bar.Marker(
#                                             color='#45b6fe'
#                                         )
#                                     ),
#                                 ],
#                                 layout=go.Layout(
#                                     # barmode="stack",
#                                     showlegend=True,
#                                     legend=go.layout.Legend(
#                                         x=1.0,
#                                         y=1.0,
#                                         xanchor="center",
#                                         yanchor="top",
#                                     ),
#                                     margin=go.layout.Margin(l=40, r=0, t=40, b=30),
#         # 						            barmode="stack",                                    
#                                     title=go.layout.Title(
#                                         text="Deposits based on customer age(in Millions rwf)[{}]".format(cust_type),
# #                                     # 	xref="paper",
# #                                         x=0.5
#                                     ),
#                                     xaxis=go.layout.XAxis(
#                                         title=go.layout.xaxis.Title(
#                                             text="Age group",
#                                             # font=dict(
#                                             #     family="Courier New, monospace",
#                                             #     size=18,
#                                             #     color="#7f7f7f"
#                                             # )
#                                         )
#                                     ),
#                                     yaxis=go.layout.YAxis(
#                                         title=go.layout.yaxis.Title(
#                                             text="Amount(Millions rwf)",
#                                             # font=dict(
#                                             #     family="Courier New, monospace",
#                                             #     size=18,
#                                             #     color="#7f7f7f"
#                                             # )
#                                         )
#                                     )
#                                 )
#                             ),
#                             # style={'height': 400,},
#                             id='my-graph_1',
#                             config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Deposits based on customer age" )}),
#                         ),
#                         ], 
#                         id="loan",
#                         # style={'width': 700,},
#                     ),
#                 ],                
#                 body=True,
#                 style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
#             ),           
        ])                
#        
	else:
		deposit_output=dbc.CardGroup([])
        
	output =  html.Div([

        
        deposit_output,        
		##############################################################
		dbc.CardGroup([
# 			dbc.Card(
#                 [
#                     html.Div([
#                     	dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=deposit_branch.rename(index=branch_name_mapping).index,
# 						                y=(deposit_branch).round(),
# 						                name='Amount(Millions)_others',
# 						                text=get_percentage_label((deposit_branch*100//(deposit_branch_main.sum()+deposit_branch.sum()))),
#             							textposition='outside',
#           #   							base=0,
#           #   							width = 0.4,
# 										# offset = -0.4,
# 						                marker=go.bar.Marker(
# 						                    color="#45b6fe"
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=deposit_branch_main.rename(index=branch_name_mapping).index,
# 						                y=(deposit_branch_main).round(),
# 						                name='Amount(Millions)-Head office',
# 						                text=get_percentage_label((deposit_branch_main*100//(deposit_branch_main.sum()+deposit_branch.sum()))),
#             							textposition='outside',
#           #   							base=0,
#           #   							width = 0.4,
# 										# offset = -0.4,
# 						                marker=go.bar.Marker(
# 						                    color="#45b6fe"
# 						                )
# 						            ),                                    
# 						        ],
# 						        layout=go.Layout(
# 						            # barmode="stack",
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
# 										text="Deposits at Branch level(in millions Rwf)[{}]".format(cust_type),
# 									# 	xref="paper",
# # 										x=0.5
# 									),
# 									xaxis=go.layout.XAxis(
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
# 										title=go.layout.yaxis.Title(
# 											text="Amount",
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
		]),
                  
	])

	return output

##########################################################################################################
