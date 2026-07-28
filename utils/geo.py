import json
from shapely.geometry import shape, Point

def load_school_polygon(filename, school_name):
    with open(filename, encoding="utf-8") as f:
        geojson = json.load(f)

    for feature in geojson["features"]:
        if feature["properties"]["school"] == school_name:
            return shape(feature["geometry"])

    raise ValueError(f"{school_name} Polygon을 찾을 수 없습니다.")

def filter_dataframe(df, polygon):
    return df[
        df.apply(
            lambda row: polygon.contains(
                Point(row["lng"], row["lat"])
            ),
            axis=1
        )
    ].reset_index(drop=True)