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
import datetime as dt
import pandas as pd
from app import cache1, TIMEOUT, app, session_id
from components import *
from config import *


ussd_common_layout = html.Div(
	[
		# html.Hr(),
		html.Div(id="ussd_overview", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
		html.Div([
			html.Div(id="ussd_info"),
			dcc.Interval(id="update_ussd_overview", interval=1000*60*60*2, n_intervals=0),
		]),
	],
)        

# 	],
# )

layout = html.Div([
    html.H1('USSD'),
   
	dbc.Row([
		dbc.Col([
			dcc.RadioItems(
				id= "MOB_CAT",
				options=[
				    {'label': 'ALL', 'value': 'All'},#Mobile_APP.VISION_SBU.unique()
				    {'label': 'Retail', 'value':'R'},#Mobile_APP[Mobile_APP.VISION_SBU=='R'].VISION_SBU.unique() 
				    {'label': 'Corporate', 'value':'C'},# Mobile_APP[Mobile_APP.VISION_SBU=='C'].VISION_SBU.unique()                    
				    {'label': 'MSME', 'value':'S' },# Mobile_APP[Mobile_APP.VISION_SBU=='S'].VISION_SBU.unique()
				],
				value='All',
				labelStyle={'display': 'inline-block', 'margin':'10px 10px 10px 10px', 'font-size':20, 'font-style': 'italic'}
			),
		]),
	]),    
	ussd_common_layout,
])


@app.callback(
	Output("ussd_info","children"),
	[
		Input("update_ussd_overview", "n_intervals"),
		Input("MOB_CAT", "value"),
    
	]
)
@cache1.memoize(timeout=TIMEOUT)
def update_ussd_info(n,cust_type):
#     Start = time.time()
    (ussd_Female_overtime,ussd_Male_overtime,ussd_age_female_tr,
     ussd_age_male_tr,ussd_age_female,ussd_age_male)=get_ussd_data(session_id,cust_type)
    
    (ussd_trans_numb,ussd_trans_amt,ussd_cat_INACT,ussd_cat_ACT,ussd_cust,
     ussd_numb,ussd_amt,ussd_trans_cust,customer)=get_ussd_user(session_id,cust_type)
    
    colors_sbu=['darkblue','grey','#45b6fe']
    colors_gender=['#45b6fe','darkblue']       
    
    output= [
		html.Div([]),
        dbc.CardDeck(
			[
	            dbc.Card(
	                [
	                    html.H5("User customers"),                        
	                    html.H3("{:,.0f}".format(ussd_cust), style={"color":"DarkBlue"}),
# 	                    html.H6("Total number of registered customers"),
	                    html.H5("Rate of channel users compared with all customers"),                         
	                    html.H3("{:,.1f}%".format(ussd_cust*100/customer), style={"color":"DarkBlue"}), 
# 	                    html.H6("Rate of channel users compared with all customers"),                    
	                ],
	                body=True,
	                style={"align":"center", "justify":"center",}
	            ),

	            dbc.Card(
	                [
                       
	                    html.H5("Total transaction volume per customer"),                          
	                    html.H3(" rwf {:,.0f}".format(ussd_amt/ussd_cust), style={"color":"#45b6fe"}),                       
	                    html.H5("Number of transactions per customer"),                        
	                    html.H3("{:,.0f}".format(ussd_numb/ussd_cust), style={"color":"#45b6fe"}),
# 	                    html.H6("Total number of transactions"),
	                ],
	                body=True,
	            ),
			],
		),
        dbc.CardGroup(
            [
                dbc.Card(
                    [
                        html.Div([
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Pie(
                                            labels=ussd_cat_ACT.rename(index=SBU_MAPPING).index, 
                                            values=ussd_cat_ACT,
                                            text = ussd_cat_ACT,
                                            hoverinfo= "label+percent+text",
                                            hole=0.5,
                                            marker=go.pie.Marker(
                                                colors= colors_sbu,
                                                # line=dict(color='#000000', width=1),
                                            ),	
                                            # hoverinfo='label+value',
                                        ),
                                    ],
                                    layout=go.Layout(
                                        title="Rate of channel usage based on customer's category",
                                        showlegend=True,
                                        legend=go.layout.Legend(
                                            x=1.0,
                                            y=1.0
                                        ),
                                        margin=go.layout.Margin(l=5, r=5, t=70, b=5),
                                    ),
                                ),
                                style={'height': 300, "top":30},
                            )
                        ]),
                    ],
                    body=True,
                    style={"padding":"5px 5px 5px 5px", },
                ),
                dbc.Card(
                    [
                        html.Div([
                                dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Pie(
                                            labels=ussd_cat_INACT.rename(index=GENDER_MAPPING).index, 
                                            values=ussd_cat_INACT,
                                            text = ussd_cat_INACT,
                                            hoverinfo= "label+percent+text",
                                            hole=0.5,
                                            marker=go.pie.Marker(
                                                colors=  colors_gender,
                                                # line=dict(color='#000000', width=1),
                                            ),						            		
                                        ),
                                    ],
                                    layout=go.Layout(
                                        title="Gender",
                                        showlegend=True,
                                        legend=go.layout.Legend(
                                            x=1.0,
                                            y=1.0
                                        ),
                                        margin=go.layout.Margin(l=5, r=5, t=70, b=5),

                                    )
                                ),
                                style={'height': 300, "top":30},
                            )
                        ]),
                    ],
                    body=True,
                ),  
            ],
        ),        
# ######################################################################################################
# ##########################################customer_trend############################################################

    html.Div([
		dbc.CardGroup([
	        dbc.Card([
			    dcc.Graph(
			        figure=go.Figure(
			            data=[
			                go.Scatter(
			                    x= ussd_Male_overtime.index, 
			                    y= ussd_Male_overtime,
			                    name='Male',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='darkblue'
			                    )
			                ),
			                go.Scatter(
			                    x= ussd_Female_overtime.index, 
			                    y= ussd_Female_overtime,
			                    name='Female',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='#45b6fe'
			                    )
			                ),
			            ],
			            layout=go.Layout(
			                showlegend=True,
# 			                xaxis_rangeslider_visible= True,
			                legend=go.layout.Legend(
			                    x=0,
			                    y=1.0
			                ),
			                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
			             
						    title=go.layout.Title(
								text="Customers usage trend",
                                x=0.5,
                                y=1
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

			]),	
	    ]),
##################################Age ######################################################################
		    dbc.CardGroup([
			    dbc.Card(
		            [
		                html.Div([
					        dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=ussd_age_male.index,
						                y=ussd_age_male,
						                name='Male',
						                text=get_percentage_label((ussd_age_male*100/(ussd_age_male+ussd_age_female)).round(2)),
		    							textposition='auto',
						                marker=go.bar.Marker(
						                    color='darkblue'
						                )
						            ),
						            go.Bar(
						                x=ussd_age_female.index,
						                y=ussd_age_female,
						                name='Female',
						                text=get_percentage_label((ussd_age_female*100/(ussd_age_male+ussd_age_female)).round(2)),
		    							textposition='auto',
						                marker=go.bar.Marker(
						                    color='#45b6fe'
						                )
						            ),  
  
		                        ],   
						        layout=go.Layout(
		                          	title=go.layout.Title(
										text="Amount spent on Channel based on customer's age",
									# 	xref="paper",
									# 	x=0
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
		                                    text="Transaction amount",
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
						            go.Bar(
						                x=ussd_age_male_tr.index,
						                y=ussd_age_male_tr,
						                name='Male',
						                text=get_percentage_label((ussd_age_male_tr*100/(ussd_age_male_tr+ussd_age_female_tr)).round(2)),
		    							textposition='auto',
						                marker=go.bar.Marker(
						                    color='darkblue'
						                )
						            ),
						            go.Bar(
						                x=ussd_age_female_tr.index,
						                y=ussd_age_female_tr,
						                name='Female',
						                text=get_percentage_label((ussd_age_female_tr*100/(ussd_age_male_tr+ussd_age_female_tr)).round(2)),
		    							textposition='auto',
						                marker=go.bar.Marker(
						                    color='#45b6fe'
						                )
						            ),  
  
		                        ],   
						        layout=go.Layout(
		                          	title=go.layout.Title(
										text="Number of transactions based on customers age",
									# 	xref="paper",
									# 	x=0
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
		                                    text="Number of transactions",
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
						                x=ussd_trans_amt.rename(index=tran_type_descr).index,
						                y=(ussd_trans_amt/ussd_trans_numb).round(),
						                name='Amount',
						                text=(ussd_trans_amt/ussd_trans_numb).round(),
		    							textposition='auto',
						                marker=go.bar.Marker(
						                    color='#45b6fe'
						                )
						            ),  
  
		                        ],   
						        layout=go.Layout(
		                          	title=go.layout.Title(
										text=" Amount spent per each transaction(rwf)",
									# 	xref="paper",
									# 	x=0
									),
		                            xaxis=go.layout.XAxis(
		                                title=go.layout.xaxis.Title(
			                                text="Transaction type",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
		                                )
		                            ),
		                            yaxis=go.layout.YAxis(
		                                title=go.layout.yaxis.Title(
		                                    text="Amount per transaction",
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
						),

		                ]),
		            ],
		            body=True,
		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
		        ),
            ]),        
        ]),
# 		#############################Transaction amount and number based on transaction type#################################################
    html.Div([        
		    dbc.CardGroup([
			    dbc.Card(
		            [
		                html.Div([
					        dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=ussd_trans_amt.rename(index=tran_type_descr).index,
						                y=(ussd_trans_amt/ussd_trans_cust).round(),
						                name='Amount',
						                text=(ussd_trans_amt/ussd_trans_cust).round(),
		    							textposition='auto',
						                marker=go.bar.Marker(
						                    color='#45b6fe'
						                )
						            ),        
		                        ],   
						        layout=go.Layout(
		                          	title=go.layout.Title(
										text="Amount per customer(rwf)",
									# 	xref="paper",
									# 	x=0
									),
		                            xaxis=go.layout.XAxis(
		                                title=go.layout.xaxis.Title(
			                                text="Transaction type",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
		                                )
		                            ),
		                            yaxis=go.layout.YAxis(
		                                title=go.layout.yaxis.Title(
		                                    text=" Transaction Amount per customer",
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
						            go.Bar(
						                x=ussd_trans_numb.rename(index=tran_type_descr).index,
						                y=(ussd_trans_numb/ussd_trans_cust).round(),
						                name='Number of Transactions',
						                text=(ussd_trans_numb/ussd_trans_cust).round(),
		    							textposition='auto',
						                marker=go.bar.Marker(
						                    color='#45b6fe'
						                )
						            ),         
		                        ],   
						        layout=go.Layout(
		                          	title=go.layout.Title(
										text="Number of transactions per customer",
									# 	xref="paper",
									# 	x=0
									),
		                            xaxis=go.layout.XAxis(
		                                title=go.layout.xaxis.Title(
			                                text="Transaction type",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
		                                )
		                            ),
		                            yaxis=go.layout.YAxis(
		                                title=go.layout.yaxis.Title(
		                                    text="Transactions per customer",
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
						),

		                ]),
		            ],
		            body=True,
		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
		        ),                 
		    ]),
	    ]),
    ]
#     End = time.time()
#     print("mob_info()", End - Start)    
    return output

# #######################################################################################################
# #######################################################################################################
