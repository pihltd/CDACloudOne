from cdapython import *
import pandas as pd
import json
import io

from dash import html, dcc, dash_table, Output, Input, State, Dash
import dash_bootstrap_components  as dbc
import plotly.express as px


#######################################
#                                     #
#       App Definition                #
#                                     #
#######################################

external_stylesheets = [
    {  "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    dbc.themes.BOOTSTRAP
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    update_title="Updating..."
)
app.title ="Submission Dashboard"


############################################
#                                          #
#                 Styles                   #
#                                          #
############################################

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1 rem",
    "background-color": "#f8f9fa"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "12rem",
    "padding": "2rem 1 rem"
}

SELECTED_TAB_STYLE = {
    'borderTop': '2px solid #000204',
    'borderBottom': '2px solid #000204',
    'backgroundColor': '#0d7cf5',
    'color': 'white',
    'padding': '6px'
}

TAB_STYLE = {
    'borderBottom': '2px solid #000204',
    'padding': '6px',
    'fontWeight': 'bold'
}

#######################################
#                                     #
#       Subroutines                   #
#                                     #
#######################################

def subjectDistribution():
    subject_dict = summarize_subjects(return_data_as='dict')
    return subject_dict['data_source']


############################################
#                                          #
#             Components                   #
#                                          #
############################################

subjectdistpie = html.Div(
    [
    html.Div(
        #Subject  Pie Chart
        className='SubjectDistributionPieChart',
        children=[
            html.Hr(),
            html.H2("Subject Distribution", id='subjectdisttitle'),
            dcc.Graph(id='subjectDistributionPie')
        ],
        style={'width':'49%', 'display':'inline-block'}
    )
    ]
)

filedistpie = html.Div(
    [
    html.Div(
        #File Distributaion Pie Chart
        className='FileDistributionPieChart',
        children=[
            html.Hr(),
            html.H2("File Distribution", id='filedisttitle'),
            dcc.Graph(id='fileDistributionPie')
        ],
        style={'width':'49%', 'display':'inline-block'}
    )
    ]
)

anatomicsitepie = html.Div(
    [
    html.Div(
        #Anatomic Site Pie Chart
        # This would benefit from using slim terms
        className='AnatomicDistributionPieChart',
        children=[
            html.Hr(),
            html.H2("Anatomic Site Distribution", id='anatomictitle'),
            dcc.Graph(id='anatomicDistributionPie')
        ],
        style={'width':'49%', 'display':'inline-block'}
    )
    ]
)

radiobutton = html.Div([
    dcc.RadioItems(
        ["Graphs", "Tables"], "Graphs",
        id="graphtableradio",
        inline=True
        )
])

gobutton = html.Div([
    dbc.Button("Get Data", id='gobutton')

])

####################################
#                                  #
#         Layouts                  #
#                                  #
####################################

app.layout = html.Div([
    dcc.Store(id="subjectsummary"),
    dcc.Store(id="filesummary"),
    html.Div([gobutton]),
    html.Div([filedistpie, subjectdistpie]),
    html.Div([anatomicsitepie])
])


####################################
#                                  #
#         Callbacks                #
#                                  #
####################################
@app.callback(
    Output("subjectsummary", "data"),
    Input("gobutton", "n_clicks")
)
def populateSubjectSummaryStore(value):
    return json.dumps(summarize_subjects(return_data_as='dict'))

@app.callback(
    Output("filesummary", "data"),
    Input("gobutton", "n_clicks")
)
def populateFileSummaryStore(value):
    return json.dumps(summarize_files(return_data_as='dict')) 




@app.callback(
    Output("subjectDistributionPie", "figure"),
    Input("subjectsummary", "data")
)
def subjectDistPie(data):
    subjectjson = json.loads(data)
    sub_dict = subjectjson['data_source']
    sub_df = pd.DataFrame.from_dict({"DataCommons":sub_dict.keys(), "Subject Count":sub_dict.values()})
    return px.pie(sub_df,values="Subject Count", names="DataCommons")



@app.callback(
    Output("fileDistributionPie", "figure"),
    Input("filesummary", "data")
)
def fileDistPie(data):
    filejson = json.loads(data)
    file_dict = filejson['data_source']
    file_df = pd.DataFrame.from_dict({"Data Commons": file_dict.keys(), "File Count":file_dict.values()})
    return px.pie(file_df, values="File Count", names="Data Commons")

@app.callback(
    Output("anatomicDistributionPie", "figure"),
    Input("filesummary", "data")
)
def anatomicDistPie(data):
    filejson = json.loads(data)
    file_dict = filejson['anatomic_site']
    file_df = pd.DataFrame.from_dict({"Anatomic Site":file_dict.keys(), "Count":file_dict.values()})
    return px.pie(file_df, values="Count", names="Anatomic Site" )

####################################
#                                  #
#         Run Program              #
#                                  #
####################################


#app.run_server(port=8050, debug=True)
if __name__ == "__main__":
    app.run(port=8050, debug=True)