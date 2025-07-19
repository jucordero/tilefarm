from .render import render
from typing import Literal

def tilefarm(
    areas: list,
    types: list,
    tile_size: tuple = (20, 20),
    method: Literal['random', 'sorted', 'treemap'] = 'treemap',
    scale: float = 1.0,
    padding: tuple = (0, 0),
    output_size: tuple = None  # Optional: final image size
):
    """
    Generate a tiled map based on the provided areas and types.
    
    :param areas: List of area identifiers.
    :param types: List of tile type names.
    :param tile_size: Size of each tile in pixels.
    :param method: Method for arranging tiles ('random', 'sorted', 'treemap').
    :param scale: Scale factor for the tiles.
    :param padding: Padding around the rendered map.
    :param output_size: Optional final image size.
    """
    render(areas, types, tile_size, method, scale, padding, output_size)