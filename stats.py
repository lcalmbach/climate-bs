import streamlit as st
import pandas as pd

#local
from const import *
from texts import *
import plots
import locale
from utils import get_max_month_name

class Stats():
    def __init__(self, type):
        self.type = type
        self.data = self.get_data()
        self.parameters = list(self.data['parameter'].unique())
        self.years = list(self.data['jahr'].unique())
        self.min_year, self.max_year = min(self.years), max(self.years)
        self.max_date = self.data['datum'].max()
        
    def get_data(self):
        # years = list(range(1910,2031,10))
        # group = pd.cut(s, bins=years, labels=years[:-1])
        # grouped = data.groupby([group, 'type']).size()
        df = pd.read_csv(URL_CLIMATE, sep=';')
        
        df['datum'] = pd.to_datetime(df['datum'])
        df['jahrzent'] = (df['jahr'] / 10).astype(int) * 10
        id_vars=['datum','jahr','monat', 'jahrzent']
        value_vars = [i for i in df.columns if i not in id_vars]

        df = df.melt(id_vars=id_vars,value_vars=value_vars,
            var_name='parameter', 
            value_name='wert')
        return df

    def show_histogram(self, month, param):
        df = self.data[(self.data['monat']==month) & (self.data['parameter']==param)]
        settings = {'width': 800, 'height': 400, 'x': 'wert', 'x_title': param, 'y_title': 'Anzahl Monate'}
        if st.sidebar.checkbox('Zeige letzten Monat in Grafik'):
            value = self.data[(self.data['datum'] == self.max_date) & (self.data['parameter'] == param)].iloc[0]['wert']
            settings['show_current_month'] = value
        plots.histogram(df, settings)
    
    def show_heatmap(self, month, param, sel_years):
        df = self.data[ (self.data['parameter']==param) & (self.data['jahr'].isin(range(sel_years[0],sel_years[1]+1))) ]
        settings = {'width': 800, 'height': 800, 'x': 'monat:N', 'y': 'jahr:N', 'color': 'wert:Q', 'tooltip':['parameter', 'jahr:O', 'monat', 'wert']}
        plots.heatmap(df, settings)
    
    def show_timeseries(self, month, param):
        df = self.data[(self.data['monat']==month) & (self.data['parameter']==param)]
        settings = {'width': 800, 'height': 400, 'x': 'datum', 'y': 'wert', 'x_title': 'Jahr', 
            'y_title': param, 'tooltip':['datum', 'parameter', 'wert']}
        settings['y_domain'] = [df['wert'].min(), df['wert'].max()]
        settings['show_regression'] = st.sidebar.checkbox('Zeige Regressionslinie')
        settings['show_average'] = st.sidebar.checkbox('Zeige Mittelwert')
        plots.time_series_chart(df, settings)

    def show_table(self, month, param, sel_years):
        df = self.data[(self.data['jahr'].isin(range(sel_years[0],sel_years[1]+1))) & \
            (self.data['monat'] == month) & \
            (self.data['parameter'] == param)]
        df = df[['parameter','jahr', 'wert']]
        df['rang'] = df.groupby('parameter')["wert"].rank("max", ascending=False)
        max_rank = int(df['rang'].max())
        current_year_rank = int(df.loc[df['jahr']==df['jahr'].max(), 'rang'].iloc[0])
        st.write(df)
        st.markdown(MONTH_VALUES_TABLE_LEGEND.format(param, month, current_year_rank, max_rank))
        # = """Alle Werte für Parameter {} seit 1921 für den Mponat {}. Das aktuelle Jahr hat Rang {} von {}"""

    def show_menu(self):
        locale.setlocale(locale.LC_TIME, 'de_DE')
        max_date = self.data['datum'].max()
        max_month_name = get_max_month_name(self.data, 'datum')
        sel_par = st.sidebar.selectbox('Parameter', options=self.parameters)
        sel_plot = st.sidebar.selectbox('Ausgabe', options=STAT_PLOTS)
        idx = STAT_MONTHS.index(max_month_name)
        sel_monat = st.sidebar.selectbox('Monat', options=STAT_MONTHS, index=idx)
        sel_years = st.sidebar.slider('Jahr', min_value=1921, max_value=2022, value =(1921,2022))

        if STAT_PLOTS.index(sel_plot) == 0:
            self.show_histogram(sel_monat, sel_par)
        if STAT_PLOTS.index(sel_plot) == 1:
            self.show_timeseries(sel_monat, sel_par)
        if STAT_PLOTS.index(sel_plot) == 2:
            self.show_heatmap(sel_monat, sel_par, sel_years)
        if STAT_PLOTS.index(sel_plot) == 3:
            self.show_table(sel_monat, sel_par, sel_years)