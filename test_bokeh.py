import numpy as np
import scipy.special
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# d = {'Valori': [10, 20, 30, 40, 50],
#      'Paesi': ['A', 'B', 'C', 'D', 'E']}  #[1, 2, 3, 4, 5]
# df = pd.DataFrame(data=d)
# p = figure(x_range=df['Paesi'], plot_height=250, title="Paesi Eolico",
#            toolbar_location=None, tools="")
# p.vbar(x=df['Paesi'], top=df['Valori'], width=0.5)
# show(p)




df_global = pd.read_csv('/home/osboxes/Scrivania/Eolico.csv', sep=';')

country_to_compare = ['Italy', 'France', 'Germany', 'Norway', 'United Kingdom', 'Romania']
# df = df_global[(df_global['Country or Area'] == 'Italy') |
#                (df_global['Country or Area'] == 'Spain')].reset_index(drop=True)
df = df_global[df_global['Country or Area'].isin(country_to_compare)]


unique_country = df['Country or Area'].unique().tolist()
unique_year = df['Year'].unique().tolist()
unique_year = unique_year[:9]

data_dict = {'country': unique_country}
big_list = []

for i in unique_year:
    if str(i) not in data_dict.keys():
        data_dict[str(i)] = {}
        data_dict[str(i)] = df[df['Year'] == i]['Quantity'].tolist()
        big_list.append(data_dict[str(i)])

unique_year = [str(i) for i in unique_year]
'''creo le tuple (Italy, 2018), (Italy,2017), ...(Spain, 2018), ...'''
x = [(country, year) for country in unique_country for year in unique_year]
counts = sum(zip(*big_list), ())

source = ColumnDataSource(data=dict(x=x, counts=counts))

'''grafico'''
p = figure(x_range=FactorRange(*x), plot_width=1500, plot_height=600,
           # title="Eolico {} {}".format(unique_country[0], unique_country[1]),
           title="Eolico",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=0.9, source=source)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None
p.yaxis.axis_label = 'Kilowatt-hours, million'

show(p)




