from openpyxl import load_workbook
import pandas as pd

from bokeh.plotting import figure
from bokeh.io import show, output_notebook

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


xlsx_path = '/home/osboxes/Scrivania/Eolico.xlsx'
sheet_name = 'UNdata_Export_20210303_11213883'
csv_path = '/home/osboxes/Scrivania/Eolico.csv'


'''Data preparation: in questa fase carico il file excel con i dati allo scopo di salvarlo come csv,
   questo metodo viene lanciato solo per creare il file csv'''
def get_data_from_xlsx(xlsx_path, sheet_name):
    wb = load_workbook(xlsx_path)
    ws = wb[sheet_name]
    df = pd.DataFrame(ws.values)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df.to_csv(csv_path, sep=';', index=False)

def get_Europe_country(df):
    df_europe = df[df['Continents'] == 'Europe'].reset_index(drop=True)
    return df_europe


def get_single_country(df, country):
    df_country = df[df['Country or Area'] == country].reset_index(drop=True)
    return df_country


def get_unique_value(df):
    unique_country = df['Country or Area'].unique()
    unique_data = df['Year'].unique()
    return unique_country, unique_data


def bokeh_histogram_single_country_per_year(df, country):
    df = get_single_country(df, country)
    p = figure(x_range=df['Year'].astype(str), plot_width=1500, plot_height=600, title="Eolico {}".format(country),
               toolbar_location=None, tools="")
    p.vbar(x=df['Year'].astype(str), top=df['Quantity'], width=0.5)
    p.yaxis.axis_label = 'Kilowatt-hours, million'
    show(p)

def bokeh_histogram_energy_prod_vs_surface(df, title, variabile):
    p = figure(x_range=df['Country or Area'], plot_width=1500, plot_height=600,
               title=title,
               toolbar_location=None, tools="")
    p.vbar(x=df['Country or Area'], top=df['{}'.format(variabile)], width=0.5)
    p.xaxis.major_label_orientation = "vertical"
    show(p)




if __name__ == '__main__':
    '''Creo il file csv a partire dal file excel, eseguire solo se non si possiede già il file csv'''
    get_data_from_xlsx(xlsx_path, sheet_name)

    '''read csv'''
    df_global = pd.read_csv(csv_path, sep=';')

    '''Lista valori unici per paese ed anno'''
    unique_country, unique_data = get_unique_value(df_global)


    df_europe = get_Europe_country(df_global)

    df_europe_2018 = df_europe[df_europe['Year'] == 2018]
    df_europe_2019 = df_europe[df_europe['Year'] == 2019]

    print(df_europe.sort_values('Quantity', ascending=False))


    # print(df_europe[df_europe['Year'] == 2018])
    # print(df_europe[df_europe['Country or Area'] == 'Italy'])

    eu_unique_country, eu_unique_data = get_unique_value(df_europe)

    # df_grouped = df_europe[['Country or Area', 'Year']].groupby(['Country or Area']).count()
    # df_grouped = df_europe[['Country or Area', 'Year']].groupby(['Country or Area']).agg([min, max])

    df_europe = df_europe.drop_duplicates(subset=['Country or Area']).reset_index(drop=True)
    df_europe['Eolic prod / kmq'] = df_europe['Quantity'] / df_europe['Kmq']
    # print(df_europe[['Country or Area', 'Eolic prod / kmq']])

    # bokeh_histogram_energy_prod_vs_surface(df_europe[['Country or Area', 'Eolic prod / kmq']],
    #                                        title="Rapporto prod. eolico vs superficie")

    df_europe_2018 = df_europe[df_europe['Year'] == 2018]
    bokeh_histogram_energy_prod_vs_surface(df_europe_2018[['Country or Area', 'Quantity']],
                                           title="Produzione eolico 2018 per nazioni",
                                           variabile='Quantity')

    print(df_europe[df_europe['Country or Area']=='Kosovo'])
    # bokeh_histogram_single_country_per_year(df_europe, 'Italy')







