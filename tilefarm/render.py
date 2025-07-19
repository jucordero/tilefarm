import pygame as pyg
import numpy as np
import os
import random
from typing import Literal

from .core import pixelmap

TILE_WIDTH = 32
TILE_HEIGHT = 16
TILE_THICK = 48

def load_tile_variants(types):
    base_path = os.path.join(os.path.dirname(__file__), "assets")
    tile_variants = {}
    for t in types:
        path = os.path.join(base_path, t)
        if os.path.isdir(path):
            files = [f for f in os.listdir(path) if f.endswith(".png")]
            tile_variants[t] = [
                pyg.image.load(os.path.join(path, f)).convert_alpha() for f in files
            ]
        else:
            # fallback to single image if folder not found
            tile_variants[t] = [pyg.image.load(f"{path}.png").convert_alpha()]
    return tile_variants

def render(
    areas: list,
    types: list,
    tile_size: tuple = (20, 20),
    method : Literal['random', 'sorted', 'treemap'] = 'treemap',
    scale: float = 1.0,
    padding: tuple = (0, 0),
    output_size: tuple = None  # Optional: final image size
    ):
    
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pyg.display.set_mode((1, 1))  # Initialize display with dummy size
    pyg.init()

    map = pixelmap(areas, width=tile_size[0], height=tile_size[1], method=method)
    # tilemap = [pyg.image.load(f"assets/{t}.png").convert_alpha() for t in types]
    tile_variants = load_tile_variants(types)

    # Compute full render size based on tilemap dimensions
    width_tiles, height_tiles = tile_size
    full_width = (width_tiles + height_tiles) * TILE_WIDTH + padding[0]*2
    full_height = (width_tiles + height_tiles) * TILE_HEIGHT + TILE_THICK + padding[1]*2

    # Create large surface
    full_surface = pyg.Surface((full_width, full_height), pyg.SRCALPHA)

    # Center the map
    start_x = full_width // 2 - TILE_WIDTH
    start_y = padding[1]

    for y in range(height_tiles):
        for x in range(width_tiles):
            i = map[x, y]
            type_name = types[i]
            tile = random.choice(tile_variants[type_name])
            px = start_x + x * TILE_WIDTH - y * TILE_WIDTH
            py = start_y + x * TILE_HEIGHT + y * TILE_HEIGHT
            full_surface.blit(tile, (px, py))

    # Apply scaling
    if scale != 1.0:
        scaled_size = (int(full_width * scale), int(full_height * scale))
        full_surface = pyg.transform.smoothscale(full_surface, scaled_size)

    # Crop or fit to output_size
    if output_size:
        output_surface = pyg.Surface(output_size, pyg.SRCALPHA)
        fw, fh = full_surface.get_size()
        ox, oy = max((output_size[0] - fw) // 2, 0), max((output_size[1] - fh) // 2, 0)
        output_surface.blit(full_surface, (ox, oy))
        pyg.image.save(output_surface, "tilemap.png")
    else:
        pyg.image.save(full_surface, "tilemap.png")

    pyg.quit()

if __name__ == "__main__":
    render(np.random.rand(6),
           ['forest', 'wheat', 'grass', 'sheep', 'water', 'urban'],
           tile_size=(10, 10),
           method='treemap',
           padding=(10, 10),
           )