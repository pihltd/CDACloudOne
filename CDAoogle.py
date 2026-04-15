import cdapython
import dash
from dash import html, dcc, dash_table, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import io


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

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    update_title="Updating..."
)
app.title ="CDAoogle"




#######################################
#                                     #
#       Subroutines                   #
#                                     #
#######################################

def buildDataTable(df, page_current, page_size):

    return  dash_table.DataTable(
        id = 'pagingDataTable',
        columns=[{"name": e, "id": e} for e in (df.columns)],
        data=df.to_dict('records'),
        page_current=page_current,
        page_size=page_size,
        page_action='custom',
        style_table={'overflowX':'auto'},
        style_cell={'overflow':'hidden', 'textOverflow':'ellipsis', 'maxWidth':10, 'textAlign':'center'},
        style_data={'color':'black', 'backgroundColor':'white'},
        style_data_conditional=[{'if':{'row_index':'odd'}, 'backgroundColor': 'rgb(220,220,220)'}],
        style_header={'backgroundColor': 'rgb(210,210,210)', 'color':'black', 'fontWeight':'bold', 'textAlign':'center'},
        tooltip_data=[
            {
                column:{'value': str(value), 'type':'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_duration=None,
        export_format="csv"

        )



def buildMarkdownString(dfsize, current, pagesize):
    print(f"Dataframe size: {dfsize}\tCurrent Page: {current}\t Page Size: {pagesize}")
    totalpages = round(dfsize/pagesize)
    if current >= 1:
        currentend = (current+1)*pagesize
        if currentend > dfsize:
            currentend = dfsize
        currentstart = (current)*pagesize
        current = current+1
    else:
        currentend = pagesize
        currentstart = 1
        current = 1

    return f"Showing results **{currentstart}** through **{currentend}** of **{dfsize}** and Page **{current}** of **{totalpages}**"


############################################
#                                          #
#             Components                   #
#                                          #
############################################

#table_df = pd.DataFrame([{"One": 1, "Two": 2}])
PAGE_SIZE=25

searchbox = dbc.Input(id="searchterms", placeholder="Enter search terms.....", type="text")
gobutton = dbc.Button("Search CRDC", id='gobutton')

resultcontent = html.Div([
    dcc.Loading(
        id="tableloading",
        children= [html.Div(id="resultsgohere")],
        type="circle"
    )
])



# https://dash.plotly.com/datatable/callbacks

####################################
#                                  #
#         Layouts                  #
#                                  #
####################################

app.layout = html.Div([
    dcc.Store(id='querystore', storage_type='memory'),
    html.Div([
        html.Hr(),
        html.H1("CDAoogle", id="sitetitle"),
        html.Hr()
    ], style={'textAlign': 'center'}),
    html.Center(
        html.Div([
            searchbox
        ], style={'width': '80%'})
    ),
    html.Div([
        html.Hr(),
        html.Hr(),
        gobutton
    ], style={'textAlign':'center'}),
    html.Div([
        dcc.Markdown(id='markdowntext',children='')
    ]),
    html.Div([
        html.Div(resultcontent, style={'width':'80%', 'marginLeft':'auto', 'marginRight':'auto'} )
    ])
])


####################################
#                                  #
#         Callbacks                #
#                                  #
####################################


@app.callback(
    Output("resultsgohere", "children", allow_duplicate=True),
    Input("querystore", "data"),
)
def updateTable(data):
    current = 0
    size = PAGE_SIZE
    res_df = pd.read_json(io.StringIO(data), orient='split')
    display_df = res_df.iloc[current*size:(current+1)*size]
    return buildDataTable(display_df, 0, PAGE_SIZE)


@app.callback(
    Output("resultsgohere", "children", allow_duplicate=True),
    Input("pagingDataTable", "page_current"),
    Input("pagingDataTable", "page_size"),
    State("querystore", "data")
)
def pageTable(page_current, page_size, data):
    res_df = pd.read_json(io.StringIO(data), orient='split')
    display_df = res_df.iloc[page_current*page_size:(page_current+1)*page_size]
    return buildDataTable(display_df, page_current, page_size)



@app.callback(
        Output("querystore", "data"),
        Input("gobutton", "n_clicks"),
        State("searchterms", "value")
)
def searchIt2(gobutton, searchterms):
    table_df = cdapython.get_subject_data(searchterms, add_columns=["diagnosis","morphology", "observed_anatomic_site"],return_data_as='dataframe')
    if table_df is not None:
        table_df = table_df.astype(str)
        return table_df.to_json(orient='split')
    else:
        return pd.DataFrame([{"Result":"No Data Returned"}]).to_json(orient='split')
        print(f"Query Error: {table_df}")

@app.callback(
    Output("markdowntext", "children", allow_duplicate=True),
    Input("querystore", "data"),
    #State("pagingDataTable", "page_current")
)
def displayResultCount(data):
    res_df = pd.read_json(io.StringIO(data), orient='split')
    return buildMarkdownString(len(res_df), 0, PAGE_SIZE)


@app.callback(
    Output("markdowntext", "children", allow_duplicate=True),
    Input("pagingDataTable", "page_current"),
    State("querystore", "data")
)
def updateResultCount(current, data) :
    res_df = pd.read_json(io.StringIO(data), orient='split')
    return buildMarkdownString(len(res_df), current, PAGE_SIZE)


####################################
#                                  #
#         Run Program              #
#                                  #
####################################


if __name__ == "__main__":
    app.run(port=8050, debug=True)