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

from app import cache1, TIMEOUT, app, session_id
from components import *
from config import *
import datetime as dt
import pandas as pd

mtn_common_layout = html.Div(
	[
		# html.Hr(),
		html.Div(id="mtn_overview", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
		html.Div([
			html.Div(id="mtn_info"),
			dcc.Interval(id="update-mtn_overview", interval=1000*60*60*2, n_intervals=0),
		]),
	],
)

layout = html.Div([

    html.H1('PUSH&PULL'),    
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
	mtn_common_layout,
])

#############################################################################################
###################### Layout callback #####################################################
#############################################################################################

@app.callback(
	Output("mtn_info","children"),
	[
		Input("update-mtn_overview", "n_intervals"),
		Input("MOB_CAT", "value"),
	]
)
@cache1.memoize(timeout=TIMEOUT)
def channel_info(n, cust_type):
    start = time.time()    
    (Inactive_Female,Inactive_Male,Active_Female,Active_Male,age_inactive_female_tr,
     age_inactive_male_tr,age_active_female_tr,age_active_male_tr,
     age_inactive_female,age_inactive_male,age_active_female,age_active_male)=get_MTN_USER(session_id,cust_type)
    
    (Bank_to_wallet_num,Bank_to_wallet,Number_pl,Amount_pl,MTN_TIGO_inact,
     MTN_TIGO_act,Customers_reg,MTN_TIGO_cat_inac,MTN_TIGO_cat_act,MTN_TIGO_inact,
     MTN_TIGO_act,MTN_TIGO_cat_act_num,MTN_TIGO_cat_act_am,MTN_TIGO_cat_inac,
     MTN_TIGO_cat_act,MTN_TIGO_trans_cust,customer,
     male_active,female_active,male_inactive,female_inactive)=get_MTN_info(session_id,cust_type)
#     MTN_TIGO=get_MTN_USER(session_id,cust_type)
    end = time.time()     
    print("one", end - start)  
    colors_sbu=['#45b6fe','darkblue','grey']
    colors_gender=['#45b6fe','darkblue']    
#     start = time.time()

#age_inactive_female_tigo,age_active_female_tigo,age_active_female_tigo,
    output= [
		html.Div([]),
        dbc.CardDeck(
			[
	            dbc.Card(
	                [
	                    html.H5("Registered customers"),                           
	                    html.H3("{:,.0f}".format(Customers_reg), style={"color":"DarkBlue"}),
# 	                    html.H6("Total number of registered customers"),
	                    html.H5("Rate of channel users compared with all customers"),                         
	                    html.H3("{:,.1f}%".format(Customers_reg*100/customer), style={"color":"darkblue"}), 
# 	                    html.H6("Rate of channel users compared with all customers"),                    
	                ],
	                body=True,
	                style={"align":"center", "justify":"center",}
	            ),
	            dbc.Card(
	                [
	                    html.H5("Active customers"),                        
	                    html.H3("{:,.0f}".format(MTN_TIGO_act), style={"color":"darkred"}),
	                    html.H5("Rate of active users from all registered"),                         
	                    html.H3("{:,.1f}%".format(MTN_TIGO_act*100/Customers_reg), style={"color":"darkblue"}), 
                        
# 	                    html.H6("Active customers"),
	                    html.H5("Inactive Customers"),                         
	                    html.H3("{:,.0f}".format(MTN_TIGO_inact), style={"color":"darkred"}),
	                    html.H5("Rate of Inactive users from all registered"),                         
	                    html.H3("{:,.1f}%".format(MTN_TIGO_inact*100/Customers_reg), style={"color":"darkblue"}), 
                        
# 	                    html.H6("Inactive Customers"), 
	                ],
	                body=True,
	            ),
	            dbc.Card(
	                [
# 	                    html.H5("Transaction volume"),                         
# 	                    html.H3("rwf {:,.0f}".format(Amount_pl), style={"color":"#45b6fe"}),                        
	                    html.H5("Transaction volume per customer"),                         
	                    html.H3("rwf {:,.0f}".format(Amount_pl/Customers_reg), style={"color":"#45b6fe"}),
# 	                    html.H6("Total transaction volume"),
# 	                    html.H5("#Transactions value"),                        
# 	                    html.H3("{:,.0f}".format(Number_pl), style={"color":"#45b6fe"}),                        
	                    html.H5("#Transactions per customer"),                        
	                    html.H3("{:,.0f}".format(Number_pl/Customers_reg), style={"color":"#45b6fe"}),
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
                                        labels=MTN_TIGO_cat_act.rename(index=SBU_MAPPING).index, 
                                        values=MTN_TIGO_cat_act,
                                        text = MTN_TIGO_cat_act,
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
                            id="customer_cat_pie_mtn",
# 								    config= add_image_file_name_to_config(PIE_PLOT_CONFIG, {"filename": "{}-{}".format(loan_group, "Rate of channel usage based on customer's category")}),
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
                                        labels=MTN_TIGO_cat_inac.rename(index=GENDER_MAPPING).index, 
                                        values=MTN_TIGO_cat_inac,
                                        text =MTN_TIGO_cat_inac,
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
 
# # ######################################################################################################
# # ##########################################customer_trend############################################################
        
    html.Div([
		dbc.CardGroup([
	        dbc.Card([
			    dcc.Graph(
			        figure=go.Figure(
			            data=[
			                go.Scatter(
			                    x= Active_Male.index, 
			                    y= Active_Male,
			                    name='Male Active',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='darkblue'
			                    )
			                ),
			                go.Scatter(
			                    x= Active_Female.index, 
			                    y= Active_Female,
			                    name='Female Active',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='darkred'
			                    )
			                ),
			                go.Scatter(
			                    x= Inactive_Male.index, 
			                    y= Inactive_Male,
			                    name='Male Inactive',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='#45b6fe'
			                    )
			                ),
			                go.Scatter(
			                    x= Inactive_Female.index, 
			                    y= Inactive_Female,
			                    name='Female Inactive',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='#F5D3C7'
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
            dbc.Card(
                [
                    html.Div([
                        dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x=male_active.index,
                                    y=male_active,
                                    name='Male Active',
                                    text=get_percentage_label((male_active*100/(male_active+male_inactive)).round(2)),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),
                                go.Bar(
                                    x=male_inactive.index,
                                    y=male_inactive,
                                    name='Male Inactive',
                                    text=get_percentage_label((male_inactive*100/(male_active+male_inactive)).round(2)),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#45b6fe'
                                    )
                                ),  
                                go.Bar(
                                    x=female_active.index,
                                    y=female_active,
                                    name='Female Active',
                                    text=get_percentage_label((female_active*100/(female_active+female_inactive)).round(2)),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='darkred'
                                    )
                                ),
                                go.Bar(
                                    x=female_inactive.index,
                                    y=female_inactive,
                                    name='Female Inactive',
                                    text=get_percentage_label((female_inactive*100/(female_inactive+female_active)).round(2)),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#F5D3C7'
                                    )
                                ),  

                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text="Active vs Inactive customers",
                                # 	xref="paper",
                                # 	x=0
                                ),
                                xaxis=go.layout.XAxis(
                                    title=go.layout.xaxis.Title(
                                        text="Gender",
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
    
   
# ###################################Age ######################################################################
        
    dbc.CardGroup([
        dbc.Card(
            [
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x=age_active_male.index,
                                y=age_active_male,
                                name='Male Active',
                                text=get_percentage_label((age_active_male*100/(age_active_male+age_inactive_male)).round(2)),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='darkblue'
                                )
                            ),
                            go.Bar(
                                x=age_inactive_male.index,
                                y=age_inactive_male,
                                name='Male Inactive',
                                text=get_percentage_label((age_inactive_male*100/(age_active_male+age_inactive_male)).round(2)),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='#45b6fe'
                                )
                            ),  
                            go.Bar(
                                x=age_active_female.index,
                                y=age_active_female,
                                name='Female Active',
                                text=get_percentage_label((age_active_female*100/(age_active_female+age_inactive_female)).round(2)),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='darkred'
                                )
                            ),
                            go.Bar(
                                x=age_inactive_female.index,
                                y=age_inactive_female,
                                name='Female Inactive',
                                text=get_percentage_label((age_inactive_female*100/(age_inactive_female+age_active_female)).round(2)),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='#F5D3C7'
                                )
                            ),  

                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text="Amount spent on channel based on customer's age",
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
                                x=age_active_male_tr.index,
                                y=age_active_male_tr,
                                name='Male Active',
                                text=get_percentage_label((age_active_male_tr*100/(age_active_male_tr+age_inactive_male_tr)).round(2)),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='darkblue'
                                )
                            ),
                            go.Bar(
                                x=age_inactive_male_tr.index,
                                y=age_inactive_male_tr,
                                name='Male Inactive',
                                text=get_percentage_label((age_inactive_male_tr*100/(age_active_male_tr+age_inactive_male_tr)).round(2)),

                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='#45b6fe'
                                )
                            ),  
                            go.Bar(
                                x=age_active_female_tr.index,
                                y=age_active_female_tr,
                                name='Female Active',
                                text=get_percentage_label((age_active_female_tr*100/(age_active_female_tr+age_inactive_female_tr)).round(2)),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='darkred'
                                )
                            ),
                            go.Bar(
                                x=age_inactive_female_tr.index,
                                y=age_inactive_female_tr,
                                name='Female Inactive',
                                text=get_percentage_label((age_inactive_female_tr*100/(age_inactive_female_tr+age_active_female_tr)).round(2)),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='#F5D3C7'
                                )
                            ),  

                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text="Channel transactions based on customers age",
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
                                x=Bank_to_wallet.rename(index=push_MAPPING).index,
                                y=(Bank_to_wallet/Bank_to_wallet_num).round(),
                                name='Transaction amount',
                                text=(Bank_to_wallet/Bank_to_wallet_num).round(),
# 						                customdata= age_perf_male_balance,
#                                 hovertemplate= format_hover_template(x_label= "Transaction type", y_label= "Amount"),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='#45b6fe'
                                )
                            ), 
                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text="Amount spent per each transaction(rwf)",
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
    html.Div([
        dbc.CardGroup([
            dbc.Card(
            [
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x=Bank_to_wallet.rename(index=push_MAPPING).index,
                                y=(Bank_to_wallet/MTN_TIGO_trans_cust).round(),
                                name='Amount',
                                text=(Bank_to_wallet/MTN_TIGO_trans_cust).round(),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='#45b6fe'
                                )
                            ),        
                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text="Transaction amount per customer(rwf)",
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
                                    text=" Amount per customer",
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
                                x=Bank_to_wallet_num.rename(index=push_MAPPING).index,
                                y=(Bank_to_wallet_num/MTN_TIGO_trans_cust).round(),
                                name='Transactions',
                                text=(Bank_to_wallet_num/MTN_TIGO_trans_cust).round(),
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
                                    text="Transactions",
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

    return output

# #######################################################################################################
# #######################################################################################################
