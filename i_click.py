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
# import datetime as dt
import pandas as pd

# i_click,Mobile_APP,ussd=get_och_data()
min_date_allow= '2018-09-01'
init_start_date= str(dt.today().year)+'-'+str(dt.today().month)+'-01'
init_end_date= str(dt.today().year)+'-'+str(dt.today().month)+'-'+str(dt.today().day)    

iclick_common_layout = html.Div(
	[
		# html.Hr(),
		html.Div(id="iclick_overview", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
		html.Div([
			html.Div(id="iclick_info"),
			dcc.Interval(id="update-iclick_overview", interval=1000*60*60*2, n_intervals=0),
		]),        

	],
)

layout = html.Div([
    html.H1('i_click'),
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
    
	iclick_common_layout,
])

#############################################################################################
###################### Layout callback #####################################################
# #############################################################################################

@app.callback(
	Output("iclick_info","children"),
	[
		Input("update-iclick_overview", "n_intervals"),
		Input("MOB_CAT", "value"),
       
	],
)
@cache1.memoize(timeout=TIMEOUT)
def iclick_infos(n,cust_type):
    (i_click_Female_overtime,i_click_Male_overtime,i_click_age_female_tr,
     i_click_age_male_tr,i_click_age_female,i_click_age_male)=get_iclick_data(session_id,cust_type) 
    
    (i_click_trans_numb,i_click_trans_amt,iclick_cust,i_click_numb,
     i_click_amt,i_click_cat_INACT,i_click_cat_ACT,i_click_trans_cust,customer)=get_iclick_user(session_id,cust_type)
    
    colors_sbu=['#45b6fe','darkblue','grey']
    colors_gender=['#45b6fe','darkblue']  
   
    output= [
		html.Div([]),
        dbc.CardDeck(
            [
                dbc.Card(
                    [
                        html.H5("User customers"),                         
                        html.H3("{:,.0f}".format(iclick_cust), style={"color":"DarkBlue"}),
#                         html.H6("Total number of registered customers"),
                        html.H5("Rate of channel users compared with all customers"),                           
                        html.H3("{:,.1f}%".format(iclick_cust*100/customer), style={"color":"darkblue"}), 
#                         html.H6("Rate of channel users compared with all customers"),                    
                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
                ),
                dbc.Card(
                    [
#                         html.H5("Total transaction volume"),                        
#                         html.H3("rwf {:,.0f}".format(i_click_amt), style={"color":"#45b6fe"}),                        
                        html.H5("Total transaction volume per customer"),                        
                        html.H3("rwf {:,.0f}".format(i_click_amt/iclick_cust), style={"color":"#45b6fe"}),
#                         html.H6("Total transaction volume in RWF per customer"),
#                         html.H5("Total number of transactions"),                        
#                         html.H3("{:,.0f}".format(i_click_numb), style={"color":"#45b6fe"}),                        
                        html.H5("Total number of transactions per customer"),                        
                        html.H3("{:,.0f}".format(i_click_numb/iclick_cust), style={"color":"#45b6fe"}),
#                         html.H6("Total number of transactions per customer"),
                    ],
                    body=True,
	            ),
			],
		),
#     html.Div([        
        dbc.CardGroup(
            [
                dbc.Card(
                    [
                        html.Div([
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Pie(
                                            labels=i_click_cat_ACT.rename(index=SBU_MAPPING).index, 
                                            values=i_click_cat_ACT,
                                            text = i_click_cat_ACT,
                                            hole=0.5,
                                            hoverinfo= "label+percent+text",
#                                             hole=0.2
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
    #                             style={'height': 300, "top":30},
                                id="customer_cat_pie_icl",
                            )
                        ]),
                    ],
                    body=True,
                    style={"padding":"5px 5px 5px 5px", },
                ),
    ############################## customer's gender###################################################################
                dbc.Card(
                    [
                        html.Div([
                                dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Pie(
                                            labels=i_click_cat_INACT.rename(index=GENDER_MAPPING).index, 
                                            values=i_click_cat_INACT,
                                            text = i_click_cat_INACT,
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
                                        # showlegend=True,
                                        legend=go.layout.Legend(
                                            x=1.0,
                                            y=1.0
                                        ),
                                        margin=go.layout.Margin(l=5, r=5, t=70, b=5),

                                    )
                                ),
    #                             style={'height': 300, "top":30},
                                id="cat_active_pie_icl",
                            )
                        ]),
                    ],
                    body=True,
                ),  
            ],
        ),

    html.Div([
        dbc.CardGroup([
	        dbc.Card([
			    dcc.Graph(
			        figure=go.Figure(
			            data=[
			                go.Scatter(
			                    x= i_click_Male_overtime.index, 
			                    y= i_click_Male_overtime,
			                    name='Male',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='darkblue'
			                    )
			                ),
			                go.Scatter(
			                    x= i_click_Female_overtime.index, 
			                    y= i_click_Female_overtime,
			                    name='Female',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='#45b6fe'
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
    ]),

#############Age ######################################################################

    html.Div([        
        dbc.CardGroup([
            dbc.Card(
            [
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x=i_click_age_male.index,
                                y=i_click_age_male,
                                name='Male',
                                text=get_percentage_label((i_click_age_male*100/(i_click_age_male+i_click_age_female)).round()),

                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='darkblue'
                                )
                            ),
                            go.Bar(
                                x=i_click_age_female.index,
                                y=i_click_age_female,
                                name='Female',
                                text=get_percentage_label((i_click_age_female*100/(i_click_age_male+i_click_age_female)).round()),
                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='#45b6fe'
                                )
                            ),  

                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text=" Amount spent on Channel based on customer's age",

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
                                    text="Transaction amount per customer",
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
                                x=i_click_age_male_tr.index,
                                y=i_click_age_male_tr,
                                name='Male',
                                text=get_percentage_label((i_click_age_male_tr*100/(i_click_age_male_tr+i_click_age_female_tr)).round()),

                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='darkblue'
                                )
                            ),
                            go.Bar(
                                x=i_click_age_female_tr.index,
                                y=i_click_age_female_tr,
                                name='Female',
                                text=get_percentage_label((i_click_age_female_tr*100/(i_click_age_male_tr+i_click_age_female_tr)).round()),

                                textposition='auto',
                                marker=go.bar.Marker(
                                    color='#45b6fe'
                                )
                            ),  

                        ],   
                        layout=go.Layout(
                            title=go.layout.Title(
                                text=" Number of transactions based on customer's age",
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
                                    text="Number of transactions per customer",
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
                    id='channel_age_icl',

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
                                x=i_click_trans_amt.rename(index=tran_type_descr).index,
                                y=(i_click_trans_amt/i_click_trans_numb).round(),
                                name='Amount',
                                text=(i_click_trans_amt/i_click_trans_numb).round(),

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
                    # style={'height': 400,},
                    id='channel_sector_mob',

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
                                x=i_click_trans_amt.rename(index=tran_type_descr).index,
                                y=(i_click_trans_amt/i_click_trans_cust).round(),
                                name='Amount',
                                text=(i_click_trans_amt/i_click_trans_cust).round(),
#                                 customdata= i_click_trans_amt,
# 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
                                textposition='outside',
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
                                    text="Amount per customer",
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
                                x=i_click_trans_numb.rename(index=tran_type_descr).index,
                                y=(i_click_trans_numb/i_click_trans_cust).round(),
                                name='Transactions',
                                text=(i_click_trans_numb/i_click_trans_cust).round(),
#                                 customdata= i_click_trans_numb,
# 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
                                textposition='outside',
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
                    # style={'height': 400,},
                    id='Transaction_number_icl',

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
