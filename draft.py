
hovertemplate ="Age Range: %{x:.0%}<br>"+
	"# Accounts: %{y:,.0f}<br>"+
	"Rate: %{text}<br>"+
	"<extra>Balance: {fullData.name:,.0f} RWF</extra>"
      
def format_hover_template(x_label= "Age Range", y_label= "# Accounts", text_label= "Rate", extra_label, extras_values="fullData.name"):
    
    template = x_label+": %{x:.0%}<br>"+\
        y_label+": %{y:,.0f}<br>"+\
        "Rate: %{text}<br>"+\
        "<extra>Balance: {"+extras_values+":,.0f} RWF</extra>"
    return template


# html.Div([
  	# dcc.Graph(
	#     figure=go.Figure(
	#         data=[
	#             go.Scatter(
	#                 x= list(X), 
	#                 y= list(Y),
	#                 name='line plot',
	#                 mode= "lines+markers",
	#                 marker=go.scatter.Marker(
	#                     color='rgb(55, 83, 109)'
	#                 )
	#             ),
	#         ],
	#         layout=go.Layout(
	#             title="Line plot",
	#             showlegend=False,
	#             legend=go.layout.Legend(
	#                 x=0,
	#                 y=1.0
	#             ),
	#             margin=go.layout.Margin(l=5, r=5, t=30, b=5)
	#         )
	#     ),
	#     style={'height': 300, "top":30},
	#     id="graph1"
	# )
#               ]),



####################################################################################

 # dbc.Card(
      #           [
      #               html.Div([
      #               	dcc.Graph(
						#     figure=go.Figure(
						#         data=[
						#             go.Bar(
						#                 x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
						#                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
						#                 y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
						#                    350, 430, 474, 526, 488, 537, 500, 439],
						#                 name='Rest of world',
						#                 marker=go.bar.Marker(
						#                     color='rgb(55, 83, 109)'
						#                 )
						#             ),
						#             go.Bar(
						#                 x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
						#                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
						#                 y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
						#                    299, 340, 403, 549, 499],
						#                 name='China',
						#                 marker=go.bar.Marker(
						#                     color='rgb(26, 118, 255)'
						#                 )
						#             )
						#         ],
						#         layout=go.Layout(
						#             title='US Export of Plastic Scrap',
						#             showlegend=True,
						#             legend=go.layout.Legend(
						#                 x=0,
						#                 y=1.0
						#             ),
						#             margin=go.layout.Margin(l=40, r=0, t=40, b=30)
						#         )
						#     ),
						#     style={'height': 300},
						#     id='graph3'
						# )

      #               	], 
      #               	id=""),
      #           ],
      #           body=True,
      #           style={"padding":"5px 5px 5px 5px", },
      #       ),		


#########################################################################################################
# 'staticPlot', 'plotlyServerURL', 'editable', 'edits', 'autosizable', 'responsive', 'queueLength', 'fillFrame', 'frameMargins', 'scrollZoom', 
# 'doubleClick', 'doubleClickDelay', 'showTips', 'showAxisDragHandles', 'showAxisRangeEntryBoxes', 'showLink', 'sendData', 'linkText', 'displayModeBar', 
# 'showSendToCloud', 'showEditInChartStudio', 'modeBarButtonsToRemove', 'modeBarButtonsToAdd', 'modeBarButtons', 'toImageButtonOptions', 'displaylogo', 
# 'watermark', 'plotGlPixelRatio', 'topojsonURL', 'mapboxAccessToken', 'locale', 'locales'


####################################################################################
dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x= customer_opening.index, 
                        y= np.cumsum(customer_opening.values),
                        name='Customers Opening',
                        mode= "lines",
                        marker=go.scatter.Marker(
                            color='blue'
                        )
                    ),
                    go.Scatter(
                        x= account_opening.index, 
                        y= np.cumsum(account_opening.values),
                        name='Accounts Opening',
                        mode= "lines",
                        marker=go.scatter.Marker(
                            color='green'
                        )
                    ),
                ],
                layout=go.Layout(
                    title="Customers/Accounts Opening Trend",
                    showlegend=True,
                    legend=go.layout.Legend(
                        x=0,
                        y=1.0
                    ),
                    margin=go.layout.Margin(l=10, r=10, t=30, b=10),
                    xaxis = go.layout.XAxis(
                    	# tick0=start_date,
                    	nticks=24,
                    	tickmode= "auto",
				        # tickformatstops = [				          
				        #     go.layout.xaxis.Tickformatstop(
				        #         dtickrange=[None, "M12"],
				        #         value="%b-%Y"
				        #     ),
				        #     go.layout.xaxis.Tickformatstop(
				        #         dtickrange=["M12", "M48"],
				        #         value="%q Q %Y"
				        #       ),
				        #     go.layout.xaxis.Tickformatstop(
				        #         dtickrange=["M48", None],
				        #         value="%Y"
				        #     ),
				        # ]
				    ),
                )
            ),
#             style={'height': 300, "top":30},
            id="trend-graph-2",
            config=LINE_PLOT_CONFIG,
        ),

####################################################################################
 #   dbc.Row([
			# dbc.Col([
    	# dcc.DatePickerRange(
	    #     id='my-date-picker-range',
	    #     min_date_allowed=customer_opening.index.min(),
	    #     max_date_allowed=customer_opening.index.max() +timedelta(days=1),
	    #     initial_visible_month=customer_opening.index.max(),
	    #     start_date=customer_opening.index.min(),
	    #     end_date =customer_opening.index.max(),
	    #     start_date_placeholder_text="Start date",
	    #     end_date_placeholder_text="End date",
	    #     first_day_of_week=1,
	    #     number_of_months_shown=2,
	    #     minimum_nights=3,
	    #     display_format="DD-MM-YYYY",
	    #     # show_outside_days=True,
	    #     # style={"margin":"0px 0px 10px 0px"},
    	# ),
	    	# ]),
	    	# dbc.Col([
    	# dbc.Button("Reset",id="reset-new_opening_trend_line", className="float-right", 
     #        style={
     #            "color": "white",
     #            "text-align": "center",
     #            "display": "inline-block",
     #            "opacity": 0.8,
     #        }
    	# ), 
	    #     ]),
	    # ]),    



	    ################################################################################

dash_page_layout_more = html.Div([

	html.Div([
		dash_common_layout,
		html.Hr(),
		html.Div([
			html.Div(id="overview_tables"),
			dcc.Interval(id="update-overview_tables", interval=1000*60*60*3, n_intervals=0),
		]),
		html.H2("Loan Overview", style={"color":"DarkRed", "margin":"25px 0 0 0"}),
		html.Hr(),
		html.Div([
			html.Div(id="loan_overview"),
			dcc.Interval(id="update-loan_overview", interval=1000*60*60*24, n_intervals=0),
		]),
		html.H2("Channel Overview", style={"color":"DarkRed", "margin":"25px 0 0 0"}),
		html.Hr(),
		html.Div([
			html.Div(id="channel_overview"),
			dcc.Interval(id="update-channel_overview", interval=1000*60*60*3, n_intervals=0),
		]),
		html.H2("Cards Overview", style={"color":"DarkRed", "margin":"25px 0 0 0"}),
		html.Hr(),
		html.Div([
			html.Div(id="cards_overview"),
			dcc.Interval(id="update-cards_overview", interval=1000*60*60*3, n_intervals=0),
		]),
	],)
])

######################################
def get_customer_channel_choice():
	chunksize = 2000000

	func = {
	    "TRAN_AMT":["sum"],
	}

	result = get_data_aggregated(func, chunksize)

	#%% Change all TELLER into PBI
	result.TRANSACTION_CHANNEL = np.where(result.TRANSACTION_CHANNEL == "TELLER", "PBI",result.TRANSACTION_CHANNEL)

	df1 = result.pivot_table(values="TRAN_AMT_sum", 
	                index=["CONTRACT_ID","CURRENCY"], columns=["TRANSACTION_CHANNEL"],
	                aggfunc=["count","sum"], fill_value=0, margins=False, 
	                dropna=False, margins_name='All')

	df1.columns = ['_'.join(col).strip() for col in df1.columns.values]

	df1.reset_index(["CONTRACT_ID","CURRENCY"], inplace=True)

	#%%
	df2 = result.pivot_table(values="TRAN_AMT_sum", index="CONTRACT_ID", 
	                        columns=["CURRENCY"],aggfunc=["count","sum"], 
	                        fill_value=0, margins=False, dropna=False, margins_name='All')

	df2.columns = ['_'.join(col).strip() for col in df2.columns.values]

	## Task: automate both some below
	count_cols = []
	sum_cols = []
	for col in df2.columns.values:
	    if "count" in col:
	        count_cols += [col]
	    elif "sum" in col:
	        sum_cols += [col]
	        
	df2["transaction_no"] = df2[count_cols].sum(axis=1)
	df2["transaction_amt"] = df2[sum_cols].sum(axis=1)

	df2 = df2.drop(df2.columns.values[:-2], axis=1)
	df2.reset_index("CONTRACT_ID", inplace=True)

	#%% Merge both dfs above
	df=df1.merge(df2, on="CONTRACT_ID")
	df.columns=df.columns.str.lower()

	#%%
	forex = get_currency_exchange_rate()[["I&M Bank Mid Rate","Currency"]]
	forex["I&M Bank Mid Rate"] = forex["I&M Bank Mid Rate"].astype(np.float32)

	#%%
	mapping ={"RWF":1}
	for val in forex.Currency.values:
	    if val in df.currency.unique():
	        mapping[val] = (forex[val == forex.Currency.values]["I&M Bank Mid Rate"]).values[0]
	    
	print(mapping)

	## Convert each column of amount to rwf
	for col in df.columns.values:
	    if "sum" in col:
	        df[col] = df.currency.map(mapping)*df[col]

	df['transaction_amt'] = df.currency.map(mapping)*df.transaction_amt
	df.drop("currency", axis=1, inplace=True)

	#%%
	cols_name_map ={}

	for col in df.columns.values:
	    if "count" in col:
	        cols_name_map[col] = col[6:]
	    elif "sum" in col:
	        cols_name_map[col] = col[4:]+"_amt"
	        
	# print(cols_name_map)

	df.rename(columns=cols_name_map, inplace=True) # Rename cols

	#%% Get channels columns index 
	idx = df.columns.values[1:-2]
	# print(idx)

	## Compute the mean amount per transaction by channel
	for col in idx[:9]:
	    df[col+"_mean"] = df[col+"_amt"]/ df[col]
	    df[col+"_mean"].fillna(0, inplace=True)
	    
	## Compute the mean amount per transaction 
	df["mean_transact_amt"] = df.transaction_amt/ df.transaction_no

	#%%
	df["customer_id"] = df.contract_id.astype(str).str[:-3]

	df_grp = df.groupby("customer_id", sort = False)[(df.columns.values[1:-1])].sum()
	df_grp.reset_index("customer_id", inplace=True)

	## Get channels columns index 
	idx = df_grp.columns.values[1:-3]
	# print(idx)

	## Compute the mean amount per transaction per customer by channel
	for col in idx[:8]:
	    df_grp[col+"_mean"] = df_grp[col+"_amt"]/ df_grp[col]
	    df_grp[col+"_mean"].fillna(0, inplace=True)
	    
	## Compute the mean amount per transaction per customer
	df_grp["mean_transact_amt"] = df_grp.transaction_amt/ df_grp.transaction_no

	#%% 
	## Get channels columns index 
	idx = df_grp.columns.values[1:]
	print(idx)

	### Customer preferred Channel in terms of amount spent, #of time chose channel
	##Get the prefered customer's channel in terms of amount spent
	df_grp["prefered_channel_by_amt"] = df_grp[idx[21:-1]].idxmax(axis=1)
	df_grp["prefered_channel_by_amt"] = df_grp["prefered_channel_by_amt"].astype(str).str[:-5]

	##Get the prefered customer's channel in terms #of time chose channel
	df_grp["prefered_channel_by_trans"] = df_grp[idx[:9]].idxmax(axis=1)
	# df_grp["prefered_channel_by_trans"] = df_grp["prefered_channel_by_trans"].astype(str).str[:-5]

	#%% Get the number of channels a customer already used
	df_grp["no_channel_used"] = df_grp[idx[:9]].replace(0, np.nan).count(axis=1).astype(np.uint8)

	return df_grp

#########################################################
@app.callback(
	Output("loan_overview","children"),
	[Input("update-loan_overview", "n_intervals")]
)
def update_loan_overview(n):

	# X.append(X[-1]+1)
	# Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

	# output =  dbc.CardGroup(
	# 	[
 #            dbc.Card(
 #                [
 #                    html.Div([
 #                    	dcc.Graph(
	# 					    figure=go.Figure(
	# 					        data=[
	# 					            go.Bar(
	# 					                x=["1 year", "2 years", "3 years", "5 years", "5+ years"],
	# 					                y=[219, 146, 112, 127, 124],
	# 					                name='Maturity',
	# 					                text=[219, 146, 112, 127, 124],
 #            							textposition='auto',
 #            							base=0,
 #            							width = 0.4,
	# 									offset = -0.4,
	# 					                marker=go.bar.Marker(
	# 					                    color='rgb(55, 83, 109)'
	# 					                )
	# 					            ),
	# 					            go.Bar(
	# 					                x=["1 year", "2 years", "3 years", "5 years", "5+ years"],
	# 					                y=[200, 116, 110, 107, 114],
	# 					                name='Performing',
	# 					                text=[200, 116, 110, 107, 114],
 #            							textposition='auto',
 #            							width = 0.4,
	# 									offset = 0.0,
	# 					                marker=go.bar.Marker(
	# 					                    color='rgb(26, 118, 255)'
	# 					                )
	# 					            ),
	# 					            go.Bar(
	# 					                x=["1 year", "2 years", "3 years", "5 years", "5+ years"],
	# 					                y=[19, 30, 2, 20, 10],
	# 					                name='Non Performing',
	# 					                text=[19, 30, 2, 20, 10],
 #            							textposition='auto',
 #            							width = 0.4,
	# 									offset = 0.0,
	# 					                marker=go.bar.Marker(
	# 					                    color='red'
	# 					                )
	# 					            ),  
	# 					        ],
	# 					        layout=go.Layout(
	# 					            title="Loan Maturity vs Loan Performance",
	# 					            barmode="relative",
	# 					            showlegend=True,
	# 					            legend=go.layout.Legend(
	# 					                x=0.5,
	# 					                y=1.0,
	# 					                xanchor="center",
 #    									yanchor="top",
	# 					            ),
	# 					            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
	# 					        )
	# 					    ),
	# 					    # style={'height': 400,},
	# 					    id='my-graph',
	# 					    config=BAR_PLOT_CONFIG,
	# 					),
 #                    	], 
 #                    	id="loan",
 #                    	# style={'width': 700,},
 #                    ),
 #                ],
 #                body=True,
 #                style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
 #            ),
 #            dbc.Card(
 #                [
 #                    html.Div([
	# 				        dcc.Graph(
	# 					    figure=go.Figure(
	# 					        data=[
	# 					            go.Pie(labels=labels_3, values=values_3),
	# 					        ],
	# 					        layout=go.Layout(
	# 					            title="Loan Type",
	# 					            showlegend=True,
	# 					            # legend=go.layout.Legend(
	# 					            #     x=0,
	# 					            #     y=1.0
	# 					            # ),
	# 					            margin=go.layout.Margin(l=5, r=5, t=30, b=5)
	# 					        )
	# 					    ),
	# 					    # style={'height': 300, "top":30},
	# 					    id="",
	# 					    config={
	# 					        "displaylogo": False,
	# 						},
	# 					)
 #                    ]),
 #                ],
 #                body=True,
 #                # style={"padding":"5px 5px 5px 5px", "margin":"25px 25px 25px 35px",},#"border-left":"1px inset #DCDCDC"},
 #            ),	

	# 	],
	# 	# style={"justify":"center", },
	# )

	# return output
#####################################################################
def get_bnr_current_exchange_rate():
    
    for i in range(32):
        
        query = """
        SELECT YEAR_MONTH, CURRENCY, RATE_{}, DATE_LAST_MODIFIED
        FROM VISIONRW.Currency_Rates_Daily
        WHERE TO_CHAR(DATE_LAST_MODIFIED, 'yyyy-mm-dd') = '{}'
        """.format((date.today()-timedelta(i)).day, str(date.today()-timedelta(i)))

        forex = pd.read_sql(query, con=get_connection())
    
        if forex.shape[0] != 0:
            return forex, i

###################################################################################
# @app.callback(
# 	Output("select-loanType","value"),
# 	[Input("select-loanType", "options")],
# 	# [State("select-loanType", "options")],
# )
# def set_loan_type_value(options):
# 	return options[0]['value']

###############################################################################
# @app.callback(
# 	Output("loan_tables","children"),
# 	[Input("select-loan_group", "value"), Input("select-loanType", "value")]
# )
# def update_loan_tables(n, value):


# 	if value :

# 		title = value+" loan"

# 		output =  html.Div(
# 	    	[
# 		    	html.Div(
# 					[
# 						# html.Col(
# 						html.H2("{}".format(title).title(), style={"margin":"25px 0 0 45px"}),
# 						dash_table.DataTable(
# 						    id="table1",
# 						    columns=[{"name": i, "id": i} for i in df4.columns],
# 						    data=df4.to_dict('records'),
# 						    style_table={
# 						    	'whiteSpace': 'normal',
# 						        # 'maxHeight': '300px',
# 						        'maxWidth': '1250px',
# 						        # 'overflowY': 'scroll',
# 						        # 'overflowX': 'scroll',
# 						        'overflow': 'scroll',
# 						        'border': 'thin lightgrey solid',
# 						    },					  
# 						),
# 					],
# 				),
# 			],
# 		),
	
# 		return output

# 	return html.H3("Nothing is selected")

# #################################################################################################
# @app.callback(
# 	Output("loan_graph","children"),
# 	[Input("update-loan_graph", "n_intervals"), Input("select-loanType", "value")]
# )
# def update_loan_graph(n, value):
	
# 	if value :

# 		title = value+" loan"

# 		output =  html.Div([
# 			dbc.CardGroup(
# 				[
# 		            dbc.Card(
# 		                [
# 		                    html.Div([
# 		                    	dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Bar(
# 								                x=["1 year", "2 years", "3 years", "5 years", "5+ years"],
# 								                y=[219, 146, 112, 127, 124],
# 								                name='Maturity',
# 								                text=[219, 146, 112, 127, 124],
# 		            							textposition='auto',
# 								                marker=go.bar.Marker(
# 								                    color='rgb(55, 83, 109)'
# 								                )
# 								            ),
# 								            go.Bar(
# 								                x=["1 year", "2 years", "3 years", "5 years", "5+ years"],
# 								                y=[200, 116, 110, 107, 114],
# 								                name='Performing',
# 								                text=[200, 116, 110, 107, 114],
# 		            							textposition='auto',
# 								                marker=go.bar.Marker(
# 								                    color='rgb(26, 118, 255)'
# 								                )
# 								            ),
# 								            go.Bar(
# 								                x=["1 year", "2 years", "3 years", "5 years", "5+ years"],
# 								                y=[19, 30, 2, 20, 10],
# 								                name='Non Performing',
# 								                text=[19, 30, 2, 20, 10],
# 		            							textposition='auto',
# 								                marker=go.bar.Marker(
# 								                    color='red'
# 								                )
# 								            ),  
# 								        ],
# 								        layout=go.Layout(
# 								            title="{} Loan Maturity vs {} Loan Performance".format(value,value).title(),
# 								            # base=0,
# 								            # barmode="stack",
# 								            showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=0.5,
# 								                y=1.0,
# 								                xanchor="center",
# 		    									yanchor="top",
# 								            ),
# 								            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
# 								        )
# 								    ),
# 								    # style={'height': 400,},
# 								    id='loan-cart1',
# 								    config=BAR_PLOT_CONFIG,
# 								),
# 		                    	], 
# 		                    	# id="",
# 		                    	# style={'width': 700,},
# 		                    ),
# 		                ],
# 		                body=True,
# 		                style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
# 		            ),
# 		            dbc.Card(
# 		                [
# 		                    html.Div([
# 							        dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Pie(labels=labels_2, values=values_2),
# 								        ],
# 								        layout=go.Layout(
# 								            title="SBU for {} Loan ".format(value).title(),
# 								            showlegend=True,
# 								            # legend=go.layout.Legend(
# 								            #     x=0,
# 								            #     y=1.0
# 								            # ),
# 								            margin=go.layout.Margin(l=5, r=5, t=30, b=5)
# 								        )
# 								    ),
# 								    # style={'height': 300, "top":30},
# 								    id="",
# 								    config={
# 								        "displaylogo": False,
# 									},
# 								)
# 		                    ]),
# 		                ],
# 		                body=True,
# 		                # style={"padding":"5px 5px 5px 5px", "margin":"25px 25px 25px 35px",},#"border-left":"1px inset #DCDCDC"},
# 		            ),		
# 				],
# 				# style={"justify":"center", },
# 			),
# 			dbc.CardGroup(
# 				[
# 		            dbc.Card(
# 		                [
# 		      				html.Div([
# 							        dcc.Graph(
# 								    figure=go.Figure(
# 								        data=[
# 								            go.Pie(labels=labels_4, values=values_4),
# 								        ],
# 								        layout=go.Layout(
# 								            title="Customer's Age segments",
# 								            showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=0,
# 								                y=1.0
# 								            ),
# 								            margin=go.layout.Margin(l=5, r=5, t=30, b=5)
# 								        ),
								        
# 									    # displaylogo=False,
# 								    ),
# 								    style={'height': 300, "top":30},
# 								    id="pie-cart1",
# 								    config={
# 								        "displaylogo": False,
# 									},
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
# 								            go.Pie(labels=labels, values=values),
# 								        ],
# 								        layout=go.Layout(
# 								            title="Customer's Gender",
# 								            showlegend=True,
# 								            legend=go.layout.Legend(
# 								                x=0,
# 								                y=1.0
# 								            ),
# 								            margin=go.layout.Margin(l=5, r=5, t=30, b=5)
# 								        )
# 								    ),
# 								    style={'height': 300, "top":30},
# 								    id="pie-cart2",
# 								    config={
# 								        "displaylogo": False,
# 									},
# 								)
# 		                    ]),
# 		                ],
# 		                body=True,
# 		            ),
# 				],
# 				# style={"height":"400px", },
# 			),
# 		])

# 		return output
# 	return html.Div()

#############################################################
# dbc.CardGroup([
			# dbc.Card([
			#     dcc.Graph(
			#         figure=go.Figure(
			#             data=[
			#                 go.Bar(
			#                     x= performing_by_sector.index, 
			#                     y= performing_by_sector,
			#                     text = get_percentage_label((performing_by_sector/(performing_by_sector + non_performing_by_sector)).fillna(0.0).round(2)),
			#                     name='Performing',
			#                     textposition='auto',
			#                     # mode = "lines+markers",
			#                     marker=go.bar.Marker(
			#                         color='green'
			#                     )
			#                 ),
			#                 go.Bar(
			#                     x= non_performing_by_sector.index, 
			#                     y= non_performing_by_sector,
			#                     text = get_percentage_label((non_performing_by_sector/(performing_by_sector + non_performing_by_sector)).fillna(0.0).round(2)),
			#                     name='Non Performing',
			#                     textposition='auto',
			#                     # mode = "lines+markers",
			#                     marker=go.bar.Marker(
			#                         color='red'
			#                     )
			#                 ),
			              
			#             ],
			#             layout=go.Layout(
			#                 # showlegend=True,
			#                 # xaxis_rangeslider_visible= True,
			#                 legend=go.layout.Legend(
			#                     x=0,
			#                     y=1.0
			#                 ),
			#                 margin=go.layout.Margin(l=10, r=10, t=30, b=10),
			             
			# 			    title=go.layout.Title(
			# 					text="Number of (Non) Performing Loan per Sector",
			# 				# 	xref="paper",
			# 				# 	x=0
			# 				),
			# 				xaxis=go.layout.XAxis(
			# 					title=go.layout.xaxis.Title(
			# 						text="Sectors",
			# 						# font=dict(
			# 						#     family="Courier New, monospace",
			# 						#     size=18,
			# 						#     color="#7f7f7f"
			# 						# )
			# 					)
			# 				),
			# 				yaxis=go.layout.YAxis(
			# 					title=go.layout.yaxis.Title(
			# 						text="Number of Loan Accounts",
			# 						# font=dict(
			# 						#     family="Courier New, monospace",
			# 						#     size=18,
			# 						#     color="#7f7f7f"
			# 						# )
			# 					)
			# 				)
			#             )
			#         ),
			#         id="loan-trend-graph-6",
			#         config=BAR_PLOT_CONFIG,
			#         style={"height":"600px"},
			#     ),
			# ]),






########################################################

		 #    dbc.CardGroup([
			# 	dbc.Card([
			# 	    dcc.Graph(
			# 	        figure=go.Figure(
			# 	            data=[
			# 	                go.Bar(
			# 	                    x= segment_perf.rename(index=SEGMENTS_MAPPING).index, 
			# 	                    y= segment_perf,
			# 	                    text = get_percentage_label((segment_perf/(segment_perf + segment_nonperf)*100).fillna(100).round(2)),
			# 	                    name='Performing Segments',
			# 	                    textposition='auto',
			# 	                    marker=go.bar.Marker(
			# 	                        color='green'
			# 	                    )
			# 	                ),
			# 	                go.Bar(
			# 	                    x= segment_nonperf.rename(index=SEGMENTS_MAPPING).index, 
			# 	                    y= segment_nonperf,
			# 	                    text = get_percentage_label((segment_nonperf/(segment_perf + segment_nonperf)*100).dropna().round(2)),
			# 	                    name='Non Performing Segments',
			# 	                    textposition='auto',
			# 	                    marker=go.bar.Marker(
			# 	                        color='red'
			# 	                    )
			# 	                ),
			# 	            ],
			# 	            layout=go.Layout(
			# 	                legend=go.layout.Legend(
			# 	                    x=0.6,
			# 	                    y=1.0
			# 	                ),
			# 	                margin=go.layout.Margin(l=10, r=10, t=30, b=10),
				             
			# 				    title=go.layout.Title(
			# 						text="Number of Loan Accounts per Segments",
			# 					# 	xref="paper",
			# 					# 	x=0
			# 					),
			# 					xaxis=go.layout.XAxis(
			# 						title=go.layout.xaxis.Title(
			# 							text="Segments Type",
			# 							# font=dict(
			# 							#     family="Courier New, monospace",
			# 							#     size=18,
			# 							#     color="#7f7f7f"
			# 							# )
			# 						)
			# 					),
			# 					yaxis=go.layout.YAxis(
			# 						title=go.layout.yaxis.Title(
			# 							text="Number of Loan Accounts",
			# 							# font=dict(
			# 							#     family="Courier New, monospace",
			# 							#     size=18,
			# 							#     color="#7f7f7f"
			# 							# )
			# 						)
			# 					)
			# 	            )

			# 	        ),
			# 	        id="loan-trend-graph-3.1",
			# 	        config=BAR_PLOT_CONFIG,
			# 	    ),
			# 	]),
			# ]),


#######################################################

def get_loans_over_time_and_by_sector(session_id, loans, loan_group, loan_selected):

	loans['REMAINING_TIME']= (loans.MATURITY_DATE.apply(lambda x:(x- dt.now()) // timedelta(days=365.2425/12))).fillna(0).astype(int)
	

	if loan_selected is None:
		if loan_group == "ALL":
			bins = np.arange(0, loans.REMAINING_TIME.max()+4, 3)

			performing = loans[loans.MAIN_CLASSIFICATION_DESC=="PERFORMING ASSETS"]
			retail_performing = performing[performing.VISION_SBU=="R"]
			sme_performing = performing[performing.VISION_SBU=="S"]
			corp_performing = performing[performing.VISION_SBU=="C"]

			non_performing = loans[loans.MAIN_CLASSIFICATION_DESC=="NON PERFORMING ASSETS"]
			retail_non_performing = non_performing[non_performing.VISION_SBU=="R"]
			sme_non_performing = non_performing[non_performing.VISION_SBU=="S"]
			corp_non_performing = non_performing[non_performing.VISION_SBU=="C"]

			### Performing and non performing loan over time
			performing_over_time = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			retail_performing_over_time =retail_performing.groupby(pd.cut(retail_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			sme_performing_over_time =sme_performing.groupby(pd.cut(sme_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			corp_performing_over_time =corp_performing.groupby(pd.cut(corp_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()

			non_performing_over_time =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			retail_non_performing_over_time =retail_non_performing.groupby(pd.cut(retail_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			sme_non_performing_over_time =sme_non_performing.groupby(pd.cut(sme_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			corp_non_performing_over_time =corp_non_performing.groupby(pd.cut(corp_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()

			## Set the index to string index
			performing_over_time.index = performing_over_time.index.astype(str)
			retail_performing_over_time.index = retail_performing_over_time.index.astype(str)
			sme_performing_over_time.index = sme_performing_over_time.index.astype(str)
			corp_performing_over_time.index = corp_performing_over_time.index.astype(str)

			non_performing_over_time.index = non_performing_over_time.index.astype(str)
			retail_non_performing_over_time.index = retail_non_performing_over_time.index.astype(str)
			sme_non_performing_over_time.index = sme_non_performing_over_time.index.astype(str)
			corp_non_performing_over_time.index = corp_non_performing_over_time.index.astype(str)

			### Performing and non performing loan per sector
			performing_by_sector = performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			retail_performing_by_sector = retail_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			sme_performing_by_sector = sme_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			corp_performing_by_sector = corp_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()

			non_performing_by_sector = non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			retail_non_performing_by_sector = retail_non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			sme_non_performing_by_sector = sme_non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			corp_non_performing_by_sector = corp_non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()

			return (
			    performing_over_time, retail_performing_over_time, sme_performing_over_time, corp_performing_over_time,
			    non_performing_over_time, retail_non_performing_over_time, sme_non_performing_over_time, corp_non_performing_over_time,
			    performing_by_sector, retail_performing_by_sector, sme_performing_by_sector, corp_performing_by_sector,
			    non_performing_by_sector, retail_non_performing_by_sector, sme_non_performing_by_sector, corp_non_performing_by_sector
			)

		elif loan_group == "RETAIL" or loan_group == "STAFF":

			performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="PERFORMING ASSETS")&(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, loans, loan_group)))]
			non_performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="NON PERFORMING ASSETS")&(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, loans, loan_group)))]



			### Performing and non performing loan over time
			bins = np.arange(0, performing.REMAINING_TIME.max()+4, 3)
			performing_over_time = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			
			bins = np.arange(0, non_performing.REMAINING_TIME.max()+4, 3)
			non_performing_over_time =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
		

			## Set the index to string index
			performing_over_time.index = performing_over_time.index.astype(str)
			non_performing_over_time.index = non_performing_over_time.index.astype(str)

			### Performing and non performing loan per sector
			performing_by_sector = performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			non_performing_by_sector = non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()

			return (
			    performing_over_time, non_performing_over_time,
			    performing_by_sector, non_performing_by_sector
			)

		elif loan_group == "STAFF":

			performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="PERFORMING ASSETS")&(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, loans, loan_group)))]
			non_performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="NON PERFORMING ASSETS")&(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, loans, loan_group)))]


			### Performing and non performing loan over time
			performing_over_time = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			non_performing_over_time =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
		

			## Set the index to string index
			performing_over_time.index = performing_over_time.index.astype(str)
			non_performing_over_time.index = non_performing_over_time.index.astype(str)

			### Performing and non performing loan per sector
			performing_by_sector = performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			non_performing_by_sector = non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()

			return (
			    performing_over_time, non_performing_over_time,
			    performing_by_sector, non_performing_by_sector
			)

		elif loan_group == "CORPORATE AND SME":

			performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="PERFORMING ASSETS")&(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, loans, loan_group)))]
			# sme_performing = performing[performing.VISION_SBU=="S"]
			# corp_performing = performing[performing.VISION_SBU=="C"]

			non_performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="NON PERFORMING ASSETS")&(loans.SCHEME_DESC.isin(get_loan_type_list(session_id, loans, loan_group)))]
			# sme_non_performing = non_performingg[non_performing.VISION_SBU=="S"]
			# corp_non_performing = non_performin[non_performing.VISION_SBU=="C"]


			### Performing and non performing loan over time
			performing_over_time = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			# sme_performing_over_time =sme_performing.groupby(pd.cut(sme_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			# corp_performing_over_time =corp_performing.groupby(pd.cut(corp_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()

			non_performing_over_time =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			# sme_non_performing_over_time =sme_non_performing.groupby(pd.cut(sme_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
			# corp_non_performing_over_time =corp_non_performing.groupby(pd.cut(corp_non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()

			## Set the index to string index
			performing_over_time.index = performing_over_time.index.astype(str)
			# sme_performing_over_time.index = sme_performing_over_time.index.astype(str)
			# corp_performing_over_time.index = corp_performing_over_time.index.astype(str)

			non_performing_over_time.index = non_performing_over_time.index.astype(str)
			# sme_non_performing_over_time.index = sme_non_performing_over_time.index.astype(str)
			# corp_non_performing_over_time.index = corp_non_performing_over_time.index.astype(str)

			### Performing and non performing loan per sector
			performing_by_sector = performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			# sme_performing_by_sector = sme_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			# corp_performing_by_sector = corp_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()

			non_performing_by_sector = non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			# sme_non_performing_by_sector = sme_non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
			# corp_non_performing_by_sector = corp_non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()

			# return (
			#     performing_over_time, sme_performing_over_time, corp_performing_over_time,
			#     non_performing_over_time, sme_non_performing_over_time, corp_non_performing_over_time,
			#     performing_by_sector, sme_performing_by_sector, corp_performing_by_sector,
			#     non_performing_by_sector, sme_non_performing_by_sector, corp_non_performing_by_sector
			# )
			
			return (
			    performing_over_time, non_performing_over_time,
			    performing_by_sector, non_performing_by_sector
			)
	else:
		performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="PERFORMING ASSETS")&(loans.SCHEME_DESC==loan_selected)]
		non_performing = loans[(loans.MAIN_CLASSIFICATION_DESC=="NON PERFORMING ASSETS")&(loans.SCHEME_DESC==loan_selected)]


		### Performing and non performing loan over time
		performing_over_time = performing.groupby(pd.cut(performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
		non_performing_over_time =non_performing.groupby(pd.cut(non_performing['REMAINING_TIME'], bins, include_lowest=True, right = False, )).CONTRACT_ID.nunique()
	

		## Set the index to string index
		performing_over_time.index = performing_over_time.index.astype(str)
		non_performing_over_time.index = non_performing_over_time.index.astype(str)

		### Performing and non performing loan per sector
		performing_by_sector = performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()
		non_performing_by_sector = non_performing.groupby("SECTOR_CODE_DESC").CONTRACT_ID.nunique()

		return (
		    performing_over_time, non_performing_over_time,
		    performing_by_sector, non_performing_by_sector
		)
