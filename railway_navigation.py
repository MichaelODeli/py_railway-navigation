graph_type = 'full' # or 'simple'

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
# import taxicab as tc
import plotly.graph_objects as go
import osmnx as ox
import networkx as nx
import datetime
ox.settings.log_console=True
ox.settings.max_query_area_size=50000000000
# ox.settings.use_cache=True
# ox.settings.cache_folder='C:/Users/MichaelODeli/OneDrive/DEVELOP/work/Python/projects/py_railway_navigation/osmnx_cache'

def node_list_to_path(G, node_list):
    """
    Given a list of nodes, return a list of lines that together
    follow the path
    defined by the list of nodes.

    Parameters
    ----------
    G : networkx multidigraph
    route : list
        the route as a list of nodes

    Returns
    -------
    lines : list of lines given as pairs ( (x_start, y_start), 
    (x_stop, y_stop) )
    """
    edge_nodes = list(zip(node_list[:-1], node_list[1:]))
    lines = []
    for u, v in edge_nodes:
        # if there are parallel edges, select the shortest in length
        data = min(G.get_edge_data(u, v).values(), 
                   key=lambda x: x['length'])
        # if it has a geometry attribute
        if 'geometry' in data:
            # add them to the list of lines to plot
            xs, ys = data['geometry'].xy
            lines.append(list(zip(xs, ys)))
        else:
            # if it doesn't have a geometry attribute,
            # then the edge is a straight line from node to node
            x1 = G.nodes[u]['x']
            y1 = G.nodes[u]['y']
            x2 = G.nodes[v]['x']
            y2 = G.nodes[v]['y']
            line = [(x1, y1), (x2, y2)]
            lines.append(line)
    return lines

def plot_path(route, origin_point, destination_point, mode, G, way_stations=[]):
    
    """
    Given a list of latitudes and longitudes, origin 
    and destination point, plots a path on a map
    
    Parameters
    ----------
    route: node's route
    origin_point, destination_point: co-ordinates of origin
    and destination
    mode: simple or full
    G: graph

    Returns
    -------
    Nothing. Only shows the map.
    """

    if mode == 'simple':
        long = [] 
        lat = []  
        for i in route:
            point = G.nodes[i]
            long.append(point['x'])
            lat.append(point['y'])
    elif mode == 'full':
        lines = node_list_to_path(G, route)
        long = []
        lat = []
        for i in range(len(lines)):
            z = list(lines[i])
            l1 = list(list(zip(*z))[0])
            l2 = list(list(zip(*z))[1])
            for j in range(len(l1)):
                long.append(l1[j])
                lat.append(l2[j])
    else:
        raise ValueError('mode not equals to "full" or "simple"')
    # adding the lines joining the nodes
    fig = go.Figure(go.Scattermapbox(name = "Path", mode = "lines", lon = long, lat = lat, marker = {'size': 10}, line = dict(width = 3, color = 'blue')))
    # adding source marker
    fig.add_trace(go.Scattermapbox(name = "Source", mode = "markers", lon = [origin_point[1]], lat = [origin_point[0]], marker = {'size': 12, 'color':"red"}))
     
    # adding destination marker
    fig.add_trace(go.Scattermapbox(name = "Destination", mode = "markers", lon = [destination_point[1]], lat = [destination_point[0]], marker = {'size': 12, 'color':'green'}))
    
    # if way_stations!=[]:
    #     for name_way, lat_way, lon_way in way_stations:
    #         fig.add_trace(go.Scattermapbox(name = name_way, mode = "markers+text", lon = [lon_way], lat = [lat_way], marker = {'size':20, 'color': 'black'}, text=name_way, textposition = "bottom right"))

    # getting center for plots:
    lat_center = np.mean(lat)
    long_center = np.mean(long)
    # defining the layout using mapbox_style
    fig.update_layout(mapbox_style="open-street-map", mapbox_center_lat = 30, mapbox_center_lon=-80)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      mapbox = {
                          'center': {'lat': lat_center, 
                          'lon': long_center},
                          'zoom': 13})
    return fig

if graph_type == 'full':
    G = ox.load_graphml("full_svzd_graph.graphml")
elif graph_type == 'simple':
    G = ox.load_graphml("simple_svzd_graph.graphml")
else: 
    raise ValueError('Incorrect graph_type provided. Supported only "simple" and "full" graphs')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

stations_df = pd.read_csv('all_stations/RU_stations_new.csv', sep='\t', encoding='utf-8')
stations_df = stations_df[stations_df["name"].str.contains(" км") == False]
stations_df['name_with_region'] = stations_df["name"] + ' (' + stations_df["region"] + ')'
stations_df = stations_df[stations_df["region"] == "Свердловская область"]

neighb_df = pd.read_csv('all_stations/svzd_sosedi.csv', sep=';')
neighb_df = neighb_df.sort_values(by='from_esr')
G_st = nx.Graph()
G_st.add_nodes_from(list(stations_df.esr))
G_st.add_edges_from(neighb_df.values.tolist())

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([dcc.Graph(id='mapbox', style={'height': '750px'})], style={'height': '750px'}), 
    
    html.Div([
        html.Div([html.P('From station'), dcc.Dropdown(stations_df['name_with_region'].sort_values(), 'Исеть (Свердловская область)', id='from-station-name')], style={'padding': '0 0 10px 0'}),
        html.Div([html.P('To station'), dcc.Dropdown(stations_df['name_with_region'].sort_values(), 'Нижний Тагил (Свердловская область)', id='to-station-name')], style={'padding': '0 0 10px 0'})
    ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div([html.H3('Route statistics', style={'margin': '10px 0 0 0'}),
        html.P('Total length (km) - ', id='total_way_length'),
        html.P('Total segments - ', id='total_points'),
    ])], style={'width': '40%', 'display': 'inline-block', 'margin': '0 auto', 'padding': '0 0 0 10px'}),
])

@app.callback(
    [Output('mapbox', 'figure'), Output('total_way_length', 'children'), Output('total_points', 'children')],
    [Input('from-station-name', 'value'), Input('to-station-name', 'value')]
)
def update_graph(from_station_name, to_station_name):
    origin_point = [stations_df[stations_df["name_with_region"] == from_station_name]['lat'].tolist()[0], stations_df[stations_df["name_with_region"] == from_station_name]['lon'].tolist()[0]]
    destination_point = [stations_df[stations_df["name_with_region"] == to_station_name]['lat'].tolist()[0], stations_df[stations_df["name_with_region"] == to_station_name]['lon'].tolist()[0]]

    # замедляет работу - определитель промежуточных станций
    # 
    # origin_esr = stations_df[stations_df["name_with_region"] == from_station_name]['esr'].tolist()[0]
    # destination_esr = stations_df[stations_df["name_with_region"] == to_station_name]['esr'].tolist()[0]
    # try:
    #     stations_path = nx.dijkstra_path(G_st, int(origin_esr), int(destination_esr))
    #     way_stations = []
    #     for station_esr in stations_path:
    #         try:
    #             st_name = stations_df[stations_df['esr']==station_esr]['name'].tolist()[0]
    #             st_lat = stations_df[stations_df['esr']==station_esr]['lat'].tolist()[0]
    #             st_lon = stations_df[stations_df['esr']==station_esr]['lon'].tolist()[0]
    #             way_stations.append([st_name, st_lat, st_lon])
    #         except IndexError:
    #             pass
    # except Exception as e:
    #     print(e)
    #     way_stations = []
    # 
    # замедляет работу

    way_stations = []

    # Определение ближайшей вершины графа
    origin_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])
    destination_node = ox.distance.nearest_nodes(G, destination_point[1], destination_point[0])
    # Определение кратчайшего пути
    route = ox.shortest_path(G, origin_node, destination_node)
    # route = tc.distance.shortest_path(G, origin_point, destination_point) # не подходит - другой тип графа выдает
    # print(route)
    
    # Определение расстояния - разобраться
    # for index, row in tqdm(df_railway.iterrows(), total=len(df_railway)):
    #     origin = (row['lat_from'], row['lon_from'])
    #     destination = (row['lat_to'], row['lon_to'])
    #     # Определение ближайшей вершины графа
    #     print(row.name[1], origin,row.name[3], destination)
    #     origin_node = ox.distance.nearest_nodes(G, origin[1], origin[0])
    #     destination_node = ox.distance.nearest_nodes(G, destination[1], destination[0])
    #     # Определение кратчайшего пути
    #     route_1 = ox.shortest_path(G, origin_node, destination_node)
    #     lenght = nodes_to_linestring(route_1)/1000

    length = 0
    print(f'{datetime.datetime.now()} Made route from {from_station_name} to {to_station_name}')
    return plot_path(route, origin_point, destination_point, mode='full', G=G, way_stations=way_stations), f'Total length - {length} km', f'Total segments - {len(route)}'

if __name__ == '__main__':
    app.run_server(debug=True)