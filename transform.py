import pandas as pd
df = pd.read_json ('./location.json', convert_dates=False)
df.to_csv ('./location.csv', index = None)