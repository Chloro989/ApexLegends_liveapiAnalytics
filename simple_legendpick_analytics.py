import json
import numpy as np
import pandas as pd

#pandas display setting
pd.set_option('display.max_rows', 500)

# Open JSON file(edit encoding if you need to)
with open('something.json',encoding="utf-8") as f:
    data = json.load(f)
    print(type(data))  # Add this line to check the type of the data variable

# Find all the "character" keys and get their values
characters = []
names =[]
for item in data:
    if isinstance(item, dict) and 'player' in item:
        names.append(item['player']['name'])
        characters.append(item['player']['character'])

#array
arr1 = np.array([names,characters])

#.T
df = pd.DataFrame(data=arr1,index=["name","legend"]).T
dropped_df = df.drop_duplicates(subset='name')
print(dropped_df)

#Output to csv
#dropped_df.to_csv("legendpick.csv")


