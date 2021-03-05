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

min_date_allow= '2020-01-01'
init_start_date= str(dt.today().year)+'-'+str(dt.today().month)+'-01'
init_end_date= str(dt.today().year)+'-'+str(dt.today().month)+'-'+str(dt.today().day)


(card_primary_supp,card_branch,card_status,customers,cards_numb,
 card_product,supply,primary,compr_card,Stol_card,
 Lost_card,clos_card,decl_card,Open_card,Open_card_status,decl_card_status,clos_card_status,
 Lost_card_status,Stol_card_status,compr_card_status,Open_card_branch,decl_card_branch,
 clos_card_branch,Lost_card_branch,Stol_card_branch,compr_card_branch,
 classic_deb_branch,classic_pre_branch,gold_cre_branch,gold_deb_branch,
 classic_deb_state,classic_pre_state,gold_cre_state,gold_deb_state,Card_type)=get_cards_details(session_id)
card_common_layout = html.Div(
	[        
		html.Div(id="card_overview1", style={"color":"DarkRed", "margin":"25px 0px 0px 0px"}),
		html.Div([
			html.Div(id="card_info1"),
			dcc.Interval(id="update-card_overview1", interval=1000*60*60*2, n_intervals=0),
		]),
		html.Div(
        [
            dbc.Row([
                dbc.Col([
                    dcc.DatePickerRange(
                        id='channels-date-picker-range',
                        min_date_allowed= min_date_allow,
                        max_date_allowed= dt.today().strftime("%Y-%m-%d"),
                        initial_visible_month= dt.today().strftime("%Y-%m-%d"),
                        start_date= '2020-01-01',
                        end_date = '2020-03-01',
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
		html.Div([
			html.Div(id="card_tran1"),
			dcc.Interval(id="update-card_tran1", interval=1000*60*60*2, n_intervals=0),
		]),
        
    

	],
)

layout= html.Div([

	card_common_layout,
])

@app.callback(
	Output("card_tran1","children"),
# 	[
    [Input("update-card_tran1", "n_intervals"),
    Input("channels-date-picker-range","start_date"),
    Input("channels-date-picker-range","end_date"),],
# 		Input("MOB_CAT", "value"),
# 	]
)
def card_trans(section_id,start_date, end_date):
#     (pos_female_overtime,pos_male_overtime,atm_female_overtime,atm_male_overtime)=get_cards_transactions(session_id)
    (pos_female_overtime,pos_male_overtime,atm_female_overtime,
     atm_male_overtime,POS_tran,POS_AM,ATM_tran,ATM_AM,POS_trend,ATM_trend)= get_cards_transactions(session_id,start_date, end_date)
    output= [
		html.Div([]),
    html.H1('Cards Transactions'),
    dbc.CardDeck(
        [
            dbc.Card(
                [
                    html.H6("POS transactions"),                         
                    html.H3("{:,.0f}".format(POS_tran), style={"color":"DarkBlue"}),
                    html.H6("POS Amount"),                         
                    html.H3("Rwf {:,.0f}".format(POS_AM), style={"color":"DarkBlue"}),                    
                    
                ],
                body=True,
                style={"align":"center", "justify":"center",}
            ),            
            dbc.Card(
                [
                    html.H6("ATM transactions"),                        
                    html.H2("{:,.0f}".format(ATM_tran), style={"color":"LightBlue"}),
                    html.H6("ATM amount"),                        
                    html.H2("Rwf {:,.0f}".format(ATM_AM), style={"color":"LightBlue"}),                    
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
			                    x= POS_trend.index, 
			                    y= POS_trend,
			                    name='POS transactions',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='DarkBlue'
			                    )
			                ),
			                go.Scatter(
			                    x= ATM_trend.index, 
			                    y= ATM_trend,
			                    name='ATM transactions',
#                                 visible='legendonly',
# 			                    mode= "lines",
			                    marker=go.scatter.Marker(
			                        color='lightblue'
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
								text="POS vs ATM usage trend",
                                x=0.5
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
#                                         dict(count=1,
#                                              label="YTD",
#                                              step="year",
#                                              stepmode="todate"),
                                        dict(count=1,
                                             label="1YEAR",
                                             step="year",
                                             stepmode="backward"),
#                                         dict(count=5,
#                                              label="5y",
#                                              step="year",
#                                              stepmode="backward"),
#                                         dict(count=10,
#                                              label="10y",
#                                              step="year",
#                                              stepmode="backward"),                                 
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
        
    html.Div([        
#         dbc.CardGroup([
#             dbc.Card(
#             [
#                 html.Div([
#                     dcc.Graph(
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(
#                                 x=atm_age_male.index,
#                                 y=atm_age_male,
#                                 name='Male',
#                                 text=get_percentage_label((atm_age_male*100/(atm_age_male+atm_age_female)).round(2)),
# # 						                customdata= age_perf_male_balance,
# # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
#                                 textposition='auto',
#                                 marker=go.bar.Marker(
#                                     color='darkblue'
#                                 )
#                             ),
#                             go.Bar(
#                                 x=atm_age_female.index,
#                                 y=atm_age_female,
#                                 name='Female',
# #                                 visible='legendonly',
#                                 text=get_percentage_label((atm_age_female*100/(atm_age_male+atm_age_female)).round(2)),
# # 		    							customdata= age_nonperf_male_balance,
# # 		    							hovertemplate= format_hover_template(),
#                                 textposition='auto',
#                                 marker=go.bar.Marker(
#                                     color='lightblue'
#                                 )
#                             ),  

#                         ],   
#                         layout=go.Layout(
#                             title=go.layout.Title(
#                                 text=" Amount spent on ATM based on customer's age",
#                             # 	xref="paper",
#                             # 	x=0
#                             ),
#                             xaxis=go.layout.XAxis(
#                                 title=go.layout.xaxis.Title(
#                                     text="Age Group",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ),
#                             yaxis=go.layout.YAxis(
#                                 title=go.layout.yaxis.Title(
#                                     text="Transaction amount",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ), 
#                             # barmode="stack",
#                             showlegend=True,
#                             legend=go.layout.Legend(
#                                 x=0.9,
#                                 y=1.0,
#                                 xanchor="center",
#                                 yanchor="top",
#                             ),
#                             margin=go.layout.Margin(l=40, r=0, t=40, b=30)
#                         )
#                     ),
#                     # style={'height': 400,},
#                     id='channel_age_icl',
# #                    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( " Amount spent on Channel based on customer's age" )}),
#                 ),

#                 ]),
#             ],
#             body=True,
#             style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
#         ),
#         dbc.Card(
#             [
#                 html.Div([
#                     dcc.Graph(
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(
#                                 x=atm_age_male_num.index,
#                                 y=atm_age_male_num,
#                                 name='Male',
#                                 text=get_percentage_label((atm_age_male_num*100/(atm_age_male_num+atm_age_female_num)).round(2)),
# # 						                customdata= age_perf_male_balance,
# # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
#                                 textposition='auto',
#                                 marker=go.bar.Marker(
#                                     color='darkblue'
#                                 )
#                             ),
#                             go.Bar(
#                                 x=atm_age_female_num.index,
#                                 y=atm_age_female_num,
#                                 name='Female',
# #                                 visible='legendonly',
#                                 text=get_percentage_label((atm_age_female_num*100/(atm_age_female_num+atm_age_male_num)).round(2)),
# # 		    							customdata= age_nonperf_male_balance,
# # 		    							hovertemplate= format_hover_template(),
#                                 textposition='auto',
#                                 marker=go.bar.Marker(
#                                     color='lightblue'
#                                 )
#                             ),  

#                         ],   
#                         layout=go.Layout(
#                             title=go.layout.Title(
#                                 text=" Number of ATM transactions based on customer's age",
#                             # 	xref="paper",
#                             # 	x=0
#                             ),
#                             xaxis=go.layout.XAxis(
#                                 title=go.layout.xaxis.Title(
#                                     text="Age Group",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ),
#                             yaxis=go.layout.YAxis(
#                                 title=go.layout.yaxis.Title(
#                                     text="Number of transactions",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ), 
#                             # barmode="stack",
#                             showlegend=True,
#                             legend=go.layout.Legend(
#                                 x=0.9,
#                                 y=1.0,
#                                 xanchor="center",
#                                 yanchor="top",
#                             ),
#                             margin=go.layout.Margin(l=40, r=0, t=40, b=30)
#                         )
#                     ),
#                     # style={'height': 400,},
#                     id='channel_age_icl',
#                 ),

#                 ]),
#             ],
#             body=True,
#             style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
#         ),                
#     ]),
# ]),
#     html.Div([        
#         dbc.CardGroup([
#             dbc.Card(
#             [
#                 html.Div([
#                     dcc.Graph(
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(
#                                 x=pos_age_male.index,
#                                 y=pos_age_male,
#                                 name='Male',
#                                 text=get_percentage_label((pos_age_male*100/(pos_age_male+pos_age_female)).round(2)),
# # 						                customdata= age_perf_male_balance,
# # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
#                                 textposition='auto',
#                                 marker=go.bar.Marker(
#                                     color='darkblue'
#                                 )
#                             ),
#                             go.Bar(
#                                 x=pos_age_female.index,
#                                 y=pos_age_female,
#                                 name='Female',
# #                                 visible='legendonly',
#                                 text=get_percentage_label((pos_age_female*100/(pos_age_male+pos_age_female)).round(2)),
# # 		    							customdata= age_nonperf_male_balance,
# # 		    							hovertemplate= format_hover_template(),
#                                 textposition='auto',
#                                 marker=go.bar.Marker(
#                                     color='lightblue'
#                                 )
#                             ),  

#                         ],   
#                         layout=go.Layout(
#                             title=go.layout.Title(
#                                 text=" Amount spent on POS based on customer's age",
#                             # 	xref="paper",
#                             # 	x=0
#                             ),
#                             xaxis=go.layout.XAxis(
#                                 title=go.layout.xaxis.Title(
#                                     text="Age Group",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ),
#                             yaxis=go.layout.YAxis(
#                                 title=go.layout.yaxis.Title(
#                                     text="Transaction amount",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ), 
#                             # barmode="stack",
#                             showlegend=True,
#                             legend=go.layout.Legend(
#                                 x=0.9,
#                                 y=1.0,
#                                 xanchor="center",
#                                 yanchor="top",
#                             ),
#                             margin=go.layout.Margin(l=40, r=0, t=40, b=30)
#                         )
#                     ),
#                     # style={'height': 400,},
#                     id='channel_age_icl',
# #                    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( " Amount spent on Channel based on customer's age" )}),
#                 ),

#                 ]),
#             ],
#             body=True,
#             style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
#         ),
#         dbc.Card(
#             [
#                 html.Div([
#                     dcc.Graph(
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(
#                                 x=pos_age_male_num.index,
#                                 y=pos_age_male_num,
#                                 name='Male',
#                                 text=get_percentage_label((pos_age_male_num*100/(pos_age_male_num+pos_age_female_num)).round(2)),
# # 						                customdata= age_perf_male_balance,
# # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
#                                 textposition='auto',
#                                 marker=go.bar.Marker(
#                                     color='darkblue'
#                                 )
#                             ),
#                             go.Bar(
#                                 x=pos_age_female_num.index,
#                                 y=pos_age_female_num,
#                                 name='Female',
# #                                 visible='legendonly',
#                                 text=get_percentage_label((pos_age_female_num*100/(pos_age_female_num+pos_age_male_num)).round(2)),
# # 		    							customdata= age_nonperf_male_balance,
# # 		    							hovertemplate= format_hover_template(),
#                                 textposition='auto',
#                                 marker=go.bar.Marker(
#                                     color='lightblue'
#                                 )
#                             ),  

#                         ],   
#                         layout=go.Layout(
#                             title=go.layout.Title(
#                                 text=" Number of POS transactions based on customer's age",
#                             # 	xref="paper",
#                             # 	x=0
#                             ),
#                             xaxis=go.layout.XAxis(
#                                 title=go.layout.xaxis.Title(
#                                     text="Age Group",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ),
#                             yaxis=go.layout.YAxis(
#                                 title=go.layout.yaxis.Title(
#                                     text="Number of transactions",
#                                     # font=dict(
#                                     #     family="Courier New, monospace",
#                                     #     size=18,
#                                     #     color="#7f7f7f"
#                                     # )
#                                 )
#                             ), 
#                             # barmode="stack",
#                             showlegend=True,
#                             legend=go.layout.Legend(
#                                 x=0.9,
#                                 y=1.0,
#                                 xanchor="center",
#                                 yanchor="top",
#                             ),
#                             margin=go.layout.Margin(l=40, r=0, t=40, b=30)
#                         )
#                     ),
#                     # style={'height': 400,},
#                     id='channel_age_icl',
# #                    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( " Amount spent on Channel based on customer's age" )}),
#                 ),

#                 ]),
#             ],
#             body=True,
#             style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
#         ),                
#     ]),
]),
]
    return output
