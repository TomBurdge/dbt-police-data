import glob

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Replace 'path/to/your/repository' with the actual path to your repository
repository_path = "local/geojsons"

# Use glob to get a list of all GeoJSON files in the repository
geojson_files = glob.glob(f"{repository_path}/*.geojson")

gdfs = []
# Iterate through each GeoJSON file and append its contents to the list
for file in geojson_files:
    force = file.replace("local/geojsons/", "").replace(".geojson", "")
    gdf = gpd.read_file(file)
    gdf["force"] = force
    gdfs.append(gdf)
all_forces_df = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

# Display the combined GeoDataFrame

all_forces_df.plot()
plt.show()
