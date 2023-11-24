import os
import tempfile
import zipfile
from io import BytesIO

import requests
from geojson import FeatureCollection, dump
from kml2geojson.main import convert

zip_url = "https://data.police.uk/data/boundaries/force_kmls.zip"

response = requests.get(zip_url)
coords = []
if response.status_code == 200:
    with zipfile.ZipFile(BytesIO(response.content), "r") as zip_ref:
        file_list = zip_ref.namelist()

        # Loop through each file in the zip archive
        for file_name in file_list:
            # Read the contents of the file
            with zip_ref.open(file_name) as file:
                # Process the file contents as needed
                content = file.read()
                # Save contents to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(content)

                    # Get the path to the temporary file
                    temp_file_path = temp_file.name

                # Convert KML to GeoJSON using kml2geojson
                geojson_data = convert(temp_file_path)

                # Clean up the temporary file
                feature_col = FeatureCollection(geojson_data[0])
                os.remove(temp_file_path)

                if isinstance(geojson_data, list):
                    geojson_data = geojson_data[0]

                try:
                    collection = FeatureCollection(geojson_data.get("features"))
                    with open(
                        os.path.join(
                            "local",
                            "geojsons",
                            file_name.replace(".kml", "").replace("force kmls/", "")
                            + ".geojson",
                        ),
                        "w",
                    ) as f:
                        dump(collection, f)
                except Exception as e:
                    print(e)
                    # print(geojson_data)
                    exit()


# print(coords[0])  # .get("coords")[0])
# g_df =


# kml2geojson.main.convert("local/avon-and-somerset.kml")
