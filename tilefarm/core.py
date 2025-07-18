import matplotlib.pyplot as plt
import squarify
import numpy as np
from typing import Literal
import sys

def _plot_treemap(areas, width, height):
    """
    Plots a treemap based on land use data.

    Parameters
    ----------
    land_uses : list
        List of land use types.
    areas : list
        Corresponding areas for each land use type.
    width : int, optional
        Width of the treemap. Default is 100.
    height : int, optional
        Height of the treemap. Default is 100.

    Returns
    -------
    None
    """

    # Normalize areas to total area
    total = sum(areas)
    normed_areas = [a / total for a in areas]

    # Generate treemap
    colors = ['#228B22', '#DEB887', '#808080', '#1E90FF']
    squarify.plot(sizes=normed_areas, norm_x=width, norm_y=height, color=colors, alpha=0.8)
    plt.show()

def _treemap_rects(areas, width, height):
    """
    Returns rectangles for the treemap layout.
    
    Parameters:
    -----------
    land_uses : (list)
        List of land use types.
    areas : (list)
        Corresponding areas for each land use type.
    width : (int, optional)
        Width of the treemap.
    height : (int, optional)
        Height of the treemap.

    Returns:
    --------
    list:
        List of rectangles for each land use type.
    """

    normed_areas = squarify.normalize_sizes(areas, width, height)
    rects = squarify.squarify(normed_areas, 0, 0, width, height)
    return rects

def _rectangles_to_pixelmap(rects, width, height):
    """
    Converts rectangles to a pixel map.

    Parameters
    ----------
    rects : list
        List of rectangles to convert.
    width : int, optional
        Width of the pixel map.
    height : int, optional
        Height of the pixel map.

    Returns
    -------
    list
        Array of pixel values representing the rectangles.
    """

    pixelmap = np.empty((width, height), dtype=int)

    for i, rect in enumerate(rects):
        for w in range(width):
            for h in range(height):
                if (rect['x'] <= w < rect['x'] + rect['dx']) and (rect['y'] <= h < rect['y'] + rect['dy']):
                    pixelmap[w, h] = i

    return pixelmap

def _sorted_pixelmap(areas, width, height):
    """
    Generates a random pixel map for the given areas.

    Parameters
    ----------
    areas : list
        List of areas to be represented.
    width : int, optional
        Width of the pixel map. Default is 20.
    height : int, optional
        Height of the pixel map. Default is 20.

    Returns
    -------
    list
        List of rectangles representing the pixel map.
    """

    total_pixels = width * height
    total_area = sum(areas)
    normalized_areas = [a / total_area for a in areas]

    pixel_counts = [int(total_pixels * a) for a in normalized_areas]

    pixels = np.zeros(total_pixels, dtype=int)

    tcount = 0
    for i, count in enumerate(pixel_counts[1:]):
        pixels[tcount:tcount + count] = i+1
        tcount += count

    pixels = np.sort(pixels)

    pixel_map = pixels.reshape((width, height))
    return pixel_map


def pixelmap(areas,
             width=20,
             height=20,
             method : Literal['random', 'sorted', 'treemap'] = 'treemap'):
    """
    Generates a pixel map for the given areas.

    Parameters
    ----------
    areas : list
        List of areas to be represented.
    width : int, optional
        Width of the pixel map. Default is 20.
    height : int, optional
        Height of the pixel map. Default is 20.
    method : Literal['random', 'sorted', 'treemap'], optional
        Method to generate the pixel map. Default is 'treemap'.

    Returns
    -------
    list
        List of rectangles representing the pixel map.
    """

    if method == 'random':
        # Randomly generate rectangles (not implemented)
        pixmap = _sorted_pixelmap(areas, width, height)
        pixmap = pixmap.flatten()
        np.random.shuffle(pixmap)
        pixmap = pixmap.reshape((width, height))
        return pixmap
    
    elif method == 'sorted':
        # Sort areas and generate rectangles (not implemented)
        return _sorted_pixelmap(areas, width, height)
    
    elif method == 'treemap':
        # Use treemap method to generate rectangles
        rects = _treemap_rects(areas, width, height)
        return _rectangles_to_pixelmap(rects, width, height)
    
def _plot_pixelmap(pixel_map):
    """
    Plots the pixel map.

    Parameters
    ----------
    pixel_map : list
        List of pixel values to be plotted.

    Returns
    -------
    None
    """
    
    plt.imshow(pixel_map, cmap='viridis', interpolation='none')
    plt.show()

if __name__ == "__main__":

    # Example land use data
    areas = [50, 30, 10, 10]  # Percentages or actual areas
    
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    height = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    print(_treemap_rects(areas, width=width, height=height))
    _plot_treemap(areas, width=width, height=height)

    pixel_map = pixelmap(areas, width=width, height=height, method='random')
    _plot_pixelmap(pixel_map)
    print(pixel_map)