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


import numpy as np

from app import app, session_id
from components import *
from config import *

pio.templates.default = "plotly_white"

layout = html.Div(
	[	        
		html.H1("Accounts ownership",id="general_overview"),
		html.Hr(),        
#     html.P('This section shows the details of all account types such as current, Saving and Term deposit accounts. To view information based on business category, choose one of the radio buttons i.e. ALL, RETAIL, SME, CORPORATE. For graphs showing trends overtime, buttons 1 MONTH, 3 MONTHS, 6 MONTHS, 1 YEAR and ALL allow one to see trends over one month, three months and so on. In addition, for each graph you can choose one field you want to see clearly by disabling others i.e. click on an item in the legend to disable it for example to view all accounts apart from current ones, double click on the current item in the legend.'),        
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
			html.Div(id="overview_infoo"),
			dcc.Interval(id="update-overview_infoo", interval=1000*60*60*2, n_intervals=0),
		]),
		html.Div([
			html.Div(id="overview_grapho"),
			dcc.Interval(id="update-overview_grapho", interval=1000*60*60*2, n_intervals=0),
		]),                    
	],
)

#############################################################################################
###################### layout callback ######################################################
#############################################################################################
@app.callback(
	[
		Output("overview_infoo","children"),
	],
	[
		Input("update-overview_infoo", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_info(n, cust_type):
    

    (
		current_acc, saving_acc, term_acc,credit_acc, youth_acc, term_deposit_acc, 
        acc_type,term_deposit_dorm,term_deposit_clos,term_deposit_inact,term_deposit_act,youth_dorm,
        youth_clos,youth_inact,youth_act,current_dorm,current_clos,
        current_inact,current_act,term_acc_age,saving_acc_age,current_acc_age
	)=get_account_branch_level(session_id, cust_type)
    
    current=current_act.sum()+ current_inact.sum()+ current_dorm.sum()
    saving=youth_act.sum()+youth_inact.sum()+youth_dorm.sum()
    term_deposit=term_deposit_act.sum()+term_deposit_inact.sum()+term_deposit_dorm.sum()    

    return [dbc.CardDeck(
			[
                dbc.Card(
                    [
                        html.H5("Current accounts"),                        
                        html.H2("{:,.0f}({:,.0f}%)".format(current,current*100/(current+saving+term_deposit))),
                       
                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
                ),
                dbc.Card(
                    [
                        html.H5("Saving accounts"),                        
                        html.H2("{:,.0f}({:,.0f}%)".format(saving,saving*100/(current+saving+term_deposit))),
                    
                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.H5("Term deposit accounts"),                        
                        html.H2("{:,.0f}({:,.1f}%)".format(term_deposit,term_deposit*100/(current+saving+term_deposit))),
                    ],
                    body=True,
                ),
			],
			
		),
    ]

###################################################################################################
@app.callback(
	Output("overview_grapho","children"),
	[
		Input("update-overview_grapho", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_graph(n, cust_type):

	colors_sbu=['#45b6fe', '#000080', 'blueviolet']
	colors_gender=['#45b6fe', '#000080', 'blueviolet']
# 	colors_acc=['#45b6fe','#000080','blueviolet', '#494c53']    
	colors_acc=['#45b6fe','#000080','#494c53']    
	customers, num_accounts= get_customer_sbu_gender_age_segment(session_id, cust_type)    

	(
		current_acc, saving_acc, term_acc,credit_acc, youth_acc, term_deposit_acc, 
        acc_type,term_deposit_dorm,term_deposit_clos,term_deposit_inact,term_deposit_act,youth_dorm,
        youth_clos,youth_inact,youth_act,current_dorm,current_clos,
        current_inact,current_act,term_acc_age,saving_acc_age,current_acc_age
	)= get_account_branch_level(session_id, cust_type)


	customer_sbu = customers[customers.VISION_SBU!='NA'].groupby("VISION_SBU").CUSTOMER_ID.nunique()
       
	customer_gender = customers[(customers.CUSTOMER_SEX!='NA')&(customers.VISION_SBU == "R")].groupby("CUSTOMER_SEX").CUSTOMER_ID.nunique()
  
	colors_overd = ["#000080","#45b6fe"]
        
	output =  html.Div([            
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([
                    	dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Scatter(
						                x=credit_acc.index,
						                y=np.cumsum(credit_acc),
						                name='Current',
                                        fill="tonexty",
										marker=go.scatter.Marker(color='#494c53'),
						            ),
						            go.Scatter(
						                x=youth_acc.index,
						                y=np.cumsum(youth_acc),
						                name='Saving',
                                        fill="tonexty",
                                        visible='legendonly',
										marker=go.scatter.Marker(color='#000080'),
						            ),
						            go.Scatter(
						                x=term_deposit_acc.index,
						                y=np.cumsum(term_deposit_acc),
						                name='Term deposit',
                                        fill="tonexty",
                                        visible='legendonly',
										marker=go.scatter.Marker(color='#004206')
						            ),
						        ],
#                                 data=[trace]
						        layout=go.Layout(
						            showlegend=True,
						            legend=go.layout.Legend(
						                x=0.09,
						                y=1.0,
						                xanchor="center",
    									yanchor="top",
						            ),
						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
                                    xaxis_rangeslider_visible=True,
						            title=go.layout.Title(
										text="Accounts type overtime[{}]".format(cust_type),
#                                         x=0.5, 
#                                         y=0.99
									),
									xaxis=go.layout.XAxis(
                                        type="date"
                                        ),                                        

									),                                
						        )                           
						    ),
                        
                    	], 
                    	id="account_time",

                    ),
                ],
                body=True,
                style={"margin":"15px 15px 15px 15px",}# "margin":"5px 15px 5px 5px",},
            ),
        ]),        
		dbc.CardGroup(
			[
	            dbc.Card(
	                [
	      				html.Div([
						    dcc.Graph(
							    figure=go.Figure(
							        data=[
							        	go.Bar(
							                x=num_accounts.index,
							                y=num_accounts,
							                name='Number of Accounts',
							                text=get_percentage_label((num_accounts/num_accounts.sum()*100).round(2)),
	            							textposition='auto',
							                marker=go.bar.Marker(
							                    color="#000080"
							                )
							            ),
							        ],
							        layout=go.Layout(
                                        showlegend=False,
                                        title=go.layout.Title(
                                            text="Number of Accounts  per Customer[{}]".format(cust_type),
                                        # 	xref="paper",
                                        	x=0.1
                                        ),  
                                        xaxis=go.layout.XAxis(
                                            title=go.layout.xaxis.Title(
                                            text="Number of accounts",
#                                             x=0.5,
                                            # y=-0.3,
#                                             font=dict(
# #                                                 family="Courier New, monospace",
#                                                 size=18,
#                                                 color="#7f7f7f"
#                                                 )
                                            )
                                        ),
                                        yaxis=go.layout.YAxis(
                                            title=go.layout.yaxis.Title(
                                            text="Number of customers",
                                            # font=dict(
#                                                 family="Courier New, monospace",
                                                # size=18,
                                                # color="#7f7f7f"
                                                # )
                                            )
                                        ),
							            margin=go.layout.Margin(l=5, r=5, t=30, b=5)
							        ),
							    ),
							    id='my-graph-60',
							    config = add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Distribution of the Number of Accounts  per Customer")}),
							)
						])
	                ],
	                body=True,
	                style={"padding":"5px 5px 5px 5px", },
	            ),               
	        ]
	    ),                
		############################autoscaling of graph##########
               
		dbc.CardGroup([
			dbc.Card(
				[
					dcc.Graph(
					    figure=go.Figure(
					        data=[
					            go.Bar(
					                x=current_acc_age.index,
					                y=current_acc_age,
					                name='Current',
					                text=get_percentage_label((current_acc_age*100/(current_acc_age.sum())).round()),
	    							textposition='auto',

					                marker=go.bar.Marker(
					                    color='#45b6fe'# "color='rgb(26, 118, 255)'
					                )
                                ),
					            go.Bar(
					                x=saving_acc_age.index,
					                y=saving_acc_age,
					                name='Saving',
                                    visible='legendonly',
					                text=get_percentage_label((saving_acc_age*100/(saving_acc_age.sum())).round(2)),
	#                                         line_color='dimgray'
	    							textposition='auto',
	    				# 			base=retail_perf,
	    				# 			width = 0.3,
									# offset = -0.3,
					                marker=go.bar.Marker(
					                    color='#000080'#color='rgb(55, 83, 109)'
					                )
					            ),
					            go.Bar(
					                x=term_acc_age.index,
					                y=term_acc_age,
					                name='Term deposit',
                                    visible='legendonly',
					                text= get_percentage_label((term_acc_age*100/(term_acc_age.sum())).round(2)),
	    							textposition='auto',
					                marker=go.bar.Marker(
					                    color='#004206'# "color='rgb(26, 118, 255)'
					                )
					            ),					            
					        ],
					        layout=go.Layout(
					            showlegend=True,
					            barmode="stack",
					            legend=go.layout.Legend(
					                x=1.0,
					                y=1.0,
					                xanchor="right",
									yanchor="auto",
					            ),
					            margin=go.layout.Margin(l=10, r=0, t=40, b=10),
# 					            barmode="stack",                                
					            title=go.layout.Title(
									text="Account type by customer's age[{}]".format(cust_type),
								# 	xref="paper",
# 									x=0.5
								),
								xaxis=go.layout.XAxis(
									title=go.layout.xaxis.Title(
										text="Age Group",
									)
								),
								yaxis=go.layout.YAxis(
									title=go.layout.yaxis.Title(
										text="Number of accounts",
									)
								)
					        ),
					    ),
					    # style = {'display': 'inline-block', 'width': '50%'}, #style={'height': 300, 'width': 100},
					    id='my-graph-0_4',
					    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Account type by customer's age" )}),
					    # style={'height': 700,},
					),
	            ],
	            body=True,
                style={"padding":"5px 5px 5px 5px", },                
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
						                x=current_acc.rename(index=branch_name_mapping).index,
						                y=current_acc.values,#.round(2),
						                name='Current',
						                text=get_percentage_label((current_acc/current_acc.sum()*100).round()),
	        							textposition='auto',
	        	# 						base=overdraft,
	        	# 						width = 0.5,
										# offset = -0.5,
						                marker=go.bar.Marker(
						                    color="#45b6fe"
						                )
						            ),
						        	go.Bar(
						                x=saving_acc.rename(index=branch_name_mapping).index,
						                y=saving_acc.values,#.round(2),
						                name='Saving',
                                        visible='legendonly',
						                text=get_percentage_label((saving_acc/saving_acc.sum()*100).round()),
	        							textposition='auto',
	        	# 						base=overdraft+current_acc,
	        	# 						width = 0.5,
										# offset = -0.5,
						                marker=go.bar.Marker(
						                    color="#000080"
						                )
						            ), 
						            go.Bar(
						                x=term_acc.rename(index=branch_name_mapping).index,
						                y=term_acc.values,#.round(2),
						                name='Term Deposit',
                                        visible='legendonly',
						                text=get_percentage_label((term_acc/term_acc.sum()*100).round(2)),
	        							textposition='auto',

						                marker=go.bar.Marker(
						                    color="#004206"
						                )
						            ),                                        
						        ],
						        layout=go.Layout(
						            barmode="stack",
						            # showlegend=True,
						            legend=go.layout.Legend(
						                x=1.0,
						                y=1.0,
						                xanchor="center",
										yanchor="top",
						            ),
						            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
#                                     barmode='stack',
						            title=go.layout.Title(
										text="Number of accounts at Branch level[{}]".format(cust_type),
#                                         x=0.5
									),
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
											text="Number of Accounts",
										)
									)
						        )
						    ),

						    id='graph-11.1',
						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Number of accounts at Branch level: Overdraft Account & Current Account" )}),
						),
	                ]),
	            ],
	            body=True,
                style={"padding":"5px 5px 5px 5px", },# "margin":"5px 15px 5px 5px",},
	        ),
	    ]),                
	])
	return output

