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
		html.H1("Accounts status",id="general_overview"),
		html.Hr(),        
#     html.P('This section shows accounts status, the number of active, inactive,dormant and closed. To view information based on business category, choose one of the radio buttons i.e. ALL, RETAIL, SME, CORPORATE. For graphs showing trends overtime, buttons 1 MONTH, 3 MONTHS, 6 MONTHS, 1 YEAR and ALL allow one to see trends over one month, three months and so on. In addition, for each graph you can choose one field you want to see clearly by disabling others i.e. click on an item in the legend to disable it for example to view all accounts apart from active ones, double click on the active item in the legend.'),        
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
			html.Div(id="overview_infos"),
			dcc.Interval(id="update-overview_infos", interval=1000*60*60*2, n_intervals=0),
		]),
		html.Div([
			html.Div(id="overview_graphs"),
			dcc.Interval(id="update-overview_graphs", interval=1000*60*60*2, n_intervals=0),
		]),                    
	],
)

#############################################################################################
###################### layout callback ######################################################
#############################################################################################
@app.callback(
	[
		Output("overview_infos","children"),
	],
	[
		Input("update-overview_infos", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_info(n, cust_type):

    (customer_Opening,account_Opening,customer_open,account_open,active_cust,inactive_cust,active,inactive,dormant,active_cust,inactive_cust,dormant_cust) = get_customer_account_trend_data(session_id, cust_type)


    (active_accounts, inactive_accounts, closed_accounts, dormant_accounts,active_overtime,
            inactive_overtime,closed_overtime,dormant_overtime,Account_status,active_off,inactive_off,closed_off,dormant_off,
           active_life,inactive_life,closed_life,dormant_life,Account_active,Account_inactive,Account_closed,Account_dormant)= get_accounts_status(session_id, cust_type)
    all_accounts = active_accounts + inactive_accounts + closed_accounts + dormant_accounts    
    return [dbc.CardDeck(
			[
                dbc.Card(
                    [
                        html.H5("Active accounts"),                        
                        html.H2("{:,.0f}({:,.0f} %)".format(Account_active,Account_active*100/(Account_active+Account_inactive+Account_closed+Account_dormant))),
                       
                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
                ),
                dbc.Card(
                    [
                        html.H5("Inactive accounts"),                        
                        html.H2("{:,.0f}({:,.0f} %)".format(Account_inactive,Account_inactive*100/(Account_active+Account_inactive+Account_closed+Account_dormant))),
                      
                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.H5("Dormant accounts"),                                             
                        html.H2("{:,.0f}({:,.0f} % )".format(Account_dormant,Account_dormant*100/(Account_active+Account_inactive+Account_closed+Account_dormant)), style={"color":"#000080"}),

                    ],
                    body=True,
                ),
                dbc.Card(
                    [
                        html.H5("Closed accounts"),                                             
                        html.H2("{:,.0f}({:,.0f} % )".format(Account_closed,Account_closed*100/(Account_active+Account_inactive+Account_closed+Account_dormant)), style={"color":"#000080"}),

                    ],
                    body=True,
                ),                
			],
			
		),
	]

###################################################################################################
@app.callback(
	Output("overview_graphs","children"),
	[
		Input("update-overview_graphs", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_graph(n, cust_type):

	colors_sbu=['#45b6fe', '#000080', 'blueviolet']
	colors_gender=['#45b6fe', '#000080', 'blueviolet']
# 	colors_acc=['#45b6fe','#000080','blueviolet', '#494c53']    
	colors_acc=['#45b6fe','#000080','#494c53']    
	customers= get_customer_sbu_gender_age_segment(session_id, cust_type)    

	(
		current_acc, saving_acc, term_acc,credit_acc, youth_acc, term_deposit_acc, 
        acc_type,term_deposit_dorm,term_deposit_clos,term_deposit_inact,term_deposit_act,youth_dorm,
        youth_clos,youth_inact,youth_act,current_dorm,current_clos,
        current_inact,current_act,term_acc_age,saving_acc_age,current_acc_age
	)= get_account_branch_level(session_id, cust_type)
    
	(
	    # active_, inactive_, closed_, dormant_,
        age_active, age_inactive, age_closed, age_dormant,
	) = get_customer_status_sbu_gender_age(session_id, cust_type)


	(active_accounts, inactive_accounts, closed_accounts, dormant_accounts,active_overtime,
            inactive_overtime,closed_overtime,dormant_overtime,Account_status,active_off,inactive_off,closed_off,dormant_off,
    active_life,inactive_life,closed_life,dormant_life,Account_active,Account_inactive,Account_closed,Account_dormant)= get_accounts_status(session_id, cust_type)
	all_accounts = active_accounts + inactive_accounts + closed_accounts + dormant_accounts

	active_customers, inactive_customers, closed_customers, dormant_customers = get_customer_by_accounts_status(session_id, cust_type)
	all_customers = active_customers + inactive_customers + closed_customers + dormant_customers
    
	age=age_active+age_inactive+age_closed+age_dormant

# 	colors_interest=['grey','darkred']    
	colors_overd = ["#000080","#45b6fe"]
# 	colors_sbu = ["#494c53","#000080","45b6fe"]

        
	output =  html.Div([
               
		dbc.CardGroup([
			dbc.Card(
                [
                    html.Div([
                    	dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=active_accounts.index,
						                y=active_accounts,
						                name='Active',
						                text=get_percentage_label((active_accounts/all_accounts*100).round()),
            							textposition='auto',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color="#45b6fe"
						                )
						            ),
						            go.Bar(
						                x=dormant_accounts.index,
						                y=dormant_accounts,
						                name='Dormant',
						                text=get_percentage_label((dormant_accounts/all_accounts*100).round()),
            							textposition='auto',
          #   							base=0,
          #   							width = 0.4,
										# offset = -0.4,
						                marker=go.bar.Marker(
						                    color='#494c53'
						                )
						            ),
						            go.Bar(
						                x=inactive_accounts.index,
						                y=inactive_accounts,
						                name='Inactive',
                                        visible='legendonly',
						                text=get_percentage_label((inactive_accounts/all_accounts*100).round()),
            							textposition='auto',
          #   							width = 0.4,
										# offset = 0.0,
						                marker=go.bar.Marker(
						                    color='#000080'
						                )
						            ),
						            go.Bar(
						                x=closed_accounts.index,
						                y=closed_accounts,
						                name='Closed',
                                        visible='legendonly',
						                text=get_percentage_label((closed_accounts/all_accounts*100).round()),
            							textposition='auto',
          #   							width = 0.4,
										# offset = 0.0,
						                marker=go.bar.Marker(
						                    color='blueviolet'
						                )
						            ),  
						        ],
						        layout=go.Layout(
						            barmode="stack",
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
										text="Account Status based on account tenure[{}]".format(cust_type),
									# 	xref="paper",
# 										x=0.5
									),
									xaxis=go.layout.XAxis(
										title=go.layout.xaxis.Title(
											text="Accounts tenure",
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
						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Account Status Segmentation Over Time" )}),
						),
                    	], 
                    	id="loan",
                    	# style={'width': 700,},
                    ),
                ],
                body=True,
                style={"padding":"5px 5px 5px 5px", },# "margin":"5px 15px 5px 5px",},
            ),
            dbc.Card(
                [
                    html.Div([
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Bar(
                                        x=current_act.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=current_act,
                                        legendgroup="active",
#                                             legendgroup="",
                                        name='Active',
text=get_percentage_label((current_act*100/(current_dorm+current_act+current_inact+current_clos))[current_act.index].fillna(0).round(2)),
#                                         showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#45b6fe"
                                        )
                                    ),
                                    go.Bar(
                                        x=current_inact.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=current_inact,
                                        legendgroup="inactive",
#                                             legendgroup="",
                                        name='Inactive',
                                        visible='legendonly',
text=get_percentage_label((current_inact*100/(current_dorm+current_act+current_inact+current_clos))[current_inact.index].fillna(0).round(2)),
#                                         showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#000080"
                                        )
                                    ),
                                    go.Bar(
                                        x=current_clos.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=current_clos,
                                        legendgroup="closed",
#                                             legendgroup="",
                                        name='Closed',
                                        visible='legendonly',
text=get_percentage_label((current_clos*100/(current_dorm+current_act+current_inact+current_clos))[current_clos.index].fillna(0).round(2)),
#                                         showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="blueviolet"
                                        )
                                    ), 
                                    go.Bar(
                                        x=current_dorm.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=current_dorm,
                                        legendgroup="dormant",
#                                             legendgroup="",
                                        name='Dormant',
text=get_percentage_label((current_dorm*100/(current_dorm+current_act+current_inact+current_clos))[current_clos.index].fillna(0).round(2)),
#                                         showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#494c53"
                                        )
                                    ),
                                    go.Bar(
                                        x=youth_act.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=youth_act,
                                        legendgroup="active",
#                                             legendgroup="",
                                        name='Active',
text=get_percentage_label((youth_act*100/(youth_act+youth_clos)).round(2)),
                                        showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#45b6fe"
                                        )
                                    ),                                        
                                    go.Bar(
                                        x=youth_inact.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=youth_inact,
                                        legendgroup="inactive",
#                                             legendgroup="",
                                        name='Inactive',
                                        visible='legendonly',
text=get_percentage_label((youth_inact*100/(youth_dorm+youth_act+youth_inact+youth_clos)).round(2)),
                                        showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#000080"
                                        )
                                    ),
                                    go.Bar(
                                        x=youth_clos.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=youth_clos,
                                        legendgroup="closed",
#                                             legendgroup="",
                                        name='Closed',
                                        visible='legendonly',
text=get_percentage_label((youth_clos*100/(youth_act+youth_clos)).round(2)),
                                        showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="blueviolet"
                                        )
                                    ),
                                    go.Bar(
                                        x=youth_dorm.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=youth_dorm,
                                        legendgroup="dormant",
#                                             legendgroup="",
                                        name='Dormant',
text=get_percentage_label((youth_dorm*100/(youth_dorm+youth_act+youth_inact+youth_clos)).round(2)),
                                        showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#494c53"
                                        )
                                    ),
                                    go.Bar(
                                        x=term_deposit_act.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=term_deposit_act,
                                        legendgroup="active",
#                                             legendgroup="",
                                        name='Active',
text=get_percentage_label((term_deposit_act*100/(term_deposit_act)).round(2)),
                                        showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#45b6fe"
                                        )
                                    ),
                                    go.Bar(
                                        x=term_deposit_inact.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=term_deposit_inact,
                                        legendgroup="inactive",
#                                             legendgroup="",
                                        name='Inactive',
                                        visible='legendonly',
text=get_percentage_label((term_deposit_inact*100/(term_deposit_dorm+term_deposit_act+term_deposit_inact+term_deposit_clos))[term_deposit_inact.index].fillna(0).round(2)),
                                        showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#000080"
                                        )
                                    ),
                                    go.Bar(
                                        x=term_deposit_clos.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=term_deposit_clos,
                                        legendgroup="closed",
#                                             legendgroup="",
                                        name='Closed',
                                        visible='legendonly',
text=get_percentage_label((term_deposit_clos*100/(term_deposit_dorm+term_deposit_act+term_deposit_inact+term_deposit_clos))[term_deposit_clos.index].fillna(0).round(2)),
                                        showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="blueviolet"
                                        )
                                    ),
                                    go.Bar(
                                        x=term_deposit_dorm.rename(index=ACCOUNT_TYPE_MAPPING).index,
                                        y=term_deposit_dorm,
                                        legendgroup="dormant",
#                                             legendgroup="",
                                        name='Dormant',
text=get_percentage_label((term_deposit_dorm*100/(term_deposit_dorm+term_deposit_act+term_deposit_inact+term_deposit_clos))[term_deposit_dorm.index].fillna(0).round(2)),
                                        showlegend=False,
                                        textposition='auto',
                                        marker=go.bar.Marker(
                                            color="#494c53"
                                        )
                                    ),                                       
                                ],
                                layout=go.Layout(
                                    margin=go.layout.Margin(l=40, r=0, t=40, b=30),                                    
                                   title=go.layout.Title(
                                        text="Accounts Distribution[{}]".format(cust_type),
                                    # 	xref="paper",
                                        x=0.1
                                    ),
                                    legend=go.layout.Legend(
                                        x=1.0,
                                        y=1.0,
                                        xanchor="center",
                                        yanchor="top",
                                    ),                                        
# 							            title="Number of Accounts per Account Type",
                                    barmode='stack',
                                    xaxis=go.layout.XAxis(
                                        title=go.layout.xaxis.Title(
                                        text="Account Type",

                                        )
                                    ),
                                    yaxis=go.layout.YAxis(
                                        title=go.layout.yaxis.Title(
                                        text="Number of Accounts",
)
                                        )
                                    ),

#                                     margin=go.layout.Margin(l=5, r=5, t=30, b=5)
                                ),
                            ),
                    ])
                ],
                body=True,
                style={"padding":"5px 5px 5px 5px", },
            ),                
            
		]),
		dbc.CardGroup([
			dbc.Card(
				[
					dcc.Graph(
					    figure=go.Figure(
					        data=[
					            go.Bar(
					                x=age_active.index,
					                y=age_active,
					                name='Active',
					                text=get_percentage_label((age_active*100/age_active.sum()).round()),
	    							textposition='auto',
	    				# 			base=0,
	    				# 			width = 0.3,
									# offset = -0.3,
					                marker=go.bar.Marker(
					                    color='#45b6fe'#color='rgb(55, 83, 109)'
					                )
					            ),
					            go.Bar(
					                x=age_dormant.index,
					                y=age_dormant,
					                name='Dormant',
	#                                       line_color='deepskyblue'
					                text= get_percentage_label((age_dormant*100/age_dormant.sum()).round()),
	    							textposition='outside',
	    							# base=sme_perf,
	    				# 			width = 0.3,
									# offset = 0.0,
					                marker=go.bar.Marker(
					                    color='#494c53'# "color='rgb(26, 118, 255)'
					                )
					            ),
					            go.Bar(
					                x=age_inactive.index,
					                y=age_inactive,
					                name='Inactive',
                                    visible='legendonly',
					                text=get_percentage_label((age_inactive*100/age_inactive.sum()).round()),
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
					                x=age_closed.index,
					                y=age_closed,
					                name='Closed',
                                    visible='legendonly',
	#                                       line_color='deepskyblue'
					                text= get_percentage_label((age_closed*100/age_closed.sum()).round()),
	    							textposition='auto',

					                marker=go.bar.Marker(
					                    color='blueviolet'# "color='rgb(26, 118, 255)'
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
									yanchor="top",
					            ),
					            margin=go.layout.Margin(l=10, r=0, t=40, b=10),
# 					            barmode="stack",                                
					            title=go.layout.Title(
									text="Accounts status by customer's Age[{}]".format(cust_type),
								# 	xref="paper",
# 									x=0.5
								),
								xaxis=go.layout.XAxis(
									title=go.layout.xaxis.Title(
										text="Age Group",
										# font=dict(
										#     family="Courier New, monospace",
										#     size=18,
										#     color="#7f7f7f"
										# )
									)
								),
								yaxis=go.layout.YAxis(
									title=go.layout.yaxis.Title(
										text="Number of Customers",
										# font=dict(
										#     family="Courier New, monospace",
										#     size=18,
										#     color="#7f7f7f"
										# )
									)
								)
					        ),
					    ),
					    # style = {'display': 'inline-block', 'width': '50%'}, #style={'height': 300, 'width': 100},
					    id='my-graph-0_4',
					    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Customer Segmentation by Age" )}),
					    # style={'height': 700,},
					),
	            ],
	            body=True,
                style={"padding":"5px 5px 5px 5px", },                
            ),
        ]),
# 		dbc.CardGroup([
# 			dbc.Card(
#                 [
#                     html.Div([
#                     	dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=active_num.index,
# 						                y=active_num,
# 						                name='Active',
# 						                text=get_percentage_label((active_num*100/(active_num.sum())).round(2)),
#             							textposition='auto',
#           #   							base=0,
#           #   							width = 0.4,
# 										# offset = -0.4,
# 						                marker=go.bar.Marker(
# 						                    color="#45b6fe"
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=dorm_num.index,
# 						                y=dorm_num,
# 						                name='Dormant',
# 						                text=get_percentage_label((dorm_num*100/(dorm_num.sum())).round(2)),
#             							textposition='auto',
#           #   							base=0,
#           #   							width = 0.4,
# 										# offset = -0.4,
# 						                marker=go.bar.Marker(
# 						                    color='#494c53'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=inactive_num.index,
# 						                y=inactive_num,
# 						                name='Inactive',
#                                         visible='legendonly',
# 						                text=get_percentage_label((inactive_num*100/(inactive_num.sum())).round(2)),
#             							textposition='auto',
#           #   							width = 0.4,
# 										# offset = 0.0,
# 						                marker=go.bar.Marker(
# 						                    color='#000080'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=clos_num.index,
# 						                y=clos_num,
# 						                name='Closed',
#                                         visible='legendonly',
# 						                text=get_percentage_label((clos_num*100/(clos_num.sum())).round(2)),
#             							textposition='auto',
#           #   							width = 0.4,
# 										# offset = 0.0,
# 						                marker=go.bar.Marker(
# 						                    color='blueviolet'
# 						                )
# 						            ),  
# 						        ],
# 						        layout=go.Layout(
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
# 										text="Account Status based on account's ownership per customer[{}]".format(cust_type),
# 									# 	xref="paper",
# # 										x=0.5
# 									),
# 									xaxis=go.layout.XAxis(
# #                                         tickangle=55,
# 										title=go.layout.xaxis.Title(
# 											text="Number of Accounts per customer",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									),
# 									yaxis=go.layout.YAxis(
# 										title=go.layout.yaxis.Title(
# 											text="Number of customers",
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
# 						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Account Status based on accounts ownership" )}),
# 						),
#                     	], 
#                     	id="loan",
#                     	# style={'width': 700,},
#                     ),
#                 ],
#                 body=True,
#                 style={"padding":"5px 5px 5px 5px", },# "margin":"5px 15px 5px 5px",},
#             ),
# 		]),
	])

	return output

##########################################################################################################
