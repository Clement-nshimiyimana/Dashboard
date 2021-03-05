import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly import tools
import plotly.io as pio
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime

import numpy as np

from app import app, session_id
from components import *
from config import *

pio.templates.default = "plotly_white"
init_start_date= str(dt.today().year)+'-'+str(dt.today().month)+'-01'
init_end_date= str(dt.today().year)+'-'+str(dt.today().month)+'-'+str(dt.today().day)
layout = html.Div(
	[	        
		html.H1("Revenues&Expenses",id="general_overview"),       
#     html.P('This section is a general overview of customers and accounts including customer trends, accounts status, age and gender segmentation at I&M bank. To view information based on business category, choose one of the radio buttons i.e. ALL, RETAIL, SME, CORPORATE. For graphs showing trends overtime, buttons 1 MONTH, 3 MONTHS, 6 MONTHS, 1 YEAR and ALL allow one to see trends over one month, three months and so on. In addition, for each graph you can choose one field you want to see clearly by disabling others i.e. click on an item in the legend to disable it for example to view all accounts apart from active ones, double click on the active item in the legend.'),        

		html.Div(
        [
            dbc.Row([
                dbc.Col([
                    dcc.DatePickerRange(
                        id='channels-date-picker-range',
                        min_date_allowed= datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d"),
                        max_date_allowed= dt.today().strftime("%Y-%m-%d"),
                        initial_visible_month= dt.today().strftime("%Y-%m-%d"),
                        start_date= init_start_date,
                        end_date = init_end_date,
                        start_date_placeholder_text= "Start date",
                        end_date_placeholder_text= "End date",
                        first_day_of_week= 1,
                        number_of_months_shown= 1,
                        minimum_nights= 3,
                        display_format= "DD-MM-YYYY",
                        # show_outside_days=True,
                        style={"margin":"0px 0px 10px 0px"},
                    ),
                ]),
            ]),
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
			html.Div(id="Overview_graph2"),
			dcc.Interval(id="Update-overview_graph2", interval=1000*60*60*2, n_intervals=0),
		]),
		html.Div([
			html.Div(id="Overview_info2"),
			dcc.Interval(id="Update-overview_info2", interval=1000*60*60*2, n_intervals=0),
		]),
		html.Div([
			html.Div(id="Overview_graph3"),
			dcc.Interval(id="Update-overview_graph3", interval=1000*60*60*2, n_intervals=0),
		]),        
    	# html.Hr(),
	],
)

#############################################################################################
###################### layout callback ######################################################
#############################################################################################
@app.callback(
	[
		Output("Overview_info2","children"),
	],
	[
		Input("Update-overview_info2", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_trend_info(n, cust_type):
	fees_overtime=get_fees_trend(session_id, cust_type)
	fees_overtime,fees_trend=get_fees_trend(session_id, cust_type)
	expense_overtime=get_expense_trend(session_id, cust_type)
	income_overtime,income_trend=get_income_trend(session_id, cust_type)
	output= [html.Div([
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([
                    	dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Scatter(
						                x=income_overtime.index,
						                y=income_overtime.round(),
						                name='Interest income',
# 						                text=income_overtime//1e6,
text=get_percentage_label((income_overtime).pct_change(fill_method='pad').round(2)*100),                                        
            							mode="lines+markers",
                                        textposition="top center",
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.scatter.Marker(
						                    color="#45b6fe"
						                )
						            ),
						            go.Scatter(
						                x=fees_overtime.index,
						                y=fees_overtime.round(),
						                name='Fees&commissions',
# 						                text=fees_overtime//1e6,
text=get_percentage_label((fees_overtime).pct_change().round(2)*100),                                        
            							mode="lines+markers",
                                        textposition="top center",
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.scatter.Marker(
						                    color='#000080'
						                )
						            ),
						            go.Scatter(
						                x=expense_overtime.index,
						                y=expense_overtime.round(),
						                name='Expenses',
# 						                text=expense_overtime//1e6,
text=get_percentage_label((expense_overtime).pct_change().round(2)*100),                                        
            							mode="lines+markers",
                                        textposition="top center",
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.scatter.Marker(
						                    color='darkred'
						                )
						            ),
						            go.Scatter(
						                x=(expense_overtime+income_overtime+fees_overtime).index,
						                y=(expense_overtime+income_overtime+fees_overtime).round(),
						                name='Net income',
						                text=get_percentage_label((expense_overtime+income_overtime+fees_overtime).pct_change().round(2)*100),
                                        mode="lines+text+markers",
                                        textposition="top center",
#             							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.scatter.Marker(
						                    color='green'
						                )
						            ),                                    
						        ],
						        layout=go.Layout(
                                    height=600,
						            # barmode="stack",
						            showlegend=True,
						            legend=go.layout.Legend(
						                x=0.0,
						                y=1.0,
                                        orientation='h',
# 						                xanchor="center",
#     									yanchor="top",
						            ),
						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
# 						            barmode="stack",                                    
						            title=go.layout.Title(
										text="Profitability trend[{}]".format(cust_type),
									# 	xref="paper",
# 										x=0.5
									),
									xaxis=go.layout.XAxis(
                                        tickformat='%b%Y',
                                        type="category",
                                        categoryorder='category ascending',                                        
#                                         zeroline= True,
#                                         tickvals=income_overtime,
#                                         ticktext=income_overtime.index,
										title=go.layout.xaxis.Title(
											text="Time",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
										)
									),
									yaxis=go.layout.YAxis(
                                        tickformat = ',3%',
										title=go.layout.yaxis.Title(
											text="Amount(rwf)",
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
						    id='my-graph_1',
						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Profitability trend" )}),
						),
                    	], 
                    	id="loan",
                    	# style={'width': 700,},
                    ),
                ],
                body=True,
                style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
            ),                      
		]),    
	]),
]
	return output
###################################################################################################
@app.callback(
	Output("Overview_graph2","children"),
	[
		Input("Update-overview_graph2", "n_intervals"),
		Input("select-cust_type", "value"),
#         Input("year_range","value"),        
	]
)

def update_profit_graph(n, cust_type):
	(Income,Expenses,FC,Loan_product,Overdraft_product,Saving_product,
     Term_Dep_product,Current_product,Loan_product_ex,
     Overdraft_product_ex,Saving_product_ex,Term_Dep_product_ex,
     Current_product_ex,Loan_product_fee,
     Overdraft_product_fee,Saving_product_fee,Term_Dep_product_fee,Current_product_fee)=get_pl(session_id, cust_type)

	output =[dbc.CardDeck(
			[
                dbc.Card(
                    [
                        html.H5("Interest income"),                        
                        html.H2("Rwf {:,.0f}".format(Income)),
                 
                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
                ),
                dbc.Card(
                    [
                        html.H5("Fees & commissions"),                        
                        html.H2(" Rwf {:,.0f}".format(FC)),

                     
                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.H5("Expenses"),                        
                        html.H2("Rwf {:,.0f} ".format(-1*Expenses)),
                     
                    ],
                    body=True,
                ),                
                dbc.Card(
                    [
                        html.H5("Net income"),                                             
                        html.H2("Rwf {:,.0f}".format(Income+Expenses+FC), style={"color":"#000080"}),

                    ],
                    body=True,
                ),
			],
			
		),  
	]
	return output

@app.callback(
	Output("Overview_graph3","children"),
	[
		Input("Update-overview_graph3", "n_intervals"),
		Input("select-cust_type", "value"),       
	]
)

def update_profit_graph(n, cust_type):
	(Income,Expenses,FC,Loan_product,Overdraft_product,Saving_product,
     Term_Dep_product,Current_product,Loan_product_ex,
     Overdraft_product_ex,Saving_product_ex,Term_Dep_product_ex,
     Current_product_ex,Loan_product_fee,
     Overdraft_product_fee,Saving_product_fee,Term_Dep_product_fee,Current_product_fee)=get_pl(session_id, cust_type)

	output =html.Div([
        html.Div([]),        
        html.Div([html.H3(['Loan products'])]),
        html.Div([]),        
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([
                    	dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=Loan_product.index,
						                y=Loan_product,
						                name='Interest income',
						                text=(Loan_product/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color="#45b6fe"
						                )
						            ),
						            go.Bar(
						                x=Loan_product_fee.index,
						                y=Loan_product_fee,
						                name='Fees&commissions',
						                text=(Loan_product_fee/1e6).round(2),
            							textposition='outside',
                                        visible="legendonly",
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='#000080'
						                )
						            ),
						            go.Bar(
						                x=Loan_product_ex.index,
						                y=Loan_product_ex,
						                name='Expenses',
						                text=(Loan_product_ex/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='darkred'
						                )
						            ),                                   
						        ],
						        layout=go.Layout(
						            # barmode="stack",
						            showlegend=True,
						            legend=go.layout.Legend(
						                x=1.0,
						                y=1.0,
						                xanchor="center",
    									yanchor="top",
						            ),
						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
# 						            barmode="stack",                                    
						            title=go.layout.Title(
										text="Profitability on loans(Million Rwf)[{}]".format(cust_type),
									# 	xref="paper",
# 										x=0.5
									),
									xaxis=go.layout.XAxis(
										title=go.layout.xaxis.Title(
											text="Products",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
										)
									),
									yaxis=go.layout.YAxis(
										tickformat = ',3%',                                        
										title=go.layout.yaxis.Title(
											text="Amount(rwf)",
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
						    id='my-graph_1',
						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Profitability trend" )}),
						),
                    	], 
                    	id="loan",
                    	# style={'width': 700,},
                    ),
                ],
                body=True,
                style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
            ),                      
		]),
        html.Div([]),        
        html.Div([html.H3(['Overdraft products'])]),
        html.Div([]),
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([
                    	dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=Overdraft_product.index,
						                y=Overdraft_product,
						                name='Interest income',
						                text=(Overdraft_product/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color="#45b6fe"
						                )
						            ),
						            go.Bar(
						                x=Overdraft_product_fee.index,
						                y=Overdraft_product_fee,
						                name='Fees&commissions',
						                text=(Overdraft_product_fee/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='#000080'
						                )
						            ),
						            go.Bar(
						                x=Overdraft_product_ex.index,
						                y=Overdraft_product_ex,
						                name='Expenses',
						                text=(Overdraft_product_ex/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='darkred'
						                )
						            ),
                                  
						        ],
						        layout=go.Layout(
						            # barmode="stack",
						            showlegend=True,
						            legend=go.layout.Legend(
						                x=1.0,
						                y=1.0,
						                xanchor="center",
    									yanchor="top",
						            ),
						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
# 						            barmode="stack",                                    
						            title=go.layout.Title(
										text="Profitability on overdrafts(Million Rwf)[{}]".format(cust_type),
									# 	xref="paper",
# 										x=0.5
									),
									xaxis=go.layout.XAxis(
										title=go.layout.xaxis.Title(
											text="Products",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
										)
									),
									yaxis=go.layout.YAxis(
										tickformat = ',3%',                                        
										title=go.layout.yaxis.Title(
											text="Amount(rwf)",
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
						),
                    	], 
                    	id="loan",
                    	# style={'width': 700,},
                    ),
                ],
                body=True,
                style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
            ),                      
		]),
        html.Div([]),        
        html.Div([html.H3(['Current account products'])]),
        html.Div([]),
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([
                    	dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=Current_product.index,
						                y=Current_product,
						                name='Interest income',
						                text=(Current_product/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color="#45b6fe"
						                )
						            ),
						            go.Bar(
						                x=Current_product_fee.index,
						                y=Current_product_fee,
						                name='Fees&commissions',
						                text=(Current_product_fee/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='#000080'
						                )
						            ),
						            go.Bar(
						                x=Current_product_ex.index,
						                y=Current_product_ex,
						                name='Expenses',
						                text=(Current_product_ex/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='darkred'
						                )
						            ),
                                    
						        ],
						        layout=go.Layout(
						            # barmode="stack",
						            showlegend=True,
						            legend=go.layout.Legend(
						                x=1.0,
						                y=1.0,
						                xanchor="center",
    									yanchor="top",
						            ),
						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
# 						            barmode="stack",                                    
						            title=go.layout.Title(
										text="Profitability on current account products(Millions Rwf)[{}]".format(cust_type),
									# 	xref="paper",
# 										x=0.5
									),
									xaxis=go.layout.XAxis(
										title=go.layout.xaxis.Title(
											text="Products",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
										)
									),
									yaxis=go.layout.YAxis(
										tickformat = ',3%',                                         
										title=go.layout.yaxis.Title(
											text="Amount(Rwf)",
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
						    id='my-graph_1',
						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Profitability trend" )}),
						),
                    	], 
                    	id="loan",
                    	# style={'width': 700,},
                    ),
                ],
                body=True,
                style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
            ),                      
		]),        
        html.Div([]),        
        html.Div([html.H3(['Saving account products'])]),
        html.Div([]),
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([
                    	dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=Saving_product.index,
						                y=Saving_product,
						                name='Interest income',
						                text=(Saving_product/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color="#45b6fe"
						                )
						            ),
						            go.Bar(
						                x=Saving_product_fee.index,
						                y=Saving_product_fee,
						                name='Fees&commissions', 
						                text=(Saving_product_fee/1e6).round(2),
            							textposition='outside',
                                        visible="legendonly",
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='#000080'
						                )
						            ),
						            go.Bar(
						                x=Saving_product_ex.index,
						                y=Saving_product_ex,
						                name='Expenses',
						                text=(Saving_product_ex/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='darkred'
						                )
						            ),                                    
						        ],
						        layout=go.Layout(
						            # barmode="stack",
						            showlegend=True,
						            legend=go.layout.Legend(
						                x=1.0,
						                y=1.0,
						                xanchor="center",
    									yanchor="top",
						            ),
						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
# 						            barmode="stack",                                    
						            title=go.layout.Title(
										text="Profitability on saving account products (Million Rwf)[{}]".format(cust_type),
									# 	xref="paper",
# 										x=0.5
									),
									xaxis=go.layout.XAxis(
										title=go.layout.xaxis.Title(
											text="Products",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
										)
									),
									yaxis=go.layout.YAxis(
										title=go.layout.yaxis.Title(
											text="Amount(Rwf)",
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
						    id='my-graph_1',
						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Profitability trend" )}),
						),
                    	], 
                    	id="loan",
                    	# style={'width': 700,},
                    ),
                ],
                body=True,
                style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
            ),                      
		]),        
        html.Div([]),        
        html.Div([html.H3(['Term deposit account products'])]),
        html.Div([]),
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([
                    	dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=Term_Dep_product.index,
						                y=Term_Dep_product,
						                name='Interest income',
						                text=(Term_Dep_product/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color="#45b6fe"
						                )
						            ),
						            go.Bar(
						                x=Term_Dep_product_fee.index,
						                y=Term_Dep_product_fee,
						                name='Fees&commissions',
						                text=(Term_Dep_product_fee/1e6).round(2),
            							textposition='outside',
                                        visible="legendonly",
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='#000080'
						                )
						            ),
						            go.Bar(
						                x=Term_Dep_product_ex.index,
						                y=Term_Dep_product_ex,
						                name='Expenses',
						                text=(Term_Dep_product_ex/1e6).round(2),
            							textposition='outside',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='darkred'
						                )
						            ),                                   
						        ],
						        layout=go.Layout(
						            # barmode="stack",
						            showlegend=True,
						            legend=go.layout.Legend(
						                x=1.0,
						                y=1.0,
						                xanchor="center",
    									yanchor="top",
						            ),
						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
# 						            barmode="stack",                                    
						            title=go.layout.Title(
										text="Profitability on term deposit account products(Million Rwf)[{}]".format(cust_type),
									# 	xref="paper",
# 										x=0.5
									),
									xaxis=go.layout.XAxis(
										title=go.layout.xaxis.Title(
											text="Products",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
										)
									),
									yaxis=go.layout.YAxis(
										tickformat = ',3%',                                         
										title=go.layout.yaxis.Title(
											text="Amount(Rwf)",
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
						    id='my-graph_1', 
						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Profitability trend" )}),
						),
                    	], 
                    	id="loan",
                    	# style={'width': 700,},
                    ),
                ],
                body=True,
                style={"padding":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
            ),                      
		]),        
        ##################################################
	])

	return output