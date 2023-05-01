This script generates a customized map tiles that can be used with [Leaflet](https://leafletjs.com/).

It is not very accurate but very stylish.

# Installation

```
$ pip install -r requirements.txt
```

This must be patched in osmnx/geometries.py:_create_gdf line 427 to not remove bus lanes (operator: vbz)

```python
 elif (element["type"] == "relation" and element.get("tags").get("type") == "route"):
     # add relevant tags to the members of the relation
     for member in element["members"]:
         if member["type"] == "way" and f"way/{member['ref']}" in geometries:
             for tag in tags:
                 if tag in element["tags"]:
                     geometries[f"way/{member['ref']}"][tag]=element["tags"][tag]
```
                                     
# Usage

## Create map

```
$ python map.py {zoom-level}
```

Reasonable zoom levels are 13 to 16

## Cut tiles

```
$ python cut.py {zoom-levels}
```

Multiple previously created map zoom levels (space separated) can be cut into tiles.

# Fonts

The script uses the GT Walsheim font which can not be included in this repository due to the license.

# Credits

This script uses [prettymaps](https://pypi.org/project/prettymaps/).
