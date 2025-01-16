from matplotlib.colors import LinearSegmentedColormap
import numpy as np

def phase_colormap():
    colors = [
        (-3.14159, (0/255, 191/255, 169/255)),
        (-2.35619, (0/255, 60/255, 248/255)),
        (-1.57080, (102/255, 0/255, 234/255)),
        (-0.78540, (217/255, 0/255, 133/255)),
        (0.00000, (255/255, 0/255, 0/255)),
        (0.78540, (212/255, 142/255, 0/255)),
        (1.57080, (98/255, 236/255, 0/255)),
        (2.35619, (0/255, 253/255, 35/255)),
        (3.14159, (0/255, 191/255, 169/255))
    ]

    positions, color_values = zip(*colors)
    normalized_positions = (np.array(positions) - min(positions)) / (max(positions) - min(positions))
    return LinearSegmentedColormap.from_list('custom_colormap', list(zip(normalized_positions, color_values)))

