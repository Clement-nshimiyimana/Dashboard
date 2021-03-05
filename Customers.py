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

from datetime import datetime, timedelta
import numpy as np

from app import app, session_id
from components import *
from config import *

pio.templates.default = "plotly_white"

layout = html.Div(
	[	        
		html.H1("Customers",id="general_overview"),
# 		html.Hr(),        
#     html.P('This section shows customers details including customer trends,age and gender segmentation. To view information based on business category, choose one of the radio buttons i.e. ALL, RETAIL, SME, CORPORATE. For graphs showing trends overtime, buttons 1 MONTH, 3 MONTHS, 6 MONTHS, 1 YEAR and ALL allow one to see trends over one month, three months and so on. In addition, for each graph you can choose one field you want to see clearly by disabling others i.e. click on an item in the legend to disable it for example to view Male double click on the Male item in the legend.'),        
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
			html.Div(id="overview_info1"),
			dcc.Interval(id="update-overview_info1", interval=1000*60*60*2, n_intervals=0),
		]),
		html.Div([
			html.Div(id="new_opening_trend-line1"),
			dcc.Interval(id="update-new_opening_trend1", interval=1000*60*60*2, n_intervals=0),
		]),        

		html.Div([
			html.Div(id="overview_graph1"),
			dcc.Interval(id="update-overview_graph1", interval=1000*60*60*2, n_intervals=0),
		]),                    
    	# html.Hr(),
	],
)

#############################################################################################
###################### layout callback ######################################################
#############################################################################################
@app.callback(
	[
		Output("overview_info1","children"),
	],
	[
		Input("update-overview_info1", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_info(n, cust_type):

    (customer_Opening,account_Opening,customer_open,account_open,active_cust,inactive_cust,active,inactive,dormant,active_cust,inactive_cust,dormant_cust) = get_customer_account_trend_data(session_id, cust_type)

    Borrowers,od_cust, od_accs,appr_amount,outstanding_am=get_borrowers(session_id, cust_type)    

    return [dbc.CardDeck(
			[
                dbc.Card(
                    [
                        html.H5("Active customers"),                        
                        html.H2("{:,.0f}({:,.0f}%)".format(active_cust,active_cust*100/customer_Opening.sum())),

                        html.H5("Inactive Customers"),                        
                        html.H2("{:,.0f}({:,.0f}%)".format((customer_Opening.sum()-active_cust),(customer_Opening.sum()-active_cust)*100/customer_Opening.sum())),
                        
                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
                ),

                dbc.Card(
                    [
                        html.H5("Borrowing"),                                             
                        html.H2("{:,.0f}({:,.0f}%)".format(Borrowers,Borrowers*100/(customer_Opening.sum())), style={"color":"#000080"}),

                        html.H5("Non Borrowing"),                        
                        html.H2("{:,.0f}({:,.0f}%)".format(customer_Opening.sum()-Borrowers,(customer_Opening.sum()-Borrowers)*100/(customer_Opening.sum())), style={"color":"blueviolet"}),

                    ],
                    body=True,
                ),
			],
			
		),

    ]


###################################################################################################
@app.callback(
	Output("overview_graph1","children"),
	[
		Input("update-overview_graph1", "n_intervals"),
		Input("select-cust_type", "value"),
	]
)
def update_overview_graph(n, cust_type):

	colors_sbu=['#45b6fe', '#000080', 'blueviolet']
	colors_gender=['#45b6fe', '#000080', 'violet']
# 	colors_acc=['#45b6fe','#000080','blueviolet', '#494c53']    
	colors_acc=['#45b6fe','#000080','#494c53']    
	customers, num_accounts= get_customer_sbu_gender_age_segment(session_id, cust_type)    


	customer_sbu = customers[customers.VISION_SBU!='NA'].groupby("VISION_SBU").CUSTOMER_ID.nunique()

	customer_gender = customers[customers.VISION_SBU == "R"].groupby("CUSTOMER_SEX").CUSTOMER_ID.nunique()

	active_customers, inactive_customers, closed_customers, dormant_customers = get_customer_by_accounts_status(session_id, cust_type)
	all_customers = active_customers + inactive_customers + closed_customers + dormant_customers


# 	colors_interest=['grey','darkred']    
	colors_overd = ["#000080","#45b6fe"]
# 	colors_sbu = ["#494c53","#000080","45b6fe"]

	df = customers[(customers.VISION_SBU == "R")]
	retail_trend = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()

	df = customers[(customers.VISION_SBU == "S")]
	sme_trend = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()

	df = customers[(customers.VISION_SBU == "C")]
	corp_trend = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()

	df = customers[(customers.VISION_SBU == "R")&(customers.CUSTOMER_OPEN_DATE>='2015-01-01')]
	retail_new = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()

	df = customers[(customers.VISION_SBU == "S")&(customers.CUSTOMER_OPEN_DATE>='2015-01-01')]
	sme_new = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()

	df = customers[(customers.VISION_SBU == "C")&(customers.CUSTOMER_OPEN_DATE>='2015-01-01')]
	corp_new = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()
    
	# all_sbu = retail_trend + sme_trend + corp_trend

	## Get trend by gender
	df = customers[(customers.CUSTOMER_SEX == "M")&(customers.VISION_SBU == "R")]
	male_trend = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()

	df = customers[(customers.CUSTOMER_SEX == "F")&(customers.VISION_SBU == "R")]
	female_trend = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()

	df = customers[(customers.CUSTOMER_SEX == "M")&(customers.CUSTOMER_OPEN_DATE>='2015-01-01')&(customers.VISION_SBU == "R")]
	male_new = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()

	df = customers[(customers.CUSTOMER_SEX == "F")&(customers.CUSTOMER_OPEN_DATE>='2015-01-01')&(customers.VISION_SBU == "R")]
	female_new = df.groupby("CUSTOMER_OPEN_DATE").CUSTOMER_ID.nunique()
	customers["DATE_OF_BIRTH"]=pd.to_datetime(customers.DATE_OF_BIRTH,errors='coerce')    
	customers['AGE']= (customers.DATE_OF_BIRTH.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425))).fillna(0).astype(int)
	bins=[18, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
	labels = ["18-25","25-30","30-35","35-40","40-45","45-50","50-55","55-60","60+"] 

	df = customers[customers.CUSTOMER_SEX =='M']
	male = df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()

	df = customers[customers.CUSTOMER_SEX =='F']
	female =df.groupby(pd.cut(df["AGE"], bins, include_lowest=True, right=False, labels=labels)).CUSTOMER_ID.nunique()    
	# all_gender = male_trend + female_trend
###########################################Number of accounts vs account status####################################    
	# all_gender = male_trend + female_trend    

	if cust_type == 'R':
		sbu_output= dbc.CardGroup(
			[
                dbc.Card(
                    [
                        html.Div([
                            dcc.Graph(
                                figure=go.Figure(
                                        data=[
                                            go.Scatter(
                                                x= male_new.index, 
                                                y= np.cumsum(male_new.values),
#                                                 text=male_new.pct_change(),
                                                name='Male',
#                                                 fill='tozeroy',
                                                mode= "lines",
                                                marker=go.scatter.Marker(
                                                    color='#000080'
                                                )
                                            ),
                                            go.Scatter(
                                                x= female_new.index, 
                                                y= np.cumsum(female_new.values),
#                                                 text=female_new.pct_change(),
                                                name='Female',
#                                                 fill='tonexty',
                                                mode= "lines",
#                                                 visible='legendonly',
                                                marker=go.scatter.Marker(
                                                    color='#45b6fe'
                                                )
                                            ),
                                        ],
                                        layout=go.Layout(
                                            showlegend=True,
        #                                         xaxis_rangeslider_visible= True,
                                            legend=go.layout.Legend(
                                                x=0,
                                                y=1.0
                                            ),
                                            margin=go.layout.Margin(l=10, r=10, t=60, b=10),

                                            title=go.layout.Title(
                                                text="New Customers over time by Gender[{}]".format(cust_type),
                                            # 	xref="paper",
                                                x=0,
                                                y=0.99
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

                                    ),

                            )
                        ]),
                    ],
                    body=True,
                ),            

            ],            
        )
        

		gender_output= dbc.CardGroup(
			[
                dbc.Card(
                    [
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Bar(
                                        x= male.index,
                                        y= male,
                                        name='Male',
        #                                       line_color='deepskyblue'
                                        text=get_percentage_label((male*100/(male.sum())).round()),
                                        textposition='auto',
                                        # base=sme_perf,
                            # 			width = 0.3,
                                        # offset = 0.0,
                                        marker=go.bar.Marker(
                                            color='#000080'# "color='rgb(26, 118, 255)'
                                        )
                                    ),
                                    go.Bar(
                                        x=female.index,
                                        y=female,
                                        name='Female',
    #                                         visible='legendonly',
                                        text=get_percentage_label((female*100/(female.sum())).round()),
        #                                         line_color='dimgray'
                                        textposition='auto',
                            # 			base=retail_perf,
                            # 			width = 0.3,
                                        # offset = -0.3,
                                        marker=go.bar.Marker(
                                            color='#45b6fe'#color='rgb(55, 83, 109)'
                                        )
                                    ),       
                                ],
                                layout=go.Layout(
                                    showlegend=True,
                                    # barmode="stack",
                                    legend=go.layout.Legend(
                                        x=1.0,
                                        y=1.0,
                                        xanchor="right",
                                        yanchor="auto",
                                    ),
                                    margin=go.layout.Margin(l=10, r=0, t=40, b=10),
    # 					            barmode="stack",                                
                                    title=go.layout.Title(
                                        text="Number of customers per age[{}]".format(cust_type),
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
                                            text="Number of customers",
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
                            config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Number of customers per age" )}),
                            # style={'height': 700,},
                        ),
                    ],
                    body=True,
                    style={"padding":"5px 5px 5px 5px", },                
                ),                
            ],
        )
		gender_output1= dbc.CardGroup(
            [            
            ],
        )    
	elif cust_type == 'ALL':
		sbu_output= dbc.CardGroup(
			[
	            dbc.Card(
	                [
	      				html.Div([
						        dcc.Graph(
							    figure=go.Figure(
							        data=[
							            go.Pie(
							            	labels=customer_sbu.rename(index=SBU_MAPPING).index, 
							            	values=customer_sbu,
							            	hole=0.5,	
							            	marker=go.pie.Marker(
							            		colors=colors_sbu, 
							            		# line=dict(color='#000000', width=1),
						            		),	
						            		# hoverinfo='label+value',
							            ),
							        ],
                                    layout=go.Layout(
                                        title={'text':"Customers per segment"},
                                        showlegend=True,
                                        legend=go.layout.Legend(
                                            x=0,
                                            y=1.0
                                        ),
                                        margin=go.layout.Margin(l=5, r=5, t=30, b=5),

                                    ),

                                    # displaylogo=False,
                                ),
                                style={'height': 300, "top":30},
                                id="pie-cart_1",
                                config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "Customer per Strategy Business Unit (SBU)" )}),
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
                                            labels=customer_gender.rename(index=GENDER_MAPPING).index, 
                                            values=customer_gender,
                                            hole=0.5,
                                            marker=go.pie.Marker(
                                                colors=colors_gender, 
                                                # line=dict(color='#000000', width=1),
                                            ),						            		
                                        ),
                                    ],
                                    layout=go.Layout(
                                        title={'text':"Customer's Gender",'x': 0},
                                        showlegend=True,
                                        legend=go.layout.Legend(
                                            x=0,
                                            y=1.0
                                        ),
                                        margin=go.layout.Margin(l=5, r=5, t=30, b=5),

                                    )
                                ),
                                style={'height': 300, "top":30},
                                id="cart_2",
                                config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "Retail Customers Gender" )}),
                            )
                        ]),
                    ],
                    body=True,
                ),
            ],
        )

		gender_output= dbc.CardGroup(
			[
	            dbc.Card(
	                [
	      				html.Div([
						        dcc.Graph(
								    figure=go.Figure(
							            data=[
							                go.Scatter(
                                                x= retail_trend.index, 
                                                y= np.cumsum(retail_trend.values),
                                                name='Retail Customers',
                                                mode= "lines",
#                                                 fill="tozeroy",
                                                marker=go.scatter.Marker(
                                                    color='#000080'
                                                )
                                            ),
                                            go.Scatter(
                                                x= sme_trend.index, 
                                                y= np.cumsum(sme_trend.values),
                                                name='SME Customers',
#                                                 fill="tonexty",
                                                mode= "lines",
#                                                 visible='legendonly',
                                                marker=go.scatter.Marker(
                                                    color='#494c53'
                                                )
                                            ),
                                            go.Scatter(
                                                x= corp_trend.index, 
                                                y= np.cumsum(corp_trend.values),
                                                name='Corporate Customers',
                                                mode= "lines",
#                                                 fill="tonexty",
                                                visible='legendonly',
                                                marker=go.scatter.Marker(
                                                    color='#45b6fe'
                                                )
                                            ),
                                        ],
                                        layout=go.Layout(
                                            showlegend=True,
        #                                         xaxis_rangeslider_visible= True,
                                            # legend_orientation="h",
                                            legend=go.layout.Legend(
                                                x=0,
                                                y=1.0
                                            ),
                                            margin=go.layout.Margin(l=10, r=10, t=50, b=10),
                                            xaxis_rangeslider_visible=True,
                                            title=go.layout.Title(
                                                text="Segments over time[{}]".format(cust_type),
#                                                 x=0.01,
#                                                 y=0.99
                                            ),
                                            xaxis=go.layout.XAxis(
                                                nticks=24,
                                                tickmode= "auto",
                                                type="date"
                                                ),                                                        
      
                                            )

                                        )
                                    ),

                        ]),
                    ],
                    body=True,
                    style={"padding":"5px 5px 5px 5px", },
                ),
            ]            
        )

	else:
		sbu_output= dbc.CardGroup([])
		gender_output= dbc.CardGroup([])
        
    
	output =  html.Div([
		sbu_output,
		######################################################
		gender_output,
         
	])

	return output


#############################################################################################
@app.callback(
    Output("new_opening_trend-line1","children"),
    [
    	Input('update-new_opening_trend1', 'n_intervals'),
    	Input("select-cust_type", "value"),
    ]
)
def update_new_opening_trend_graph(n, cust_type):

	positive_amt, negative_amt=get_account_cleared_balance_lcy(session_id, cust_type)

	output = html.Div([
# 		dbc.CardGroup([
# 			dbc.Card(
#                 [
#                     html.Div([
#                     	dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=cust_branch.rename(index=branch_name_mapping).index,
# 						                y=cust_branch,
# 						                name='Number of customers',
# 						                text=cust_branch,
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
# 										text="Customers at Branch level[{}]".format(cust_type),
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
# 						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Customers at Branch level" )}),
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
##########################################################Graph aggregation###############################################

