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

####################################################Date picker range########################################################################
# from datetime import datetime as dt
# import dash
# import dash_html_components as html
# import dash_core_components as dcc

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.layout = html.Div([
#     dcc.DatePickerRange(
#         id='my-date-picker-range',
#         min_date_allowed=dt(1995, 8, 5),
#         max_date_allowed=dt(2017, 9, 19),
#         initial_visible_month=dt(2017, 8, 5),
#         end_date=dt(2017, 8, 25)
#     ),
#     html.Div(id='output-container-date-picker-range')
# ])
# ##############Date picker range update################### 
# @app.callback(
#     dash.dependencies.Output('output-container-date-picker-range', 'children'),
#     [dash.dependencies.Input('my-date-picker-range', 'start_date'),
#      dash.dependencies.Input('my-date-picker-range', 'end_date')])
# def update_output(start_date, end_date):
#     string_prefix = 'You have selected: '
#     if start_date is not None:
#         start_date = dt.strptime(start_date.split(' ')[0], '%Y-%m-%d')
#         start_date_string = start_date.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
#     if end_date is not None:
#         end_date = dt.strptime(end_date.split(' ')[0], '%Y-%m-%d')
#         end_date_string = end_date.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'End Date: ' + end_date_string
#     if len(string_prefix) == len('You have selected: '):
#         return 'Select a date to see it displayed here'
#     else:
#         return string_prefix
###############################################################################################################################

####################################################Export excel files###########################################################################
# import dash
# import dash_html_components as html
# from flask import send_file
# import pandas as pd


# app = dash.Dash()
# app.layout = html.Div(
#     children=[html.A("download excel", href="/download_excel/")])


# @app.server.route("/download_excel/")
# def download_excel():
#     # Create DF
#     d = {"col1": [1, 2], "col2": [3, 4]}
#     df = pd.DataFrame(data=d)

#     # Convert DF
#     buf = io.BytesIO()
#     excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
#     df.to_excel(excel_writer, sheet_name="sheet1")
#     excel_writer.save()
#     excel_data = buf.getvalue()
#     buf.seek(0)

#     return send_file(
#         buf,
#         mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
#         attachment_filename="test11311.xlsx",
#         as_attachment=True,
#         cache_timeout=0
#     )
#############################################################################################################################
# import base64
# import io
# import dash
# import pandas as pd

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.A(
#         'Download Excel Data',
#         id='excel-download',
#         download="data.xlsx",
#         href="",
#         target="_blank"
#     )
# ])
 
# @app.callback(Output('excel-download', 'href'),
#              [Input(...)])
# def update_dashboard(...):
#     df = pd.DataFrame(...)
#     xlsx_io = io.BytesIO()
#     writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter')
#     df.to_excel(writer, sheet_name=period)
#     writer.save()
#     xlsx_io.seek(0)
#     # https://en.wikipedia.org/wiki/Data_URI_scheme
#     media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     data = base64.b64encode(xlsx_io.read()).decode("utf-8")
#     href_data_downloadable = f'data:{media_type};base64,{data}'
#     return href_data_downloadable 

#############################################################################################################################
# import dash
# import dash_html_components as html
# from flask import send_file
# import pandas as pd


# app = dash.Dash()
# app.layout = html.Div(
#     children=[html.A("download excel", href="/download_excel/")])


# @app.server.route("/download_excel/")
# def download_excel():
#     # Create DF
#     d = {"col1": [1, 2], "col2": [3, 4]}
#     df = pd.DataFrame(data=d)

#     # Convert DF
#     buf = io.BytesIO()
#     excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
#     df.to_excel(excel_writer, sheet_name="sheet1")
#     excel_writer.save()
#     excel_data = buf.getvalue()
#     buf.seek(0)

#     return send_file(
#         buf,
#         mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
#         attachment_filename="test11311.xlsx",
#         as_attachment=True,
#         cache_timeout=0
#     )
###############################################################################################################################
od_common_layout = html.Div(
	[
		# html.Hr(),
		html.Div(id="set_title", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
		html.Div([
			html.Div(id="loans_info"),
			dcc.Interval(id="update-loans_info", interval=1000*60*60*12, n_intervals=0),
		]),
		html.Hr(),
		html.Div([
			html.Div(id="loans_income_trend"),
			dcc.Interval(id="update-loans_trend", interval=1000*60*60*12, n_intervals=0),
		]),
		html.Hr(),
		html.Div([
			html.Div(id="sbu_gender_segmentation"),
			dcc.Interval(id="update-loans_trend", interval=1000*60*60*12, n_intervals=0),
		]),
    	html.Div(id="set_title_2", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
    	html.Hr(),
		html.Div([
			html.Div(id="segments_interest_rate_segmentation"),
			dcc.Interval(id="update-interest_rate_segmentation", interval=1000*60*60*12, n_intervals=0),
		]),

		html.Hr(),
		html.Div([
			html.Div(id="age_segmentation"),
			dcc.Interval(id="update-age_segmentation", interval=1000*60*60*12, n_intervals=0),
		]),
		html.Div(id="set_title_1", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
		html.Hr(),
		html.Div([
			html.Div(id="loan_over_time"),
			dcc.Interval(id="update-loan_over_time", interval=1000*60*60*12, n_intervals=0),
		]),
		html.Hr(),
		html.Div([
			html.Div(id="loan_by_sector"),
			dcc.Interval(id="update-loan_by_sector", interval=1000*60*60*12, n_intervals=0),
		]),
	],
)

###################################################################################

layout = html.Div([
    html.H1('Overdraft'),
    html.Hr(),
#     html.P('Loan part contains the information specifically to loans including loan types(Vehicle, Construction, Mortgage, Home equity,..) , loan performance at branch level, based on industry sectors(Manufacturing, education, electricity,..), gender and customer’s age range.'),
    html.P('This page contains the information specifically on loans including loan types e.g. Vehicle, Construction, Mortgage, Home equity etc, loan performance at branch level, based on industry sectors, gender and customer’s age range. To view information based on business category, you can select one of the buttons (ALL, Retail, SME, Corporate) and you can select loan types. For graphs showing trend overtime, there are buttons 1MONTH, 3MONTH,1YEAR which allow one to see the trends over time. In addition, for each graph you can choose one field you want see clearly by disabling others on the plot legend.'),   
    html.Hr(),
    html.Div([]),
	html.H5("Select loan Type:"), # It allows to chose a loan product.
	dbc.Row([
		dbc.Col([
			dcc.RadioItems(
				id= "select-loans_group",
				options=[
				    {'label': 'ALL', 'value': 'ALL'},
				    {'label': 'RETAIL', 'value': 'RETAIL'},
				    {'label': 'CORPORATE', 'value': 'CORPORATE'},
				    {'label': 'SME', 'value': 'SME'},
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
	# dbc.Row([
	# 	dbc.Col([
	# 		html.Div([
	# 			html.Div(id="loan_graph"),
	# 			dcc.Interval(id="update-loan_graph", interval=1000*60*60*12, n_intervals=0),
	# 		], style={"margin":"10px 0 0 0"}
	# 		),
	# 	]),
	# ]),
	# dbc.Row([
	# 	dbc.Col([
	# 		html.Div([
	# 			html.Div(id="loan_tables"),
	# 			dcc.Interval(id="update-loan_tables", interval=1000*60*60*12, n_intervals=0),
	# 		], style={"margin":"10px 0 0 0"}
	# 		),
	# 	]),
	# ]),
])


#############################################################################################
###################### Llayout callback #####################################################
#############################################################################################

@app.callback(
	Output("select-loanType","options"),
	[Input("select-loans_group", "value")],
	# [State("select-loans_group", "value")],
)
def select_od_group(value):
	od = get_overdraft_dataset(session_id)

	return select_overdraft_group_options( session_id, loans, value)

######################################################################################################
######################################################################################################
@cache1.memoize(timeout=TIMEOUT)
def get_loans_overview_info(od_data, od_group,od_selected):
	od_cust=od.groupby("SANCTION_DATE").CUSTOMER_ID.nunique()
	od_accs=od.groupby("SANCTION_DATE").OD_ID.nunique()
	appr_amount=od.groupby("SANCTION_DATE").SANCTION_LIMIT.sum()
	outstanding_am=-1*od.groupby("BUSINESS_DATE").BALANCE_LCY.sum()  
# 	(customer_opening, account_opening,customer_open,account_open,active_cust,inactive_cust,closed_cust,dormant_cust) = get_customer_account_trend_data(session_id,is_loan=True)
#     Borrowers,od_cust, od_accs,appr_amount,outstanding_am=get_borrowers(session_id, cust_type) 
# 	customer_sbu = loans_data.groupby("VISION_SBU").CUSTOMER_ID.nunique()
# 	loan_opening=loans_data.groupby("START_DATE").CONTRACT_ID.nunique()
# 	cust_opening=loans_data.groupby("START_DATE").CUSTOMER_ID.nunique()
# 	appr_amount=loans_data.groupby("START_DATE").APPROVED_AMOUNT_LCY.sum()

# 	customer_sbu = loans_data.groupby("VISION_SBU").CUSTOMER_ID.nunique()
# 	retail_cust = loans_data[loans_data.VISION_SBU == "R"]#["VISION_SBU", "CUSTOMER_ID"]
# 	retail_cust = retail_cust[retail_cust["GENDER"]!="O"]
# 	customer_gender = retail_cust.groupby("GENDER").CUSTOMER_ID.nunique()
    
#     #loan performance based on the approved amount    
# # 	amount_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("START_DATE").APPROVED_AMOUNT_LCY.sum()
# # 	amount_non_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("START_DATE").APPROVED_AMOUNT_LCY.sum()
# 	amount_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
# 	amount_non_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
    
# 	branch_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("VISION_OUC").CONTRACT_ID.nunique()
# 	branch_nonperf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("VISION_OUC").CONTRACT_ID.nunique()
# 	branch_nonperf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()
# 	branch_perf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()    
    
    

# # 	retail_cust = loans_data[loans_data.VISION_SBU == "R"]#["VISION_SBU", "CUSTOMER_ID"]
# # 	retail_cust = retail_cust[retail_cust["GENDER"]!="O"]
# # 	customer_gender = retail_cust.groupby("GENDER").CUSTOMER_ID.nunique()

# 	### Segments data
# 	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS']
# 	segment_perf = dF.groupby('SEGMENT').CONTRACT_ID.nunique()
# 	segment_perf_balance = dF.groupby('SEGMENT').OUTSTANDING_PRINCIPAL_LCY.sum()

# 	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS']
# 	segment_nonperf = dF.groupby('SEGMENT').CONTRACT_ID.nunique()
# 	segment_nonperf_balance = dF.groupby('SEGMENT').OUTSTANDING_PRINCIPAL_LCY.sum()

# 	product_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').CONTRACT_ID.nunique()
# 	product_non_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').CONTRACT_ID.nunique() 
# 	product_nonperf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').OUTSTANDING_PRINCIPAL_LCY.sum()
# 	product_perf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').OUTSTANDING_PRINCIPAL_LCY.sum()    
    
    
# 	## Get interest rate segments
# 	bins=[0, 18, np.inf]
# 	labels = ["interest rate < 18%", "interest rate >= 18%"]
# 	loans_interest_rate = loans_data.groupby(pd.cut(loans_data['INTEREST_RATE'], bins, include_lowest=True, right = False, labels=labels)).CONTRACT_ID.nunique()

# 	colors_interest=['grey','darkred']    
# 	colors_gender = ["#242444","gray"]
# 	colors_sbu = ["#46648c","grey","#242444"]

# 	### Performing and non performing loan over time and by sector
# 	(
#         performing_over_time, retail_performing_over_time, sme_performing_over_time, corp_performing_over_time,
#         non_performing_over_time, retail_non_performing_over_time, sme_non_performing_over_time, corp_non_performing_over_time,
#         performing_by_sector, retail_performing_by_sector, sme_performing_by_sector, corp_performing_by_sector,
#         non_performing_by_sector, retail_non_performing_by_sector, sme_non_performing_by_sector, corp_non_performing_by_sector,
# 		performing_over_time_balance, retail_performing_over_time_balance, sme_performing_over_time_balance, corp_performing_over_time_balance,
# 		non_performing_over_time_balance, retail_non_performing_over_time_balance, sme_non_performing_over_time_balance, corp_non_performing_over_time_balance,
# 		performing_by_sector_balance, retail_performing_by_sector_balance, sme_performing_by_sector_balance, corp_performing_by_sector_balance,
# 		non_performing_by_sector_balance, retail_non_performing_by_sector_balance, sme_non_performing_by_sector_balance, corp_non_performing_by_sector_balance
#     ) = get_loans_over_time_and_by_sector(session_id, loans_data, loan_group, loan_selected)

# 	### Get age segment data
# 	(
# 	    age_perf_male, age_nonperf_male, age_perf_fem, age_nonperf_fem,
# 	    age_perf_male_balance, age_nonperf_male_balance, age_perf_fem_balance, age_nonperf_fem_balance
# 	) = get_loan_age(session_id, loans_data)


# 	## Get Total Amount PL and NPL
# 	number_pl_npl = loans_data.groupby("MAIN_CLASSIFICATION_DESC").CONTRACT_ID.nunique()
# 	total_amt_pl_non_pl = loans_data.groupby("MAIN_CLASSIFICATION_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()

	colors_pl_npl = None
	if number_pl_npl.index[0] != "NON PERFORMING ASSETS":
		colors_pl_npl =  ["grey", "darkred"]
	else:
		colors_pl_npl =  [ "darkred", "grey"]

	output =  [
		html.Div([]),
		dbc.CardDeck(
			[
	            dbc.Card(
	                [
	                    html.H6("New disbursed Loans  from: {}".format(od_accs.index[-1].strftime("%b %d (%a), %Y"))),                        
	                    html.H3(" {:,.0f}".format(od_accs[-1]), style={"color":"green"}),
# 	                    html.H6("New Loans from: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                        
# 	                    html.H3(" {:,.0f}".format(loan_opening[-1]), style={"color":"green"}),                        
# 	                    html.H6("New Loan Customers from: {}".format(cust_opening.index[-1].strftime("%b %d (%a), %Y"))),                   
# 	                    html.H3("+ {:,.0f}".format(cust_opening[-1]), style={"color":"green"}),                     
	                ],
	                body=True,
	                style={"align":"center", "justify":"center",}
	            ),
	            dbc.Card(
	                [
	                    html.H6("Total Number of ongoing Loans"),                        
	                    html.H2("{:,.0f}".format(od_accs.sum()),style={"color":"#45b6fe"}),
	                    html.H6("Total Number of Borrowers"),                         
	                    html.H2("{:,.0f}".format(od_cust.sum()), style={"color":"#45b6fe"}),
# 	                    html.H6("Total Number of ongoing  term Loans"),                        
# 	                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()),style={"color":"#45b6fe"}),
# 	                    html.H6("Total Number of ongoing Overdrafts"),                         
# 	                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),                        
	                ],
	                body=True,
	            ),
	            dbc.Card(
	                [
	                    html.H6("Total sanction Amount in Million "),                         
	                    html.H2("rwf {:,.0f}".format(appr_amount.sum()/1e6), style={"color":"darkred"}),
	                    html.H6("Total loan Outstanding Amount in Million"),                    
	                    html.H2("rwf {:,.0f}".format(outstanding_am.sum()/1e6), style={"color":"DarkRed"}),
# 	                    html.H6("Total Approved Amount in Million(term loans) "),                         
# 	                    html.H2("rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()/1e6), style={"color":"darkred"}),
# 	                    html.H6("Total loan Outstanding Amount in Million(term loans)"),                    
# 	                    html.H2("rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()/1e6), style={"color":"DarkRed"}), 
# 	                    html.H6("Total Approved Amount in Million(Overdraft) "),                         
# 	                    html.H2("rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()/1e6), style={"color":"darkred"}),
# 	                    html.H6("Total loan Outstanding Amount in Million(Overdraft)"),                    
# 	                    html.H2("rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()/1e6), style={"color":"DarkRed"}),                           
	                ],
	                body=True,
	            ),
# 	            dbc.Card(
# 	                [
# 	                    html.H6("Total Net Income in Million"),                         
# 	                    html.H2("rwf {:,.0f}".format(loans_data.NET_INCOME_LCY.sum()/1e6), style={"color":"#000080"}),  
# 	                    html.H6("Total Fee Income in Million "),                        
# 	                    html.H2("rwf {:,.0f}".format(loans_data.CHARGES_RECEIVED_LCY.sum()/1e6), style={"color":"#000080"}),
# 	                ],
# 	                body=True,
# 	            ),
			],	            
		),
# 		dbc.CardDeck(
# 			[
# 	            dbc.Card(
# 	                [
# 	                    html.H6("New Loans from: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                        
# 	                    html.H3(" {:,.0f}".format(loan_opening[-1]), style={"color":"green"}),
# # 	                    html.H6("New Loan Customers from: {}".format(cust_opening.index[-1].strftime("%b %d (%a), %Y"))),                   
# # 	                    html.H3("+ {:,.0f}".format(cust_opening[-1]), style={"color":"green"}),                     
# 	                ],
# 	                body=True,
# 	                style={"align":"center", "justify":"center",}
# 	            ),
# 	            dbc.Card(
# 	                [
# 	                    html.H6("Total Number of ongoing Loans"),                        
# 	                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()),style={"color":"#45b6fe"}),
# 	                    html.H6("Total Number of Borrowers"),                         
# 	                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),
# 	                ],
# 	                body=True,
# 	            ),
# 	            dbc.Card(
# 	                [
# 	                    html.H6("Total Approved Amount in Million "),                         
# 	                    html.H2("rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()/1e6), style={"color":"darkred"}),
# 	                    html.H6("Total loan Outstanding Amount in Million"),                    
# 	                    html.H2("rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()/1e6), style={"color":"DarkRed"}),
# 	                ],
# 	                body=True,
# 	            ),
# 	            dbc.Card(
# 	                [
# 	                    html.H6("Total Net Income in Million"),                         
# 	                    html.H2("rwf {:,.0f}".format(loans_data.NET_INCOME_LCY.sum()/1e6), style={"color":"#000080"}),  
# 	                    html.H6("Total Fee Income in Million "),                        
# 	                    html.H2("rwf {:,.0f}".format(loans_data.CHARGES_RECEIVED_LCY.sum()/1e6), style={"color":"#000080"}),
# 	                ],
# 	                body=True,
# 	            ),
# 			],	
#         ),
		###############################################################################################################
# 		html.Div([
# 			dbc.CardGroup(
# 				[
# 		            dbc.Card(
# 		                [
# 		      				html.Div([
# 							    dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Pie(
# 								            	labels=number_pl_npl.index, 
# 								            	values=number_pl_npl,
# 								            	text = number_pl_npl,
# 								            	hoverinfo= "label+percent+text",
#                                                 hole=0.5,
# 								            	marker=go.pie.Marker(
# 								            		colors= colors_pl_npl,
# 								            		# line=dict(color='#000000', width=1),
# 							            		),	
# 							            		# hoverinfo='label+value',
# 								            ),
# 								        ],
# 								        layout=go.Layout(
# 								            title="Rate of Loan Performance",
# 								            showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=1.0,
# 								                y=1.0
# 								            ),
# 								            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
# 										),
# 								    ),
# 								    style={'height': 300, "top":30},
# 								    id="loan-pie-cart-1.1.1",
# 								    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Rate of Loan Performance")}),
# 								)
# 		                    ]),
# 		                ],
# 		                body=True,
# 		                style={"padding":"5px 5px 5px 5px", },
# 		            ),
# 		            dbc.Card(
# 		                [
# 		                    html.Div([
# 							        dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Pie(
# 								            	labels=total_amt_pl_non_pl.index, 
# 								            	values=total_amt_pl_non_pl,
# 								            	text = total_amt_pl_non_pl,
# 								            	hoverinfo= "label+percent+text",
#                                                 hole=0.5,
# 								            	marker=go.pie.Marker(
# 								            		colors=  colors_pl_npl,
# 								            		# line=dict(color='#000000', width=1),
# 							            		),						            		
# 								            ),
# 								        ],
# 								        layout=go.Layout(
# 								            title="Rate of Loan Performance Based on Outstanding Amount",
# 								            # showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=1.0,
# 								                y=1.0
# 								            ),
# 								            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
								            							            				                    	
# 								        )
# 								    ),
# 								    style={'height': 300, "top":30},
# 								    id="loan-pie-cart0.1",
# 								    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Rate of Loan Performance Based on Outstanding Amount")}),
# 								)
# 		                    ]),
# 		                ],
# 		                body=True,
# 		            ),  
# 				],
# 			),
# 			dbc.CardGroup(
# 				[
# 		            dbc.Card(
# 		                [
# 		      				html.Div([
# 							    dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Pie(
# 								            	labels=customer_sbu.rename(index=SBU_MAPPING).index, 
# 								            	values=customer_sbu,
#                                                 hole=0.5,
# 								            	marker=go.pie.Marker(
# 								            		colors=colors_sbu, 
# 								            		# line=dict(color='#000000', width=1),
# 							            		),	
# 							            		# hoverinfo='label+value',
# 								            ),
# 								        ],
# 								        layout=go.Layout(
# 								            title="Borrowers per Strategy Business Unit (SBU)",
# 								            showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=1.0,
# 								                y=1.0
# 								            ),
# 								            margin=go.layout.Margin(l=5, r=5, t=50, b=5),
# 										),
# 								    ),
# 								    style={'height': 300, "top":30},
# 								    id="loan-pie-cart-1",
# 								    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "Borrowers per Strategy Business Unit (SBU)" )}),
# 								)
# 		                    ]),
# 		                ],
# 		                body=True,
# 		                style={"padding":"5px 5px 5px 5px", },
# 		            ),
# 		            dbc.Card(
# 		                [
# 		                    html.Div([
# 							        dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Pie(
# 								            	labels=customer_gender.rename(index=GENDER_MAPPING).index, 
# 								            	values=customer_gender,
#                                                 hole=0.5,
# 								            	marker=go.pie.Marker(
# 								            		colors=colors_gender, 
# 								            		# line=dict(color='#000000', width=1),
# 							            		),						            		
# 								            ),
# 								        ],
# 								        layout=go.Layout(
# 								            title="Retail borrower's Gender",
# 								            # showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=1.0,
# 								                y=1.0
# 								            ),
# 								            margin=go.layout.Margin(l=5, r=5, t=50, b=5),
								            							            				                    	
# 								        )
# 								    ),
# 								    style={'height': 300, "top":30},
# 								    id="loan-pie-cart",
# 								    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "borrower's" )}),
# 								)
# 		                    ]),
# 		                ],
# 		                body=True,
# 		            ),  
# 				],
# 			),
# 		]),
# 		####################################################################################
# 		dbc.CardGroup([
# 	        dbc.Card([
# 			    dcc.Graph(
# 			        figure=go.Figure(
# 			            data=[
# # 			                go.Scatter(
# # 			                    x= customer_opening.index, 
# # 			                    y= customer_opening.values,
# # 			                    name='Customers',
# # 			                    mode= "lines",
# # 			                    marker=go.scatter.Marker(
# # 			                        color='#000080'
# # 			                    )
# # 			                ),
# 			                go.Scatter(
# 			                    x= loan_opening.index, 
# 			                    y= loan_opening.values,
# 			                    name='Loans',
# 			                    mode= "lines",
# #                                 connectgaps='True',
# 			                    marker=go.scatter.Marker(
# 			                        color='#494c53'
# 			                    )
# 			                ),
# 			            ],
# 			            layout=go.Layout(
# 			                showlegend=True,
# 			                xaxis_rangeslider_visible= True,
# 			                legend=go.layout.Legend(
# 			                    x=0,
# 			                    y=1.0
# 			                ),
# 			                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
			             
# 						    title=go.layout.Title(
# 								text="Loan disbursed Over Time",
# #                                 x=0,
# #                                 y=1
# 							),
#                             xaxis=go.layout.XAxis(
#                                 rangeselector=dict(
#                                     buttons=list([
#                                         dict(count=1,
#                                              label="1MONTH",
#                                              step="month",
#                                              stepmode="backward"),
#                                         dict(count=3,
#                                              label="3MONTHS",
#                                              step="month",
#                                              stepmode="backward"),                                                    
#                                         dict(count=6,
#                                              label="6MONTHS",
#                                              step="month",
#                                              stepmode="backward"),
#                                         dict(count=1,
#                                              label="1YEAR",
#                                              step="year",
#                                              stepmode="backward"),
#                                         dict(step="all")
#                                     ])
#                                 ),
#                                 rangeslider=dict(
#                                     visible=True
#                                 ),
#                                 type="date"
#                                 ),                                                                         
# #                                             ),                                                        
# #                                             title=go.layout.xaxis.Title(
# #                                                 text="Years",
# #                                                 # font=dict(
# #                                                 #     family="Courier New, monospace",
# #                                                 #     size=18,
# #                                                 #     color="#7f7f7f"
# #                                                 # )
# #                                             )
#                             )
# #                                         yaxis=go.layout.YAxis(
# #                                             title=go.layout.yaxis.Title(
# #                                                 text="Number of Customers",
# #                                                 # font=dict(
# #                                                 #     family="Courier New, monospace",
# #                                                 #     size=18,
# #                                                 #     color="#7f7f7f"
# # #                                                 # )
# # #                                             )
# #                                         )
#                         )
#                     ),
# #                     body=True,
# #                     style={"padding":"5px 5px 5px 5px", },
# # 			        id="loan-trend-graph-1",
# # 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
# # 			    ),
# 			],style={'padding': 10}),
# 	        dbc.Card([
# 			    dcc.Graph(
# 			        figure=go.Figure(
# 			            data=[
# # 			                go.Scatter(
# # 			                    x= customer_opening.index, 
# # 			                    y= customer_opening.values,
# # 			                    name='Customers',
# # 			                    mode= "lines",
# # 			                    marker=go.scatter.Marker(
# # 			                        color='#000080'
# # 			                    )
# # 			                ),
# 			                go.Scatter(
# 			                    x= loan_opening.index, 
# 			                    y= np.cumsum(loan_opening.values),
# 			                    name='Loans',
# 			                    mode= "lines",
#                                 fill="tozeroy",
# 			                    marker=go.scatter.Marker(
# 			                        color='#494c53'
# 			                    )
# 			                ),
# 			            ],
# 			            layout=go.Layout(
# 			                showlegend=True,
# 			                xaxis_rangeslider_visible= True,
# 			                legend=go.layout.Legend(
# 			                    x=0,
# 			                    y=1.0
# 			                ),
# 			                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
			             
# 						    title=go.layout.Title(
# 								text="Loan disbursed Over Time",
# #                                 x=0,
# #                                 y=1
# 							),
# #                             xaxis=go.layout.XAxis(
# #                                 rangeselector=dict(
# #                                     buttons=list([
# #                                         dict(count=1,
# #                                              label="1MONTH",
# #                                              step="month",
# #                                              stepmode="backward"),
# #                                         dict(count=3,
# #                                              label="3MONTHS",
# #                                              step="month",
# #                                              stepmode="backward"),                                                    
# #                                         dict(count=6,
# #                                              label="6MONTHS",
# #                                              step="month",
# #                                              stepmode="backward"),
# #                                         dict(count=1,
# #                                              label="1YEAR",
# #                                              step="year",
# #                                              stepmode="backward"),
# #                                         dict(step="all")
# #                                     ])
# #                                 ),
# #                                 rangeslider=dict(
# #                                     visible=True
# #                                 ),
# #                                 type="date"
# #                                 ),                                                                         
# #                                             ),                                                        
# #                                             title=go.layout.xaxis.Title(
# #                                                 text="Years",
# #                                                 # font=dict(
# #                                                 #     family="Courier New, monospace",
# #                                                 #     size=18,
# #                                                 #     color="#7f7f7f"
# #                                                 # )
# #                                             )
#                             )
# #                                         yaxis=go.layout.YAxis(
# #                                             title=go.layout.yaxis.Title(
# #                                                 text="Number of Customers",
# #                                                 # font=dict(
# #                                                 #     family="Courier New, monospace",
# #                                                 #     size=18,
# #                                                 #     color="#7f7f7f"
# # #                                                 # )
# # #                                             )
# #                                         )
#                         )
#                     ),
# #                     body=True,
# #                     style={"padding":"5px 5px 5px 5px", },
# # 			        id="loan-trend-graph-1",
# # 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
# # 			    ),
# 			],style={'padding': 10}),
            
# #             dbc.Card([
# #                 dcc.Graph(
# #                     figure=go.Figure(
# #                         data=[
# #                             go.Scatter(
# #                                 x= appr_amount.index, 
# #                                 y= amount_perf.values,
# #                                 name='Performing',
# #                                 mode= "lines",
# #                                 marker=go.scatter.Marker(
# #                                     color='grey'
# #                                 )
# #                             ),
# #                             go.Scatter(
# #                                 x= amount_non_perf.index, 
# #                                 y= amount_non_perf.values,
# #                                 name='Non Performing',
# #                                 mode= "lines",
# #                                 marker=go.scatter.Marker(
# #                                     color='darkred'
# #                                 )
# #                             ),
# #                         ],
# #                         layout=go.Layout(
# #                             showlegend=True,
# #                             xaxis_rangeslider_visible= True,
# #                             legend=go.layout.Legend(
# #                                 x=0,
# #                                 y=1.0
# #                             ),
# #                             margin=go.layout.Margin(l=10, r=10, t=30, b=10),

# #                             title=go.layout.Title(
# #                                 text="Loan performance based on approved amount",
# #                                 x=0.6,
# #                                 y=1
# #                             ),
# #                             xaxis=go.layout.XAxis(
# #                                 rangeselector=dict(
# #                                     buttons=list([
# #                                         dict(count=1,
# #                                              label="1month",
# #                                              step="month",
# #                                              stepmode="backward"),
# #                                         dict(count=3,
# #                                              label="3months",
# #                                              step="month",
# #                                              stepmode="backward"),                                                    
# #                                         dict(count=6,
# #                                              label="6months",
# #                                              step="month",
# #                                              stepmode="backward"),
# #                                         dict(count=1,
# #                                              label="1year",
# #                                              step="year",
# #                                              stepmode="backward"),
# #                                         dict(step="all")
# #                                     ])
# #                                 ),
# #                                 rangeslider=dict(
# #                                     visible=True
# #                                 ),
# #                                 type="date"
# #                                 ),                                                                         
# # #                                             ),                                                        
# # #                                             title=go.layout.xaxis.Title(
# # #                                                 text="Years",
# # #                                                 # font=dict(
# # #                                                 #     family="Courier New, monospace",
# # #                                                 #     size=18,
# # #                                                 #     color="#7f7f7f"
# # #                                                 # )
# # #                                             )
# #                             )
# # #                                         yaxis=go.layout.YAxis(
# # #                                             title=go.layout.yaxis.Title(
# # #                                                 text="Number of Customers",
# # #                                                 # font=dict(
# # #                                                 #     family="Courier New, monospace",
# # #                                                 #     size=18,
# # #                                                 #     color="#7f7f7f"
# # # #                                                 # )
# # # #                                             )
# # #                                         )
# #                         )
# #                     ),
# # #                     body=True,
# # #                     style={"padding":"5px 5px 5px 5px", },
# # # 			        id="loan-trend-graph-1",
# # # 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
# # # 			    ),
# # 			]),            
# #             body=True,
# #             style={"padding":"5px 5px 5px 5px", },            
# 	    ]),
# 	    #############################################################################
# #             dbc.CardGroup([
# #                 dbc.Card([
# #                     dcc.Graph(
# #                         figure=go.Figure(
# #                             data=[
# #                                 go.Scatter(
# #                                     x= amount_perf.index, 
# #                                     y= amount_perf.values,
# #                                     name='Performing',
# #                                     mode= "lines",
# #                                     marker=go.scatter.Marker(
# #                                         color='grey'
# #                                     )
# #                                 ),
# #                                 go.Scatter(
# #                                     x= amount_non_perf.index, 
# #                                     y= amount_non_perf.values,
# #                                     name='Non Performing',
# #                                     mode= "lines",
# #                                     marker=go.scatter.Marker(
# #                                         color='darkred'
# #                                     )
# #                                 ),
# #                             ],
# #                             layout=go.Layout(
# #                                 showlegend=True,
# #                                 xaxis_rangeslider_visible= True,
# #                                 legend=go.layout.Legend(
# #                                     x=0,
# #                                     y=1.0
# #                                 ),
# #                                 margin=go.layout.Margin(l=10, r=10, t=30, b=10),

# #                                 title=go.layout.Title(
# #                                     text="Loan performance based on approved amount",
# #                                     x=0.6,
# #                                     y=1
# #                                 ),
# #                                 xaxis=go.layout.XAxis(
# #                                     rangeselector=dict(
# #                                         buttons=list([
# #                                             dict(count=1,
# #                                                  label="1month",
# #                                                  step="month",
# #                                                  stepmode="backward"),
# #                                             dict(count=3,
# #                                                  label="3months",
# #                                                  step="month",
# #                                                  stepmode="backward"),                                                    
# #                                             dict(count=6,
# #                                                  label="6months",
# #                                                  step="month",
# #                                                  stepmode="backward"),
# #                                             dict(count=1,
# #                                                  label="1year",
# #                                                  step="year",
# #                                                  stepmode="backward"),
# #                                             dict(step="all")
# #                                         ])
# #                                     ),
# #                                     rangeslider=dict(
# #                                         visible=True
# #                                     ),
# #                                     type="date"
# #                                     ),                                                                         
# #     #                                             ),                                                        
# #     #                                             title=go.layout.xaxis.Title(
# #     #                                                 text="Years",
# #     #                                                 # font=dict(
# #     #                                                 #     family="Courier New, monospace",
# #     #                                                 #     size=18,
# #     #                                                 #     color="#7f7f7f"
# #     #                                                 # )
# #     #                                             )
# #                                 )
# #     #                                         yaxis=go.layout.YAxis(
# #     #                                             title=go.layout.yaxis.Title(
# #     #                                                 text="Number of Customers",
# #     #                                                 # font=dict(
# #     #                                                 #     family="Courier New, monospace",
# #     #                                                 #     size=18,
# #     #                                                 #     color="#7f7f7f"
# #     # #                                                 # )
# #     # #                                             )
# #     #                                         )
# #                             )
# #                         ),
# #     #                     body=True,
# #     #                     style={"padding":"5px 5px 5px 5px", },
# #     # 			        id="loan-trend-graph-1",
# #     # 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
# #     # 			    ),
# #                 ]),	
        
# 	    html.Div([
# 		    dbc.CardGroup([
# 				dbc.Card([
# 				    dcc.Graph(
# 				        figure=go.Figure(
# 				            data=[
# 				                go.Bar(
# 				                    x= segment_perf.rename(index=SEGMENTS_MAPPING).index, 
# 				                    y= segment_perf,
# 				                    text = get_percentage_label((segment_perf/(segment_perf + segment_nonperf)*100)[segment_perf.index].fillna(100).round(2)),
# 				                    name='Performing',
# 				                    textposition='auto',
# # 				                    customdata= segment_perf_balance,
# # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# 				                    marker=go.bar.Marker(
# 				                        color='grey'
# 				                    )
# 				                ),
# 				                go.Bar(
# 				                    x= segment_nonperf.rename(index=SEGMENTS_MAPPING).index, 
# 				                    y= segment_nonperf,
# 				                    text = get_percentage_label((segment_nonperf/(segment_perf + segment_nonperf)*100)[segment_nonperf.index].dropna().round(2)),
# 				                    name='Non Performing',
# 				                    textposition='auto',
# # 				                    customdata= segment_nonperf_balance,
# # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# 				                    marker=go.bar.Marker(
# 				                        color='darkred'
# 				                    )
# 				                ),
# 				            ],
# 				            layout=go.Layout(
# 				                legend=go.layout.Legend(
# 				                    x=0.7,
# 				                    y=1.0
# 				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# 							    title=go.layout.Title(
# 									text="Loans performance based on customer's category",
# 								),
# 								xaxis=go.layout.XAxis(
# 									title=go.layout.xaxis.Title(
# 										text="Category",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								),
# 								yaxis=go.layout.YAxis(
# 									title=go.layout.yaxis.Title(
# 										text="Number of Loans",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								)
# 				            )
# 				        ),
# 				        id="loan-trend-graph-3.1",
# 				        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loans performance based on customer's category" )}),
# 				    ),
# 				]),
# 				dbc.Card(
# 		            [
# 		                html.Div([
# 						        dcc.Graph(
# 							    figure=go.Figure(
# 							        data=[
# 							            go.Pie(
# 							            	labels=loans_interest_rate.index, 
# 							            	values=loans_interest_rate,
#                                             hole=0.5,
# 							            	marker=go.pie.Marker(
# 							            		colors=colors_interest, 
# 							            		# line=dict(color='#000000', width=1),
# 						            		),						            		
# 							            ),
# 							        ],
# 							        layout=go.Layout(
# 							            title="Loan Interest Rate Segmentation",
# 							            showlegend=True,
# 							            legend=go.layout.Legend(
# 							                x=1.0,
# 							                y=1.0
# 							            ),
# 							            margin=go.layout.Margin(l=25, r=25, t=50, b=25),
							            							            				                    	
# 							        )
# 							    ),
# 							    # style={'height': 300, "top":30},
# 							    id="loan-pie-cart-3",
# 							    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}".format( "Number of Loan Accounts per Segments" )}),
# 							)
# 		                ]),
# 		            ],
# 		            body=True,
# 		        ),	
# 		    ]),
# 		]),
# 		#########################################################################
# 		html.Div([]),
# 	    ##########################################################################
# 	    html.Div([
# 		    dbc.CardGroup([
# 			    dbc.Card(
# 		            [
# 		                html.Div([
# 					        dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=age_perf_male.index,
# 						                y=age_perf_male.values,
# 						                name='Male Performing',
#                                         visible='legendonly',
# 						                text=get_percentage_label((age_perf_male.values*100/(age_nonperf_male.values+age_perf_male.values)).round(2)),
# 						                customdata= age_perf_male_balance,
# 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=age_nonperf_male.index,
# 						                y=age_nonperf_male.values,
# 						                name='Male Non Performing',
# 						                text=get_percentage_label((age_nonperf_male.values*100/(age_nonperf_male.values+age_perf_male.values)).round(2)),
# 		    							customdata= age_nonperf_male_balance,
# 		    							hovertemplate= format_hover_template(),
# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='lightblue'
# 						                )
# 						            ),  
# 						            go.Bar(
# 						                x=age_perf_fem.index,
# 						                y=age_perf_fem.values,
# 						                name='Female Performing',
#                                         visible='legendonly',
# 						                text=get_percentage_label((age_perf_fem.values*100/(age_nonperf_fem.values+age_perf_fem.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_perf_fem_balance,
# 						                hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='darkred'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=age_nonperf_fem.index,
# 						                y=age_nonperf_fem.values,
# 						                name='Female Non Performing',
# 						                text=get_percentage_label((age_nonperf_fem.values*100/(age_nonperf_fem.values+age_perf_fem.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_nonperf_fem_balance,
# 						                hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='red'
# 						                )
# 						            ),           
# 		                        ],   
# 						        layout=go.Layout(
# 		                          	title=go.layout.Title(
# 										text="Loan performance based on customer's age",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
# 		                                title=go.layout.xaxis.Title(
# 			                                text="Age Group",
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
# 						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loan performance based on customer's age" )}),
# 						),

# 		                ]),
# 		            ],
# 		            body=True,
# 		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
# 		        ),       
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
# 						                y=branch_perf,
# 						                name='Performing',
# 						                text=get_percentage_label((branch_perf*100/(branch_nonperf+branch_perf)).round()),
# 						                customdata= branch_perf_balance,
# 						                hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),
# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='grey'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=branch_nonperf.rename(index=branch_name_mapping).index,
# 						                y=branch_nonperf,
# 						                name='Non Performing',
#                                         text=get_percentage_label((branch_nonperf*100/(branch_nonperf+branch_perf)).round()),
# # 						                text=branch_nonperf,
# 						                customdata= branch_nonperf_balance,
# 						                hovertemplate= format_hover_template(x_label= "Branch", y_label= "# of Accounts"),
# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='darkred'
# 						                )
# 						            ),  
# 		                        ],   
# 						        layout=go.Layout(
# 		                          	title=go.layout.Title(
# 										text="Loan performance based on branch level",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
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
# 		]),
# 		##########################################################################
# 		html.Div([]),
# 	    ###########################################################################
# 	    html.Div([
# 			dbc.CardGroup([
# 		        dbc.Card([
# 				    dcc.Graph(
# 				        figure=go.Figure(
# 				            data=[
# 				                go.Scatter(
# 				                    x= format_time_index(performing_over_time.index), 
# 				                    y= performing_over_time,
# 				                    text = get_percentage_label((performing_over_time/(performing_over_time + non_performing_over_time)*100).round(2)),
# 				                    name='Performing ',
# 				                    mode = "lines+markers",
# 				                    customdata= performing_over_time_balance,
# 						            hovertemplate= format_hover_template(x_label= "Remaining Time" , x_unit="Months"),
# 				                    marker=go.scatter.Marker(
# 				                        color='grey'
# 				                    )
# 				                ),
# 				                go.Scatter(
# 				                    x= format_time_index(non_performing_over_time.index), 
# 				                    y= non_performing_over_time,
# 				                    text = get_percentage_label((non_performing_over_time/(performing_over_time + non_performing_over_time)*100).round(2)),
# 				                    name='Non Performing ',
# 				                    mode = "lines+markers",
# 				                    customdata= non_performing_over_time_balance,
# 						            hovertemplate= format_hover_template(x_label= "Remaining Time" , x_unit="Months"),
# 				                    marker=go.scatter.Marker(
# 				                        color='darkred'
# 				                    )
# 				                ),
# 				            ],
# 				            layout=go.Layout(
# 				                legend=go.layout.Legend(
# 				                    x=1.0,
# 				                    y=1.0
# 				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# 							    title=go.layout.Title(
# 									text="Loans Performance based on tenor months",
# 								),
# 								xaxis=go.layout.XAxis(
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
# 									title=go.layout.yaxis.Title(
# 										text="Number of Loans",
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
# # 				dbc.Card([
# # 				    dcc.Graph(
# # 				        figure=go.Figure(
# # 				            data=[
# # 				                go.Bar(
# # 				                    x= amount_perf.index, 
# # 				                    y= amount_perf,
# # 				                    text = get_percentage_label((amount_perf/(amount_non_perf + amount_perf)*100)[segment_perf.index].fillna(100).round(2)),
# # 				                    name='Performing',
# # 				                    textposition='auto',
# # # 				                    customdata= segment_perf_balance,
# # # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# # 				                    marker=go.bar.Marker(
# # 				                        color='grey'
# # 				                    )
# # 				                ),
# # 				                go.Bar(
# # 				                    x= amount_non_perf.index, 
# # 				                    y= amount_non_perf,
# # 				                    text = get_percentage_label((amount_non_perf/(amount_non_perf + amount_perf)*100)[segment_nonperf.index].dropna().round(2)),
# # 				                    name='Non Performing',
# # 				                    textposition='auto',
# # # 				                    customdata= segment_nonperf_balance,
# # # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# # 				                    marker=go.bar.Marker(
# # 				                        color='darkred'
# # 				                    )
# # 				                ),
# # 				            ],
# # 				            layout=go.Layout(
# # 				                legend=go.layout.Legend(
# # 				                    x=0.7,
# # 				                    y=1.0
# # 				                ),
# # 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# # 							    title=go.layout.Title(
# # 									text="Loans performance based on approved amount",
# # 								),
# # 								xaxis=go.layout.XAxis(
# # 									title=go.layout.xaxis.Title(
# # 										text=" loan Performing Class ",
# # 										# font=dict(
# # 										#     family="Courier New, monospace",
# # 										#     size=18,
# # 										#     color="#7f7f7f"
# # 										# )
# # 									)
# # 								),
# # 								yaxis=go.layout.YAxis(
# # 									title=go.layout.yaxis.Title(
# # 										text="Approved amount",
# # 										# font=dict(
# # 										#     family="Courier New, monospace",
# # 										#     size=18,
# # 										#     color="#7f7f7f"
# # 										# )
# # 									)
# # 								)
# # 				            )
# # 				        ),
# # 				        id="loan-trend-graph-3.1",
# # 				        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loans performance based on approved amount" )}),
# # 				    ),
# # 				]),                
# 			]),
# 		]),
# 		##########################################################################
# 		html.Div([
# 			dbc.CardGroup([
# 				dbc.Card([
# 				    dcc.Graph(
# 				        figure=go.Figure(
# 				            data=[
# 				                go.Bar(
# 				                    x= performing_by_sector.index, 
# 				                    y= performing_by_sector,
# 				                    text = get_percentage_label(((performing_by_sector/(performing_by_sector + non_performing_by_sector))[performing_by_sector.index].fillna(1)*100).round(2)),
# 				                    name='Performing',
# 				                    textposition='auto',
# 				                    customdata= performing_by_sector_balance,
# 						            hovertemplate= format_hover_template(x_label= "Sector" , x_unit=""),
# 				                    marker=go.bar.Marker(
# 				                        color='grey'
# 				                    )
# 				                ),
# 				                go.Bar(
# 				                    x= non_performing_by_sector.index, 
# 				                    y= non_performing_by_sector,
# 				                    text = get_percentage_label(((non_performing_by_sector/(performing_by_sector + non_performing_by_sector))[non_performing_by_sector.index].fillna(1)*100).round(2)),
# 				                    name='Non Performing',
# 				                    textposition='auto',
# 				                    customdata= non_performing_by_sector_balance,
# 						            hovertemplate= format_hover_template(x_label= "Sector" , x_unit=""),
# 				                    marker=go.bar.Marker(
# 				                        color='darkred'
# 				                    )
# 				                ),
# 				            ],
# 				            layout=go.Layout(
# 				                # showlegend=True,
# 				                legend=go.layout.Legend(
# 				                    x=1.0,
# 				                    y=1.0
# 				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# 							    title=go.layout.Title(
# 									text="(Non) Performing Loans per industry Sectors",
# 								),
# 								xaxis=go.layout.XAxis(
# 									tickangle=55,
# 									title=go.layout.xaxis.Title(
# 										text="Sectors",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								),
# 								yaxis=go.layout.YAxis(
# 									title=go.layout.yaxis.Title(
# 										text="Number of Loans",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								)
# 				            )
# 				        ),
# 				        id="loan-trend-graph-4",
# 				        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "(Non) Performing Loans per industry Sectors" )}),
# 				        style = {"height":750}
# 				    ),
# 				]),
# 			]),
# 		]),
	]
	return output

# @cache1.memoize(timeout=TIMEOUT)
# def get_selected_loan_info(loans_data, loan_group,loan_selected):
# # 	(customer_opening, account_opening,customer_open,account_open,active_cust,inactive_cust,closed_cust,dormant_cust) = get_customer_account_trend_data(session_id,is_loan=True)
# 	loan_opening=loans_data.groupby("START_DATE").CONTRACT_ID.nunique()
# 	cust_opening=loans_data.groupby("START_DATE").CUSTOMER_ID.nunique()
# 	appr_amount=loans_data.groupby("START_DATE").APPROVED_AMOUNT_LCY.sum()

# 	customer_sbu = loans_data.groupby("VISION_SBU").CUSTOMER_ID.nunique()

# 	retail_cust = loans_data[loans_data.VISION_SBU == "R"]#["VISION_SBU", "CUSTOMER_ID"]
# 	retail_cust = retail_cust[retail_cust["GENDER"]!="O"]
# 	customer_gender = retail_cust.groupby("GENDER").CUSTOMER_ID.nunique()
    
#     #loan performance based on the approved amount    
# # 	amount_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("START_DATE").APPROVED_AMOUNT_LCY.sum()
# # 	amount_non_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("START_DATE").APPROVED_AMOUNT_LCY.sum()
# 	amount_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
# 	amount_non_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("MAIN_CLASSIFICATION_DESC").APPROVED_AMOUNT_LCY.sum()
    
    
# 	branch_perf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby("VISION_OUC").CONTRACT_ID.nunique()
# 	branch_nonperf=loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby("VISION_OUC").CONTRACT_ID.nunique()
# 	branch_nonperf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()
# 	branch_perf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('VISION_OUC').OUTSTANDING_PRINCIPAL_LCY.sum()     
    
# 	product_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').CONTRACT_ID.nunique()
# 	product_non_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').CONTRACT_ID.nunique()
# 	product_nonperf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').OUTSTANDING_PRINCIPAL_LCY.sum()
# 	product_perf_balance = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').OUTSTANDING_PRINCIPAL_LCY.sum()    

# 	### Segments data
# 	segments = loans_data.groupby("SEGMENT").CONTRACT_ID.nunique()
# 	segments_balance = loans_data.groupby("SEGMENT").OUTSTANDING_PRINCIPAL_LCY.sum()

# 	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS']
# 	segment_perf = dF.groupby('SEGMENT').CONTRACT_ID.nunique()
# 	segment_perf_balance = dF.groupby('SEGMENT').OUTSTANDING_PRINCIPAL_LCY.sum()

# 	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS']
# 	segment_nonperf = dF.groupby('SEGMENT').CONTRACT_ID.nunique()
# 	segment_nonperf_balance = dF.groupby('SEGMENT').OUTSTANDING_PRINCIPAL_LCY.sum()

# 	### Account Officer data
# 	# ao_data = loans_data.groupby("SEGMENT").CONTRACT_ID.nunique()
# 	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS']
# 	ao_perf = dF.groupby('AO_NAME').CONTRACT_ID.nunique()
# 	ao_perf_balance = dF.groupby('AO_NAME').OUTSTANDING_PRINCIPAL_LCY.sum()

# 	dF = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS']
# 	ao_nonperf = dF.groupby('AO_NAME').CONTRACT_ID.nunique()
# 	ao_nonperf_balance = dF.groupby('AO_NAME').OUTSTANDING_PRINCIPAL_LCY.sum()
    
# 	product_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='PERFORMING ASSETS'].groupby('SCHEME_DESC').CONTRACT_ID.nunique()
# 	product_non_perf = loans_data[loans_data.MAIN_CLASSIFICATION_DESC=='NON PERFORMING ASSETS'].groupby('SCHEME_DESC').CONTRACT_ID.nunique()   
# 	## Get interest rate segments
# 	bins=[0, 18, np.inf]
# 	labels = ["interest rate < 18%", "interest rate >= 18%"]
# 	loans_interest_rate = loans_data.groupby(pd.cut(loans_data['INTEREST_RATE'], bins, include_lowest=True, right = False, labels=labels)).CONTRACT_ID.nunique()

# 	colors_interest=['grey','darkred']    
# # 	colors_gender = ["#45b6fe","#000080"]
# 	colors_gender = ["#242444","gray"]
# 	colors_sbu = ["#46648c","grey","#242444"]

# 	## Get Total Amount PL and NPL
# 	number_pl_npl = loans_data.groupby("MAIN_CLASSIFICATION_DESC").CONTRACT_ID.nunique()
# 	total_amt_pl_non_pl = loans_data.groupby("MAIN_CLASSIFICATION_DESC").OUTSTANDING_PRINCIPAL_LCY.sum()

# 	colors_pl_npl = None
# 	if number_pl_npl.index[0] != "NON PERFORMING ASSETS":
# 		colors_pl_npl =  ["grey", "darkred"]
# 	else:
# 		colors_pl_npl =  [ "darkred", "grey"]


# 	age_output = None
# 	segmentation_over_time_output = None
# 	segmentation_by_sector_output = None

# 	account_officer_output= html.Div([dbc.CardGroup([
# 	    	dbc.Card([
# 			    dcc.Graph(
# 			        figure=go.Figure(
# 			            data=[
# 			                go.Bar(
# 			                    x= ao_perf.index, 
# 			                    y= ao_perf,
# 			                    text = get_percentage_label((ao_perf/(ao_perf + ao_nonperf)*100)[ao_perf.index].fillna(100).round(2)),
# 			                    name='Performing',
# 			                    textposition='auto',
# 			                    customdata= ao_perf_balance,
# 					            hovertemplate= format_hover_template(x_label= "AO name"),
# 			                    marker=go.bar.Marker(
# 			                        color='grey'
# 			                    )
# 			                ),
# 			                go.Bar(
# 			                    x= ao_nonperf.index, 
# 			                    y= ao_nonperf,
# 			                    text = get_percentage_label((ao_nonperf/(ao_perf + ao_nonperf)*100)[ao_nonperf.index].fillna(100).round(2)),
# 			                    name='Non Performing',
# 			                    textposition='auto',
# 			                    customdata= ao_nonperf_balance,
# 					            hovertemplate= format_hover_template(x_label= "AO name"),
# 			                    marker=go.bar.Marker(
# 			                        color='darkred'
# 			                    )
# 			                ),
# 			            ],
# 			            layout=go.Layout(
# 			            	showlegend=True,
# 			                legend=go.layout.Legend(
# 			                    x=1.0,
# 			                    y=1.0
# 			                ),
# 			                # margin=go.layout.Margin(l=10, r=10, t=30, b=10),
			             
# 						    title=go.layout.Title(
# 								text="(Non) Performing Loans per Account Officer",
# 							),
# 							xaxis=go.layout.XAxis(
#                                 tickangle=55,
# 								title=go.layout.xaxis.Title(
# 									text="Account Officer Name",
# 									# font=dict(
# 									#     family="Courier New, monospace",
# 									#     size=18,
# 									#     color="#7f7f7f"
# 									# )
# 								)
# 							),
# 							yaxis=go.layout.YAxis(
# 								title=go.layout.yaxis.Title(
# 									text="Number of Loans",
# 									# font=dict(
# 									#     family="Courier New, monospace",
# 									#     size=18,
# 									#     color="#7f7f7f"
# 									# )
# 								)
# 							)
# 			            )
# 			        ),
# 			        id="ao-graph-20",
# 			        style={"width": "100%", "height": "600px"},
# 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Number of (Non) Performing Loan per Account Officer")}),
# 			    ),
# 			], body=True,
# 			),
# 		]),                                      
#         dbc.CardGroup([
#             dbc.Card([
#                 dcc.Graph(
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(
#                                 x= product_perf.index, 
#                                 y= product_perf,
#                                 text = get_percentage_label((product_perf*100/(product_perf+product_non_perf))[product_perf.index].fillna(1).round()),
#                                 name='Performing',
#                                 textposition='auto',
#                                 customdata= product_perf_balance,
#                                 hovertemplate= format_hover_template(x_label= "Product" , x_unit=""),
#                                 marker=go.bar.Marker(
#                                     color='grey'
#                                 )
#                             ),
#                              go.Bar(
#                                 x= product_non_perf.index, 
#                                 y= product_non_perf,
#                                 text = get_percentage_label((product_non_perf*100/(product_perf+product_non_perf))[product_non_perf.index].fillna(1).round()),
#                                 name='Non Performing',
#                                 textposition='auto',
#                                 customdata= product_nonperf_balance,
#                                 hovertemplate= format_hover_template(x_label= "Product" , x_unit=""),                                 
#     #                                 customdata= performing_over_time_balance,
# #                                 hovertemplate= format_hover_template(x_label= "S", x_unit=""),
#                                 marker=go.bar.Marker(
#                                     color='darkred'
#                                 )
#                             ),                           
#                         ],
#                         layout=go.Layout(
#                             showlegend=True,
#                             legend=go.layout.Legend(
#                                 x=1.0,
#                                 y=1.0
#                             ),
#                             margin=go.layout.Margin(l=10, r=10, t=30, b=10),

#                             title=go.layout.Title(
#                                 text="Loans performance per product",
#                             ),
#                             xaxis=go.layout.XAxis(
#                                 tickangle=55,
#                                 title=go.layout.xaxis.Title(
#                                     text="Product",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ),
#                             yaxis=go.layout.YAxis(
#                                 title=go.layout.yaxis.Title(
#                                     text="Number of Loans ",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             )
#                         )
#                     ),
#                     id="loan-trend-graph-4",
#                     config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans performance per product")}),
#                     style = {"height":750}
#                 ),
#             ]),
#         ]),                                      
# 	])


# 	if loan_selected:
# 		(
# 		    performing_over_time, non_performing_over_time,
# 		    performing_by_sector, non_performing_by_sector,
# 			performing_over_time_balance, non_performing_over_time_balance,
# 			performing_by_sector_balance, non_performing_by_sector_balance
# 		) = get_loans_over_time_and_by_sector(session_id, loans_data, loan_group, loan_selected)

# 		if loan_selected in get_loan_type_list(session_id, loans_data, "RETAIL") or loan_selected in get_loan_type_list(session_id, loans_data, "STAFF"):

# 			(
# 			    age_perf_male, age_nonperf_male, age_perf_fem, age_nonperf_fem,
# 			    age_perf_male_balance, age_nonperf_male_balance, age_perf_fem_balance, age_nonperf_fem_balance
# 			) = get_loan_age(session_id, loans_data, loan_group)
			
# 			age_output = dbc.CardGroup([
# 			    dbc.Card(
# 		            [
# 		                html.Div([
# 					        dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=age_perf_male.index,
# 						                y=age_perf_male.values,
# 						                name='Male Performing',
# 						                text=get_percentage_label((age_perf_male.values*100/(age_nonperf_male.values+age_perf_male.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_perf_male_balance,
# 					                	hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=age_nonperf_male.index,
# 						                y=age_nonperf_male.values,
# 						                name='Male Non Performing',
# 						                text=get_percentage_label((age_nonperf_male.values*100/(age_nonperf_male.values+age_perf_male.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_nonperf_male_balance,
# 					                	hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='lightblue'
# 						                )
# 						            ),  
# 						            go.Bar(
# 						                x=age_perf_fem.index,
# 						                y=age_perf_fem.values,
# 						                name='Female Performing',
# 						                text=get_percentage_label((age_perf_fem.values*100/(age_nonperf_fem.values+age_perf_fem.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_perf_fem_balance,
# 					                	hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='darkred'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=age_nonperf_fem.index,
# 						                y=age_nonperf_fem.values,
# 						                name='Female Non Performing',
# 						                text=get_percentage_label((age_nonperf_fem.values*100/(age_nonperf_fem.values+age_perf_fem.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_nonperf_fem_balance,
# 					                	hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='#F5D3C7'
# 						                )
# 						            ),           
# 		                        ],   
# 						        layout=go.Layout(
# 		                          	title=go.layout.Title(
# 										text="Loans performance based on customer's age",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
# 		                                title=go.layout.xaxis.Title(
# 			                                text="Age Group",
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
# 						    config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Loans performance based on customer's age")}),
# 						),

# 		                ]),
# 		            ],
# 		            body=True,
# 		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
# 		        ),       
# 		    ])

# 		if non_performing_over_time is None:

# 			segmentation_over_time_output = html.Div([                
# 				dbc.CardGroup([
# 			        dbc.Card([
# 					    dcc.Graph(
# 					        figure=go.Figure(
# 					            data=[
# 					                go.Scatter(
# 					                    x= format_time_index(performing_over_time.index), 
# 					                    y= performing_over_time,
# 					                    text = get_percentage_label((performing_over_time/(performing_over_time)*100).round(2)),
# 					                    name='Performing ',
# 					                    mode = "lines+markers",
# 					                    customdata= performing_over_time_balance,
# 							            hovertemplate= format_hover_template(x_label= "Remaining Time", x_unit="Months"),
# 					                    marker=go.scatter.Marker(
# 					                        color='grey'
# 					                    )
# 					                ),
# 					            ],
# 					            layout=go.Layout(
# 					            	showlegend=True,
# 					                legend=go.layout.Legend(
# 					                    x=1.0,
# 					                    y=1.0
# 					                ),
# 					                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
					             
# 								    title=go.layout.Title(
# 										text="Loans Performance based on tenor months",
# 									),
# 									xaxis=go.layout.XAxis(
# 										title=go.layout.xaxis.Title(
# 											text="Tenor months",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									),
# 									yaxis=go.layout.YAxis(
# 										title=go.layout.yaxis.Title(
# 											text="Number of Loans",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									)
# 					            )
# 					        ),
# 					        id="loan-trend-graph-5",
# 					        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans Performance based on tenor months")}),
# 					    ),
# 					]),
# #                     dbc.Card([
# #                         dcc.Graph(
# #                             figure=go.Figure(
# #                                 data=[
# #                                     go.Bar(
# #                                         x= amount_perf.index, 
# #                                         y= amount_perf,
# #                                         text = get_percentage_label((amount_perf/(amount_non_perf + amount_perf)*100)[segment_perf.index].fillna(100).round(2)),
# #                                         name='Performing',
# #                                         textposition='auto',
# #     # 				                    customdata= segment_perf_balance,
# #     # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# #     				                    marker=go.bar.Marker(
# #     				                        color='grey'
# #     				                    )
# #                                     ),
# #                                     go.Bar(
# #                                         x= amount_non_perf.index, 
# #                                         y= amount_non_perf,
# #                                         text = get_percentage_label((amount_non_perf/(amount_non_perf + amount_perf)*100)[segment_nonperf.index].dropna().round(2)),
# #                                         name='Non Performing',
# #                                         textposition='auto',
# #     # 				                    customdata= segment_nonperf_balance,
# #     # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# #                                         marker=go.bar.Marker(
# #                                             color='darkred'
# #                                         )
# #                                     ),
# #                                 ],
# #                                 layout=go.Layout(
# #                                     legend=go.layout.Legend(
# #                                         x=0.7,
# #                                         y=1.0
# #                                     ),
# #                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

# #                                     title=go.layout.Title(
# #                                         text="Loans performance based on approved amount",
# #                                     ),
# #                                     xaxis=go.layout.XAxis(
# #                                         title=go.layout.xaxis.Title(
# #                                             text=" loan Performing Class ",
# #                                             # font=dict(
# #                                             #     family="Courier New, monospace",
# #                                             #     size=18,
# #                                             #     color="#7f7f7f"
# #                                             # )
# #                                         )
# #                                     ),
# #                                     yaxis=go.layout.YAxis(
# #                                         title=go.layout.yaxis.Title(
# #                                             text="Approved amount",
# #                                             # font=dict(
# #                                             #     family="Courier New, monospace",
# #                                             #     size=18,
# #                                             #     color="#7f7f7f"
# #                                             # )
# #                                         )
# #                                     )
# #                                 )
# #                             ),
# #                             id="loan-trend-graph-3.1",
# #                             config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loans performance based on approved amount" )}),
# #                         ),
# #                     ]),                
                                    
# 				]),
# 			])

# 			segmentation_by_sector_output = html.Div([
# 				dbc.CardGroup([
# 					dbc.Card([
# 					    dcc.Graph(
# 					        figure=go.Figure(
# 					            data=[
# 					                go.Bar(
# 					                    x= performing_by_sector.index, 
# 					                    y= performing_by_sector,
# 					                    text = get_percentage_label(((performing_by_sector/(performing_by_sector ))[performing_by_sector.index].fillna(1)*100).round(2)),
# 					                    name='Performing',
# 					                    textposition='auto',
# 					                    customdata= performing_over_time_balance,
# 							            hovertemplate= format_hover_template(x_label= "Sector", x_unit=""),
# 					                    marker=go.bar.Marker(
# 					                        color='grey'
# 					                    )
# 					                ),
# 					            ],
# 					            layout=go.Layout(
# 					                showlegend=True,
# 					                legend=go.layout.Legend(
# 					                    x=1.0,
# 					                    y=1.0
# 					                ),
# 					                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
					             
# 								    title=go.layout.Title(
# 										text="Performing loans per industry Sectors",
# 									),
# 									xaxis=go.layout.XAxis(
# 										tickangle=55,
# 										title=go.layout.xaxis.Title(
# 											text="Sectors",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									),
# 									yaxis=go.layout.YAxis(
# 										title=go.layout.yaxis.Title(
# 											text="Number of Loans ",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									)
# 					            )
# 					        ),
# 					        id="loan-trend-graph-4",
# 					        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Performing loans per industry Sectors")}),
# 					        style = {"height":750}
# 					    ),
# 					]),
# 				]),
# 			])
# 		else:
# 			segmentation_over_time_output = html.Div([
# 				dbc.CardGroup([
# 			        dbc.Card([
# 					    dcc.Graph(
# 					        figure=go.Figure(
# 					            data=[
# 					                go.Scatter(
# 					                    x= format_time_index(performing_over_time.index), 
# 					                    y= performing_over_time,
# 					                    text = get_percentage_label((performing_over_time/(performing_over_time + non_performing_over_time)*100).round(2)),
# 					                    name='Performing ',
# 					                    mode = "lines+markers",
# 					                    customdata= performing_over_time_balance,
# 							            hovertemplate= format_hover_template(x_label= "Remaining Time", x_unit="Months"),
# 					                    marker=go.scatter.Marker(
# 					                        color='grey'
# 					                    )
# 					                ),
# 					                go.Scatter(
# 					                    x= format_time_index(non_performing_over_time.index), 
# 					                    y= non_performing_over_time,
# 					                    text = get_percentage_label((non_performing_over_time/(performing_over_time + non_performing_over_time)*100).round(2)),
# 					                    name='Non Performing ',
# 					                    mode = "lines+markers",
# 					                    customdata= non_performing_over_time_balance,
# 							            hovertemplate= format_hover_template(x_label= "Remaining Time", x_unit="Months"),
# 					                    marker=go.scatter.Marker(
# 					                        color='darkred'
# 					                    )
# 					                ),
# 					            ],
# 					            layout=go.Layout(
# 					            	showlegend=True,
# 					                legend=go.layout.Legend(
# 					                    x=1.0,
# 					                    y=1.0
# 					                ),
# 					                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
					             
# 								    title=go.layout.Title(
# 										text="Loans Performance based on tenor months",
# 									),
# 									xaxis=go.layout.XAxis(
# 										title=go.layout.xaxis.Title(
# 											text="Tenor months",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									),
# 									yaxis=go.layout.YAxis(
# 										title=go.layout.yaxis.Title(
# 											text="Number of Loan Accounts",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									)
# 					            )
# 					        ),
# 					        id="loan-trend-graph-5",
# 					        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans Performance based on tenor months")}),
# 					    ),
# 					]),
# #                     dbc.Card([
# #                         dcc.Graph(
# #                             figure=go.Figure(
# #                                 data=[
# #                                     go.Bar(
# #                                         x= amount_perf.index, 
# #                                         y= amount_perf,
# #                                         text = get_percentage_label((amount_perf/(amount_non_perf + amount_perf)*100)[segment_perf.index].fillna(100).round(2)),
# #                                         name='Performing',
# #                                         textposition='auto',
# #     # 				                    customdata= segment_perf_balance,
# #     # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# #     				                    marker=go.bar.Marker(
# #     				                        color='grey'
# #     				                    )
# #                                     ),
# #                                     go.Bar(
# #                                         x= amount_non_perf.index, 
# #                                         y= amount_non_perf,
# #                                         text = get_percentage_label((amount_non_perf/(amount_non_perf + amount_perf)*100)[segment_nonperf.index].dropna().round(2)),
# #                                         name='Non Performing',
# #                                         textposition='auto',
# #     # 				                    customdata= segment_nonperf_balance,
# #     # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# #                                         marker=go.bar.Marker(
# #                                             color='darkred'
# #                                         )
# #                                     ),
# #                                 ],
# #                                 layout=go.Layout(
# #                                     legend=go.layout.Legend(
# #                                         x=0.7,
# #                                         y=1.0
# #                                     ),
# #                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

# #                                     title=go.layout.Title(
# #                                         text="Loans performance based on approved amount",
# #                                     ),
# #                                     xaxis=go.layout.XAxis(
# #                                         title=go.layout.xaxis.Title(
# #                                             text=" loan Performing Class ",
# #                                             # font=dict(
# #                                             #     family="Courier New, monospace",
# #                                             #     size=18,
# #                                             #     color="#7f7f7f"
# #                                             # )
# #                                         )
# #                                     ),
# #                                     yaxis=go.layout.YAxis(
# #                                         title=go.layout.yaxis.Title(
# #                                             text="Approved amount",
# #                                             # font=dict(
# #                                             #     family="Courier New, monospace",
# #                                             #     size=18,
# #                                             #     color="#7f7f7f"
# #                                             # )
# #                                         )
# #                                     )
# #                                 )
# #                             ),
# #                             id="loan-trend-graph-3.1",
# #                             config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loans performance based on approved amount" )}),
# #                         ),
# #                     ]),                
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
#                                             y=branch_perf,
#                                             name='Performing',
# #                                             text=branch_perf,
#                                             text=get_percentage_label((branch_perf*100/(branch_nonperf+branch_perf)).round()),
#                                             customdata= branch_perf_balance,
#                                             hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),
#                                             textposition='auto',
#                                             marker=go.bar.Marker(
#                                                 color='grey'
#                                             )
#                                         ),
#                                         go.Bar(
#                                             x=branch_nonperf.rename(index=branch_name_mapping).index,
#                                             y=branch_nonperf,
#                                             name='Non Performing',
# #                                             text=branch_nonperf,
#                                             text=get_percentage_label((branch_nonperf*100/(branch_nonperf+branch_perf)).round()),
#                                             customdata= branch_nonperf_balance,
#                                             hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),
#                                             textposition='auto',
#                                             marker=go.bar.Marker(
#                                                 color='darkred'
#                                             )
#                                         ),  
 
#                                     ],   
#                                     layout=go.Layout(
#                                         title=go.layout.Title(
#                                             text="Loan performance based on branch level",
#                                         # 	xref="paper",
#                                         # 	x=0
#                                         ),
#                                         xaxis=go.layout.XAxis(
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
# 			])

# 			segmentation_by_sector_output = html.Div([
# 				dbc.CardGroup([
# 					dbc.Card([
# 					    dcc.Graph(
# 					        figure=go.Figure(
# 					            data=[
# 					                go.Bar(
# 					                    x= performing_by_sector.index, 
# 					                    y= performing_by_sector,
# 					                    text = get_percentage_label(((performing_by_sector/(performing_by_sector + non_performing_by_sector))[performing_by_sector.index].fillna(1)*100).round(2)),
# 					                    name='Performing',
# 					                    textposition='auto',
# 					                    customdata= performing_by_sector_balance,
# 							            hovertemplate= format_hover_template(x_label= "Sector", x_unit=""),
# 					                    marker=go.bar.Marker(
# 					                        color='grey'
# 					                    )
# 					                ),
# 					                go.Bar(
# 					                    x= non_performing_by_sector.index, 
# 					                    y= non_performing_by_sector,
# 					                    text = get_percentage_label(((non_performing_by_sector/(performing_by_sector + non_performing_by_sector))[non_performing_by_sector.index].fillna(1)*100).round(2)),
# 					                    name='Non Performing',
# 					                    textposition='auto',
# 					                    customdata= non_performing_by_sector_balance,
# 							            hovertemplate= format_hover_template(x_label= "Sector", x_unit=""),
# 					                    marker=go.bar.Marker(
# 					                        color='darkred'
# 					                    )
# 					                ),
# 					            ],
# 					            layout=go.Layout(
# 					                showlegend=True,
# 					                legend=go.layout.Legend(
# 					                    x=1.0,
# 					                    y=1.0
# 					                ),
# 					                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
					             
# 								    title=go.layout.Title(
# 										text="Loans Performance based per industry Sectors",
# 									),
# 									xaxis=go.layout.XAxis(
# 										tickangle=55,
# 										title=go.layout.xaxis.Title(
# 											text="Sectors",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									),
# 									yaxis=go.layout.YAxis(
# 										title=go.layout.yaxis.Title(
# 											text="Number of Loans",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									)
# 					            )
# 					        ),
# 					        id="loan-trend-graph-4",
# 					        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans Performance based per industry Sectors")}),
# 					        style = {"height":750}
# 					    ),
# 					]),
# 				]),
# 			])

# 		output =  [
# 			html.Div([
# 				html.H2("{}".format(loan_selected or loan_group), ),
# 				html.Hr(),
# 			]),
# 			dbc.CardDeck(
# 				[
#                     dbc.Card(
#                         [
#                             html.H6("New disbursed Loans from: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                            
#                             html.H3(" {:,.0f}".format(loan_opening[-1]), style={"color":"green"}), 
# #                             html.H6("New Loan Customers from: {}".format(customer_opening.index[-1].strftime("%b %d (%a), %Y"))),                            
# #                             html.H3("+ {:,.0f}".format(customer_opening[-1]), style={"color":"green"}),                     
#                         ],
#                         body=True,
#                         style={"align":"center", "justify":"center",}
#                     ),    
#                     dbc.Card(
# 		                [
# 		                    html.H6("Total Number of ongoing Loans"),                            
# 		                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()), style={"color":"#45b6fe"} ),
# 		                    html.H6("Total Number of Borrowers"),
# 		                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),
# 		                ],
# 		                body=True,
# 		            ),
# 		            dbc.Card(
# 		                [
# 		                    html.H6("Total Approved Amount in million"),                            
# 		                    html.H2("rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()/1e6), style={"color":"darkred"}),
# 		                    html.H6("Total loan Outstanding Amount in million"),                            
# 		                    html.H2("rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()/1e6), style={"color":"DarkRed"}),
# 		                ],
# 		                body=True,
# 		            ),
# 		            dbc.Card(
# 		                [
# 		                    html.H6("Total Net Income in million"),                            
# 		                    html.H2("rwf {:,.0f}".format(loans_data.NET_INCOME_LCY.sum()/1e6), style={"color":"blue"}),
# 		                    html.H6("Total Fee Income in million"),                     
# 		                    html.H2("rwf {:,.0f}".format(loans_data.CHARGES_RECEIVED_LCY.sum()/1e6), style={"color":"blue"}),
# 		                ],
# 		                body=True,
# 		            ),
# 				],	
# 			),
# # 		dbc.CardDeck(
# # 			[
# # 	            dbc.Card(
# # 	                [
# # 	                    html.H6("New Loans from: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                        
# # 	                    html.H3(" {:,.0f}".format(loan_opening[-1]), style={"color":"green"}),
# # # 	                    html.H6("New Loan Customers from: {}".format(cust_opening.index[-1].strftime("%b %d (%a), %Y"))),                   
# # # 	                    html.H3("+ {:,.0f}".format(cust_opening[-1]), style={"color":"green"}),                     
# # 	                ],
# # 	                body=True,
# # 	                style={"align":"center", "justify":"center",}
# # 	            ),
# # 	            dbc.Card(
# # 	                [
# # 	                    html.H6("Total Number of ongoing Loans"),                        
# # 	                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()),style={"color":"#45b6fe"}),
# # 	                    html.H6("Total Number of Borrowers"),                         
# # 	                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),
# # 	                ],
# # 	                body=True,
# # 	            ),
# # 	            dbc.Card(
# # 	                [
# # 	                    html.H6("Total Approved Amount in Million "),                         
# # 	                    html.H2("rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()/1e6), style={"color":"darkred"}),
# # 	                    html.H6("Total loan Outstanding Amount in Million"),                    
# # 	                    html.H2("rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()/1e6), style={"color":"DarkRed"}),
# # 	                ],
# # 	                body=True,
# # 	            ),
# # 	            dbc.Card(
# # 	                [
# # 	                    html.H6("Total Net Income in Million"),                         
# # 	                    html.H2("rwf {:,.0f}".format(loans_data.NET_INCOME_LCY.sum()/1e6), style={"color":"#000080"}),  
# # 	                    html.H6("Total Fee Income in Million "),                        
# # 	                    html.H2("rwf {:,.0f}".format(loans_data.CHARGES_RECEIVED_LCY.sum()/1e6), style={"color":"#000080"}),
# # 	                ],
# # 	                body=True,
# # 	            ),
# # 			],	
# #         ),
            
# 			#################################################################################
# 			html.Div([
# 				dbc.CardGroup(
# 					[
# 			            dbc.Card(
# 			                [
# 			      				html.Div([
# 								    dcc.Graph(
# 									    figure=go.Figure(
# 									        data=[
# 									            go.Pie(
# 									            	labels=number_pl_npl.index, 
# 									            	values=number_pl_npl,
# 									            	text = number_pl_npl,
# 									            	hoverinfo= "label+percent+text",
#                                                     hole=0.5,
# 									            	marker=go.pie.Marker(
# 									            		colors= colors_pl_npl,
# 									            		# line=dict(color='#000000', width=1),
# 								            		),	
# 								            		# hoverinfo='label+value',
# 									            ),
# 									        ],
# 									        layout=go.Layout(
# 									            title="Rate of Loans Performance",
# 									            showlegend=True,
# 									            legend=go.layout.Legend(
# 									                x=1.0,
# 									                y=1.0
# 									            ),
# 									            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
# 											),
# 									    ),
# 									    style={'height': 300, "top":30},
# 									    id="loan-pie-cart-1.1.1",
# 									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Rate of Loans Performance")}),
# 									)
# 			                    ]),
# 			                ],
# 			                body=True,
# 			                style={"padding":"5px 5px 5px 5px", },
# 			            ),
# 			            dbc.Card(
# 			                [
# 			                    html.Div([
# 								        dcc.Graph(
# 									    figure=go.Figure(
# 									        data=[
# 									            go.Pie(
# 									            	labels=total_amt_pl_non_pl.index, 
# 									            	values=total_amt_pl_non_pl,
# 									            	text = total_amt_pl_non_pl,
# 									            	hoverinfo= "label+percent+text",
#                                                     hole=0.5,
# 									            	marker=go.pie.Marker(
# 									            		colors=  colors_pl_npl,
# 									            		# line=dict(color='#000000', width=1),
# 								            		),						            		
# 									            ),
# 									        ],
# 									        layout=go.Layout(
# 									            title="Rate of Loan Performance Based on Outstanding Amount",
# 									            # showlegend=True,
# 									            legend=go.layout.Legend(
# 									                x=1.0,
# 									                y=1.0
# 									            ),
# 									            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
									            							            				                    	
# 									        )
# 									    ),
# 									    style={'height': 300, "top":30},
# 									    id="loan-pie-cart0.1",
# 									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Rate of Loan Performance Based on Outstanding Amount")}),
# 									)
# 			                    ]),
# 			                ],
# 			                body=True,
# 			            ),  
# 					],
# 				),
# 				###############
# 				dbc.CardGroup(
# 					[
# 			            dbc.Card(
# 			                [
# 			      				html.Div([
# 								    dcc.Graph(
# 									    figure=go.Figure(
# 									        data=[
# 									            go.Pie(
# 									            	labels=customer_sbu.rename(index=SBU_MAPPING).index, 
# 									            	values=customer_sbu,
#                                                     hole=0.5,
# 									            	marker=go.pie.Marker(
# 									            		colors=colors_sbu, 
# 									            		# line=dict(color='#000000', width=1),
# 								            		),	
# 								            		# hoverinfo='label+value',
# 									            ),
# 									        ],
# 									        layout=go.Layout(
# 									            title="Borrowers per Strategy Business Unit (SBU)",
# 									            showlegend=True,
# 									            legend=go.layout.Legend(
# 									                x=1.0,
# 									                y=1.0
# 									            ),
# 									            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
# 											),
# 									    ),
# 									    style={'height': 300, "top":30},
# 									    id="loan-pie-cart-1",
# 									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Borrowers per Strategy Business Unit (SBU)")}),
# 									)
# 			                    ]),
# 			                ],
# 			                body=True,
# 			                style={"padding":"5px 5px 5px 5px", },
# 			            ),
# 			            dbc.Card(
# 			                [
# 			                    html.Div([
# 								        dcc.Graph(
# 									    figure=go.Figure(
# 									        data=[
# 									            go.Pie(
# 									            	labels=customer_gender.rename(index=GENDER_MAPPING).index, 
# 									            	values=customer_gender,
#                                                     hole=0.5,
# 									            	marker=go.pie.Marker(
# 									            		colors=colors_gender, 
# 									            		# line=dict(color='#000000', width=1),
# 								            		),						            		
# 									            ),
# 									        ],
# 									        layout=go.Layout(
# 									            title="Retail borrower's Gender",
# 									            # showlegend=True,
# 									            legend=go.layout.Legend(
# 									                x=1.0,
# 									                y=1.0
# 									            ),
# 									            margin=go.layout.Margin(l=5, r=5, t=50, b=5),
									            							            				                    	
# 									        )
# 									    ),
# 									    style={'height': 300, "top":30},
# 									    id="loan-pie-cart",
# 									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Retail borrower's Gender")}),
# 									)
# 			                    ]),
# 			                ],
# 			                body=True,
# 			            ),  
# 					],
# 				),
#                 dbc.CardGroup([
#                     dbc.Card([
#                         dcc.Graph(
#                             figure=go.Figure(
#                                 data=[
#         # 			                go.Scatter(
#         # 			                    x= customer_opening.index, 
#         # 			                    y= customer_opening.values,
#         # 			                    name='Customers',
#         # 			                    mode= "lines",
#         # 			                    marker=go.scatter.Marker(
#         # 			                        color='#000080'
#         # 			                    )
#         # 			                ),
#                                     go.Scatter(
#                                         x= loan_opening.index, 
#                                         y= loan_opening.values,
#                                         name='Loans',
#                                         mode= "lines",
#                                         marker=go.scatter.Marker(
#                                             color='#494c53'
#                                         )
#                                     ),
#                                 ],
#                                 layout=go.Layout(
#                                     showlegend=True,
#                                     xaxis_rangeslider_visible= True,
#                                     legend=go.layout.Legend(
#                                         x=0,
#                                         y=1.0
#                                     ),
#                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

#                                     title=go.layout.Title(
#                                         text="Loan disbursed Over Time",
# #                                         x=0,
# #                                         y=1
#                                     ),
#                                     xaxis=go.layout.XAxis(
#                                         rangeselector=dict(
#                                             buttons=list([
#                                                 dict(count=1,
#                                                      label="1MONTH",
#                                                      step="month",
#                                                      stepmode="backward"),
#                                                 dict(count=3,
#                                                      label="3MONTHS",
#                                                      step="month",
#                                                      stepmode="backward"),                                                    
#                                                 dict(count=6,
#                                                      label="6MONTHS",
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
#                                         ),                                                                         
#         #                                             ),                                                        
#         #                                             title=go.layout.xaxis.Title(
#         #                                                 text="Years",
#         #                                                 # font=dict(
#         #                                                 #     family="Courier New, monospace",
#         #                                                 #     size=18,
#         #                                                 #     color="#7f7f7f"
#         #                                                 # )
#         #                                             )
#                                     )
#         #                                         yaxis=go.layout.YAxis(
#         #                                             title=go.layout.yaxis.Title(
#         #                                                 text="Number of Customers",
#         #                                                 # font=dict(
#         #                                                 #     family="Courier New, monospace",
#         #                                                 #     size=18,
#         #                                                 #     color="#7f7f7f"
#         # #                                                 # )
#         # #                                             )
#         #                                         )
#                                 )
#                             ),
#         #                     body=True,
#         #                     style={"padding":"5px 5px 5px 5px", },
#         # 			        id="loan-trend-graph-1",
#         # 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
#         # 			    ),
#                     ],style={'padding': 10}),
#                     dbc.Card([
#                         dcc.Graph(
#                             figure=go.Figure(
#                                 data=[
#         # 			                go.Scatter(
#         # 			                    x= customer_opening.index, 
#         # 			                    y= customer_opening.values,
#         # 			                    name='Customers',
#         # 			                    mode= "lines",
#         # 			                    marker=go.scatter.Marker(
#         # 			                        color='#000080'
#         # 			                    )
#         # 			                ),
#                                     go.Scatter(
#                                         x= loan_opening.index, 
#                                         y= np.cumsum(loan_opening.values),
#                                         name='Loans',
#                                         mode= "lines",
#                                         marker=go.scatter.Marker(
#                                             color='#494c53'
#                                         )
#                                     ),
#                                 ],
#                                 layout=go.Layout(
#                                     showlegend=True,
#                                     xaxis_rangeslider_visible= True,
#                                     legend=go.layout.Legend(
#                                         x=0,
#                                         y=1.0
#                                     ),
#                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

#                                     title=go.layout.Title(
#                                         text="Loan disbursed Over Time",
#                                         x=0,
#                                         y=1
#                                     ),
#         #                             xaxis=go.layout.XAxis(
#         #                                 rangeselector=dict(
#         #                                     buttons=list([
#         #                                         dict(count=1,
#         #                                              label="1MONTH",
#         #                                              step="month",
#         #                                              stepmode="backward"),
#         #                                         dict(count=3,
#         #                                              label="3MONTHS",
#         #                                              step="month",
#         #                                              stepmode="backward"),                                                    
#         #                                         dict(count=6,
#         #                                              label="6MONTHS",
#         #                                              step="month",
#         #                                              stepmode="backward"),
#         #                                         dict(count=1,
#         #                                              label="1YEAR",
#         #                                              step="year",
#         #                                              stepmode="backward"),
#         #                                         dict(step="all")
#         #                                     ])
#         #                                 ),
#         #                                 rangeslider=dict(
#         #                                     visible=True
#         #                                 ),
#         #                                 type="date"
#         #                                 ),                                                                         
#         #                                             ),                                                        
#         #                                             title=go.layout.xaxis.Title(
#         #                                                 text="Years",
#         #                                                 # font=dict(
#         #                                                 #     family="Courier New, monospace",
#         #                                                 #     size=18,
#         #                                                 #     color="#7f7f7f"
#         #                                                 # )
#         #                                             )
#                                     )
#         #                                         yaxis=go.layout.YAxis(
#         #                                             title=go.layout.yaxis.Title(
#         #                                                 text="Number of Customers",
#         #                                                 # font=dict(
#         #                                                 #     family="Courier New, monospace",
#         #                                                 #     size=18,
#         #                                                 #     color="#7f7f7f"
#         # #                                                 # )
#         # #                                             )
#         #                                         )
#                                 )
#                             ),
#         #                     body=True,
#         #                     style={"padding":"5px 5px 5px 5px", },
#         # 			        id="loan-trend-graph-1",
#         # 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
#         # 			    ),
#                     ],style={'padding': 10}),
                    
#                 ]),                
# 			]),
# 			####################################################################################
# 			# html.Div([]),
# 		    #############################################################################
# 		    html.Div([
# 			    dbc.CardGroup([
# 					dbc.Card([
# 					    dcc.Graph(
# 					        figure=go.Figure(
# 					            data=[
# 					                go.Bar(
# 					                    x= segment_perf.rename(index=SEGMENTS_MAPPING).index, 
# 					                    y= segment_perf,
# 					                    text = get_percentage_label((segment_perf/(segment_perf + segment_nonperf)*100)[segment_perf.index].fillna(100).round(2)),
# 					                    name='Performing',
# 					                    textposition='auto',
# # 					                    customdata= segment_perf_balance,
# # 					                	hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# 					                    marker=go.bar.Marker(
# 					                        color='grey'
# 					                    )
# 					                ),
# 					                go.Bar(
# 					                    x= segment_nonperf.rename(index=SEGMENTS_MAPPING).index, 
# 					                    y= segment_nonperf,
# 					                    text = get_percentage_label((segment_nonperf/(segment_perf + segment_nonperf)*100)[segment_nonperf.index].fillna(100).round(2)),
# 					                    name='Non Performing',
# 					                    textposition='auto',
# # 					                    customdata= segment_nonperf_balance,
# # 					                	hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# 					                    marker=go.bar.Marker(
# 					                        color='darkred'
# 					                    )
# 					                ),
# 					            ],
# 					            layout=go.Layout(
# 					            	showlegend=True,
# 					                legend=go.layout.Legend(
# 					                    x=0.5,
# 					                    y=1.0
# 					                ),
# 					                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
					             
# 								    title=go.layout.Title(
# 										text="Loans performance per customer's category",
# 									),
# 									xaxis=go.layout.XAxis(
# 										title=go.layout.xaxis.Title(
# 											text="Category",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									),
# 									yaxis=go.layout.YAxis(
# 										title=go.layout.yaxis.Title(
# 											text="Number of Loans",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									)
# 					            )
# 					        ),
# 					        id="loan-trend-graph-3.1",
# 					        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_selected, "Loans performance per customer's category")}),
# 					    ),
# 					]),
# 					dbc.Card(
# 			            [
# 			                html.Div([
# 							        dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Pie(
# 								            	labels=loans_interest_rate.index, 
# 								            	values=loans_interest_rate,
#                                                 hole=0.5,
# 								            	marker=go.pie.Marker(
# 								            		colors=colors_interest, 
# 								            		# line=dict(color='#000000', width=1),
# 							            		),						            		
# 								            ),
# 								        ],
# 								        layout=go.Layout(
# 								            title="Loan Interest Rate Segmentation",
# 								            showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=1.0,
# 								                y=1.0
# 								            ),
# 								            margin=go.layout.Margin(l=25, r=25, t=50, b=25), 							            				                    	
# 								        )
# 								    ),
# 								    # style={'height': 300, "top":30},
# 								    id="loan-pie-cart-3",
# 								    config={
# 								        "displaylogo": False,
# 									},
# 								)
# 			                ]),
# 			            ],
# 			            body=True,
# 			        ),	
# 			    ]),
# 			]),
# 			########################################################################
# 			html.Div([
# 				html.H2("{}".format(loan_selected or loan_group), ),
# 				# html.Hr(),
# 			]),
# 		    ##########################################################################
# 		    age_output,
# 		    ########################################################################
# 		    account_officer_output,
# 		    ###########################################################################
# 		    html.Div([
# 				html.H2("{}".format(loan_selected or loan_group), ),
# 				# html.Hr(),
# 			]),
# 			##########################################################################
# 		    segmentation_over_time_output,
# 			##########################################################################
# 			segmentation_by_sector_output,
# 		]
# 		return output

# 	################################ Overview at client type level #####################################
# 	else:
# 		(
# 		    performing_over_time, non_performing_over_time,
# 		    performing_by_sector, non_performing_by_sector,
# 		    performing_over_time_balance, non_performing_over_time_balance,
# 			performing_by_sector_balance, non_performing_by_sector_balance
# 		) = get_loans_over_time_and_by_sector(session_id, loans_data, loan_group, loan_selected)

# 		if loan_group == "RETAIL" or loan_group == "STAFF":

# 			(
# 			    age_perf_male, age_nonperf_male, age_perf_fem, age_nonperf_fem,
# 			    age_perf_male_balance, age_nonperf_male_balance, age_perf_fem_balance, age_nonperf_fem_balance
# 			) = get_loan_age(session_id, loans_data, loan_group)
			
# 			age_output = dbc.CardGroup([
# 			    dbc.Card(
# 		            [
# 		                html.Div([
# 					        dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=age_perf_male.index,
# 						                y=age_perf_male.values,
# 						                name='Male Performing',
# 						                text=get_percentage_label((age_perf_male.values*100/(age_nonperf_male.values+age_perf_male.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_perf_male_balance,
# 					                	hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='darkblue'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=age_nonperf_male.index,
# 						                y=age_nonperf_male.values,
# 						                name='Male Non Performing',
# 						                text=get_percentage_label((age_nonperf_male.values*100/(age_nonperf_male.values+age_perf_male.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_nonperf_male_balance,
# 					                	hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='lightblue'
# 						                )
# 						            ),  
# 						            go.Bar(
# 						                x=age_perf_fem.index,
# 						                y=age_perf_fem.values,
# 						                name='Female Performing',
# 						                text=get_percentage_label((age_perf_fem.values*100/(age_nonperf_fem.values+age_perf_fem.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_perf_fem_balance,
# 					                	hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='#F5D3C7'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=age_nonperf_fem.index,
# 						                y=age_nonperf_fem.values,
# 						                name='Female Non Performing',
# 						                text=get_percentage_label((age_nonperf_fem.values*100/(age_nonperf_fem.values+age_perf_fem.values)).round(2)),
# 		    							textposition='auto',
# 		    							customdata= age_nonperf_fem_balance,
# 					                	hovertemplate= format_hover_template(),
# 						                marker=go.bar.Marker(
# 						                    color='darkred'
# 						                )
# 						            ),           
# 		                        ],   
# 						        layout=go.Layout(
# 		                          	title=go.layout.Title(
# 										text="Loan performance based on customer's age",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
# 		                                title=go.layout.xaxis.Title(
# 			                                text="Age Group",
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
# 						    config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Loan performance based on customer's age")}),
# 						),

# 		                ]),
# 		            ],
# 		            body=True,
# 		            style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
# 		        ),
# 		    ])

# 		elif loan_group == "CORPORATE AND SME" :
# 			age_output = html.Div([])

# 		segmentation_over_time_output = html.Div([
# 		    dbc.CardGroup([
# 			    dbc.Card(
# 		            [
# 		                html.Div([
# 					        dcc.Graph(
# 						    figure=go.Figure(
# 						        data=[
# 						            go.Bar(
# 						                x=branch_perf.rename(index=branch_name_mapping).index,
# 						                y=branch_perf,
# 						                name='Performing',
# # 						                text=branch_perf,
#                                         text=get_percentage_label((branch_perf*100/(branch_nonperf+branch_perf)).round()),
#                                         customdata= branch_perf_balance,
#                                         hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),
# 						                marker=go.bar.Marker(
# 						                    color='grey'
# 						                )
# 						            ),
# 						            go.Bar(
# 						                x=branch_nonperf.rename(index=branch_name_mapping).index,
# 						                y=branch_nonperf,
# 						                name='Non Performing',
# # 						                text=branch_nonperf,
#                                         text=get_percentage_label((branch_nonperf*100/(branch_nonperf+branch_perf)).round()),
#                                         customdata= branch_nonperf_balance,
#                                         hovertemplate= format_hover_template(x_label= "Branch", y_label= "# Accounts"),                                        
# # 						                customdata= age_perf_male_balance,
# # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
# 		    							textposition='auto',
# 						                marker=go.bar.Marker(
# 						                    color='darkred'
# 						                )
# 						            ),  
# # 						            go.Bar(
# # 						                x=age_perf_fem.index,
# # 						                y=age_perf_fem.values,
# # 						                name='Female Performing',
# # 						                text=get_percentage_label((age_perf_fem.values*100/(age_nonperf_fem.values+age_perf_fem.values)).round(2)),
# # 		    							textposition='auto',
# # 		    							customdata= age_perf_fem_balance,
# # 						                hovertemplate= format_hover_template(),
# # 						                marker=go.bar.Marker(
# # 						                    color='darkred'
# # 						                )
# # 						            ),
# # 						            go.Bar(
# # 						                x=age_nonperf_fem.index,
# # 						                y=age_nonperf_fem.values,
# # 						                name='Female Non Performing',
# # 						                text=get_percentage_label((age_nonperf_fem.values*100/(age_nonperf_fem.values+age_perf_fem.values)).round(2)),
# # 		    							textposition='auto',
# # 		    							customdata= age_nonperf_fem_balance,
# # 						                hovertemplate= format_hover_template(),
# # 						                marker=go.bar.Marker(
# # 						                    color='red'
# # 						                )
# # 						            ),           
# 		                        ],   
# 						        layout=go.Layout(
# 		                          	title=go.layout.Title(
# 										text="Loan performance based on branch level",
# 									# 	xref="paper",
# 									# 	x=0
# 									),
# 		                            xaxis=go.layout.XAxis(
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
# 			dbc.CardGroup([
# 		        dbc.Card([
# 				    dcc.Graph(
# 				        figure=go.Figure(
# 				            data=[
# 				                go.Scatter(
# 				                    x= format_time_index(performing_over_time.index), 
# 				                    y= performing_over_time,
# 				                    text = get_percentage_label((performing_over_time/(performing_over_time + non_performing_over_time)*100).round(2)),
# 				                    name='Performing ',
# 				                    mode = "lines+markers",
# 				                    customdata= performing_over_time_balance,
# 						            hovertemplate= format_hover_template(x_label= "Remaining Time" , x_unit="Months"),
# 				                    marker=go.scatter.Marker(
# 				                        color='grey'
# 				                    )
# 				                ),
# 				                go.Scatter(
# 				                    x= format_time_index(non_performing_over_time.index), 
# 				                    y= non_performing_over_time,
# 				                    text = get_percentage_label((non_performing_over_time/(performing_over_time + non_performing_over_time)*100).round(2)),
# 				                    name='Non Performing ',
# 				                    mode = "lines+markers",
# 				                    customdata= non_performing_over_time_balance,
# 						            hovertemplate= format_hover_template(x_label= "Remaining Time" , x_unit="Months"),
# 				                    marker=go.scatter.Marker(
# 				                        color='darkred'
# 				                    )
# 				                ),
# 				            ],
# 				            layout=go.Layout(
# 				                legend=go.layout.Legend(
# 				                    x=1.0,
# 				                    y=1.0
# 				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# 							    title=go.layout.Title(
# 									text="Loans Performance based on tenor months",
# 								),
# 								xaxis=go.layout.XAxis(
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
# 									title=go.layout.yaxis.Title(
# 										text="Number of Loans",
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
# 				        config=add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Loans Performance based on tenor months")}),
# 				    ),
# 				]),
# # 				dbc.Card([
# # 				    dcc.Graph(
# # 				        figure=go.Figure(
# # 				            data=[
# # 				                go.Bar(
# # 				                    x= amount_perf.index, 
# # 				                    y= amount_perf,
# # 				                    text = get_percentage_label((amount_perf/(amount_non_perf + amount_perf)*100)[segment_perf.index].fillna(100).round(2)),
# # 				                    name='Performing',
# # 				                    textposition='auto',
# # # 				                    customdata= segment_perf_balance,
# # # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# # 				                    marker=go.bar.Marker(
# # 				                        color='grey'
# # 				                    )
# # 				                ),
# # 				                go.Bar(
# # 				                    x= amount_non_perf.index, 
# # 				                    y= amount_non_perf,
# # 				                    text = get_percentage_label((amount_non_perf/(amount_non_perf + amount_perf)*100)[segment_nonperf.index].dropna().round(2)),
# # 				                    name='Non Performing',
# # 				                    textposition='auto',
# # # 				                    customdata= segment_nonperf_balance,
# # # 					                hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# # 				                    marker=go.bar.Marker(
# # 				                        color='darkred'
# # 				                    )
# # 				                ),
# # 				            ],
# # 				            layout=go.Layout(
# # 				                legend=go.layout.Legend(
# # 				                    x=0.7,
# # 				                    y=1.0
# # 				                ),
# # 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# # 							    title=go.layout.Title(
# # 									text="Loans performance based on approved amount",
# # 								),
# # 								xaxis=go.layout.XAxis(
# # 									title=go.layout.xaxis.Title(
# # 										text=" loan Performing Class ",
# # 										# font=dict(
# # 										#     family="Courier New, monospace",
# # 										#     size=18,
# # 										#     color="#7f7f7f"
# # 										# )
# # 									)
# # 								),
# # 								yaxis=go.layout.YAxis(
# # 									title=go.layout.yaxis.Title(
# # 										text="Approved amount",
# # 										# font=dict(
# # 										#     family="Courier New, monospace",
# # 										#     size=18,
# # 										#     color="#7f7f7f"
# # 										# )
# # 									)
# # 								)
# # 				            )
# # 				        ),
# # 				        id="loan-trend-graph-3.1",
# # 				        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Loans performance based on approved amount" )}),
# # 				    ),
# # 				]),                                                
# 			]),
# 		])

# 		segmentation_by_sector_output = html.Div([
# 			dbc.CardGroup([
# 				dbc.Card([
# 				    dcc.Graph(
# 				        figure=go.Figure(
# 				            data=[
# 				                go.Bar(
# 				                    x= performing_by_sector.index, 
# 				                    y= performing_by_sector,
# 				                    text = get_percentage_label(((performing_by_sector/(performing_by_sector + non_performing_by_sector))[performing_by_sector.index].fillna(1)*100).round(2)),
# 				                    name='Performing',
# 				                    textposition='auto',
# 				                    customdata= performing_by_sector_balance,
# 						            hovertemplate= format_hover_template(x_label= "Sector" , x_unit=""),
# 				                    marker=go.bar.Marker(
# 				                        color='grey'
# 				                    )
# 				                ),
# 				                go.Bar(
# 				                    x= non_performing_by_sector.index, 
# 				                    y= non_performing_by_sector,
# 				                    text = get_percentage_label(((non_performing_by_sector/(performing_by_sector + non_performing_by_sector))[non_performing_by_sector.index].fillna(1)*100).round(2)),
# 				                    name='Non Performing',
# 				                    textposition='auto',
# 				                    customdata= non_performing_by_sector_balance,
# 						            hovertemplate= format_hover_template(x_label= "Sector" , x_unit=""),
# 				                    marker=go.bar.Marker(
# 				                        color='darkred'
# 				                    )
# 				                ),
# 				            ],
# 				            layout=go.Layout(
# 				                # showlegend=True,
# 				                legend=go.layout.Legend(
# 				                    x=1.0,
# 				                    y=1.0
# 				                ),
# 				                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
# 							    title=go.layout.Title(
# 									text="Loans Performance based per industry Sector",
# 								),
# 								xaxis=go.layout.XAxis(
# 									tickangle=55,
# 									title=go.layout.xaxis.Title(
# 										text="Sectors",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								),
# 								yaxis=go.layout.YAxis(
# 									title=go.layout.yaxis.Title(
# 										text="Number of Loans",
# 										# font=dict(
# 										#     family="Courier New, monospace",
# 										#     size=18,
# 										#     color="#7f7f7f"
# 										# )
# 									)
# 								)
# 				            )
# 				        ),
# 				        id="loan-trend-graph-4",
# 				        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Loans Performance based per industry Sector")}),
# 				        style = {"height":750}
# 				    ),
# 				]),
# 			]),
# 		])

# 		output =  [
# 			html.Div([
# 				html.H2("{}".format(loan_selected or loan_group), ),
# 				html.Hr(),
# 			]),
# 			dbc.CardDeck(
# 				[
#                     dbc.Card(
#                         [
#                             html.H6("New disbursed Loans from: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                            
#                             html.H3("{:,.0f}".format(loan_opening[-1]), style={"color":"green"}), 
# #                             html.H6("New Customers from: {}".format(customer_opening.index[-1].strftime("%b %d (%a), %Y"))),                            
# #                             html.H3("+ {:,.0f}".format(customer_opening[-1]), style={"color":"green"}),                     
#                         ],
#                         body=True,
#                         style={"align":"center", "justify":"center",}
#                     ),    
#                     dbc.Card(
# 		                [
# 		                    html.H6("Total Number of ongoing Loans"),                            
# 		                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()), style={"color":"#45b6fe"} ),
# 		                    html.H6("Total Number of Customers"),
# 		                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),
# 		                ],
# 		                body=True,
# 		            ),
# 		            dbc.Card(
# 		                [
# 		                    html.H6("Total Approved Amount in million"),                            
# 		                    html.H2("rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()/1e6), style={"color":"darkred"}),
# 		                    html.H6("Total loan Outstanding Amount in million"),                            
# 		                    html.H2("rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()/1e6), style={"color":"DarkRed"}),
# 		                ],
# 		                body=True,
# 		            ),
# 		            dbc.Card(
# 		                [
# 		                    html.H6("Total Net Income in million"),                            
# 		                    html.H2("rwf {:,.0f}".format(loans_data.NET_INCOME_LCY.sum()/1e6), style={"color":"blue"}),
# 		                    html.H6("Total Fee Income in million"),                     
# 		                    html.H2("rwf {:,.0f}".format(loans_data.CHARGES_RECEIVED_LCY.sum()/1e6), style={"color":"blue"}),
# 		                ],
# 		                body=True,
# 		            ),
# 				],	
# 			),
# # 		dbc.CardDeck(
# # 			[
# # 	            dbc.Card(
# # 	                [
# # 	                    html.H6("New Loans from: {}".format(loan_opening.index[-1].strftime("%b %d (%a), %Y"))),                        
# # 	                    html.H3(" {:,.0f}".format(loan_opening[-1]), style={"color":"green"}),
# # # 	                    html.H6("New Loan Customers from: {}".format(cust_opening.index[-1].strftime("%b %d (%a), %Y"))),                   
# # # 	                    html.H3("+ {:,.0f}".format(cust_opening[-1]), style={"color":"green"}),                     
# # 	                ],
# # 	                body=True,
# # 	                style={"align":"center", "justify":"center",}
# # 	            ),
# # 	            dbc.Card(
# # 	                [
# # 	                    html.H6("Total Number of ongoing Loans"),                        
# # 	                    html.H2("{:,.0f}".format(loans_data.CONTRACT_ID.nunique()),style={"color":"#45b6fe"}),
# # 	                    html.H6("Total Number of Borrowers"),                         
# # 	                    html.H2("{:,.0f}".format(loans_data.CUSTOMER_ID.nunique()), style={"color":"#45b6fe"}),
# # 	                ],
# # 	                body=True,
# # 	            ),
# # 	            dbc.Card(
# # 	                [
# # 	                    html.H6("Total Approved Amount in Million "),                         
# # 	                    html.H2("rwf {:,.0f}".format(loans_data.APPROVED_AMOUNT_LCY.sum()/1e6), style={"color":"darkred"}),
# # 	                    html.H6("Total loan Outstanding Amount in Million"),                    
# # 	                    html.H2("rwf {:,.0f}".format(loans_data.OUTSTANDING_PRINCIPAL_LCY.sum()/1e6), style={"color":"DarkRed"}),
# # 	                ],
# # 	                body=True,
# # 	            ),
# # 	            dbc.Card(
# # 	                [
# # 	                    html.H6("Total Net Income in Million"),                         
# # 	                    html.H2("rwf {:,.0f}".format(loans_data.NET_INCOME_LCY.sum()/1e6), style={"color":"#000080"}),  
# # 	                    html.H6("Total Fee Income in Million "),                        
# # 	                    html.H2("rwf {:,.0f}".format(loans_data.CHARGES_RECEIVED_LCY.sum()/1e6), style={"color":"#000080"}),
# # 	                ],
# # 	                body=True,
# # 	            ),
# # 			],	
# #         ),            
# 			#################################################################################
# 			html.Div([
# 				dbc.CardGroup(
# 					[
# 			            dbc.Card(
# 			                [
# 			      				html.Div([
# 								    dcc.Graph(
# 									    figure=go.Figure(
# 									        data=[
# 									            go.Pie(
# 									            	labels=number_pl_npl.index, 
# 									            	values=number_pl_npl,
# 									            	text = format_big_number(number_pl_npl),
# 									            	hoverinfo= "label+percent+text",
#                                                     hole=0.5,
# 									            	marker=go.pie.Marker(
# 									            		colors= colors_pl_npl, 
# 									            		# line=dict(color='#000000', width=1),
# 								            		),	
# 								            		# hoverinfo='label+value',
# 									            ),
# 									        ],
# 									        layout=go.Layout(
# 									            title="Rate of Loan Performance",
# 									            showlegend=True,
# 									            legend=go.layout.Legend(
# 									                x=1.0,
# 									                y=1.0
# 									            ),
# 									            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
# 											),
# 									    ),
# 									    style={'height': 300, "top":30},
# 									    id="loan-pie-cart-1.1.1",
# 									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Rate of Loan Performance")}),
# 									)
# 			                    ]),
# 			                ],
# 			                body=True,
# 			                style={"padding":"5px 5px 5px 5px", },
# 			            ),
# 			            dbc.Card(
# 			                [
# 			                    html.Div([
# 								        dcc.Graph(
# 									    figure=go.Figure(
# 									        data=[
# 									            go.Pie(
# 									            	labels=total_amt_pl_non_pl.index, 
# 									            	values=total_amt_pl_non_pl,
# 									            	text = format_big_number(total_amt_pl_non_pl),
#                                                     hole=0.5,
# 									            	hoverinfo= "label+percent+text",
# 									            	marker=go.pie.Marker(
# 									            		colors= colors_pl_npl,
# 									            		line=dict(color='#000000', width=1),
# 								            		),						            		
# 									            ),
# 									        ],
# 									        layout=go.Layout(
# 									            title="Rate of Loan Performance Based on Outstanding Amount",
# 									            # showlegend=True,
# 									            legend=go.layout.Legend(
# 									                x=1.0,
# 									                y=1.0
# 									            ),
# 									            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
									            							            				                    	
# 									        )
# 									    ),
# 									    style={'height': 300, "top":30},
# 									    id="loan-pie-cart0.1",
# 									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Rate of Loan Performance Based on Outstanding Amount")}),
# 									)
# 			                    ]),
# 			                ],
# 			                body=True,
# 			            ),  
# 					],
# 				),
# 				##########################################
# # 				dbc.CardGroup(
# # 					[
# # 			            dbc.Card(
# # 			                [
# # 			      				html.Div([
# # 								    dcc.Graph(
# # 									    figure=go.Figure(
# # 									        data=[
# # 									            go.Pie(
# # 									            	labels=customer_sbu.rename(index=SBU_MAPPING).index, 
# # 									            	values=customer_sbu,
# #                                                     hole=0.5,
# # 									            	marker=go.pie.Marker(
# # 									            		colors=colors_sbu, 
# # 									            		# line=dict(color='#000000', width=1),
# # 								            		),	
# # 								            		# hoverinfo='label+value',
# # 									            ),
# # 									        ],
# # 									        layout=go.Layout(
# # 									            title="Borrowers per Strategy Business Unit (SBU)",
# # 									            showlegend=True,
# # 									            legend=go.layout.Legend(
# # 									                x=1.0,
# # 									                y=1.0
# # 									            ),
# # 									            margin=go.layout.Margin(l=5, r=5, t=70, b=5),
# # 											),
# # 									    ),
# # 									    style={'height': 300, "top":30},
# # 									    id="loan-pie-cart-1",
# # 									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Customer per Strategy Business Unit (SBU)")}),
# # 									)
# # 			                    ]),
# # 			                ],
# # 			                body=True,
# # 			                style={"padding":"5px 5px 5px 5px", },
# # 			            ),
# # 			            dbc.Card(
# # 			                [
# # 			                    html.Div([
# # 								        dcc.Graph(
# # 									    figure=go.Figure(
# # 									        data=[
# # 									            go.Pie(
# # 									            	labels=customer_gender.rename(index=GENDER_MAPPING).index, 
# # 									            	values=customer_gender,
# #                                                     hole=0.5,
# # 									            	marker=go.pie.Marker(
# # 									            		colors=colors_gender, 
# # 									            		# line=dict(color='#000000', width=1),
# # 								            		),						            		
# # 									            ),
# # 									        ],
# # 									        layout=go.Layout(
# # 									            title="Retail borrower's Gender",
# # 									            # showlegend=True,
# # 									            legend=go.layout.Legend(
# # 									                x=1.0,
# # 									                y=1.0
# # 									            ),
# # 									            margin=go.layout.Margin(l=5, r=5, t=50, b=5),
									            							            				                    	
# # 									        )
# # 									    ),
# # 									    style={'height': 300, "top":30},
# # 									    id="loan-pie-cart",
# # 									    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Retail borrower's Gender")}),
# # 									)
# # 			                    ]),
# # 			                ],
# # 			                body=True,
# # 			            ),  
# # 					],
# # 				),
#                 dbc.CardGroup([
#                     dbc.Card([
#                         dcc.Graph(
#                             figure=go.Figure(
#                                 data=[
#         # 			                go.Scatter(
#         # 			                    x= customer_opening.index, 
#         # 			                    y= customer_opening.values,
#         # 			                    name='Customers',
#         # 			                    mode= "lines",
#         # 			                    marker=go.scatter.Marker(
#         # 			                        color='#000080'
#         # 			                    )
#         # 			                ),
#                                     go.Scatter(
#                                         x= loan_opening.index, 
#                                         y= loan_opening.values,
#                                         name='Loans',
#                                         mode= "lines",
#                                         fill='tozeroy',
#                                         marker=go.scatter.Marker(
#                                             color='#494c53'
#                                         )
#                                     ),
#                                 ],
#                                 layout=go.Layout(
#                                     showlegend=True,
#                                     xaxis_rangeslider_visible= True,
#                                     legend=go.layout.Legend(
#                                         x=0,
#                                         y=1.0
#                                     ),
#                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

#                                     title=go.layout.Title(
#                                         text="Loan disbursed Over Time",
# #                                         x=0,
# #                                         y=1
#                                     ),
#                                     xaxis=go.layout.XAxis(
#                                         rangeselector=dict(
#                                             buttons=list([
#                                                 dict(count=1,
#                                                      label="1MONTH",
#                                                      step="month",
#                                                      stepmode="backward"),
#                                                 dict(count=3,
#                                                      label="3MONTHS",
#                                                      step="month",
#                                                      stepmode="backward"),                                                    
#                                                 dict(count=6,
#                                                      label="6MONTHS",
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
#                                         ),                                                                         
#         #                                             ),                                                        
#         #                                             title=go.layout.xaxis.Title(
#         #                                                 text="Years",
#         #                                                 # font=dict(
#         #                                                 #     family="Courier New, monospace",
#         #                                                 #     size=18,
#         #                                                 #     color="#7f7f7f"
#         #                                                 # )
#         #                                             )
#                                     )
#         #                                         yaxis=go.layout.YAxis(
#         #                                             title=go.layout.yaxis.Title(
#         #                                                 text="Number of Customers",
#         #                                                 # font=dict(
#         #                                                 #     family="Courier New, monospace",
#         #                                                 #     size=18,
#         #                                                 #     color="#7f7f7f"
#         # #                                                 # )
#         # #                                             )
#         #                                         )
#                                 )
#                             ),
#         #                     body=True,
#         #                     style={"padding":"5px 5px 5px 5px", },
#         # 			        id="loan-trend-graph-1",
#         # 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
#         # 			    ),
#                     ],style={'padding': 10}),
#                     dbc.Card([
#                         dcc.Graph(
#                             figure=go.Figure(
#                                 data=[
#         # 			                go.Scatter(
#         # 			                    x= customer_opening.index, 
#         # 			                    y= customer_opening.values,
#         # 			                    name='Customers',
#         # 			                    mode= "lines",
#         # 			                    marker=go.scatter.Marker(
#         # 			                        color='#000080'
#         # 			                    )
#         # 			                ),
#                                     go.Scatter(
#                                         x= loan_opening.index, 
#                                         y= np.cumsum(loan_opening.values),
#                                         name='Loans',
#                                         mode= "lines",
#                                         fill='tozeroy',
#                                         marker=go.scatter.Marker(
#                                             color='#494c53'
#                                         )
#                                     ),
#                                 ],
#                                 layout=go.Layout(
#                                     showlegend=True,
#                                     xaxis_rangeslider_visible= True,
#                                     legend=go.layout.Legend(
#                                         x=0,
#                                         y=1.0
#                                     ),
#                                     margin=go.layout.Margin(l=10, r=10, t=30, b=10),

#                                     title=go.layout.Title(
#                                         text="Loan disbursed Over Time",
# #                                         x=0,
# #                                         y=1
#                                     ),
#         #                             xaxis=go.layout.XAxis(
#         #                                 rangeselector=dict(
#         #                                     buttons=list([
#         #                                         dict(count=1,
#         #                                              label="1MONTH",
#         #                                              step="month",
#         #                                              stepmode="backward"),
#         #                                         dict(count=3,
#         #                                              label="3MONTHS",
#         #                                              step="month",
#         #                                              stepmode="backward"),                                                    
#         #                                         dict(count=6,
#         #                                              label="6MONTHS",
#         #                                              step="month",
#         #                                              stepmode="backward"),
#         #                                         dict(count=1,
#         #                                              label="1YEAR",
#         #                                              step="year",
#         #                                              stepmode="backward"),
#         #                                         dict(step="all")
#         #                                     ])
#         #                                 ),
#         #                                 rangeslider=dict(
#         #                                     visible=True
#         #                                 ),
#         #                                 type="date"
#         #                                 ),                                                                         
#         #                                             ),                                                        
#         #                                             title=go.layout.xaxis.Title(
#         #                                                 text="Years",
#         #                                                 # font=dict(
#         #                                                 #     family="Courier New, monospace",
#         #                                                 #     size=18,
#         #                                                 #     color="#7f7f7f"
#         #                                                 # )
#         #                                             )
#                                     )
#         #                                         yaxis=go.layout.YAxis(
#         #                                             title=go.layout.yaxis.Title(
#         #                                                 text="Number of Customers",
#         #                                                 # font=dict(
#         #                                                 #     family="Courier New, monospace",
#         #                                                 #     size=18,
#         #                                                 #     color="#7f7f7f"
#         # #                                                 # )
#         # #                                             )
#         #                                         )
#                                 )
#                             ),
#         #                     body=True,
#         #                     style={"padding":"5px 5px 5px 5px", },
#         # 			        id="loan-trend-graph-1",
#         # 			        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Cumulative Number of Customers/Accounts Over Time" )}),
#         # 			    ),
#                     ],style={'padding': 10}),
                    
#                 ]),
                
# 			]),
# 			####################################################################################
# 			# html.Div([]),
# 		    #############################################################################
# 		    html.Div([
# 			    dbc.CardGroup([
# 					dbc.Card([
# 					    dcc.Graph(
# 					        figure=go.Figure(
# 					            data=[
# 					                go.Bar(
# 					                    x= segment_perf.rename(index=SEGMENTS_MAPPING).index, 
# 					                    y= segment_perf,
# 					                    text = get_percentage_label((segment_perf/(segment_perf + segment_nonperf)*100)[segment_perf.index].fillna(100).round(2)),
# 					                    name='Performing',
# 					                    textposition='auto',
# # 					                    customdata= segment_perf_balance,
# # 					                	hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# 					                    marker=go.bar.Marker(
# 					                        color='grey'
# 					                    )
# 					                ),
# 					                go.Bar(
# 					                    x= segment_nonperf.rename(index=SEGMENTS_MAPPING).index, 
# 					                    y= segment_nonperf,
# 					                    text = get_percentage_label((segment_nonperf/(segment_perf + segment_nonperf)*100)[segment_nonperf.index].fillna(100).round(2)),
# 					                    name='Non Performing',
# 					                    textposition='auto',
# # 					                    customdata= segment_nonperf_balance,
# # 					                	hovertemplate= format_hover_template(x_label= "Segment", y_label= "# of Accounts"),
# 					                    marker=go.bar.Marker(
# 					                        color='darkred'
# 					                    )
# 					                ),
# 					            ],
# 					            layout=go.Layout(
# 					                legend=go.layout.Legend(
# 					                    x=0.5,
# 					                    y=1.0
# 					                ),
# 					                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
					             
# 								    title=go.layout.Title(
# 										text="Loans performance based on customer's category",
# 									),
# 									xaxis=go.layout.XAxis(
# 										title=go.layout.xaxis.Title(
# 											text="Category",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									),
# 									yaxis=go.layout.YAxis(
# 										title=go.layout.yaxis.Title(
# 											text="Number of Loans",
# 											# font=dict(
# 											#     family="Courier New, monospace",
# 											#     size=18,
# 											#     color="#7f7f7f"
# 											# )
# 										)
# 									)
# 					            )

# 					        ),
# 					        id="loan-trend-graph-3.1",
# 					        config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Loans performance based on customer's category")}),
# 					    ),
# 					]),
# 					dbc.Card(
# 			            [
# 			                html.Div([
# 							        dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Pie(
# 								            	labels=loans_interest_rate.index, 
# 								            	values=loans_interest_rate,
#                                                 hole=0.5,
# 								            	marker=go.pie.Marker(
# 								            		colors=colors_interest, 
# 								            		# line=dict(color='#000000', width=1),
# 							            		),						            		
# 								            ),
# 								        ],
# 								        layout=go.Layout(
# 								            title="Loan Interest Rate Segmentation",
# 								            showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=1.0,
# 								                y=1.0
# 								            ),
# 								            margin=go.layout.Margin(l=25, r=25, t=50, b=25),
								            							            				                    	
# 								        )
# 								    ),
# 								    # style={'height': 300, "top":30},
# 								    id="loan-pie-cart-3",
# 								    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Loan Interest Rate Segmentation")}),
# 								)
# 			                ]),
# 			            ],
# 			            body=True,
# 			        ),	
# 			    ]),
# 			]),
# 			#########################################################################
# 			html.Div([
# 				html.H2("{}".format(loan_selected or loan_group), ),
# 				# html.Hr(),
# 			]),
# 		    ##########################################################################
# 		    age_output,
# 		    ##########################################################################
# 		    account_officer_output,
# 		    ###########################################################################
# 		    html.Div([
# 				html.H2("{}".format(loan_selected or loan_group), ),
# 				# html.Hr(),
# 			]),
# 			###########################################################################
# 		    segmentation_over_time_output,
# 			##########################################################################
# 			segmentation_by_sector_output,
# 		]
# 		return output

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
	# [State("select-loanType", "value"),]
)
def update_od_info_about_select_loan(n, od_group, options, loan_type):

	loan_type_options = [d['value'] for d in options]

	data = get_overdraft_dataset(session_id)

	if od_group == "ALL"  and loan_type is None:
		od_data = get_od_dataframe_for_values_selected(session_id, data, od_group, loan_type)
		return get_od_overview_info(od_data, od_group, loan_type)

	else:
		if loan_type not in loan_type_options:
			loan_type = None

		# output = html.Div([
		# 	html.H3("{} selected in the Group: {}".format(loan_type, loans_group))
		# ])

		od_data = get_loan_dataframe_for_values_selected(session_id, data, od_group, loan_type)
		output = get_selected_loan_info(od_data, od_group, loan_type)

		return output
