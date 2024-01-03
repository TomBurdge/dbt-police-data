import glob
import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

repository_path = "local/geojsons"

geojson_files = glob.glob(f"{repository_path}/*.geojson")

gdfs = []
# Iterate through each GeoJSON file and append its contents to the list
for file in geojson_files:
    force = file.replace("local/geojsons/", "").replace(".geojson", "")
    gdf = gpd.read_file(file)
    gdf["force"] = force
    gdfs.append(gdf)
all_forces_df = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

gcs_path = (
    f"gs://duckdb-stop-search-{os.environ.get('project', 'dev')}/all_forces.geojson"
)

# need to authenticate
all_forces_df.to_file(gcs_path, driver="GeoJSON")

not_ni_df = all_forces_df[all_forces_df["force"] != "northern-ireland"]
not_ni_df.plot()
plt.show()

all_forces_df.plot()
plt.show()

ni_df = all_forces_df[all_forces_df["force"] == "northern-ireland"]
ni_df.plot()
plt.show()
