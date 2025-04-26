import geopandas as gpd
import prettymaps
import math
import sys

from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as PathEffects
from shapely.geometry import Polygon, Point

DEBUG = False

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def xy(lat, lon):
    # returns x and y in ax coordinate system from lat and lon
    gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs='EPSG:4326')
    coords = prettymaps.draw.gdf_to_shapely('-', gdf).geoms[0].xy
    return coords[0][0], coords[1][0]


if DEBUG:
    # test only 1 tile
    boundaries = [
        [47.411325468128055, 8.543403668695255],
        [47.411325468128055, 8.543403668695255]
    ]
else:
    boundaries = [
        [47.43790627501293, 8.473034608566035],
        [47.38935788148564, 8.590284281922552]
    ]

# zoom levels to be rendered
zooms = map(int, sys.argv[1:])  # [13, 14, 15, 16, 17, 18]

# using dpi 20
plt.rcParams['figure.dpi'] = 16

for zoom in zooms:
    # get boundary tiles
    x_min, y_min = deg2num(*boundaries[0], zoom)
    x_max, y_max = deg2num(*boundaries[1], zoom)
    if not DEBUG:
        if zoom <= 14:
            x_min -= 1
            x_max += 1
        if zoom == 13:
            x_max += 1
    x_tiles = x_max - x_min + 1
    y_tiles = y_max - y_min + 1
    print(x_tiles, y_tiles)

    # back to coordinates
    lat1, lon1 = num2deg(x_min, y_min, zoom)
    lat2, lon2 = num2deg(x_max+1, y_max+1, zoom)

    # create shape from coordinates
    lat_point_list = [lat1, lat1, lat2, lat2]
    lon_point_list = [lon1, lon2, lon2, lon1]
    polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
    polygon = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[polygon_geom])

    # plot a green map
    plot = prettymaps.plot(
        polygon,
        {
            'building': {'tags': {'building': True}},
            'water': {'tags': {'natural': 'water', 'waterway': 'stream'}},
            'wetland': {'tags': {'natural': 'wetland'}},
            'fields': {'tags': {'landuse': ['farmland', 'farmyard', 'grass', 'meadow', 'cemetery', 'allotments', 'plant_nursery'],
                                'natural': ['scrub'],
                                'leisure': ['garden', 'park'], 'surface': 'grass'}},
            'forest': {'tags': {'landuse': 'forest', 'natural': 'wood'}},
            'rail': {'tags': {'railway': 'rail'}},
            'transport': {'tags': {'network': 'ZVV'}},
            'streets': {
                'width': {
                    'motorway': 1,
                    'trunk': 1,
                    'primary': 1,
                    'secondary': 1,
                    'tertiary': 0 if zoom < 15 else 1,
                    'cycleway': 1,
                    'residential': 0,
                    'service': 0,
                    'unclassified': 0,
                    'pedestrian': 0,
                    'footway': 0
                }
            }
        },
        {
            'building': {
                "fc": '#fff',
                'ec': '#ddd',
                "lw": 1,
                "zorder": 5
            },
            'water': {
                "fc": "#ddd",
                "ec": "#888",
                "lw": 1,
                "zorder": 4
            },
            'wetland': {
                "fc": "#9cb84d",
                "ec": "#9cb84d",
                "lw": 1,
                "zorder": 3
            },
            'fields': {
                "fc": '#9cb84d',
                "ec": "#9cb84d",
                "lw": 1,
                "zorder": 3
            },
            'forest': {
                "fc": '#1e3b21',
                "ec": "#1e3b21",
                "lw": 1,
                "zorder": 3
            },
            'rail': {
                "fc": '#000',
                "ec": "#000",
                "lw": 3
            },
            'transport': {
                "fc": '#000',
                "ec": "#000",
                "lw": 2
            },
            'streets': {
                "fc": '#000',
                "ec": "#000",
                "alpha": 0.25
            },
        },
        figsize=(x_tiles * 16, y_tiles * 16),
        credit=False,
        preset=None,
        rotation=0.35  # the world is a twisted place I guess
    )

    print(plot.ax.get_xlim(), plot.ax.get_ylim())

    # labels for different zoom levels.
    textprops = dict(
        font=FontProperties(
            fname='GT-Walsheim-Regular.ttf',
            size=110
        ),
        horizontalalignment='center',
        verticalalignment='center',
        path_effects=[PathEffects.withStroke(linewidth=20, foreground='w')],
        zorder=100
    )

    if zoom <= 15:
        if zoom == 15:
            textprops['font'] = FontProperties(
                fname='GT-Walsheim-Medium.ttf',
                size=90
            )
        plot.ax.text(*xy(47.40963031315938, 8.545925610656884), "Oerlikon", **textprops)
        plot.ax.text(*xy(47.42000270528023, 8.506702740175154), "Affoltern", **textprops)
        plot.ax.text(*xy(47.42316345066895, 8.545493827941502), "Seebach", **textprops)
        plot.ax.text(*xy(47.39497003269579, 8.53869662182635), "Unterstrass", **textprops)
        plot.ax.text(*xy(47.40365496042748, 8.496537516241743), "Höngg", **textprops)
        plot.ax.text(*xy(47.40476672420747, 8.575790890493852), "Schwammendingen", **textprops)
        plot.ax.text(*xy(47.433133382873905, 8.566388526241248), "Opfikon", **textprops)

    if zoom >= 15:
        textprops['font'] = FontProperties(
            fname='GT-Walsheim-Regular.ttf',
            size=80
        )
        plot.ax.text(*xy(47.413613163402225, 8.536423725213346), "Neu-Oerlikon", **textprops)
        plot.ax.text(*xy(47.412274893963065, 8.525310650600671), "Neuaffoltern", **textprops)
        plot.ax.text(*xy(47.418224114449146, 8.506547730870105), "Oberaffoltern", **textprops)
        plot.ax.text(*xy(47.42427120583319, 8.508379582172358), "Unteraffoltern", **textprops)
        plot.ax.text(*xy(47.40401807005691, 8.5379129066741), "Allenmoos", **textprops)
        plot.ax.text(*xy(47.41582226911396, 8.555587406143719), "Leutschenbach", **textprops)
        plot.ax.text(*xy(47.40868757648622, 8.507895317161015), "ETH Hönggerberg", **textprops)
        plot.ax.text(*xy(47.39845402358281, 8.544441233149024), "Irchelpark", **textprops)
        plot.ax.text(*xy(47.43243777353354, 8.493155453980425), "Chatzesee", **textprops)

    plot.ax.margins(0, 0)
    plt.savefig(f'z{zoom}_x{x_min}-{x_max}_y{y_min}-{y_max}.png')
