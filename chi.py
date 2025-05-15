import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx

# Define a place name for walkable map extraction
place_name = "White Town, Puducherry, India"

# Download walkable network from OpenStreetMap
G = ox.graph_from_place(place_name, network_type='walk')

# Compute centrality (betweenness)
centrality = nx.betweenness_centrality(ox.utils_graph.get_undirected(G), weight='length')
nx.set_node_attributes(G, centrality, 'centrality')

# Convert graph to GeoDataFrames
nodes, edges = ox.graph_to_gdfs(G)

# Create example land-use zones using buffered landmarks
zones = gpd.GeoDataFrame({
    'zone': ['Residential', 'Commercial', 'Green'],
    'geometry': [
        ox.geocode_to_gdf("White Town, Puducherry, India").geometry.buffer(0.001)[0],
        ox.geocode_to_gdf("Pondicherry Beach").geometry.buffer(0.0006)[0],
        ox.geocode_to_gdf("Botanical Garden, Puducherry").geometry.buffer(0.0005)[0]
    ]
}, crs="EPSG:4326")

# Plotting everything
fig, ax = plt.subplots(figsize=(10, 10))
zones.plot(ax=ax, color=['lightblue', 'orange', 'green'], alpha=0.4, edgecolor='black')
edges.plot(ax=ax, linewidth=0.5, color='gray')
nodes.plot(ax=ax, markersize=5, column='centrality', cmap='plasma', legend=True)

plt.title("Walkability and Land Use in White Town, Puducherry")
plt.axis('off')
plt.tight_layout()
plt.show()
