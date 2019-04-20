import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

url = 'http://api.tvmaze.com/singlesearch/shows?q=black-mirror&embed=episodes'
r = requests.get(url).json()

s = json.dumps(r, indent=2)

data = []
for e in r['_embedded']['episodes']:
    data.append(({'name': e['name'], 'runtime': e['runtime']}))

episodes = [i['name'] for i in data]
rates = [8,8.3,8.7,8.2,8.2,6.9,8.3,8.2,8.5,8.8,7.8,8.7,8.4,7.4,7.3,8.9,6.8,8.8]
ratings = dict(zip(episodes, rates))

        
df = pd.DataFrame(data)
df.set_index('name', inplace=True)
df['ratings'] = df.index.map(ratings)
print(df)


ax = df[['runtime']].plot(kind='bar')
df[['ratings']].plot(ax=ax, secondary_y=True)
ax.tick_params(axis='x', rotation=45)
plt.show()




