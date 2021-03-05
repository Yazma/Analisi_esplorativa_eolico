import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

csv_path = '/home/osboxes/Scrivania/Eolico.csv'


df_global = pd.read_csv(csv_path, sep=';')
df_europe = df_global[df_global['Continents']=='Europe'].reset_index(drop=True)

df_europe_2018_2019 = df_europe[df_europe['Year'].isin([2018, 2019])].reset_index(drop=True).\
    sort_values(['Country or Area', 'Year'], ascending=False).drop_duplicates(['Country or Area'])

df_europe_2018_2019['prod / kmq'] = df_europe_2018_2019['Quantity'] / df_europe_2018_2019['Kmq']

print('--------------------------------------------------------------------------------------------------')

df_europe_2018_2019_quantity = df_europe_2018_2019[['Country or Area', 'Year', 'Quantity']].\
    sort_values('Quantity', ascending=False).reset_index(drop=True)
df_europe_2018_2019_quantity.to_csv('/home/osboxes/Scrivania/df_europe_2018_2019_quantity.csv', sep=';', index=False)
print(df_europe_2018_2019_quantity)

print('--------------------------------------------------------------------------------------------------')

df_europe_2018_2019_kmq = df_europe_2018_2019[['Country or Area', 'Kmq']].\
    sort_values('Kmq', ascending=False).reset_index(drop=True)
df_europe_2018_2019_kmq.to_csv('/home/osboxes/Scrivania/df_europe_2018_2019_kmq.csv', sep=';', index=False)
print(df_europe_2018_2019_kmq)

print('--------------------------------------------------------------------------------------------------')

df_europe_2018_2019_quantity_vs_kmq = df_europe_2018_2019[['Country or Area', 'prod / kmq']].\
    sort_values('prod / kmq', ascending=False).reset_index(drop=True)
df_europe_2018_2019_quantity_vs_kmq.to_csv('/home/osboxes/Scrivania/df_europe_2018_2019_quantity_vs_kmq.csv',
                                           sep=';', index=False)
print(df_europe_2018_2019_quantity_vs_kmq)
