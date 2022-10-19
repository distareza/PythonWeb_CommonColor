import pandas as pd

img_arr = [ [221, 243, 255], [221, 243, 255], [221, 243, 255], [222, 244, 12], [223, 245, 255]]
img_arr.extend([ [221, 243, 255], [221, 243, 255], [221, 243, 255], [222, 244, 12], [223, 245, 255]])
print(img_arr)

# arr = [ str(x[0]) + '-' + str(x[1]) + '-' + str(x[2]) for x in img_arr ]
# print (arr)
# df = pd.Series(arr).to_frame().rename(columns={0: "Colours"})
# print(df)
# print(df.value_counts())


#colour_arr = [ img_arr[x] for x in len(img_arr)]
# df = pd.Series(img_arr).to_frame().rename(columns={0: "Colours"})
# print(df)
# print(df.value_counts())
