import pandas as pd
from .models import Lifting, Supplier


df = pd.read_csv(r'C:\Users\Basham\tut\inventory\beau.csv', converters={'Date/Time': pd.to_datetime})
df = df[df['Date/Time'] > '2019/09/01']

for idx, row in df.iterrows():
    lift = Lifting()
    lift.supplier_id = Supplier(pk=1) if row['Customer'] != 10212 else Supplier(pk=2)
    lift.contract = row['Customer']
    lift.ticket = row['Ticket']
    lift.date = row['Date/Time']
    lift.volume = row['Net']

    lift.decrement_inventory()
    lift.save()
