# Import packages
import dash
from dash import Dash, html, dcc, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import pandas as pd
import plotly.express as px
from dash.dependencies import State

from mysql_utils import get_distinct_universities, get_total_faculty, get_total_publications, get_top_RIs, get_facs_given_RI, get_all_RIs, get_top_kws, add_favorite_faculty, remove_favorite_faculty, view_favorite_faculty, add_favorite_keyword, remove_favorite_keyword, view_favorite_keyword, get_uni_imgs
from neo4j_utils import get_all_faculty, get_co_publications, get_publications_per_year
from mongodb_utils import get_fac_from_kw, get_pubs_from_fac
from ratemyprofessor import get_university_ratings

selected_university = ""

colors = {
    'one': '#223030',
    'two': '#523D35',
    'three': '#959D90', 
    'four': '#BBA58F', 
    'five': '#E8D9CD', 
    'six': '#EFEFE9',
    'seven': '#44576D',
}

# Initialize the app
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    # Title and description
    dbc.Row([
        html.H1("University and Faculty Performance Dashboard",
                style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 40}),
        html.H5("An interactive dashboard to help you explore the performance of universities and faculty members by providing visualizations and metrics",
                style={'textAlign': 'center', 'color': colors["one"], 'fontSize': 10}),
    ], align="center", justify="center"),

    # first row - university selection
    dbc.Row([
        html.H3('Select an University', style={'textAlign': 'left', 'color': colors["two"], 'fontSize': 20}),
        dcc.Dropdown(get_distinct_universities(), '', id='demo-dropdown', style={'color': colors["one"]}),
        html.Div(id='uni-output')
    ], align="left", justify="left", style={'border': '1mm ridge rgba(149, 157, 144)'}),

    # second row - university logo, statistics from ratemyprofessor.com, co-publications graph
    dbc.Row([
        dbc.Col([
            html.Img(id='uni-image', width="400", height="200"),
            html.Div(id='faculty-count', style={'border': '0.5mm ridge rgba(149, 157, 144)'}),
            html.Div(id='publication-count', style={'border': '0.5mm ridge rgba(149, 157, 144)'})
        ], style={'border': '1mm ridge rgba(149, 157, 144)'}),
        dbc.Col([
            html.H3("University Statistics (pulled from ratemyprofessor.com)",
                style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 20}),
            html.Div(id='uni-stats', style={'color': colors["two"]})
        ], style={'border': '1mm ridge rgba(149, 157, 144)'}),
        dbc.Col([
            html.H3('Explore co-publications of a faculty member',
             style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 20}),
            dcc.Dropdown(get_all_faculty(selected_university), '', id='fac_dropdown', placeholder='Select a faculty member'), 
            html.Div(id='fac-selection-neo4j'),
            cyto.Cytoscape(
                id='co-pubs-graph',
                style={'width': '100%', 'height': '400px'},
                elements=[]
            )
        ], style={'border': '1mm ridge rgba(149, 157, 144)'})
    ]),

    # third row - keywords graph, keywords search
    dbc.Row([
        dbc.Col([
            html.Div(id='kw-bar-container', style={'display': 'none'}),
            html.Div(id='kw-bar', children=[])
        ], style={'border': '1mm ridge rgba(149, 157, 144)'}),
        dbc.Col([
            html.Div([
                html.H3('See Faculty Members associated with a keyword', style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 20}),
                dcc.Input(id='keyword-input', type='text', placeholder='Search for a keyword', style={'width': 500}),
                html.Button('Search', id='search-button', n_clicks=0),
                html.Div(id='search-results')
            ])
        ], style={'border': '1mm ridge rgba(149, 157, 144)'})
    ]),

    # fourth row - publications by faculty, publications graph
    dbc.Row([
        dbc.Col([
            html.H3('See all Publications by a Faculty Member', style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 20}),
            dcc.Dropdown(get_all_faculty(selected_university), '', id='fac_dropdown2', placeholder='Select a faculty member'), 
            html.Button('Search', id='search-button2', n_clicks=0),
            html.Div(id='publication-list-container')
        ], style={'border': '1mm ridge rgba(149, 157, 144)'}),
        dbc.Col([
            html.Div(id='publications-per-year-container', style={'display': 'none'}),
            html.Div(id='publications-per-year-graph', children=[])
        ], style={'border': '1mm ridge rgba(149, 157, 144)'})
    ]),

    # fifth row - research interests graph, research interests search 
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div(id='research-interests-bar-container', style={'display': 'none'}),
                html.Div(id='research-interests-bar', children=[])
            ])
        ], style={'border': '1mm ridge rgba(149, 157, 144)'}),
        dbc.Col([
            html.H3('See Faculty Members associated with each Research Interest', style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 20}),
            dcc.Dropdown(id='ri-dropdown', placeholder='Select a research interest'),
            html.Div(id='faculty-RI-container')
        ], style={'border': '1mm ridge rgba(149, 157, 144)'})
    ]),

    # sixth row - save results section
    dbc.Row([
        html.H3('Save your results for next time', style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 20}),
        html.H5('Enter your name to save your favorite faculty members or keywords at this university!',
                style={'textAlign': 'center', 'color': colors["one"], 'fontSize': 15}),
        dcc.Input(id='user-name-input', type='text', placeholder='Enter your name'),
        dbc.Col([
            dcc.Dropdown(get_all_faculty(selected_university), '', id='fac_dropdown3', placeholder='Pick a faculty to Add/Delete'),
            html.Button('Add to Favorites', id='add-fac-button', n_clicks=0),
            html.Button('Remove from Favorites', id='delete-fac-button', n_clicks=0),
            html.Button('View My Favorites', id='view-fac-button', n_clicks=0),
            html.Div(id='favorite-fac-results'),
        ]),
        dbc.Col([
            dcc.Input(id='keyword-add-delete-input', type='text', placeholder='Search for a keyword to Add/Delete', style={'width': 700}),
            html.Button('Add to Favorites', id='add-kw-button', n_clicks=0),
            html.Button('Remove from Favorites', id='delete-kw-button', n_clicks=0),
            html.Button('View My Favorites', id='view-kw-button', n_clicks=0),
            html.Div(id='favorite-kw-results')
        ])
    ], style={'border': '1mm ridge rgba(149, 157, 144)'})
], style={'backgroundColor': colors["six"]}) 


# Callback to update selected university
@app.callback(
    Output('uni-output', 'children'),
    Input('demo-dropdown', 'value')
)
def store_uni_callback(value):
    global selected_university
    selected_university = value
    return html.Div(f"Selected University: {selected_university}")

# Callback to update faculty count
@app.callback(
    Output('faculty-count', 'children'),
    Input('demo-dropdown', 'value')
)
def update_faculty_count(value):
    faculty_count = get_total_faculty(selected_university)
    return html.Div(f"Total Faculty in Database: {faculty_count}", style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 25})

# Callback to update publication count
@app.callback(
    Output('publication-count', 'children'),
    Input('demo-dropdown', 'value')
)
def update_publication_count(value):
    publication_count = get_total_publications(selected_university)
    return html.Div(f"Total Publications Across Faculty: {publication_count}", style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 25})

# Callback to update university ratings (pulled from ratemyprofessor.com)
@app.callback(
    Output('uni-stats', 'children'),
    Output('uni-image', 'src'),
    Input('demo-dropdown', 'value')
)
def update_faculty_count(selected_university):
    if selected_university:
        stats = get_university_ratings(selected_university)
        stats_divs = [html.Div(f"{key}: {value}", style={'textAlign': 'center', 'color': colors["two"], 'fontSize': 20}) for key, value in stats.items()]
        image_url = get_uni_imgs(selected_university)
        return stats_divs, image_url
    else:
        # If no university is selected, return empty content
        return [], ''

# Callback to update all faculty dropdowns
@app.callback(
    Output('fac_dropdown', 'options'),
    Output('fac_dropdown2', 'options'),
    Output('fac_dropdown3', 'options'),
    Input('demo-dropdown', 'value')
)
def update_faculty_dropdown(selected_university):
    faculty_options = get_all_faculty(selected_university)
    return faculty_options, faculty_options, faculty_options

# Callback to update cytoscape elements
@app.callback(
    Output('co-pubs-graph', 'elements'), 
    Input('fac_dropdown', 'value')
)
def update_cytoscape_elements(selected_faculty):
    if not selected_faculty:
        return []  
    
    co_pubs = get_co_publications(selected_faculty)
    return co_pubs


# Callback for searching keyword and getting faculty members
@app.callback(
    Output('search-results', 'children'),
    Input('search-button', 'n_clicks'),
    State('keyword-input', 'value'),
    State('demo-dropdown', 'value')
)
def perform_keyword_search(n_clicks, keyword, university):
    if n_clicks > 0 and keyword:
        result = get_fac_from_kw(university, keyword)
        df = pd.DataFrame(result)
        
        table = dash_table.DataTable(
            id='table',
            columns=[
                {"name": "Name", "id": "_id"},
                {"name": "Email", "id": "email"},
                {"name": "Position", "id": "position"}
            ],
            data=df.to_dict('records'),
            page_size=10,
            style_data_conditional=[
                {
                    'if': {'column_id': '_id'},
                    'textDecoration': 'underline',
                    'textDecorationStyle': 'dotted',
                }
            ],
            tooltip_data=[
                {
                    '_id': {
                        'value': 'Faculty Image\n\n![Image]({})'.format(record['photoUrl']),
                        'type': 'markdown'
                    }
                } for record in result
            ],
            tooltip_delay=0,
            tooltip_duration=None,
            style_data={'whiteSpace': 'normal','height': 'auto',}, fill_width=False
        )
        
        return table
    else:
        return html.Div()


# Callback to update research interests bar graph
@app.callback(
    Output('research-interests-bar-container', 'style'),
    Output('research-interests-bar', 'children'),
    Input('demo-dropdown', 'value')
)
def update_research_interests_bar(selected_university):
    if selected_university:
        top_RIs = get_top_RIs(selected_university)
        
        if not top_RIs:
            # If top_RIs is empty, display message   
            return {'display': 'block'}, f"No data available for the Research Interests of Faculty at {selected_university}"
        
        RIs = [ri[0] for ri in top_RIs]
        counts = [ri[1] for ri in top_RIs]
        
        try: 
            fig = px.bar(top_RIs, x=counts, y=RIs, orientation='h', labels={'x': 'Count', 'y': 'Research Interest'}, title=f'Top 10 Research Interests by Faculty at {selected_university}', color_discrete_sequence =[colors["seven"]]*10)
        except:
            fig = px.bar(top_RIs, x=counts, y=RIs, orientation='h', labels={'x': 'Count', 'y': 'Research Interest'}, title=f'Top 10 Research Interests by Faculty at {selected_university}', color_discrete_sequence =[colors["seven"]]*10)

        return {'display': 'block'}, dcc.Graph(figure=fig)
    else:
        return {'display': 'none'}, None


# Callback to update dropdown options for research interests
@app.callback(
    Output('ri-dropdown', 'options'),
    Input('demo-dropdown', 'value')
)
def update_ri_dropdown(selected_university):
    if selected_university:
        top_RIs = get_all_RIs(selected_university)
        if top_RIs:
            return [{'label': ri[0], 'value': ri[0]} for ri in top_RIs]
    return []

# Callback to update faculty details based on selected research interest
@app.callback(
    Output('faculty-RI-container', 'children'),
    Input('ri-dropdown', 'value'),
    Input('demo-dropdown', 'value')
)
def update_faculty_details(selected_ri, selected_university):
    top_RIs = get_top_RIs(selected_university)
    if not top_RIs:
        return f"No data available for the Research Interests of Faculty at {selected_university}"
    if selected_ri and selected_university:
        faculty_details = get_facs_given_RI(selected_university, selected_ri)
        if faculty_details:
            df = pd.DataFrame(faculty_details, columns=['Name', 'Position', 'Photo'])
            
            table = dash_table.DataTable(
                id='faculty-table',
                columns=[
                    {"name": "Name", "id": "Name", "presentation": "markdown"},
                    {"name": "Position", "id": "Position"}
                ],
                data=df.to_dict('records'), page_size=10,
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                tooltip_data=[
                    {
                        'Name': {
                            'value': f"![Image]({row['Photo']})",
                            'type': 'markdown'
                        }
                    } for _, row in df.iterrows()
                ],
                tooltip_delay=0,
                tooltip_duration=None
            )
            return table
    return html.Div()


# Callback to update publications per year graph
@app.callback(
    Output('publications-per-year-container', 'style'),
    Output('publications-per-year-graph', 'children'),
    Input('demo-dropdown', 'value')
)
def update_publications_per_year_graph(selected_university):
    if selected_university:
        publications_per_year = get_publications_per_year(selected_university)
        try:
            fig1 = px.bar(publications_per_year, x='year', y='count', labels={'year': 'Year', 'count': 'Number of Publications'}, color_discrete_sequence =[colors["seven"]]*len(publications_per_year))
        except:
            fig1 = px.bar(publications_per_year, x='year', y='count', labels={'year': 'Year', 'count': 'Number of Publications'}, color_discrete_sequence =[colors["seven"]]*len(publications_per_year))

        fig1.update_layout(title=f'Number of Publications per Year at {selected_university}')
        fig1.update_layout(xaxis=dict(range=[publications_per_year['year'].min(), publications_per_year['year'].max()]))
        return {'display': 'block'}, dcc.Graph(figure=fig1)
    else:
        return {'display': 'none'}, None

# Callback for searching publications based on faculty members
@app.callback(
    Output('publication-list-container', 'children'),
    Input('search-button2', 'n_clicks'),
    State('fac_dropdown2', 'value'),
    State('demo-dropdown', 'value')
)
def update_publication_list(n_clicks, selected_faculty, selected_university):
    if n_clicks >0 and selected_faculty and selected_university:
        publications = get_pubs_from_fac(selected_university, selected_faculty)
        if publications:
            publications_html = html.Div([
                html.H3("Publications by Selected Faculty Member"),
                dash_table.DataTable(
                    id='publication-table',
                    columns=[
                        {'name': 'Publication ID', 'id': 'Publication ID'},
                        {'name': 'Title', 'id': 'Title'},
                        {'name': 'Number of Citations', 'id': 'Number of Citations'},
                        {'name': 'Year', 'id': 'Year'}
                    ],
                    data=publications, page_size=5, style_data={'whiteSpace': 'normal','height': 'auto','overflowX': 'auto'}, fill_width=False
                )
            ])
            return publications_html
    else:
        return html.Div()
    
# Callback to update top keywords graph
@app.callback(
    Output('kw-bar-container', 'style'),
    Output('kw-bar', 'children'),
    Input('demo-dropdown', 'value')
)
def update_kw_bar(selected_university):
    if selected_university:
        top_kws = get_top_kws(selected_university)
        
        if not top_kws:
            return {'display': 'block'}, {}
        
        KWs = [kw[0] for kw in top_kws]
        counts = [kw[1] for kw in top_kws]
        try:
            fig3 = px.bar(x=counts, y=KWs, orientation='h', labels={'x': 'Count', 'y': 'Keyword'}, title=f'Top 10 keywords at {selected_university}', color_discrete_sequence =[colors["seven"]]*10)
        except:
            fig3 = px.bar(x=counts, y=KWs, orientation='h', labels={'x': 'Count', 'y': 'Keyword'}, title=f'Top 10 keywords at {selected_university}', color_discrete_sequence =[colors["seven"]]*10)

        return {'display': 'block'}, dcc.Graph(figure=fig3)
    else:
        return {'display': 'none'}, None


# Callback to handle adding, removing, and viewing favorite faculty members
@app.callback(
    Output('favorite-fac-results', 'children'),
    [Input('add-fac-button', 'n_clicks'),
     Input('delete-fac-button', 'n_clicks'),
     Input('view-fac-button', 'n_clicks')],
    [State('user-name-input', 'value'),
     State('fac_dropdown3', 'value')],
     State('demo-dropdown', 'value'),
    prevent_initial_call=True
)
def manage_favorite_faculty(add_clicks, delete_clicks, view_clicks, user_name, fac_name, uni):
    ctx = dash.callback_context
    triggered_button = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_button == 'add-fac-button':
        add_favorite_faculty(user_name, uni, fac_name)
        return f"{fac_name} has been added to your favorites!"
    
    elif triggered_button == 'delete-fac-button':
        remove_favorite_faculty(user_name, uni, fac_name)
        return f"{fac_name} has been removed from your favorites!"
    
    elif triggered_button == 'view-fac-button':
        favorites = view_favorite_faculty(user_name, uni)
        if favorites:
            df = pd.DataFrame(favorites, columns=['user_name', 'uni', 'fac_name'])
            datatable = dash_table.DataTable(
                id='favorite-faculty-table',
                columns=[{'name': col, 'id': col} for col in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
            )
            return html.Div([
                html.H3("Your Favorite Faculty Members:"),
                datatable
            ])
        else:
            return "You haven't saved any favorite faculty members yet!"

# Callback to handle adding, removing, and viewing favorite keywords
@app.callback(
    Output('favorite-kw-results', 'children'),
    [Input('add-kw-button', 'n_clicks'),
     Input('delete-kw-button', 'n_clicks'),
     Input('view-kw-button', 'n_clicks')],
    [State('user-name-input', 'value'),
     State('keyword-add-delete-input', 'value')],
     State('demo-dropdown', 'value'),
    prevent_initial_call=True
)
def manage_favorite_keywords(add_clicks, delete_clicks, view_clicks, user_name, keyword, uni):
    ctx = dash.callback_context
    triggered_button = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_button == 'add-kw-button':
        add_favorite_keyword(user_name, uni, keyword)
        return f"{keyword} has been added to your favorites!"
    
    elif triggered_button == 'delete-kw-button':
        remove_favorite_keyword(user_name, uni, keyword)
        return f"{keyword} has been removed from your favorites!"
    
    elif triggered_button == 'view-kw-button':
        favorites = view_favorite_keyword(user_name, uni)
        if favorites:
            df = pd.DataFrame(favorites, columns=['user_name', 'uni', 'keyword'])
            datatable = dash_table.DataTable(
                id='favorite-keywords-table',
                columns=[{'name': col, 'id': col} for col in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
            )
            return html.Div([
                html.H3("Your Favorite Keywords:"),
                datatable
            ])
        else:
            return "You haven't saved any favorite keywords yet!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
