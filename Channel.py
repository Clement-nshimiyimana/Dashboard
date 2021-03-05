from datetime import datetime as dt
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
import plotly.graph_objs as go

from datetime import timedelta, datetime as dt
# from calendar import monthrange

from plotly import tools

import warnings
warnings.filterwarnings("ignore")

from app import cache1, TIMEOUT, app, session_id
from components import *
from config import *


# min_date_allow= pd.to_datetime('2018-09-01', errors='coerce')
min_date_allow= '2018-09-01'
init_start_date= str(dt.today().year)+'-'+str(dt.today().month)+'-01'
init_end_date= str(dt.today().year)+'-'+str(dt.today().month)+'-'+str(dt.today().day)

layout = html.Div(
    [
    html.H1('Channels transactions'),
    html.Hr(),        

#     html.P('Channels panel contains detailed information regarding bank’s channels such as internet banking(i_click), Mobile app,USSD and Push&Pull. To view information based on business category, you can choose one of the bellow buttons(All: bank level in general, Retail,SME, Corporate). There are also date picker buttons which allow to view information on the time range you set. In addition,for each graph you can choose one field you want see clearly by disabling others, e.g: you may want to see only iclick infos, you have to disable others by double clicking on iclick on legend. Notice:for graphs showing trend overtime, there are buttons 1MONTH, 3MONTH,1YEAR which allows to see the situation in one month, three months ago and so on. You can export tables in excel by clicking export button.'),
#     html.Hr(),        
	dbc.Row([
		dbc.Col([
			dcc.RadioItems(
				id= "select-channels",
				options=[
				    {'label': 'ALL', 'value': 'All'},#
				    {'label': 'Retail', 'value':'R'},#
				    {'label': 'Corporate', 'value':'C'},                    
				    {'label': 'MSME', 'value':'S' },#
				],
				value='All',
				labelStyle={'display': 'inline-block', 'margin':'10px 10px 10px 10px', 'font-size':20, 'font-style': 'italic'}
			),
		]),
	]),
#         html.Div(id='channel-content')
    html.Div(
    [
        dbc.Row([
            dbc.Col([
                dcc.DatePickerRange(
                    id='channels-date-picker-range',
#                     min_date_allowed= min_date_allow,
#                     max_date_allowed= dt.today().strftime("%Y-%m-%d"),
                    initial_visible_month= dt.today().strftime("%Y-%m-%d"),
#                     start_date= init_start_date,
#                     end_date = init_end_date,
                    start_date= '2019-10-01',
                    end_date = '2019-12-31',                    
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

        html.Div([
            html.Div(id="summary-channel"),
            dcc.Interval(id="update-channels", interval=1000*60*60*2, n_intervals=0),
        ]),
        html.Div([
            html.Div(id="summary-tables"),
            dcc.Interval(id="update-channels_info", interval=1000*60*60*2, n_intervals=0),
        ]),        
    ],
)        
],
)

@app.callback(
	Output("summary-channel","children"),
	[
	    Input("update-channels", "n_intervals"),
	    Input("channels-date-picker-range","start_date"),
	    Input("channels-date-picker-range","end_date"),
	    Input("select-channels", "value")
	]
)
@cache1.memoize(timeout=TIMEOUT)
def get_channels_summary(n, start, end,selected_channel):
    (txn_df,iclick_am,Mobile_am,ussd_am,iclick_tran,Mobile_tran,ussd_tran,
     iclick_cus,Mobile_cus,ussd_cus,iclick_cus,
     Mobile_cus,ussd_cus,iclick_trend,Mobile_trend,ussd_trend,iclick,Mobile,
     ussd,iclick_tran_num,Mobile_tran_num,ussd_tran_num,iclick_cust,
     Mobile_cust,ussd_cust,mobile_female_num,mobile_male_num,ussd_female_num,ussd_male_num,
     iclick_female_num,ICLICK_male_num,mobile_female,mobile_male,
     ussd_female,ussd_male,iclick_female,ICLICK_male)= get_och_channels_data(session_id,start, end,selected_channel)
    
    (df,MTN_cus,MTN_am,MTN_tran, MTN_trend,MTN,MTN_tran_num,MTN_cust,mtn_male,
     mtn_female,mtn_male_num,mtn_female_num,MTN_tran_numb)=get_push_and_pull_data(session_id,start, end,selected_channel)


    return [

    html.Div([]),        
        dbc.CardDeck(
            [
                dbc.Card(
	                [
                        html.H5("iclick users"),                                           
                        html.H3("{:,.0f}".format(iclick_cus), style={"color":"#45b6fe"}),
#                         html.H6("Total number of iclick users"),
#                         html.H5("Rate of iclick users to all customers"),                         
#                         html.H3("{:,.2f}%".format(iclick_cus*100/(iclick_cus+Mobile_cus+ussd_cus)), style={"color":"#45b6fe"}), 

                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
	            ),
	            dbc.Card(
	                [
	                    html.H5("Mobile app users"),                        
	                    html.H2("{:,.0f}".format(Mobile_cus),style={"color":"darkred"}),
# 	                    html.H6("Total number of Mobile app users"),
# 	                    html.H5("Rate of Mobile app users to all customers"),                         
# 	                    html.H2("{:,.2f}%".format(Mobile_cus*100/(iclick_cus+Mobile_cus+ussd_cus)), style={"color":"darkred"}),
                        
	                ],
	                body=True,
	            ),
                dbc.Card(
                    [
                        html.H5("USSD users"),                                             
                        html.H2("{:,.0f}".format(ussd_cus), style={"color":"grey"}),
#                         html.H6("Total number of USSD users"),
#                         html.H5("Rate of USSD users to all customers"),                        
#                         html.H2("{:,.2f}%".format(ussd_cus*100/(iclick_cus+Mobile_cus+ussd_cus)), style={"color":"grey"}),                        
                    ],
	                body=True,
	            ),
                dbc.Card(
                    [
                        html.H5("PUSH&PULL users"),                                             
                        html.H2("{:,.0f}".format(MTN_cus), style={"color":"DarkBlue"}),
#                         html.H6("Total number of PUSH&PULL users"),
#                         html.H5("Rate of PUSH&PULL users to all customers"),                        
#                         html.H2("{:,.2f}%".format(MTN_cus*100/(iclick_cus+Mobile_cus+ussd_cus+MTN_cus)), style={"color":"DarkBlue"}),
                       
                    ],
	                body=True,
	            ),                
			],
		),
        dbc.CardDeck(
            [
                dbc.Card(
	                [ 

                        html.H5("iclick amount in millions"),                                           
                        html.H3("Rwf {:,.0f}".format(iclick_am/1e6), style={"color":"#45b6fe"}),                        

                        html.H5("iclick number of transactions"),                         
                        html.H3("{:,.0f}".format(iclick_tran), style={"color":"#45b6fe"}),                         
                        
#                         html.H6("Rate of iclick users to all customers"),                    
                    ],
                    body=True,
                    style={"align":"center", "justify":"center",}
	            ),
	            dbc.Card(
	                [

	                    html.H5("Mobile app amount in millions"),                        
	                    html.H2("Rwf {:,.0f}".format(Mobile_am/1e6),style={"color":"darkred"}),                        
	                    html.H5("Mobile app number of transactions"),                         
	                    html.H2("{:,.0f}".format(Mobile_tran), style={"color":"darkred"}),                        
                        
	                ],
	                body=True,
	            ),
                dbc.Card(
                    [

                        html.H5("USSD amount in millions"),                                             
                        html.H2("Rwf {:,.0f}".format(ussd_am/1e6), style={"color":"grey"}),                        
                        html.H5("USSD number of transactions"),                        
                        html.H2("{:,.0f}".format(ussd_tran), style={"color":"grey"}),
                        
#                         html.H6("Rate of USSD users to all customers"),                        
                    ],
	                body=True,
	            ),
                dbc.Card(
                    [


                        html.H5("PUSH&PULL amount in millions"),                                             
                        html.H2("Rwf {:,.0f}".format(MTN_am/1e6), style={"color":"DarkBlue"}),                        
#                         html.H6("Total number of PUSH&PULL users"),
#                         html.H5("PUSH&PULL amount per transaction"),                        
#                         html.H2("rwf {:,.0f}".format(MTN_am/MTN_tran), style={"color":"DarkBlue"}),
                        html.H5("PUSH&PULL number of transactions"),                        
                        html.H2("{:,.0f}".format(MTN_tran), style={"color":"DarkBlue"}),
                        
#                         html.H6("Rate of PUSH&PULL users to all customers"),                        
                    ],
	                body=True,
	            ),                
			],
		),
# # # ######################################################################################################
# # # ##########################################customer_trend############################################################
    html.Div([
        dbc.CardGroup([
            dbc.Card([
                dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Scatter(
                                x= iclick_trend.index, 
                                y= iclick_trend,
                                name='Iclick',
                                mode= "lines",
                                marker=go.scatter.Marker(
                                    color='#45b6fe'
                                )
                            ),
                            go.Scatter(
                                x= Mobile_trend.index, 
                                y= Mobile_trend,
                                name='Mobile app',
                                mode= "lines",
                                marker=go.scatter.Marker(
                                    color='darkred'
                                )
                            ),
                            go.Scatter(
                                x= ussd_trend.index, 
                                y= ussd_trend,
                                name='USSD',
                                mode= "lines",
#                                 visible='legendonly',
                                marker=go.scatter.Marker(
                                    color='grey'
                                )
                            ),
                            go.Scatter(
                                x= MTN_trend.index, 
                                y= MTN_trend,
                                name='Push Pull',
                                mode= "lines",
#                                 visible='legendonly',
                                marker=go.scatter.Marker(
                                    color='DarkBlue'
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
                                text="Channels usage overtime[{}]".format(selected_channel),
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
        dbc.CardGroup([
            dbc.Card(
                [
                    html.Div([
                        dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x=iclick.rename(index=tran_type_descr).index,
                                    y=iclick//iclick_tran_num,
                                    name='iclick',
                                    text=iclick//iclick_tran_num,
    # 						                customdata= age_perf_male_balance,
    # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='#45b6fe'
                                    )
                                ),
                                go.Bar(
                                    x=Mobile.rename(index=tran_type_descr).index,
                                    y=Mobile//Mobile_tran_num,
                                    name='Mobile App',
                                    text=Mobile//Mobile_tran_num,
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='darkred'
                                    )
                                ),
                                go.Bar(
                                    x=ussd.rename(index=tran_type_descr).index,
                                    y=ussd//ussd_tran_num,
                                    name='USSD',
                                    text=ussd//ussd_tran_num,
#                                     visible='legendonly',
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='grey'
                                    )
                                ),
                                go.Bar(
                                    x=MTN.rename(index=push_MAPPING).index,
                                    y=MTN//MTN_tran_num,
                                    name='Push&pull',
                                    text=MTN//MTN_tran_num,
#                                     visible='legendonly',
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),             
                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text=" Amount per transaction(in Rwf)[{}]".format(selected_channel),
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
                                barmode="stack",
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
    #						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Amount spent on Channel based on customers age" )}),
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
                                    x=iclick.rename(index=tran_type_descr).index,
                                    y=iclick//1e6,
                                    name='iclick',
                                    text=iclick//1e6,
    # 						                customdata= age_perf_male_balance,
    # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='#45b6fe'
                                    )
                                ),
                                go.Bar(
                                    x=Mobile.rename(index=tran_type_descr).index,
                                    y=Mobile//1e6,
                                    name='Mobile App',
                                    text=Mobile//1e6,
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='darkred'
                                    )
                                ),
                                go.Bar(
                                    x=ussd.rename(index=tran_type_descr).index,
                                    y=ussd//1e6,
                                    name='USSD',
                                    text=ussd//1e6,
#                                     visible='legendonly',
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='grey'
                                    )
                                ),
                                go.Bar(
                                    x=MTN.rename(index=push_MAPPING).index,
                                    y=MTN//1e6,
                                    name='Push&pull',
                                    text=MTN//1e6,
#                                     visible='legendonly',
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),             
                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text="Transaction Amount(in millions Rwf)[{}]".format(selected_channel),
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
                                        text="Amount in millions",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                ), 
                                barmode="stack",
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
    #						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Amount spent on Channel based on customers age" )}),
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
                                    x=iclick_tran_num.rename(index=tran_type_descr).index,
                                    y=iclick_tran_num//iclick_cust,
                                    name='iclick',
                                    text=iclick_tran_num//iclick_cust,
    # 						                customdata= age_perf_male_balance,
    # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='#45b6fe'
                                    )
                                ),
                                go.Bar(
                                    x=Mobile_tran_num.rename(index=tran_type_descr).index,
                                    y=Mobile_tran_num//Mobile_cust,
                                    name='Mobile App',
                                    text=Mobile_tran_num//Mobile_cust,
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='darkred'
                                    )
                                ),
                                go.Bar(
                                    x=ussd_tran_num.rename(index=tran_type_descr).index,
                                    y=ussd_tran_num//ussd_cust,
                                    name='USSD',
                                    text=ussd_tran_num//ussd_cust,
#                                     visible='legendonly',
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='grey'
                                    )
                                ),
                                go.Bar(
                                    x=MTN_tran_num.rename(index=push_MAPPING).index,
                                    y=MTN_tran_num//MTN_cust,
                                    name='Push&pull',
                                    text=MTN_tran_num//MTN_cust,
#                                     visible='legendonly',
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),             
                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text="Number of transactions per customer[{}]".format(selected_channel),
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
                                barmode="stack",
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
    #						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Amount spent on Channel based on customers age" )}),
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
                                    x=iclick_tran_num.rename(index=tran_type_descr).index,
                                    y=iclick_tran_num,
                                    name='iclick',
                                    text=iclick_tran_num,
    # 						                customdata= age_perf_male_balance,
    # 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='#45b6fe'
                                    )
                                ),
                                go.Bar(
                                    x=Mobile_tran_num.rename(index=tran_type_descr).index,
                                    y=Mobile_tran_num,
                                    name='Mobile App',
                                    text=Mobile_tran_num,
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='darkred'
                                    )
                                ),
                                go.Bar(
                                    x=ussd_tran_num.rename(index=tran_type_descr).index,
                                    y=ussd_tran_num,
                                    name='USSD',
                                    text=ussd_tran_num,
#                                     visible='legendonly',
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='grey'
                                    )
                                ),
                                go.Bar(
                                    x=MTN_tran_num.rename(index=push_MAPPING).index,
                                    y=MTN_tran_num,
                                    name='Push&pull',
                                    text=MTN_tran_num,
#                                     visible='legendonly',
    # 		    							customdata= age_nonperf_male_balance,
    # 		    							hovertemplate= format_hover_template(),
                                    textposition='outside',
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),             
                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text="Number of transactions",
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
                                        text="Transactions per customer[{}]".format(selected_channel),
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                ), 
                                barmode="stack",
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
    #						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Amount spent on Channel based on customers age" )}),
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
                                    x=ICLICK_male_num.index,
                                    y=ICLICK_male_num,
                                    name=' iclick Male',
#                                     text=get_percentage_label((ICLICK_male_num*100/(ICLICK_male_num+iclick_female_num)).round()),
# 						                customdata= age_perf_male_balance,
# 						                hovertemplate= format_hover_template(x_label= "Age Range", y_label= "# of Accounts"),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),
                                go.Bar(
                                    x=ussd_male_num.index,
                                    y=ussd_male_num,
                                    name='Ussd Male',
#                                     visible='legendonly',
#                                     text=get_percentage_label((ussd_male_num*100/(ussd_male_num+ussd_female_num)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='grey'
                                    )
                                ), 
                                go.Bar(
                                    x=mobile_male_num.index,
                                    y=mobile_male_num,
                                    name='Mobile app Male',
#                                     text=get_percentage_label((mobile_male_num*100/(mobile_male_num+mobile_female_num)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='DarkRed'
                                    )
                                ),  
                                go.Bar(
                                    x=mtn_male_num.index,
                                    y=mtn_male_num,
                                    name='Push pull Male',
#                                     visible='legendonly',
#                                     text=get_percentage_label((mtn_male_num*100/(mtn_male_num+mtn_female_num)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#004206'
                                    )
                                ),        
                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text=" Amount spent on Channel based on customers age[{}]".format(selected_channel),
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
                                        text="Transaction amount per customer",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                ), 
                                barmode="stack",
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
                        id='channel_age_mob',
#						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Amount spent on Channel based on customers age" )}),
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
                                    x=iclick_female_num.index,
                                    y=iclick_female_num,
                                    name='iclick Female',
#                                     text=get_percentage_label((iclick_female_num*100/(iclick_female_num+ICLICK_male_num)).round()),

                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#45b6fe'
                                    )
                                ),  
                                go.Bar(
                                    x=ussd_female_num.index,
                                    y=ussd_female_num,
                                    name='Ussd Female',
#                                     visible='legendonly',
#                                     text=get_percentage_label((ussd_female_num*100/(ussd_female_num+ussd_male_num)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#d3d3d3'
                                    )
                                ),  
                                go.Bar(
                                    x=mobile_female_num.index,
                                    y=mobile_female_num,
                                    name=' Mobile app Female',
#                                     text=get_percentage_label((mobile_female_num*100/(mobile_female_num+mobile_male_num)).round()),

                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#F5D3C7'
                                    )
                                ),
                                go.Bar(
                                    x=mtn_female_num.index,
                                    y=mtn_female_num,
                                    name='Push pull Female',
#                                     visible='legendonly',
#                                     text=get_percentage_label((mtn_female_num*100/(mtn_female_num+mtn_male_num)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#9deda4'
                                    )
                                ),        
                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text=" Channel's transactions based on customers age[{}]".format(selected_channel),
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
                                barmode="stack",
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
                        id='channel_age_mob',
#						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Amount spent on Channel based on customers age" )}),
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
                                    x=ICLICK_male.index,
                                    y=ICLICK_male,
                                    name=' iclick Male',
#                                     text=get_percentage_label((ICLICK_male*100/(ICLICK_male+iclick_female)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='darkblue'
                                    )
                                ),
                                go.Bar(
                                    x=ussd_male.index,
                                    y=ussd_male,
                                    name='Ussd Male',
#                                     visible='legendonly',
#                                     text=get_percentage_label((ussd_male*100/(ussd_male+ussd_female)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='grey'
                                    )
                                ),  
                                go.Bar(
                                    x=mobile_male.index,
                                    y=mobile_male,
                                    name='Mobile app Male',
#                                     text=get_percentage_label((mobile_male*100/(mobile_male+mobile_female)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='Darkred'
                                    )
                                ),
                                go.Bar(
                                    x=mtn_male.index,
                                    y=mtn_male,
                                    name='Push pull Male',
#                                     visible='legendonly',
#                                     text=get_percentage_label((mtn_male*100/(mtn_male+mtn_female)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#004206'
                                    )
                                ),        
                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text=" Amount spent on Channel based on customers age[{}]".format(selected_channel),
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
                                        text="Transaction amount per customer",
                                        # font=dict(
                                        #     family="Courier New, monospace",
                                        #     size=18,
                                        #     color="#7f7f7f"
                                        # )
                                    )
                                ), 
                                barmode="stack",
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
                        id='channel_age_mob',

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
                                    x=iclick_female.index,
                                    y=iclick_female,
                                    name='iclick Female',
#                                     text=get_percentage_label((iclick_female*100/(iclick_female+ICLICK_male)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#45b6fe'
                                    )
                                ),  
                                go.Bar(
                                    x=mobile_female.index,
                                    y=mobile_female,
                                    name=' Mobile app Female',
#                                     text=get_percentage_label((mobile_female*100/(mobile_female+mobile_male)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#F5D3C7'
                                    )
                                ),  
                                go.Bar(
                                    x=ussd_female.index,
                                    y=ussd_female,
                                    name='Ussd Female',
#                                     visible='legendonly',
#                                     text=get_percentage_label((ussd_female*100/(ussd_female+ussd_male)).round()),

                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='lightgrey'
                                    )
                                ),  
                                go.Bar(
                                    x=mtn_female.index,
                                    y=mtn_female,
                                    name='Push pull Female',
#                                     visible='legendonly',
#                                     text=get_percentage_label((mtn_female*100/(mtn_female+mtn_male)).round()),
                                    textposition='auto',
                                    marker=go.bar.Marker(
                                        color='#9deda4'
                                    )
                                ),       
                            ],   
                            layout=go.Layout(
                                title=go.layout.Title(
                                    text=" Channel's transactions based on customers age[{}]".format(selected_channel),
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
                                barmode="stack",
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
                        id='channel_age_mob',
#						    config= add_image_file_name_to_config(BAR_PLOT_CONFIG, {"filename": "{}".format( "Amount spent on Channel based on customers age" )}),
                    ),

                    ]),
                ],
                body=True,
                style={"padding":"5px 10px 5px 5px",}# "margin":"5px 15px 5px 5px",},
            ),                       
        ]),        
    ]),
]

@app.callback(
	Output("summary-tables","children"),
	[
	    Input("update-channels_info", "n_intervals"),
	    Input("channels-date-picker-range","start_date"),
	    Input("channels-date-picker-range","end_date"),
	    Input("select-channels", "value")
	]
)
@cache1.memoize(timeout=TIMEOUT)
def update_table(n, start, end,selected_channel):
    (txn_df,iclick_am,Mobile_am,ussd_am,iclick_tran,Mobile_tran,ussd_tran,
            iclick_cus,Mobile_cus,ussd_cus,iclick_cus,
            Mobile_cus,ussd_cus,iclick_trend,Mobile_trend,ussd_trend,iclick,Mobile,
            ussd,iclick_tran_num,Mobile_tran_num,ussd_tran_num,iclick_cust,
            Mobile_cust,ussd_cust,mobile_female_num,mobile_male_num,ussd_female_num,ussd_male_num,
            iclick_female_num,ICLICK_male_num,mobile_female,mobile_male,
            ussd_female,ussd_male,iclick_female,ICLICK_male)= get_och_channels_data(session_id,start, end,selected_channel)
    (df,MTN_cus,MTN_am,MTN_tran, MTN_trend,MTN,MTN_tran_num,MTN_cust,mtn_male,
     mtn_female,mtn_male_num,mtn_female_num,MTN_tran_numb)=get_push_and_pull_data(session_id,start, end,selected_channel)    
    (
        Trans_Type__i_click, Total_Trans__i_click, Total_Value__i_click, National_Trans__i_click, 
        National_Value__i_click, Inter_Trans__i_click, Inter_Value__i_click,intra_cust__i_click,inter_cust__i_click,Total_users__i_click
    )= get_transact_summary_table(session_id, "I", txn_df, start, end,selected_channel)

    ## USSD
    (
        Trans_Type__ussd, Total_Trans__ussd, Total_Value__ussd, National_Trans__ussd, 
        National_Value__ussd, Inter_Trans__ussd, Inter_Value__ussd, intra_cust__ussd,inter_cust__ussd,Total_users__ussd
    )= get_transact_summary_table(session_id, "U", txn_df, start, end,selected_channel)

    ## Mobile App
    (
        Trans_Type__mobile_app, Total_Trans__mobile_app, Total_Value__mobile_app, National_Trans__mobile_app, 
        National_Value__mobile_app, Inter_Trans__mobile_app, Inter_Value__mobile_app,intra_cust__mobile_app,inter_cust__mobile_app,Total_users__mobile_app
    )= get_transact_summary_table(session_id, "G", txn_df, start, end,selected_channel)

    ## push & pull
    (
        Trans_Type__push_pull, Total_Trans__push_pull, Total_Value__push_pull, National_Trans__push_pull, 
        National_Value__push_pull, Inter_Trans__push_pull, Inter_Value__push_pull,Total_users
    )= get_transact_summary_table_push_pull(session_id, df, start, end,selected_channel)
    
    return [
    html.H1("Summary Tables"),         
    html.Div([            
        html.H2("i-Click", style={"margin":"15px 0px 10px 0px"},),
        dash_table.DataTable(
            id='iclick-data_table',
            columns=[
                {"name": ["", "Trans Type"], "id": "Trans-Type" },
                {"name": ["Total", "Number of Transactions"], "id": "Total-Trans", },
                {"name": ["Total", "Amount"], "id": "Total-Value", },
#                 {"name": ["Total", "Users"], "id": "Total-users", },
                {"name": ["National", "Number of Transactions"], "id": "National-Trans", },
                {"name": ["National", "Amount"], "id": "National-Value"},
#                 {"name":["","#Users"],"id":"n_users"},                
                {"name": ["International", "Number of Transactions"], "id": "International-Trans"},
                {"name": ["International", "Amount"], "id": "International-Value"},
#                 {"name":["","#Ex-Users"],"id":"e_users"},                
            ],
            data=[
                {
                    "Trans-Type": Trans_Type__i_click[i],
                    "Total-Trans": format_(Total_Trans__i_click[i]),
                    "Total-Value": format_(Total_Value__i_click[i]),
#                     "Total-users": format_(Total_users__i_click[i]),
                    "National-Trans": format_(National_Trans__i_click[i]),
                    "National-Value": format_(National_Value__i_click[i]),
#                     "#Users":format_(intra_cust__i_click[i]),                    
                    "International-Trans": format_(Inter_Trans__i_click[i]),
                    "International-Value": format_(Inter_Value__i_click[i]),
#                     "#Ex-Users":format_(inter_cust__i_click[i]),                    
                }
                for i in range(len(Trans_Type__i_click))
            ]+ [
                {
                    "Trans-Type": "Total",
                    "Total-Trans": format_(sum(Total_Trans__i_click)),
                    "Total-Value": format_(sum(Total_Value__i_click)),
#                     "Total-users": format_(sum(Total_users__i_click)),
                    "National-Trans": format_(sum(National_Trans__i_click)),
                    "National-Value": format_(sum(National_Value__i_click)),
#                     "#Users":format_(sum(intra_cust__i_click)),                    
                    "International-Trans": format_(sum(Inter_Trans__i_click)),
                    "International-Value": format_(sum(Inter_Value__i_click)),
#                     "#Ex-Users":format_(sum(inter_cust__i_click)),                    
                    
                }
            ],
            style_header={
                "backgroundColor": "DeepSkyBlue",
                'color': 'white',
                'fontWeight': 'bold',
            },
            style_data_conditional=[{
                "if": {"row_index": len(Total_Trans__i_click)},
                "backgroundColor": "DodgerBlue",
                'color': 'white'
            }],
            export_format='xlsx',
            export_headers='display',
            merge_duplicate_headers=True
        ),
        ######################################################################################
        html.H2("Mobile App", style={"margin":"15px 0px 10px 0px"},),
        dash_table.DataTable(
            id='mobile_app-data_table',
            columns=[
                {"name": ["", "Trans Type"], "id": "Trans-Type" },
                {"name": ["Total", "Number of Transactions"], "id": "Total-Trans", },
                {"name": ["Total", "Amount"], "id": "Total-Value", },
#                 {"name": ["Total", "Users"], "id": "Total-users", },
                {"name": ["National", "Number of Transactions"], "id": "National-Trans", },
                {"name": ["National", "Amount"], "id": "National-Value"},
#                 {"name":["National","#Users"],"id":"n_users"},                
                {"name": ["International", "Number of Transactions"], "id": "International-Trans"},
                {"name": ["International", "Amount"], "id": "International-Value"},
#                 {"name":["International","#Ex-Users"],"id":"e_users"},                
            ],
            data=[
                {
                    "Trans-Type": Trans_Type__mobile_app[i],
                    "Total-Trans": format_(Total_Trans__mobile_app[i]),
                    "Total-Value": format_(Total_Value__mobile_app[i]),
#                     "Total-users": format_(Total_users__mobile_app[i]),
                    "National-Trans": format_(National_Trans__mobile_app[i]),
                    "National-Value": format_(National_Value__mobile_app[i]),
#                     "n_users":format_(intra_cust__mobile_app[i]),                    
                    "International-Trans": format_(Inter_Trans__mobile_app[i]),
                    "International-Value": format_(Inter_Value__mobile_app[i]),
#                     "e_users":format_(inter_cust__mobile_app[i]),                    
                }
                for i in range(len(Trans_Type__mobile_app))
            ]+ [
                {
                    "Trans-Type": "Total",
                    "Total-Trans": format_(sum(Total_Trans__mobile_app)),
                    "Total-Value": format_(sum(Total_Value__mobile_app)),
#                     "Total-users": format_(sum(Total_users__mobile_app)),
                    "National-Trans": format_(sum(National_Trans__mobile_app)),
                    "National-Value": format_(sum(National_Value__mobile_app)),
#                     "n_users":format_(sum(intra_cust__mobile_app)),                    
                    "International-Trans": format_(sum(Inter_Trans__mobile_app)),
                    "International-Value": format_(sum(Inter_Value__mobile_app)),
#                     "e_users":format_(sum(inter_cust__mobile_app)),                    
                    
                }

            ],
            style_header={
                "backgroundColor": "DeepSkyBlue",
                'color': 'white',
                'fontWeight': 'bold',
            },
            style_data_conditional=[{
                "if": {"row_index": len(Total_Trans__mobile_app)},
                "backgroundColor": "DodgerBlue",
                'color': 'white'
            }],
            export_format='xlsx',
            export_headers='display',
            merge_duplicate_headers=True
        ),
        ######################################################################################
        html.H2("USSD", style={"margin":"15px 0px 10px 0px"},),
        dash_table.DataTable(
            id='ussd-data_table',
            columns=[
                {"name": ["", "Trans Type"], "id": "Trans-Type" },
                {"name": ["Total", "Number of Transactions"], "id": "Total-Trans", },
                {"name": ["Total", "Amount"], "id": "Total-Value", },
#                 {"name": ["Total", "Users"], "id": "Total-users", },
                {"name": ["National", "Number of Transactions"], "id": "National-Trans", },
                {"name": ["National", "Amount"], "id": "National-Value"},
#                 {"name":["National","#Users"],"id":"n_users"},                
                {"name": ["International", "Number of Transactions"], "id": "International-Trans"},
                {"name": ["International", "Amount"], "id": "International-Value"},
#                 {"name":["International","#Ex-Users"],"id":"e_users"},                
            ],
            data=[
                {
                    "Trans-Type": Trans_Type__ussd[i],
                    "Total-Trans": format_(Total_Trans__ussd[i]),
                    "Total-Value": format_(Total_Value__ussd[i]),
#                     "Total-users": format_(Total_users__ussd[i]),
                    "National-Trans": format_(National_Trans__ussd[i]),
                    "National-Value": format_(National_Value__ussd[i]),
#                     "n_users":format_(intra_cust__ussd[i]),                    
                    "International-Trans": format_(Inter_Trans__ussd[i]),
                    "International-Value": format_(Inter_Value__ussd[i]),
#                     "e_users":format_(inter_cust__ussd[i]),                    
                }
                for i in range(len(Trans_Type__ussd))
            ]+ [
                {
                    "Trans-Type": "Total",
                    "Total-Trans": format_(sum(Total_Trans__ussd)),
                    "Total-Value": format_(sum(Total_Value__ussd)),
#                     "Total-users": format_(sum(Total_users__ussd)),
                    "National-Trans": format_(sum(National_Trans__ussd)),
                    "National-Value": format_(sum(National_Value__ussd)),
#                     "n_users":format_(sum(intra_cust__ussd)),                    
                    "International-Trans": format_(sum(Inter_Trans__ussd)),
                    "International-Value": format_(sum(Inter_Value__ussd)),
#                     "e_users":format_(sum(inter_cust__ussd)),                    
                    
                }

            ],
            style_header={
                "backgroundColor": "DeepSkyBlue",
                'color': 'white',
                'fontWeight': 'bold',
            },
            style_data_conditional=[{
                "if": {"row_index": len(Total_Trans__ussd)},
                "backgroundColor": "DodgerBlue",
                'color': 'white'
            }],
            export_format='xlsx',
            export_headers='display',
            merge_duplicate_headers=True
        ),
        ######################################################################################
        html.H2("Push & Pull", style={"margin":"15px 0px 10px 0px"},),
        dash_table.DataTable(
            id='push_pull-data_table',
            columns=[
                {"name": ["", "Trans Type"], "id": "Trans-Type" },
                {"name": ["Total", "Number of Transactions"], "id": "Total-Trans", },
                {"name": ["Total", "Amount"], "id": "Total-Value", },
#                 {"name": ["Total", "Users"], "id": "Total-users", },
                {"name": ["National", "Number of Transactions"], "id": "National-Trans", },
                {"name": ["National", "Amount"], "id": "National-Value"},
                {"name": ["International", "Number of Transactions"], "id": "International-Trans"},
                {"name": ["International", "Amount"], "id": "International-Value"},
            ],
            data=[
                {
                    "Trans-Type": Trans_Type__push_pull[i],
                    "Total-Trans": format_(Total_Trans__push_pull[i]),
                    "Total-Value": format_(Total_Value__push_pull[i]),
#                     "Total-users": format_(Total_users__push_pull[i]),
                    "National-Trans": format_(National_Trans__push_pull[i]),
                    "National-Value": format_(National_Value__push_pull[i]),
                    "International-Trans": format_(Inter_Trans__push_pull[i]),
                    "International-Value": format_(Inter_Value__push_pull[i]),
                }
                for i in range(len(Trans_Type__push_pull))
            ]+ [
                {
                    "Trans-Type": "Total",
                    "Total-Trans": format_(sum(Total_Trans__push_pull)),
                    "Total-Value": format_(sum(Total_Value__push_pull)),
#                     "Total-users": format_(sum(Total_users__push_pull)),
                    "National-Trans": format_(sum(National_Trans__push_pull)),
                    "National-Value": format_(sum(National_Value__push_pull)),
                    "International-Trans": format_(sum(Inter_Trans__push_pull)),
                    "International-Value": format_(sum(Inter_Value__push_pull)),
                }
            ],
            style_header={
                "backgroundColor": "DeepSkyBlue",
                'color': 'white',
                'fontWeight': 'bold',
            },
            style_data_conditional=[{
                "if": {"row_index": len(Total_Trans__push_pull)},
                "backgroundColor": "DodgerBlue",
                'color': 'white',
                'fontWeight': 'bold',
            }],
            export_format='xlsx',
            export_headers='display',
            merge_duplicate_headers=True
        ),
    ])
]        
