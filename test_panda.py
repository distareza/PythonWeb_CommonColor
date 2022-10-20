import pandas as pd
import numpy as np
from PIL import Image
import json

img = Image.open("C:/tmp/Me and Thanos.jpg")
img.load()

# convert to tensor ( n-dimensional array )
img_arr = np.array(img)
print(f"array dimension {img_arr.ndim}")
print(f"array shape {img_arr.shape}")

# Group pixel color
colour_arr = []
for y in range(img_arr.shape[1]):
    colour_arr.extend([img_arr[x, y, :] for x in range(img_arr.shape[0])])
arr = [str(x[0]) + '-' + str(x[1]) + '-' + str(x[2]) for x in colour_arr]
df = pd.Series(arr).to_frame().rename(columns={0: "Colours"})
print(f"colour count : {df.count()}")
colour_group = df.value_counts().head(5)
print(colour_group)
print(colour_group.index.tolist())

colour_count = int(df.count())
group_color = []
for idx, group in enumerate(colour_group.index.tolist()):
    group_color.append([str(group[0]), int(colour_group[idx]), float(colour_group[idx] * 100 / colour_count)])

jsonString = json.dumps(group_color, indent=2)
print(jsonString)