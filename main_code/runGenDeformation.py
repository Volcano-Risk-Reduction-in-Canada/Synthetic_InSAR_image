import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

try:
    from scipy.io import savemat
except Exception:  # pragma: no cover - SciPy optional
    savemat = None

parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from deform.generateDeformation import generateDeformation

# Settings
SAVEWRAP = 1
outputRoot = r"C:/Users/arothera/GitHub/Synthetic_InSAR_image/set"
for s in ("set1", "set2"):
    os.makedirs(os.path.join(outputRoot, s, "unwrap", "deform"), exist_ok=True)
if SAVEWRAP == 1:
    for s in ("set1", "set2"):
        os.makedirs(os.path.join(outputRoot, s, "wrap", "deform"), exist_ok=True)

halfcrop = 227 // 2
Source_Type = 4


def center_crop(arr):
    r, c = arr.shape
    return arr[r // 2 - halfcrop : r // 2 + halfcrop + 1,
               c // 2 - halfcrop : c // 2 + halfcrop + 1]


def rotate_array(arr, angle):
    return np.array(Image.fromarray(arr).rotate(angle, resample=Image.BILINEAR, expand=False))


def save_unwrap(base_dir, name, data):
    path = os.path.join(base_dir, f"{name}.mat")
    if savemat:
        savemat(path, {"los_grid": data})
    else:  # fall back to NumPy binary if SciPy is unavailable
        np.save(os.path.splitext(path)[0] + ".npy", data)

# Source Parameters
Quake = {
    "Strike": 0, "Dip": 80, "Rake": -90, "Slip": 1,
    "Top_depth": 3, "Bottom_depth": 6, "Length": 2
}

Dyke = {
    "Strike": 0, "Dip": 90, "Opening": 1,
    "Top_depth": 2, "Bottom_depth": 8, "Length": 10
}

Sill = {
    "Strike": 0, "Dip": 0, "Opening": 10,
    "Depth": 5, "Width": 1, "Length": 1
}

Mogi = {
    "Depth": 5, "Volume": 10 * 1e6
}

Penny = {
    "Depth": 5, "Pressure": 1 * 1e6, "Radius": 5
}

maxnum = 5000
x = np.arange(-25000, 25000, 100)
y = np.arange(-25000, 25000, 100)

# Generate Deformation for all Source Types

# Source_Type = 1: Rectangular Dislocation (Earthquake)
if Source_Type == 1:
    count = 1
    for Strike in range(0, 360, 36):
        Quake["Strike"] = Strike
        for Dip in range(70, 91, 5):
            Quake["Dip"] = Dip
            for Rake in list(range(60, 121, 15)) + list(range(-110, -74, 15)):
                Quake["Rake"] = Rake
                for Length in [1.5, 2, 5]:
                    Quake["Length"] = Length
                    for Bottom_depth in [6, 10]:
                        Quake["Bottom_depth"] = Bottom_depth
                        Top_depth_range = [2.5, 3, 3.5] if Bottom_depth == 6 else [3, 4, 5]
                        for Top_depth in Top_depth_range:
                            Quake["Top_depth"] = Top_depth
                            allName = f"Type{Source_Type}_strike{Strike}_dip{Dip}_rake{Rake}_length{Length:.1f}_bdepth{Bottom_depth}_tdepth{Top_depth:.1f}"
                            if count < maxnum:
                                # print(allName)
                                _, los_grid = generateDeformation(Source_Type, x, y, Quake, Dyke, Sill, Mogi, Penny, 192.04, 23)
                                los_grid = los_grid / 0.028333 * 2 * np.pi
                                los_grid = center_crop(los_grid)
                                if 12 < np.ptp(los_grid) < 80:
                                    outputDirUnwrap = os.path.join(outputRoot, f"set{2 - count % 2}", "unwrap", "deform")
                                    save_unwrap(outputDirUnwrap, allName, los_grid)
                                    if SAVEWRAP == 1:
                                        outputDirWrap = os.path.join(outputRoot, f"set{2 - count % 2}", "wrap", "deform")
                                        los_grid_wrap = np.mod(los_grid, 2 * np.pi) - np.pi
                                        los_grid_wrap = (los_grid_wrap - los_grid_wrap.min()) / np.ptp(los_grid_wrap)
                                        plt.imsave(os.path.join(outputDirWrap, f"{allName}.png"), los_grid_wrap, cmap="gray")
                                    count += 1

# Source_Type = 2: Dykes
if Source_Type == 2:
    count = 1
    for Incidence in [43, 50]:
        for Heading in [0, 192]:
            for Strike in range(0, 360, 36):
                Dyke["Strike"] = Strike
                for Dip in range(70, 91, 5):
                    Dyke["Dip"] = Dip
                    for Opening in [0.5, 0.75]:
                        Dyke["Opening"] = Opening
                        for Length in [2, 5, 8]:
                            Dyke["Length"] = Length
                            for Bottom_depth in [2, 5]:
                                Dyke["Bottom_depth"] = Bottom_depth
                                Top_depth_range = [0.25, 0.5, 0.75] if Bottom_depth == 2 else [0.5, 0.75, 1]
                                for Top_depth in Top_depth_range:
                                    Dyke["Top_depth"] = Top_depth
                                    allName = f"Type{Source_Type}_strike{Strike}_dip{Dip}_opening{Opening:.2f}_length{Length:.1f}_bdepth{Bottom_depth}_tdepth{Top_depth:.2f}"
                                    if count < maxnum:
                                        print(allName)
                                        _, los_grid = generateDeformation(Source_Type, x, y, Quake, Dyke, Sill, Mogi, Penny, Heading, Incidence)
                                        los_grid = los_grid / 0.028333 * 2 * np.pi
                                        los_grid = center_crop(los_grid)
                                        if 12 < np.ptp(los_grid) < 70:
                                            outputDirUnwrap = os.path.join(outputRoot, f"set{2 - count % 2}", "unwrap", "deform")
                                            save_unwrap(outputDirUnwrap, allName, los_grid)
                                            if SAVEWRAP == 1:
                                                outputDirWrap = os.path.join(outputRoot, f"set{2 - count % 2}", "wrap", "deform")
                                                los_grid_wrap = np.mod(los_grid, 2 * np.pi) - np.pi
                                                los_grid_wrap = (los_grid_wrap - los_grid_wrap.min()) / np.ptp(los_grid_wrap)
                                                plt.imsave(os.path.join(outputDirWrap, f"{allName}.png"), los_grid_wrap, cmap="gray")
                                            count += 1

# Source_Type = 3: Rectangular Sills
if Source_Type == 3:
    count = 1
    for Incidence in range(10, 360, 72):
        for Heading in range(0, 180, 72):
            for Dip in [0, 10]:
                Sill["Dip"] = Dip
                Strike_range = [0] if Dip == 0 else range(20, 360, 90)
                for Strike in Strike_range:
                    Sill["Strike"] = Strike
                    for Opening in [5, 10, 15]:
                        Sill["Opening"] = Opening
                        for Length in [0.75, 1, 3]:
                            Sill["Length"] = Length
                            for Width in [2, 5]:
                                Sill["Width"] = Width
                                for Depth in [4, 5, 6]:
                                    Sill["Depth"] = Depth
                                    for Rotate in range(0, 360, 72):
                                        allName = f"Type{Source_Type}_dip{Dip}_strike{Strike}_opening{Opening}_length{Length}_width{Width}_depth{Depth}_rotate{Rotate}"
                                        if count < maxnum:
                                            print(allName)
                                            _, los_grid = generateDeformation(Source_Type, x, y, Quake, Dyke, Sill, Mogi, Penny, Heading, Incidence)
                                            los_grid = los_grid / 0.028333 * 2 * np.pi
                                            los_grid = rotate_array(los_grid, Rotate)
                                            los_grid = center_crop(los_grid)
                                            if 12 < np.ptp(los_grid) < 50:
                                                outputDirUnwrap = os.path.join(outputRoot, f"set{2 - count % 2}", "unwrap", "deform")
                                                save_unwrap(outputDirUnwrap, allName, los_grid)
                                                if SAVEWRAP == 1:
                                                    outputDirWrap = os.path.join(outputRoot, f"set{2 - count % 2}", "wrap", "deform")
                                                    los_grid_wrap = np.mod(los_grid, 2 * np.pi) - np.pi
                                                    los_grid_wrap = (los_grid_wrap - los_grid_wrap.min()) / np.ptp(los_grid_wrap)
                                                    plt.imsave(os.path.join(outputDirWrap, f"{allName}.png"), los_grid_wrap, cmap="gray")
                                                count += 1

# Source_Type = 4: Magma Chamber
if Source_Type == 4:
    count = 1
    for Incidence in [33]:
        for Heading in range(5, 331, 40):
            for Volume in [v + 0.2 for v in [6, 6.5, 6.7, 7, 7.2, 7.5]]:
                Mogi["Volume"] = 10**Volume
                VolumeName = f"vol1e{Volume:.1f}"
                depth_range = (
                    [1.5, 2] if Volume <= 6 else
                    [2, 2.5, 2.8, 3] if Volume <= 6.5 else
                    [2.5, 2.8, 3, 4, 5, 5.5, 6] if Volume <= 7 else
                    [5, 6, 7, 7.5, 8]
                )
                for Depth in depth_range:
                    Mogi["Depth"] = Depth
                    allName = f"Type{Source_Type}_{VolumeName}_depth{Depth:.1f}"
                    if count < maxnum:
                        print(allName)
                        _, los_grid = generateDeformation(Source_Type, x, y, Quake, Dyke, Sill, Mogi, Penny, Heading, Incidence)
                        los_grid = center_crop(los_grid)
                        if 0.10 < np.ptp(los_grid) < 20:
                            outputDirUnwrap = os.path.join(outputRoot, f"set{2 - count % 2}", "unwrap", "deform")
                            save_unwrap(outputDirUnwrap, allName, los_grid)
                            if SAVEWRAP == 1:
                                outputDirWrap = os.path.join(outputRoot, f"set{2 - count % 2}", "wrap", "deform")
                                los_grid_wrap = np.mod(los_grid, 2 * np.pi) - np.pi
                                los_grid_wrap = (los_grid_wrap - los_grid_wrap.min()) / np.ptp(los_grid_wrap)
                                plt.imsave(os.path.join(outputDirWrap, f"{allName}.png"), los_grid_wrap, cmap="gray")
                            count += 1

# Source_Type = 5: Pressurized Penny-shaped Horizontal Crack
if Source_Type == 5:
    count = 1
    for Incidence in [2, 15, 25, 160, 170, 177]:
        for Heading in range(0, 181, 72):
            for Radius in range(4, 7):
                Penny["Radius"] = Radius
                for Pressure in [6]:
                    Penny["Pressure"] = 10**Pressure
                    for Depth in [4, 4.5, 5]:
                        Penny["Depth"] = Depth
                        for Rotate in range(0, 360, 72):
                            allName = f"Type{Source_Type}_radius{Radius}_pressure{Pressure}_depth{Depth}_rotate{Rotate}"
                            if count < maxnum:
                                print(allName)
                                _, los_grid = generateDeformation(Source_Type, x, y, Quake, Dyke, Sill, Mogi, Penny, Heading, Incidence)
                                los_grid = los_grid / 0.028333 * 2 * np.pi
                                los_grid = rotate_array(los_grid, Rotate)
                                los_grid = center_crop(los_grid)
                                if 10 < np.ptp(los_grid) < 30:
                                    outputDirUnwrap = os.path.join(outputRoot, f"set{2 - count % 2}", "unwrap", "deform")
                                    save_unwrap(outputDirUnwrap, allName, los_grid)
                                    if SAVEWRAP == 1:
                                        outputDirWrap = os.path.join(outputRoot, f"set{2 - count % 2}", "wrap", "deform")
                                        los_grid_wrap = np.mod(los_grid, 2 * np.pi) - np.pi
                                        los_grid_wrap = (los_grid_wrap - los_grid_wrap.min()) / np.ptp(los_grid_wrap)
                                        plt.imsave(os.path.join(outputDirWrap, f"{allName}.png"), los_grid_wrap, cmap="gray")
                                    count += 1
