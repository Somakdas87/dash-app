######### import all libraries here ###########################
import dash

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


####### read the dataset #######################################
df = pd.read_csv('Sample_dataset.csv')

#=============================================================================
external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, 
                title='Sunthetics Data Science', 
                external_stylesheets=[external_stylesheets])
#app = dash.Dash(__name__, title='Sunthetics Data Science')
# =============================================================================
def height():
    return 500

N=len(df.index)
stp=int(height()/N)

#################### clean and transform data frame ###############
features = ['Variable-1', 
            'Variable-2', 
            'Variable-3', 
            'Variable-4', 
            'Variable-5']
x = df.loc[:, features].values
y = df.loc[:,['Output']].values
x = StandardScaler().fit_transform(x)


#################### principal component analysis ###########
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['first_principal_component', 
                          'second_principal_component'])

finalDf = pd.concat([df, principalDf], axis = 1)
# finalDf contains the pricipal component analysis along with output column
fig_pca = px.scatter(finalDf, 
                     x='first_principal_component',                        
                     y='second_principal_component', 
                     color='Output',
                     template='plotly_dark',
                     hover_data=features)


####### Application's html layout #####################################
app.layout = html.Div([
    
    html.Div([
        
        html.Div([dcc.Graph(id='graph-with-slider')
                  ], style={'width':'45%', 
                            'display':'inline-block', 
                            'padding':10}        
                 ),        
        
        
        html.Div([dcc.Graph(id='pca-graph', 
                            figure=fig_pca)
                 ], style={'width':'45%', 
                            'display':'inline-block', 
                            'padding':10,
                            }        
                 )
        ]
        ),
    
    
    html.Br(),
    
    html.Div([
        dcc.Slider(
            id='year-slider-1',
            min=df['Variable-4'].min(),
            max=df['Variable-4'].max(),
            value=df['Variable-4'].min(),
            marks={str(df['Variable-4'][i]): str(df['Variable-4'][i]) 
                   for i in range(1,len(df['Variable-4'].unique())+1)},
            step=None,
# =============================================================================
#             vertical=True,
#             verticalHeight=height()
# =============================================================================
        ),
        html.Div(id='slider-1-container',
                 style={'color':'white'})
        ], style={'align-items':'center', 
                  'justify-content':'center',
                  'fontColor':'blue'}
        ),
    
    html.Br(),
    html.Div([
        dcc.Slider(
            id='year-slider-2',
            min=df['Variable-5'].min(),
            max=df['Variable-5'].max(),
            value=df['Variable-5'].min(),
            marks={str(val): str(val) for val in df['Variable-5'].unique()},
            step=None,
# =============================================================================
#             vertical=True,
#             verticalHeight=height()
# =============================================================================
        ),
        html.Div(id='slider-2-container',
                 style={'color':'white'})
        ], style={'align-items':'center',
                  'justify-content':'center', 
                  'fontColor':'blue'}
        )        
], style={'backgroundColor':'rgb(17,17,17)'}
)


####### Callbacks in response to user activity ##########################
@app.callback(
    [Output('slider-1-container', 'children'),
    Output('slider-2-container', 'children'),
    Output('graph-with-slider', 'figure')
    ],
    [
         Input('year-slider-1', 'value'),
         Input('year-slider-2', 'value')
    ]
)
def update_slider(var4, var5):
    filtered_df = df[df['Variable-4'] == var4]
    filtered_df = filtered_df[filtered_df['Variable-5'] == var5]
    fig = px.scatter_3d(filtered_df, 
                        x="Variable-1", 
                        y="Variable-2", 
                        z="Variable-3", 
                        color="Output",
                        size="Output"
                        )
    fig.update_layout(transition_duration=500)
        
    fig.update_layout(
        #height=500, 
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        #hovermode='closest',
        template='plotly_dark'
    )
    
    container1='Variable-4 = {}'.format(var4)
    container2='Variable-5 = {}'.format(var5)
    
    return container1, container2, fig


if __name__ == '__main__':
    app.run_server(debug=False)
