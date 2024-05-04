from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output
import queries
import pandas as pd

app = Dash(__name__)

# get company data
#companies = queries.find_companies({}, {'_id': 0, 'ticker': 1, 'info': 1})

pipe = [
    {
        '$project': {
            '_id': 0,
            'ticker': 1,
            "marketCap": {"$arrayElemAt": ["$info.marketCap.Values", -1]},  # Retrieves the last marketCap value
            "shortName": {"$arrayElemAt": ["$info.shortName.Values", -1]},  # The shortName is the first element in the array
            "country": {"$arrayElemAt": ["$info.country.Values", -1]}, # The country is the first element in the array
            "sectorKey": {"$arrayElemAt": ["$info.sector.Values", -1]}, # The sector is the first element in the array
            "fullTimeEmployees": {"$arrayElemAt": ["$info.fullTimeEmployees.Values", -1]}, # The industry is the first element in the array
            "dividendYield": {"$arrayElemAt": ["$info.dividendYield.Values", -1]}, # The industry is the first element in the array
        }
    },
    {
        '$sort': {
            'dividendYield': -1
        }
    }
]

companies = queries.aggregate_companies(pipeline=pipe)
df = pd.DataFrame(list(companies))



app.layout = html.Div([
    html.H1('Company Data'),
    dcc.Dropdown(
        id='sector-filter',
        options=[{'label': sector, 'value': sector} for sector in df['sectorKey'].unique()],
        placeholder='Select a sector',
        value=None, # Default value
        multi=True  # Allow multiple selections
        ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        # style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'green',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {'if': {'column_id': 'dividendYield'},
             'backgroundColor': '#D2F3FF'}
        ],
        sort_action='native',
        filter_action='native',
        page_action='native',
        style_table={'overflowY': 'auto'},
        style_cell={'textAlign': 'left', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'},
        tooltip_data=[
            {column: {'value': str(value), 'type': 'markdown'}
             for column, value in row.items()} for row in df.to_dict('records')
        ],
        tooltip_duration=None
    )
])

@app.callback(
    Output('table', 'data'),
    [Input('sector-filter', 'value')]       
)
def update_table(selected_sectors):
    if not selected_sectors:
        return df.to_dict('records')
    filtered_df = df[df['sectorKey'].isin(selected_sectors)]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)