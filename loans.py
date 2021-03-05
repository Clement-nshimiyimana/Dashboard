import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly import tools

import warnings
warnings.filterwarnings("ignore")

from app import cache1, TIMEOUT, app, session_id
from components import *
from config import *

############################################################################################################################## 
###############################################################################################################################
loans_common_layout = html.Div(
	[
		# html.Hr(),
		html.Div(id="set_title", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
		html.Div([
			html.Div(id="loans_info"),
			dcc.Interval(id="update-loans_info", interval=1000*60*60*12, n_intervals=0),
		]),
		html.Div([
			html.Div(id="loans_income_trend"),
			dcc.Interval(id="update-loans_trend", interval=1000*60*60*12, n_intervals=0),
		]),
# 		html.Hr(),
		html.Div([
			html.Div(id="sbu_gender_segmentation"),
			dcc.Interval(id="update-loans_trend", interval=1000*60*60*12, n_intervals=0),
		]),
    	html.Div(id="set_title_2", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
#     	html.Hr(),
		html.Div([
			html.Div(id="segments_interest_rate_segmentation"),
			dcc.Interval(id="update-interest_rate_segmentation", interval=1000*60*60*12, n_intervals=0),
		]),

# 		html.Hr(),
		html.Div([
			html.Div(id="age_segmentation"),
			dcc.Interval(id="update-age_segmentation", interval=1000*60*60*12, n_intervals=0),
		]),
		html.Div(id="set_title_1", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
# 		html.Hr(),
		html.Div([
			html.Div(id="loan_over_time"),
			dcc.Interval(id="update-loan_over_time", interval=1000*60*60*12, n_intervals=0),
		]),
# 		html.Hr(),
		html.Div([
			html.Div(id="loan_by_sector"),
			dcc.Interval(id="update-loan_by_sector", interval=1000*60*60*12, n_intervals=0),
		]),
	],
)

#######################################################################################################################
layout = html.Div([
    html.H1('Loans'),
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
    html.Hr(),
#     html.P('Loan part contains the information specifically to loans including loan types(Vehicle, Construction, Mortgage, Home equity,..) , loan performance at branch level, based on industry sectors(Manufacturing, education, electricity,..), gender and customer’s age range.'),
#     html.P('This page contains the information specifically on loans including loan types e.g. Vehicle, Construction, Mortgage, Home equity etc, loan performance at branch level, based on industry sectors, gender and customer’s age range. To view information based on business category, you can select one of the buttons (ALL, Retail, SME, Corporate) and you can select loan types. For graphs showing trend overtime, there are buttons 1MONTH, 3MONTH,1YEAR which allow one to see the trends over time. In addition, for each graph you can choose one field you want see clearly by disabling others on the plot legend.'),   
#     html.Hr(),
    html.Div([]),
 
	html.H5("Select business unit:"),
	dbc.Row([
		dbc.Col([
			dcc.RadioItems(
				id= "select-loans_group",
				options=[
				    {'label': 'ALL', 'value': 'ALL'},
				    {'label': 'RETAIL', 'value': 'RETAIL'},
				    {'label': 'CORPORATE', 'value': 'CORPORATE'},
				    {'label': 'MSME', 'value': 'SME'},
# 				    {'label': 'STAFF', 'value': 'STAFF'},
				],
				value='ALL',
				labelStyle={'display': 'inline-block', 'margin':'10px 10px 10px 10px', 'font-size':20, 'font-style': 'italic'}
			),
		]),
	]),
	dbc.Row([
		dbc.Col([
			dcc.Dropdown(
		        id="select-loanType",
		        placeholder="Select loan type",
#                 multi=True
		        # style={"width":"700px", "margin":"15px 0 0 40px"},	
		    ),
		]),
	]),
   
	loans_common_layout,
])


#############################################################################################
###################### Llayout callback #####################################################
#############################################################################################

    
@app.callback(
	Output("select-loanType","options"),
	[Input("select-loans_group", "value"),

    ],

)
def select_loan_group(value):
	loans = get_loans_dataset(session_id)
	return select_loan_group_options( session_id, loans, value)

######################################################################################################
######################################################################################################
@cache1.memoize(timeout=TIMEOUT)
def get_loans_overview_info(loans_data, loan_group,loan_selected):

######################Time to default###############################################################################
	loans_data['START_DATE']=pd.to_datetime(loans_data.START_DATE)
	loans_data['years']= loans_data.START_DATE.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425)).fillna(0).astype(int)
	bins=[1, 2, 3,4, 5,np.inf]
	labels = ["1 year", "2 years", "3 years", "4 years", ">5 years"]

	Df = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')]
	TIME= Df.groupby(pd.cut(Df['years'], bins, include_lowest=True, right = False, labels=labels)).CUSTOMER_ID.nunique()    
	customer_sbu = loans_data.groupby("VISION_SBU").CUSTOMER_ID.nunique()
	loan_opening=loans_data.groupby("START_DATE").CONTRACT_ID.nunique()
	loan_open=loans_data[loans_data.START_DATE>='2015-01-01'].groupby("START_DATE").CONTRACT_ID.nunique()    
	cust_opening=loans_data.groupby("START_DATE").CUSTOMER_ID.nunique()
	appr_amount=loans_data.groupby("START_DATE").APPROVED_AMOUNT_LCY.sum()

	amount_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
	amount_non_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
    
# 	branch_perf_main=loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loans_data.VISION_OUC=='RW01002010')].groupby("VISION_OUC").CUSTOMER_ID.nunique()
# 	branch_nonperf_main=loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(loans_data.VISION_OUC=='RW01002010')].groupby("VISION_OUC").CUSTOMER_ID.nunique()

# 	branch_perf=loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loans_data.VISION_OUC!='RW01002010')].groupby("VISION_OUC").CUSTOMER_ID.nunique()
# 	branch_nonperf=loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(loans_data.VISION_OUC!='RW01002010')].groupby("VISION_OUC").CUSTOMER_ID.nunique()
    
# 	branch_nonperf_balance_main = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(loans_data.VISION_OUC=='RW01002010')].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()
# 	branch_perf_balance_main = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loans_data.VISION_OUC=='RW01002010')].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()
    
# 	branch_nonperf_balance = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(loans_data.VISION_OUC!='RW01002010')].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()
# 	branch_perf_balance = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loans_data.VISION_OUC!='RW01002010')].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()    
# 	branch=branch_perf+ branch_nonperf      
	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS']
	segment_perf = dF.groupby('SEGMENT').CUSTOMER_ID.nunique()
	segment_perf_balance = dF.groupby('SEGMENT').OUTSTANDING_PRINCIPAL_LCY.sum()

	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS']
	segment_nonperf = dF.groupby('SEGMENT').CUSTOMER_ID.nunique()
	segment_nonperf_balance = dF.groupby('SEGMENT').OUTSTANDING_PRINCIPAL_LCY.sum()

	product_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').CUSTOMER_ID.nunique()
	product_non_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').CUSTOMER_ID.nunique() 
	product_nonperf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').OUTSTANDING_PRINCIPAL_LCY.sum()
	product_perf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').OUTSTANDING_PRINCIPAL_LCY.sum()
	product= product_perf+ product_non_perf  
	retail_cust = loans_data[loans_data.VISION_SBU == "R"]#["VISION_SBU", "CUSTOMER_ID"]
	retail_cust = retail_cust[retail_cust["GENDER"]!="O"]
	customer_gender = retail_cust.groupby("GENDER").CUSTOMER_ID.nunique()
	amount_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
	amount_non_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()    
    
	## Get interest rate segments
	bins=[0, 16, np.inf]
	labels = ["interest rate < 16%", "interest rate >= 16%"]
	loans_interest_rate = loans_data.groupby(pd.cut(loans_data['INTEREST_RATE'], bins, include_lowest=True, right = False, labels=labels)).CONTRACT_ID.nunique()

	colors_interest=['darkblue','lightblue']    
	colors_sbu=['#45b6fe', '#000080', 'blueviolet']
	colors_gender=['#45b6fe', '#000080', 'violet']
    
	(
        performing_over_time, retail_performing_over_time, sme_performing_over_time, corp_performing_over_time,
        non_performing_over_time, retail_non_performing_over_time, sme_non_performing_over_time, corp_non_performing_over_time,
        performing_by_sector, retail_performing_by_sector, sme_performing_by_sector, corp_performing_by_sector,
        non_performing_by_sector, retail_non_performing_by_sector, sme_non_performing_by_sector, corp_non_performing_by_sector,
		performing_over_time_balance, retail_performing_over_time_balance, sme_performing_over_time_balance, corp_performing_over_time_balance,
		non_performing_over_time_balance, retail_non_performing_over_time_balance, sme_non_performing_over_time_balance, corp_non_performing_over_time_balance,
		performing_by_sector_balance, retail_performing_by_sector_balance, sme_performing_by_sector_balance, corp_performing_by_sector_balance,
		non_performing_by_sector_balance, retail_non_performing_by_sector_balance, sme_non_performing_by_sector_balance, corp_non_performing_by_sector_balance
    ) = get_loans_over_time_and_by_sector(session_id, loans_data, loan_group, loan_selected)

	### Get age segment data
	(
	    age_perf_male, age_nonperf_male, age_perf_fem, age_nonperf_fem,
	    age_perf_male_balance, age_nonperf_male_balance, age_perf_fem_balance, age_nonperf_fem_balance
	) = get_loan_age(session_id, loans_data)


	## Get Total Amount PL and NPL
	number_pl_npl = loans_data.groupby("MAIN_CLASSIFICATION_DESC").CUSTOMER_ID.nunique()
	total_amt_pl_non_pl = loans_data.groupby("MAIN_CLASSIFICATION_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
	sector= performing_by_sector+non_performing_by_sector
	performance_over_time= performing_over_time+non_performing_over_time    
	colors_pl_npl = None
	if number_pl_npl.index[0] != "NON PERFORMING ASSETS":
		colors_pl_npl =  ["darkblue", "darkred"]
	else:
		colors_pl_npl =  [ "darkred", "darkblue"]

	output =  [
		html.Div([]),
		dbc.CardDeck(
			[
	            dbc.Card(
	                [
	                    html.H6("New disbursed Loans on: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                        
	                    html.H3(" {:,.0f}".format(loan_opening[-1]), style={"color":"green"}),                  
	                ],
	                body=True,
	                style={"align":"center", "justify":"center",}
	            ),
	            dbc.Card(
	                [
	                    html.H6("Total Number of ongoing Loans"),                        
	                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()),style={"color":"#45b6fe"}),
	                    html.H6("Total Number of Borrowers"),                         
	                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),                       
	                ],
	                body=True,
	            ),
	            dbc.Card(
	                [
	                    html.H6("Total Approved amount"),                         
	                    html.H3("Rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()), style={"color":"darkblue"}),
	                    html.H6("Total loan Outstanding amount"),                    
	                    html.H3("Rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()), style={"color":"darkblue"}),
                         
	                ],
	                body=True,
	            ),

			],	            
		),

		###############################################################################################################
		html.Div([
			dbc.CardGroup(
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
								            title="Borrowers per Strategy Business Unit (SBU)",
								            showlegend=True,
								            legend=go.layout.Legend(
								                x=1.0,
								                y=1.0
								            ),
								            margin=go.layout.Margin(l=5, r=5, t=50, b=5),
										),
								    ),
								    style={'height': 300, "top":30},
								    id="loan-pie-cart-1",
								    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "Borrowers per Strategy Business Unit (SBU)" )}),
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
								            title="Retail borrower's Gender",
								            # showlegend=True,
								            legend=go.layout.Legend(
								                x=1.0,
								                y=1.0
								            ),
								            margin=go.layout.Margin(l=5, r=5, t=50, b=5),
								            							            				                    	
								        )
								    ),
								    style={'height': 300, "top":30},
								    id="loan-pie-cart",
								    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "borrower's" )}),
								)
		                    ]),
		                ],
		                body=True,
		            ),  
				],
			),
		]),
		####################################################################################
		dbc.CardGroup([
	        dbc.Card([
			    dcc.Graph(
			        figure=go.Figure(
			            data=[

			                go.Scatter(
			                    x= loan_open.index, 
			                    y= loan_open.values,
			                    name='Loans',
			                    mode= "lines",
#                                 connectgaps='True',
			                    marker=go.scatter.Marker(
			                        color='darkblue'
			                    )
			                ),
			            ],
			            layout=go.Layout(
			                showlegend=True,
			                xaxis_rangeslider_visible= True,
			                legend=go.layout.Legend(
			                    x=0,
			                    y=1.0
			                ),
                                       
						    title=go.layout.Title(
								text="New Loans disbursed Over Time",
#                                 x=0,
#                                 y=1
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

                            )

                        )
                    ),

			],style={'padding': 3}),
				dbc.Card(
		            [
		                html.Div([
						        dcc.Graph(
							    figure=go.Figure(
							        data=[
							            go.Pie(
							            	labels=loans_interest_rate.index, 
							            	values=loans_interest_rate,
                                            hole=0.5,
							            	marker=go.pie.Marker(
							            		colors=colors_interest, 
							            		# line=dict(color='#000000', width=1),
						            		),						            		
							            ),
							        ],
							        layout=go.Layout(
							            title="Loan Interest Rate Segmentation",
							            showlegend=True,
							            legend=go.layout.Legend(
							                x=1.0,
							                y=1.0
							            ),
							            margin=go.layout.Margin(l=25, r=25, t=50, b=25),
							            							            				                    	
							        )
							    ),
							    # style={'height': 300, "top":30},
							    id="loan-pie-cart-3",
							    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "Number of Loan Accounts per Segments" )}),
							)
		                ]),
		            ],
		            body=True,
		        ),           
	    ]),

	    html.Div([
		    dbc.CardGroup([
                dbc.Card([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x= product_perf.index, #LOANS['MAIN_CLASSIFICATION_DESC'].fillna(LOANS['MAIN_CLASS']
                                    y= (product_perf_balance+product_nonperf_balance),
                                    text = get_percentage_label(((product_perf_balance+product_nonperf_balance)*100/(product_perf_balance+product_nonperf_balance).sum()).round()),
#                                     name='Product',
                                    textposition='auto',
#                                     customdata= product_perf_balance,
#                                     hovertemplate= format_hover_template(x_label= "Product" , x_unit=""),
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),                           
                            ],
                            layout=go.Layout(
                                barmode="stack",
                                showlegend=False,
                                legend=go.layout.Legend(
                                    x=1.0,
                                    y=1.0
                                ),
#                                 margin=go.layout.Margin(l=10, r=10, t=30, b=10),

                                title=go.layout.Title(
                                    text="Loans volume per product",
                                ),
                                xaxis=go.layout.XAxis(
                                    tickangle=55,
                                    zeroline= True,
                                    title=go.layout.xaxis.Title(
                                        text="Product",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                ),
                                yaxis=go.layout.YAxis(
                                    zeroline= True,
                                    title=go.layout.yaxis.Title(
                                        text="Volume",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                )
                            )
                        ),
                        id="loan-trend-graph-4",
                        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans performance per product")}),
                        style = {"height":750}
                    ),
				]),
            ]),
		    dbc.CardGroup([
		    ]),
		]),
		#########################################################################
		html.Div([]),
	    ##########################################################################
	    html.Div([
# 		    dbc.CardGroup([
# 			    dbc.Card(
# 		            [
# 		                html.Div([
# 					        dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=TIME.index,
# 						                y=TIME,
# # 						                name='Performing', 
# 						                text=TIME,
# # 						                customdata= branch_perf_balance,
# # 						                hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),
# 		    							textposition='outside',
# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),
  
# 		                        ],   
# 						        layout=go.Layout(
# 		                          	title=go.layout.Title(
# 										text="Time to default",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
# 		                                title=go.layout.xaxis.Title(
# 			                                text="Time in years",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# ) 
# 		                                )
# 		                            ),
# 		                            yaxis=go.layout.YAxis(
# 		                                title=go.layout.yaxis.Title(
# 		                                    text="Number of Loans",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 		                                )
# 		                            ), 
# 						            # barmode="stack",
# 						            showlegend=False,
# 						            legend=go.layout.Legend(
# 						                x=0.9,
# 						                y=1.0,
# 						                xanchor="center",
# 										yanchor="top",
# 						            ),
# 						            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
# 						        )
# 						    ),
# 						),

# 		                ]),
# 		            ],
# 		            body=True,
# 		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
# 		        ),
# 		        dbc.Card([
# 				    dcc.Graph(
# 				        figure=go.Figure(
# 				            data=[
# 				                go.Bar(
# 				                    x= performing_over_time.index, 
# 				                    y= (performing_over_time_balance+non_performing_over_time_balance),
# #                                     text=performing_over_time_balance,
# 				                    text = get_percentage_label(((performing_over_time_balance+non_performing_over_time_balance)/((performing_over_time_balance+non_performing_over_time_balance).sum())*100)[performing_over_time.index].fillna(100).round()),
# 		    						textposition='outside',                                    
# 				                    marker=go.bar.Marker(
# 				                        color='darkblue'
# 				                    )
# 				                ),
# 				            ],
# 				            layout=go.Layout(
#                                 barmode="stack",
# #                                 xaxis_rangeslider_visible= True,
# 				                legend=go.layout.Legend(
# 				                    x=1.0,
# 				                    y=1.0
# 				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# 							    title=go.layout.Title(
# 									text="Loans maturity",
# 								),
# 								xaxis=go.layout.XAxis(
# #                                     tickangle=55,
#                                     zeroline= True,
# 									title=go.layout.xaxis.Title(
# 										text="Tenor months",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								),
# 								yaxis=go.layout.YAxis(
#                                     zeroline= True,
# 									title=go.layout.yaxis.Title(
# 										text="Volume",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								)
# 				            )
# 				        ),
# 				        id="loan-trend-graph-5",
# 				        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "(Non) Performing loans Over Time" )}),
# 				    ),
# 				]),                
# 		    ]),                        
# 		    dbc.CardGroup([
# 			    dbc.Card(
# 		            [
# 		                html.Div([
# 					        dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=branch_perf.rename(index=branch_name_mapping).index,
# 						                y=(branch_perf_balance+branch_nonperf_balance),
# 						                name='other branches', 
# 						                text=get_percentage_label(((branch_perf_balance+branch_nonperf_balance)*100/((branch_perf_balance+branch_nonperf_balance).sum()))[branch_perf_balance.index].fillna(100).round()),

# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=branch_perf.rename(index=branch_name_mapping).index,
# 						                y=(branch_perf_balance_main+branch_nonperf_balance_main),
# 						                name='Main branch', 
# 						                text=get_percentage_label(((branch_perf_balance_main+branch_nonperf_balance_main)*100/((branch_perf_balance_main+branch_nonperf_balance_main).sum()))[branch_perf_balance.index].fillna(100).round()),
#                                         visible='legendonly',
# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),
                                     
# 		                        ],   
# 						        layout=go.Layout(
#                                     barmode="stack",
# 		                          	title=go.layout.Title(
# 										text="Loans volume per branch",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
#                                         zeroline= True,
# 		                                title=go.layout.xaxis.Title(
# 			                                text="Branch name",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# ) 
# 		                                )
# 		                            ),
# 		                            yaxis=go.layout.YAxis(
#                                         zeroline= True,
# 		                                title=go.layout.yaxis.Title(
# 		                                    text="Volume",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 		                                )
# 		                            ), 
# 						            # barmode="stack",
# 						            showlegend=True,
# 						            legend=go.layout.Legend(
# 						                x=0.9,
# 						                y=1.0,
# 						                xanchor="center",
# 										yanchor="top",
# 						            ),
# 						            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
# 						        )
# 						    ),
# 						    # style={'height': 400,},
# 						    id='age',
# 						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loan performance based on branch level" )}),
# 						),

# 		                ]),
# 		            ],
# 		            body=True,
# 		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
# 		        ),       
# 		    ]),            
		]),
		##########################################################################
		html.Div([]),
	    ###########################################################################
	    html.Div([
			dbc.CardGroup([                
			]),
		]),
		##########################################################################
		html.Div([
			dbc.CardGroup([
				dbc.Card([
				    dcc.Graph(
				        figure=go.Figure(
				            data=[
				                go.Bar(
				                    x= performing_by_sector.index, 
				                    y= (performing_by_sector_balance+non_performing_by_sector_balance),
				                    text = get_percentage_label((((performing_by_sector_balance+non_performing_by_sector_balance)*100/((performing_by_sector_balance+non_performing_by_sector_balance).sum())))[performing_by_sector_balance.index].fillna(100).round()),
				                    name='Performing',
				                    textposition='auto',
				                    marker=go.bar.Marker(
				                        color='darkblue'
				                    )
				                ),

				            ],
				            layout=go.Layout(
#                                 barmode="stack",
				                showlegend=False,
				                legend=go.layout.Legend(
				                    x=1.0,
				                    y=1.0
				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
							    title=go.layout.Title(
									text="Loans volume per Sectors",
								),
								xaxis=go.layout.XAxis(
									tickangle=55,
                                    zeroline= True,
									title=go.layout.xaxis.Title(
										text="Sectors",
										# font=dict(
										#     family="Courier New, monospace",
										#     size=18,
										#     color="#7f7f7f"
										# )
									)
								),
								yaxis=go.layout.YAxis(
                                    zeroline= True,
									title=go.layout.yaxis.Title(
										text="Volume",
										# font=dict(
										#     family="Courier New, monospace",
										#     size=18,
										#     color="#7f7f7f"
										# )
									)
								)
				            )
				        ),
				        style = {"height":750}
				    ),
				]),
			]),
		]),
	]
	return output

@cache1.memoize(timeout=TIMEOUT)
def get_selected_loan_info(loans_data, loan_group,loan_selected): 
	loans_data['START_DATE']=pd.to_datetime(loans_data.START_DATE)    
	loans_data['years']= loans_data.START_DATE.apply(lambda x:(dt.now()-x) // timedelta(days=365.2425)).fillna(0).astype(int)
	bins=[1, 2, 3,4, 5,np.inf]
	labels = ["1 year", "2 years", "3 years", "4 years", ">5 years"]

	Df = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')]
	TIME= Df.groupby(pd.cut(Df['years'], bins, include_lowest=True, right = False, labels=labels)).CUSTOMER_ID.nunique()
    
	loan_opening=loans_data.groupby("START_DATE").CONTRACT_ID.nunique()
	loan_open=loans_data[loans_data.START_DATE>='2015-01-01'].groupby("START_DATE").CONTRACT_ID.nunique()    
	cust_opening=loans_data.groupby("START_DATE").CUSTOMER_ID.nunique()
	appr_amount=loans_data.groupby("START_DATE").APPROVED_AMOUNT_LCY.sum()

	customer_sbu = loans_data.groupby("VISION_SBU").CUSTOMER_ID.nunique()

	retail_cust = loans_data[loans_data.VISION_SBU == "R"]#["VISION_SBU", "CUSTOMER_ID"]
	retail_cust = retail_cust[retail_cust["GENDER"]!="O"]
	customer_gender = retail_cust.groupby("GENDER").CUSTOMER_ID.nunique()
	amount_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
	amount_non_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
    
    
# 	branch_perf_main=loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loans_data.VISION_OUC=='RW01002010')].groupby("VISION_OUC").CUSTOMER_ID.nunique()
# 	branch_nonperf_main=loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(loans_data.VISION_OUC=='RW01002010')].groupby("VISION_OUC").CUSTOMER_ID.nunique()

# 	branch_perf=loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loans_data.VISION_OUC!='RW01002010')].groupby("VISION_OUC").CUSTOMER_ID.nunique()
# 	branch_nonperf=loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(loans_data.VISION_OUC!='RW01002010')].groupby("VISION_OUC").CUSTOMER_ID.nunique()
    
# 	branch_nonperf_balance_main = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(loans_data.VISION_OUC=='RW01002010')].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()
# 	branch_perf_balance_main = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loans_data.VISION_OUC=='RW01002010')].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()
    
# 	branch_nonperf_balance = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS')&(loans_data.VISION_OUC!='RW01002010')].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()
# 	branch_perf_balance = loans_data[(loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS')&(loans_data.VISION_OUC!='RW01002010')].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()    
# 	branch= branch_perf+ branch_nonperf  
    
	product_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').CUSTOMER_ID.nunique()
	product_non_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').CUSTOMER_ID.nunique()
	product_nonperf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').OUTSTANDING_PRINCIPAL_LCY.sum()
	product_perf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').OUTSTANDING_PRINCIPAL_LCY.sum()
	product= product_perf+product_non_perf   

	### Segments data
	segments = loans_data.groupby("SEGMENT").CUSTOMER_ID.nunique()
	segments_balance = loans_data.groupby("SEGMENT").OUTSTANDING_PRINCIPAL_LCY.sum()

	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS']
	segment_perf = dF.groupby('SEGMENT').CUSTOMER_ID.nunique()
	segment_perf_balance = dF.groupby('SEGMENT').OUTSTANDING_PRINCIPAL_LCY.sum()

	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS']
	segment_nonperf = dF.groupby('SEGMENT').CUSTOMER_ID.nunique()
	segment_nonperf_balance = dF.groupby('SEGMENT').OUTSTANDING_PRINCIPAL_LCY.sum()

	### Account Officer data
	# ao_data = loans_data.groupby("SEGMENT").CONTRACT_ID.nunique()
	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS']
	ao_perf = dF.groupby('AO_NAME').CUSTOMER_ID.nunique()
	ao_perf_balance = dF.groupby('AO_NAME').OUTSTANDING_PRINCIPAL_LCY.sum()

	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS']
	ao_nonperf = dF.groupby('AO_NAME').CUSTOMER_ID.nunique()
	ao_nonperf_balance = dF.groupby('AO_NAME').OUTSTANDING_PRINCIPAL_LCY.sum()
	ao=  ao_perf+ ao_nonperf 
    
	product_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').CUSTOMER_ID.nunique()
	product_non_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').CUSTOMER_ID.nunique()   
	## Get interest rate segments
	bins=[0, 16, np.inf]
	labels = ["interest rate < 16%", "interest rate >= 16%"]
	loans_interest_rate = loans_data.groupby(pd.cut(loans_data['INTEREST_RATE'], bins, include_lowest=True, right = False, labels=labels)).CONTRACT_ID.nunique()

	colors_interest=['darkblue','lightblue']    
# 	colors_gender = ["#45b6fe","#000080"]
	colors_sbu=['#45b6fe', '#000080', 'blueviolet']
	colors_gender=['#45b6fe', '#000080', 'violet']

	## Get Total Amount PL and NPL
	number_pl_npl = loans_data.groupby("MAIN_CLASSIFICATION_DESC").CUSTOMER_ID.nunique()
	total_amt_pl_non_pl = loans_data.groupby("MAIN_CLASSIFICATION_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()
	colors_pl_npl = None
	if number_pl_npl.index[0] != "NON PERFORMING ASSETS":
		colors_pl_npl =  ["darkblue", "darkred"]
	else:
		colors_pl_npl =  [ "darkred", "darkblue"]


	age_output = None
	segmentation_over_time_output = None
	segmentation_by_sector_output = None
    
	account_officer_output= html.Div([dbc.CardGroup([
	    	dbc.Card([
			    dcc.Graph(
			        figure=go.Figure(
			            data=[
			                go.Bar(
			                    x= ao_perf.index, 
			                    y= (ao_perf_balance+ao_nonperf_balance),
			                    text = get_percentage_label(((ao_perf_balance+ao_nonperf_balance)/((ao_perf_balance+ao_nonperf_balance).sum())*100)[ao_perf_balance.index].fillna(100).round()),
# 			                    name='Performing',
			                    textposition='auto',
# 			                    customdata= ao_perf_balance,
# 					            hovertemplate= format_hover_template(x_label= "AO name"),
			                    marker=go.bar.Marker(
			                        color='darkblue'
			                    )
			                ),

			            ],
			            layout=go.Layout(
                            barmode="stack",
			            	showlegend=False,
			                legend=go.layout.Legend(
			                    x=1.0,
			                    y=1.0
			                ),
			                # margin=go.layout.Margin(l=10, r=10, t=30, b=10),
			             
						    title=go.layout.Title(
								text="Loans volume per Account Officer",
							),
							xaxis=go.layout.XAxis(
                                tickangle=55,
                                zeroline= True,
								title=go.layout.xaxis.Title(
									text="Account Officer Name",
									# font=dict(
									#     family="Courier New, monospace",
									#     size=18,
									#     color="#7f7f7f"
									# )
								)
							),
							yaxis=go.layout.YAxis(
                                zeroline= True,
								title=go.layout.yaxis.Title(
									text="Volume",
									# font=dict(
									#     family="Courier New, monospace",
									#     size=18,
									#     color="#7f7f7f"
									# )
								)
							)
			            )
			        ),
			        id="ao-graph-20",
			        style={"width": "100%", "height": "600px"},
			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Number of (Non) Performing Loan per Account Officer")}),
			    ),
			], body=True,
			),
		]),                                                                           
	])


	if loan_selected:
		(
		    performing_over_time, non_performing_over_time,
		    performing_by_sector, non_performing_by_sector,
			performing_over_time_balance, non_performing_over_time_balance,
			performing_by_sector_balance, non_performing_by_sector_balance
		) = get_loans_over_time_and_by_sector(session_id, loans_data, loan_group, loan_selected)
        
		sector= performing_by_sector+non_performing_by_sector
		performance_over_time= performing_over_time+non_performing_over_time  
        
		if loan_selected in get_loan_type_list(session_id, loans_data, "RETAIL") or loan_selected in get_loan_type_list(session_id, loans_data, "STAFF"):

			(
			    age_perf_male, age_nonperf_male, age_perf_fem, age_nonperf_fem,
			    age_perf_male_balance, age_nonperf_male_balance, age_perf_fem_balance, age_nonperf_fem_balance
			) = get_loan_age(session_id, loans_data, loan_group)
			
			age_output = dbc.CardGroup([
			    dbc.Card(
		            [
		                html.Div([
					        dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=age_perf_male.index,
						                y=(age_nonperf_male_balance+age_perf_male_balance),
						                name='Male',
						                text=get_percentage_label(((age_nonperf_male_balance+age_perf_male_balance)*100/((age_nonperf_male_balance+age_perf_male_balance).sum())).round()),
		    							textposition='auto',
# 		    							customdata= age_perf_male_balance,
# 					                	hovertemplate= format_hover_template(),
						                marker=go.bar.Marker(
						                    color='darkblue'
						                )
						            ),
  
						            go.Bar(
						                x=age_perf_fem.index,
						                y=(age_nonperf_fem_balance+age_perf_fem_balance),
						                name='Female',
						                text=get_percentage_label(((age_nonperf_fem_balance+age_perf_fem_balance)*100/((age_nonperf_fem_balance+age_perf_fem_balance).sum())).round()),
		    							textposition='auto',
# 		    							customdata= age_perf_fem_balance,
# 					                	hovertemplate= format_hover_template(),
						                marker=go.bar.Marker(
						                    color='lightblue'
						                )
						            ),          
		                        ],   
						        layout=go.Layout(
                                    barmode="stack",
		                          	title=go.layout.Title(
										text="Loans volume customer's age",
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
		                                    text="Volume",
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
						    id='age',
						),

		                ]),
		            ],
		            body=True,
		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
		        ),       
		    ])

		if non_performing_over_time is None:

			segmentation_over_time_output = html.Div([                
			])

			segmentation_by_sector_output = html.Div([

			])
		else:
			segmentation_over_time_output = html.Div([
				dbc.CardGroup([
                
                ]),
#                 dbc.CardGroup([
#                     dbc.Card(
#                         [
#                             html.Div([
#                                 dcc.Graph(
#                                 figure=go.Figure(
#                                     data=[
#                                         go.Bar(
#                                             x=TIME.index,
#                                             y=TIME,
#                                             textposition='auto',
#                                             marker=go.bar.Marker(
#                                                 color='darkblue'
#                                             )
#                                         ),  
 
#                                     ],   
#                                     layout=go.Layout(
#                                         title=go.layout.Title(
#                                             text="Time to default",
#                                         # 	xref="paper",
#                                         # 	x=0
#                                         ),
#                                         xaxis=go.layout.XAxis(
#                                             title=go.layout.xaxis.Title(
#                                                 text="Time in years",
#                                                 # font=dict(
#                                                 #     family="Courier New, monospace",
#                                                 #     size=18,
#                                                 #     color="#7f7f7f"
#                                                 # )
#                                             )
#                                         ),
#                                         yaxis=go.layout.YAxis(
#                                             title=go.layout.yaxis.Title(
#                                                 text="Number of Loans",
#                                                 # font=dict(
#                                                 #     family="Courier New, monospace",
#                                                 #     size=18,
#                                                 #     color="#7f7f7f"
#                                                 # )
#                                             )
#                                         ), 
#                                         # barmode="stack",
#                                         showlegend=False,
#                                         legend=go.layout.Legend(
#                                             x=0.9,
#                                             y=1.0,
#                                             xanchor="center",
#                                             yanchor="top",
#                                         ),
#                                         margin=go.layout.Margin(l=40, r=0, t=40, b=30)
#                                     )
#                                 ),
#                                 # style={'height': 400,},
#                                 id='age',
#                                 config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loan performance based on branch level" )}),
#                             ),

#                             ]),
#                         ],
#                         body=True,
#                         style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
#                     ),
#                     dbc.Card([
#                         dcc.Graph(
#                             figure=go.Figure(
#                                 data=[
#                                     go.Bar(
#                                         x= performing_over_time.index, 
#                                         y= (performing_over_time_balance+non_performing_over_time_balance),
# #                                         text=performing_over_time_balance,
#     				                    text = get_percentage_label(((performing_over_time_balance+non_performing_over_time_balance)*100/((performing_over_time_balance+non_performing_over_time_balance).sum() ))[performing_over_time.index].fillna(100).round()),
#                                         textposition='outside',                                          
#                                         marker=go.bar.Marker(
#                                             color='darkblue'
#                                         )
#                                     ),

#                                 ],
#                                 layout=go.Layout(
#                                     barmode="stack",
#     #                                 xaxis_rangeslider_visible= True,
#                                     legend=go.layout.Legend(
#                                         x=1.0,
#                                         y=1.0
#                                     ),
#                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

#                                     title=go.layout.Title(
#                                         text="Loans maturity",
#                                     ),
#                                     xaxis=go.layout.XAxis(
#     #                                     tickangle=55,
#                                         zeroline= True,
#                                         title=go.layout.xaxis.Title(
#                                             text="Tenor months",
#                                             # font=dict(
#                                             #     family="Courier New, monospace",
#                                             #     size=18,
#                                             #     color="#7f7f7f"
#                                             # )
#                                         )
#                                     ),
#                                     yaxis=go.layout.YAxis(
#                                         zeroline= True,
#                                         title=go.layout.yaxis.Title(
#                                             text="Volume",
#                                             # font=dict(
#                                             #     family="Courier New, monospace",
#                                             #     size=18,
#                                             #     color="#7f7f7f"
#                                             # )
#                                         )
#                                     )
#                                 )
#                             ),
#                             id="loan-trend-graph-5",
#                             config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "(Non) Performing loans Over Time" )}),
#                         ),
#                     ]),                    
#                 ]),                
#                 dbc.CardGroup([
#                     dbc.Card(
#                         [
#                             html.Div([
#                                 dcc.Graph(
#                                 figure=go.Figure(
#                                     data=[
#                                         go.Bar(
#                                             x=branch_perf.rename(index=branch_name_mapping).index,
#                                             y=(branch_perf_balance+branch_nonperf_balance),
#                                             name='other branches', 
#                                             text=get_percentage_label(((branch_perf_balance+branch_nonperf_balance)*100/((branch_perf_balance+branch_nonperf_balance).sum()))[branch_perf_balance.index].fillna(100).round()),

#                                             textposition='auto',
#                                             marker=go.bar.Marker(
#                                                 color='darkblue'
#                                             )
#                                         ),

#                                         go.Bar(
#                                             x=branch_perf.rename(index=branch_name_mapping).index,
#                                             y=(branch_perf_balance_main+branch_nonperf_balance_main),
#                                             name='main branch', 
#                                             text=get_percentage_label(((branch_perf_balance_main+branch_nonperf_balance_main)*100/((branch_perf_balance_main+branch_nonperf_balance_main).sum()))[branch_perf_balance.index].fillna(100).round()),
#                                             visible='legendonly',
#     # 						                customdata= branch_perf_balance,
#     # 						                hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),
#                                             textposition='auto',
#                                             marker=go.bar.Marker(
#                                                 color='darkblue'
#                                             )
#                                         ),
                                     
#                                     ],   
#                                     layout=go.Layout(
#                                         barmode="stack",
#                                         title=go.layout.Title(
#                                             text="Loan volume per branch",
#                                         # 	xref="paper",
#                                         # 	x=0
#                                         ),
#                                         xaxis=go.layout.XAxis(
#                                             zeroline= True,
#                                             title=go.layout.xaxis.Title(
#                                                 text="Branch name",
#                                                 # font=dict(
#                                                 #     family="Courier New, monospace",
#                                                 #     size=18,
#                                                 #     color="#7f7f7f"
#                                                 # ) 
#                                             )
#                                         ),
#                                         yaxis=go.layout.YAxis(
#                                             zeroline= True,
#                                             title=go.layout.yaxis.Title(
#                                                 text="Volume",
#                                                 # font=dict(
#                                                 #     family="Courier New, monospace",
#                                                 #     size=18,
#                                                 #     color="#7f7f7f"
#                                                 # )
#                                             )
#                                         ), 
#                                         # barmode="stack",
#                                         showlegend=True,
#                                         legend=go.layout.Legend(
#                                             x=0.9,
#                                             y=1.0,
#                                             xanchor="center",
#                                             yanchor="top",
#                                         ),
#                                         margin=go.layout.Margin(l=40, r=0, t=40, b=30)
#                                     )
#                                 ),
#                                 # style={'height': 400,},
#                                 id='age',
#                                 config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loan performance based on branch level" )}),
#                             ),

#                             ]),
#                         ],
#                         body=True,
#                         style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
#                     ),       
#                 ]),                            
			])

			segmentation_by_sector_output = html.Div([
				dbc.CardGroup([
					dbc.Card([
					    dcc.Graph(
					        figure=go.Figure(
					            data=[
					                go.Bar(
					                    x= performing_by_sector.index, 
					                    y= (performing_by_sector_balance+non_performing_by_sector_balance),
					                    text = get_percentage_label((((performing_by_sector_balance+non_performing_by_sector_balance)*100/((performing_by_sector_balance+non_performing_by_sector_balance).sum())))[performing_by_sector_balance.index].fillna(100).round()),
# 					                    name='Performing',
					                    textposition='auto',
# 					                    customdata= performing_by_sector_balance,
# 							            hovertemplate= format_hover_template(x_label= "Sector", x_unit=""),
					                    marker=go.bar.Marker(
					                        color='darkblue'
					                    )
					                ),

					            ],
					            layout=go.Layout(
                                    barmode="stack",
					                showlegend=False,
					                legend=go.layout.Legend(
					                    x=1.0,
					                    y=1.0
					                ),
# 					                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
					             
								    title=go.layout.Title(
										text="Loans volume per Sector",
									),
									xaxis=go.layout.XAxis(
                                        zeroline= True,
										tickangle=55,
										title=go.layout.xaxis.Title(
											text="Sectors",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
										)
									),
									yaxis=go.layout.YAxis(
                                        zeroline= True,
										title=go.layout.yaxis.Title(
											text="Volume",
											# font=dict(
											#     family="Courier New, monospace",
											#     size=18,
											#     color="#7f7f7f"
											# )
										)
									)
					            )
					        ),
					        id="loan-trend-graph-4",
					        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans Performance based per industry Sectors")}),
					        style = {"height":750}
					    ),
					]),
				]),
			])

		output =  [
			html.Div([
				html.H2("{}".format(loan_selected or loan_group), ),
				html.Hr(),
			]),
			dbc.CardDeck(
				[
                    dbc.Card(
                        [
                            html.H6("New disbursed Loans on: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                            
                            html.H3(" {:,.0f}".format(loan_opening[-1]), style={"color":"green"}), 
#                             html.H6("New Loan Customers from: {}".format(customer_opening.index[-1].strftime("%b %d (%a), %Y"))),                            
#                             html.H3("+ {:,.0f}".format(customer_opening[-1]), style={"color":"green"}),                     
                        ],
                        body=True,
                        style={"align":"center", "justify":"center",}
                    ),    
                    dbc.Card(
		                [
		                    html.H6("Total Number of ongoing Loans"),                            
		                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()), style={"color":"#45b6fe"} ),
		                    html.H6("Total Number of Borrowers"),
		                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),
		                ],
		                body=True,
		            ),
		            dbc.Card(
		                [
		                    html.H6("Total Approved Amount"),                            
		                    html.H3("Rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()), style={"color":"darkblue"}),
		                    html.H6("Total loan Outstanding Amount"),                            
		                    html.H3("Rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()), style={"color":"darkblue"}),
		                ],
		                body=True,
		            ),

				],	
			),

			#################################################################################
			html.Div([
				#######################################################################################################
				dbc.CardGroup(
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
									            title="Borrowers per Strategy Business Unit (SBU)",
									            showlegend=True,
									            legend=go.layout.Legend(
									                x=1.0,
									                y=1.0
									            ),
									            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
											),
									    ),
									    style={'height': 300, "top":30},
									    id="loan-pie-cart-1",
									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Borrowers per Strategy Business Unit (SBU)")}),
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
									            title="Retail borrower's Gender",
									            # showlegend=True,
									            legend=go.layout.Legend(
									                x=1.0,
									                y=1.0
									            ),
									            margin=go.layout.Margin(l=5, r=5, t=50, b=5),
									            							            				                    	
									        )
									    ),
									    style={'height': 300, "top":30},
									    id="loan-pie-cart",
									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Retail borrower's Gender")}),
									)
			                    ]),
			                ],
			                body=True,
			            ),  
					],
				),
                dbc.CardGroup([
                    dbc.Card([
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Scatter(
                                        x= loan_open.index, 
                                        y= loan_open.values,
                                        name='Loans',
                                        mode= "lines",
                                        marker=go.scatter.Marker(
                                            color='darkblue'
                                        )
                                    ),
                                ],
                                layout=go.Layout(
                                    showlegend=True,
                                    xaxis_rangeslider_visible= True,
                                    legend=go.layout.Legend(
                                        x=0,
                                        y=1.0
                                    ),
#                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

                                    title=go.layout.Title(
                                        text=" New Loans disbursed Over Time",
#                                         x=0,
#                                         y=1
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

                                    )

                                )
                            ),

                    ],style={'padding': 10}),
				dbc.Card(
		            [
		                html.Div([
						        dcc.Graph(
							    figure=go.Figure(
							        data=[
							            go.Pie(
							            	labels=loans_interest_rate.index, 
							            	values=loans_interest_rate,
                                            hole=0.5,
							            	marker=go.pie.Marker(
							            		colors=colors_interest, 
							            		# line=dict(color='#000000', width=1),
						            		),						            		
							            ),
							        ],
							        layout=go.Layout(
							            title="Loan Interest Rate Segmentation",
							            showlegend=True,
							            legend=go.layout.Legend(
							                x=1.0,
							                y=1.0
							            ),
							            margin=go.layout.Margin(l=25, r=25, t=50, b=25),
							            							            				                    	
							        )
							    ),
							    # style={'height': 300, "top":30},
							    id="loan-pie-cart-3",
							    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "Number of Loan Accounts per Segments" )}),
							)
		                ]),
		            ],
		            body=True,
		        ),
                    
                ]),                
			]),
			####################################################################################
			# html.Div([]),
		    #############################################################################
	    html.Div([
		    dbc.CardGroup([
                dbc.Card([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x= product_perf.index, #LOANS['MAIN_CLASSIFICATION_DESC'].fillna(LOANS['MAIN_CLASS']
                                    y= (product_nonperf_balance+product_perf_balance),
                                    text = get_percentage_label(((product_nonperf_balance+product_perf_balance)*100/((product_nonperf_balance+product_perf_balance).sum())).round()),
#                                     name='Performing',
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),
                           
                            ],
                            layout=go.Layout(
                                barmode="stack",
                                showlegend=False,
                                legend=go.layout.Legend(
                                    x=1.0,
                                    y=1.0
                                ),
#                                 margin=go.layout.Margin(l=10, r=10, t=30, b=10),

                                title=go.layout.Title(
                                    text="Loans volume per product",
                                ),
                                xaxis=go.layout.XAxis(
                                    zeroline= True,
                                    tickangle=55,
                                    title=go.layout.xaxis.Title(
                                        text="Product",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                ),
                                yaxis=go.layout.YAxis(
                                    zeroline= True,
                                    title=go.layout.yaxis.Title(
                                        text="Volume",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                )
                            )
                        ),
                        id="loan-trend-graph-4",
                        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans performance per product")}),
                        style = {"height":750}
                    ),
				]),
            ]),
		    dbc.CardGroup([	
		    ]),
		]),
			########################################################################
			html.Div([
				html.H2("{}".format(loan_selected or loan_group), ),
				# html.Hr(),
			]),
		    ##########################################################################
		    age_output,
		    ########################################################################
		    account_officer_output,
		    ###########################################################################
		    html.Div([
				html.H2("{}".format(loan_selected or loan_group), ),
				# html.Hr(),
			]),
			##########################################################################
		    segmentation_over_time_output,
			##########################################################################
			segmentation_by_sector_output,
		]
		return output

	################################ Overview at client type level #####################################
	else:
		(
		    performing_over_time, non_performing_over_time,
		    performing_by_sector, non_performing_by_sector,
		    performing_over_time_balance, non_performing_over_time_balance,
			performing_by_sector_balance, non_performing_by_sector_balance
		) = get_loans_over_time_and_by_sector(session_id, loans_data, loan_group, loan_selected)
		sector= performing_by_sector+non_performing_by_sector
		performance_over_time= performing_over_time+non_performing_over_time          

		if loan_group == "RETAIL" or loan_group == "STAFF":

			(
			    age_perf_male, age_nonperf_male, age_perf_fem, age_nonperf_fem,
			    age_perf_male_balance, age_nonperf_male_balance, age_perf_fem_balance, age_nonperf_fem_balance
			) = get_loan_age(session_id, loans_data, loan_group)
			
			age_output = dbc.CardGroup([
			    dbc.Card(
		            [
		                html.Div([
					        dcc.Graph(
						    figure=go.Figure(
						        data=[
						            go.Bar(
						                x=age_perf_male.index,
						                y=(age_nonperf_male_balance+age_perf_male_balance),
						                name='Male ',
						                text=get_percentage_label(((age_nonperf_male_balance+age_perf_male_balance)*100/((age_nonperf_male_balance+age_perf_male_balance).sum())).round()),
		    							textposition='auto',
# 		    							customdata= age_perf_male_balance,
# 					                	hovertemplate= format_hover_template(),
						                marker=go.bar.Marker(
						                    color='darkblue'
						                )
						            ), 
						            go.Bar(
						                x=age_perf_fem.index,
						                y=(age_nonperf_male_balance+age_perf_fem_balance),
						                name='Female',
						                text=get_percentage_label(((age_nonperf_male_balance+age_perf_fem_balance)*100/((age_nonperf_male_balance+age_perf_fem_balance).sum())).round(2)),
		    							textposition='auto',
# 		    							customdata= age_perf_fem_balance,
# 					                	hovertemplate= format_hover_template(),
						                marker=go.bar.Marker(
						                    color='lightblue'
						                )
						            ),           
		                        ],   
						        layout=go.Layout(
                                    barmode="stack",
		                          	title=go.layout.Title(
										text="Loans volume based on customer's age",
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
		                                    text="Volume",
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
						    id='age',
						),

		                ]),
		            ],
		            body=True,
		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
		        ),
		    ])

		elif loan_group == "CORPORATE AND SME" :
			age_output = html.Div([])

		segmentation_over_time_output = html.Div([
# 		    dbc.CardGroup([
# 			    dbc.Card(
# 		            [
# 		                html.Div([
# 					        dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=TIME.index,
# 						                y=TIME,
#                                         text=TIME,

# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),           
# 		                        ],   
# 						        layout=go.Layout(
# 		                          	title=go.layout.Title(
# 										text="Time to default",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
# 		                                title=go.layout.xaxis.Title(
# 			                                text="Time in years",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 		                                )
# 		                            ),
# 		                            yaxis=go.layout.YAxis(
# 		                                title=go.layout.yaxis.Title(
# 		                                    text="Number of Loans",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 		                                )
# 		                            ), 
# 						            # barmode="stack",
# 						            showlegend=False,
# 						            legend=go.layout.Legend(
# 						                x=0.9,
# 						                y=1.0,
# 						                xanchor="center",
# 										yanchor="top",
# 						            ),
# 						            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
# 						        )
# 						    ),
# 						    # style={'height': 400,},
# 						    id='age',
# 						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loan performance based on branch level" )}),
# 						),

# 		                ]),
# 		            ],
# 		            body=True,
# 		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
# 		        ),
# 		        dbc.Card([
# 				    dcc.Graph(
# 				        figure=go.Figure(
# 				            data=[
# 				                go.Bar(
# 				                    x= performing_over_time.index, 
# 				                    y= (performing_over_time_balance+non_performing_over_time_balance),
# #                                     text=performing_over_time_balance,
# 				                    text = get_percentage_label(((performing_over_time_balance+non_performing_over_time_balance)*100/((performing_over_time_balance+non_performing_over_time_balance).sum()))[performing_over_time.index].fillna(100).round(2)),
# # 				                    name='Performing ',
# # 				                    mode = "lines+markers",                                   
#                                     textposition='outside',
# # 				                    customdata= performing_over_time,
# # 						            hovertemplate= format_hover_template(x_label= "Remaining Time" , x_unit="Years"),
# 				                    marker=go.bar.Marker(
# 				                        color='darkblue'
# 				                    )
# 				                ),

# 				            ],
# 				            layout=go.Layout(
#                                 barmode="stack",
# #                                 xaxis_rangeslider_visible= True,
# 				                legend=go.layout.Legend(
# 				                    x=1.0,
# 				                    y=1.0
# 				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# 							    title=go.layout.Title(
# 									text="Loans maturity",
# 								),
# 								xaxis=go.layout.XAxis(
# #                                     tickangle=55,
#                                     zeroline= True,
# 									title=go.layout.xaxis.Title(
# 										text="Tenor months",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								),
# 								yaxis=go.layout.YAxis(
#                                     zeroline= True,
# 									title=go.layout.yaxis.Title(
# 										text="Volume",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								)
# 				            )
# 				        ),
# 				        id="loan-trend-graph-5",
# 				        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "(Non) Performing loans Over Time" )}),
# 				    ),
# 				]),                
# 		    ]),
# 		    dbc.CardGroup([
# 			    dbc.Card(
# 		            [
# 		                html.Div([
# 					        dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=branch_perf.rename(index=branch_name_mapping).index,
# 						                y=(branch_perf_balance+branch_nonperf_balance),
# 						                name='other branches', 
# 						                text=get_percentage_label(((branch_perf_balance+branch_nonperf_balance)*100/((branch_perf_balance+branch_nonperf_balance).sum()))[branch_perf_balance.index].fillna(100).round()),
# # 						                customdata= branch_perf_balance,
# # 						                hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),
# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),

# 						            go.Bar(
# 						                x=branch_perf.rename(index=branch_name_mapping).index,
# 						                y=(branch_perf_balance_main+branch_nonperf_balance_main),
# 						                name='Main branch', 
# 						                text=get_percentage_label(((branch_perf_balance_main+branch_nonperf_balance_main)*100/((branch_perf_balance_main+branch_nonperf_balance_main).sum()))[branch_perf_balance.index].fillna(100).round()),
#                                         visible='legendonly',
# # 						                customdata= branch_perf_balance,
# # 						                hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),
# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),
                                     
# 		                        ],   
# 						        layout=go.Layout(
#                                     barmode="stack",
# 		                          	title=go.layout.Title(
# 										text="Loans volume per branch",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
#                                         zeroline= True,
# 		                                title=go.layout.xaxis.Title(
# 			                                text="Branch name",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# ) 
# 		                                )
# 		                            ),
# 		                            yaxis=go.layout.YAxis(
#                                         zeroline= True,
# 		                                title=go.layout.yaxis.Title(
# 		                                    text="Volume",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 		                                )
# 		                            ), 
# 						            # barmode="stack",
# 						            showlegend=True,
# 						            legend=go.layout.Legend(
# 						                x=0.9,
# 						                y=1.0,
# 						                xanchor="center",
# 										yanchor="top",
# 						            ),
# 						            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
# 						        )
# 						    ),
# 						    # style={'height': 400,},
# 						    id='age',

# 						),

# 		                ]),
# 		            ],
# 		            body=True,
# 		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
# 		        ),       
# 		    ]),                                    
			dbc.CardGroup([                                                
			]),
		])

		segmentation_by_sector_output = html.Div([
			dbc.CardGroup([
				dbc.Card([
				    dcc.Graph(
				        figure=go.Figure(
				            data=[
				                go.Bar(
				                    x= performing_by_sector.index, 
				                    y= (performing_by_sector_balance+non_performing_by_sector_balance),
				                    text = get_percentage_label((((performing_by_sector_balance+non_performing_by_sector_balance)*100/((performing_by_sector_balance+non_performing_by_sector_balance).sum())))[performing_by_sector_balance.index].fillna(100).round(2)),
# 				                    name='Performing',
				                    textposition='outside',
# 				                    customdata= performing_by_sector_balance,
# 						            hovertemplate= format_hover_template(x_label= "Sector" , x_unit=""),
				                    marker=go.bar.Marker(
				                        color='darkblue'
				                    )
				                ),
				            ],
				            layout=go.Layout(
                                barmode="stack",
				                showlegend=False,
				                legend=go.layout.Legend(
				                    x=1.0,
				                    y=1.0
				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
							    title=go.layout.Title(
									text="Loans volume per Sector",
								),
								xaxis=go.layout.XAxis(
									tickangle=55,
                                    zeroline= True,
									title=go.layout.xaxis.Title(
										text="Sectors",
										# font=dict(
										#     family="Courier New, monospace",
										#     size=18,
										#     color="#7f7f7f"
										# )
									)
								),
								yaxis=go.layout.YAxis(
                                    zeroline= True,
									title=go.layout.yaxis.Title(
										text="Volume",
										# font=dict(
										#     family="Courier New, monospace",
										#     size=18,
										#     color="#7f7f7f"
										# )
									)
								)
				            )
				        ),
				        id="loan-trend-graph-4",
				        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Loans Performance based per industry Sector")}),
				        style = {"height":750}
				    ),
				]),
			]),
		])

		output =  [
			html.Div([
				html.H2("{}".format(loan_selected or loan_group), ),
				html.Hr(),
			]),
			dbc.CardDeck(
				[
                    dbc.Card(
                        [
                            html.H6("New disbursed Loans on: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                            
                            html.H3("{:,.0f}".format(loan_opening[-1]), style={"color":"green"}), 
#                             html.H6("New Customers from: {}".format(customer_opening.index[-1].strftime("%b %d (%a), %Y"))),                            
#                             html.H3("+ {:,.0f}".format(customer_opening[-1]), style={"color":"green"}),                     
                        ],
                        body=True,
                        style={"align":"center", "justify":"center",}
                    ),    
                    dbc.Card(
		                [
		                    html.H6("Total Number of ongoing Loans"),                            
		                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()), style={"color":"#45b6fe"} ),
		                    html.H6("Total Number of Borrowers"),
		                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),
		                ],
		                body=True,
		            ),
		            dbc.Card(
		                [
		                    html.H6("Total Approved Amount"),                            
		                    html.H3("Rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()), style={"color":"darkblue"}),
		                    html.H6("Total loan Outstanding Amount"),                            
		                    html.H3("Rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()), style={"color":"darkblue"}),
		                ],
		                body=True,
		            ),

				],	
			),
       
			#################################################################################
			html.Div([
                dbc.CardGroup([
                    dbc.Card([
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Scatter(
                                        x= loan_open.index, 
                                        y= loan_open.values,
                                        name='Loans',
                                        mode= "lines",
                                        fill='tozeroy',
                                        marker=go.scatter.Marker(
                                            color='darkblue'
                                        )
                                    ),
                                ],
                                layout=go.Layout(
                                    showlegend=True,
                                    xaxis_rangeslider_visible= True,
                                    legend=go.layout.Legend(
                                        x=0,
                                        y=1.0
                                    ),
#                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

                                    title=go.layout.Title(
                                        text="New Loans disbursed Over Time",
#                                         x=0,
#                                         y=1
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

                                    )
 
                                )
                            ),

                    ],style={'padding': 3}),
				dbc.Card(
		            [
		                html.Div([
						        dcc.Graph(
							    figure=go.Figure(
							        data=[
							            go.Pie(
							            	labels=loans_interest_rate.index, 
							            	values=loans_interest_rate,
                                            hole=0.5,
							            	marker=go.pie.Marker(
							            		colors=colors_interest, 
							            		# line=dict(color='#000000', width=1),
						            		),						            		
							            ),
							        ],
							        layout=go.Layout(
							            title="Loan Interest Rate Segmentation",
							            showlegend=True,
							            legend=go.layout.Legend(
							                x=1.0,
							                y=1.0
							            ),
							            margin=go.layout.Margin(l=25, r=25, t=50, b=25),
							            							            				                    	
							        )
							    ),
							    # style={'height': 300, "top":30},
							    id="loan-pie-cart-3",
							    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "Number of Loan Accounts per Segments" )}),
							)
		                ]),
		            ],
		            body=True,
		        ),

                    
                ]),
                
			]),
			####################################################################################
			# html.Div([]),
		    #############################################################################
	    html.Div([
		    dbc.CardGroup([
                dbc.Card([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x= product_perf.index, #LOANS['MAIN_CLASSIFICATION_DESC'].fillna(LOANS['MAIN_CLASS']
                                    y= (product_nonperf_balance+product_perf_balance),
                                    text = get_percentage_label(((product_nonperf_balance+product_perf_balance)*100/((product_nonperf_balance+product_perf_balance).sum())).round()),
#                                     name='Performing',
                                    textposition='auto',
#                                     customdata= product_perf_balance,
#                                     hovertemplate= format_hover_template(x_label= "Product" , x_unit=""),
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),
                        
                            ],
                            layout=go.Layout(
                                barmode="stack",
                                showlegend=False,
                                legend=go.layout.Legend(
                                    x=1.0,
                                    y=1.0
                                ),
#                                 margin=go.layout.Margin(l=10, r=10, t=30, b=10),

                                title=go.layout.Title(
                                    text="Loans volume per product",
                                ),
                                xaxis=go.layout.XAxis(
                                    tickangle=55,
                                    zeroline= True,
                                    title=go.layout.xaxis.Title(
                                        text="Product",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                ),
                                yaxis=go.layout.YAxis(
                                    title=go.layout.yaxis.Title(
                                        text="Volume",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                )
                            )
                        ),
                        id="loan-trend-graph-4",
                        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans performance per product")}),
                        style = {"height":750}
                    ),
				]),
            ]),
		    dbc.CardGroup([
	
		    ]),
		]),
			#########################################################################
			html.Div([
				html.H2("{}".format(loan_selected or loan_group), ),
				# html.Hr(),
			]),
		    ##########################################################################
		    age_output,
		    ##########################################################################
		    account_officer_output,
		    ###########################################################################
		    html.Div([
				html.H2("{}".format(loan_selected or loan_group), ),
				# html.Hr(),
			]),
			###########################################################################
		    segmentation_over_time_output,
			##########################################################################
			segmentation_by_sector_output,
		]
		return output

#######################################################################################################
#######################################################################################################
@app.callback(
	[
		Output("set_title","children"),
		Output("loans_info","children"),
		Output("loans_income_trend","children"),
		Output("sbu_gender_segmentation","children"),
		Output("set_title_2","children"),
		Output("segments_interest_rate_segmentation","children"),
		Output("age_segmentation","children"),
		Output("set_title_1","children"),
		Output("loan_over_time","children"),
		Output("loan_by_sector","children"),
	],
	[
		Input("update-loans_info", "n_intervals"),
		Input("select-loans_group", "value"),
		Input("select-loanType", "options"),
		Input("select-loanType", "value"),
	],

)
def update_loans_info_about_select_loan(n, loans_group, options, loan_type):

	loan_type_options = [d['value'] for d in options]

	data = get_loans_dataset(session_id)

	if loans_group == "ALL"  and loan_type is None:
		loans_data = get_loan_dataframe_for_values_selected(session_id, data, loans_group, loan_type)
		return get_loans_overview_info(loans_data, loans_group, loan_type)

	else:
		if loan_type not in loan_type_options:
			loan_type = None

		# output = html.Div([
		# 	html.H3("{} selected in the Group: {}".format(loan_type, loans_group))
		# ])

		loans_data = get_loan_dataframe_for_values_selected(session_id, data, loans_group, loan_type)
		output = get_selected_loan_info(loans_data, loans_group, loan_type)

		return output
