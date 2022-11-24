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
        self.current_month = get_max_month_name(self.data, 'datum')
        self.current_year = int(self.data['datum'].max().strftime('%Y'))
        self.sel_month = ''
        
    def get_data(self):
        # years = list(range(1910,2031,10))
        # group = pd.cut(s, bins=years, labels=years[:-1])
        # grouped = data.groupby([group, 'type']).size()
        df = pd.read_csv(URL_CLIMATE, sep=';')
        
        df['datum'] = pd.to_datetime(df['datum'])
        # df['jahrzent'] = (df['jahr'] / 10).astype(int) * 10
        id_vars=['datum','jahr','monat']
        value_vars = [i for i in df.columns if i not in id_vars]

        df = df.melt(id_vars=id_vars,value_vars=value_vars,
            var_name='parameter', 
            value_name='wert')
        return df

    def get_time_unit_plur(self):
        if self.type == StatType.MONTHLY.value:
            return 'Monate'
        else:
            return 'Jahre'

    def show_histogram(self, df):
        settings = {'width': 800, 'height': 400, 'x': 'wert', 'x_title': self.sel_par, 'y_title': f'Anzahl {self.get_time_unit_plur()}'}
        settings['title'] = f"Histogramm {self.sel_par}, {self.sel_years[0]} - {self.sel_years[1]}" 
        if self.type == StatType.MONTHLY.value:
            settings['title'] += f", Monat {self.sel_month}"
            if st.sidebar.checkbox('Zeige letzten Monat in Grafik'):
                value = self.data[(self.data['datum'] == self.max_date) & (self.data['parameter'] == self.sel_par)].iloc[0]['wert']
                settings['show_current_month'] = value
            
        plots.histogram(df, settings)
    
    def show_heatmap(self, df):
        settings = {'width': 800, 'height': 800, 'x': 'monat:N', 'y': 'jahr:N', 'color': 'wert:Q', 'tooltip':['parameter', 'jahr:O', 'monat', 'wert']}
        settings['title'] = f"Heatmap {self.sel_par}, {self.sel_years[0]} - {self.sel_years[1]}" 
        plots.heatmap(df, settings)
    
    def show_timeseries(self, df):
        settings = {'width': 800, 'height': 400, 'x': 'datum', 'y': 'wert', 'x_title': 'Jahr', 
            'y_title': self.sel_par, 'tooltip':['datum', 'parameter', 'wert']}
        settings['y_domain'] = [df['wert'].min(), df['wert'].max()]
        settings['show_regression'] = st.sidebar.checkbox('Zeige Regressionslinie')
        settings['show_average'] = st.sidebar.checkbox('Zeige Mittelwert')
        settings['title'] = f"Zeitreihe {self.sel_par}, {self.sel_years[0]} - {self.sel_years[1]}" 
        if self.type == StatType.MONTHLY.value:
            settings['title'] += f", Monat {self.sel_month}"
        
        plots.time_series_chart(df, settings)

    def show_table(self, df):
        current_year_rank = int(df.loc[df['jahr']==df['jahr'].max(), 'rang'].iloc[0])
        st.write(df)
        text = text = f"""Alle Werte für Parameter `{self.sel_par}` in den Jahren {self.sel_years[0]} bis {self.sel_years[1]}."""
        if self.type == StatType.MONTHLY.value:
            text += f""" für den Monat {self.sel_month}."""
        if self.current_year in range(self.sel_years[0], self.sel_years[1]+1):
            text += f""" Das aktuelle Jahr hat Rang {current_year_rank} von {len(df)}."""
        text += """ Klicke auf die Spaltentitel Rang oder Jahr um nach der entsprechenden Spalte zu sortieren."""
        st.markdown(text)
        # = """Alle Werte für Parameter {} seit 1921 für den Mponat {}. Das aktuelle Jahr hat Rang {} von {}"""

    def show_menu(self):
        def get_time_series_data():
            if self.type == StatType.MONTHLY.value:
                df = self.data[(self.data['monat']==self.sel_month) & (self.data['parameter']==self.sel_par)]
                df = df[df['jahr'].isin(range(self.sel_years[0],self.sel_years[1]+1))]
            else:
                df = self.data[(self.data['jahr'].isin(range(self.sel_years[0],self.sel_years[1]+1))) & (self.data['parameter']==self.sel_par)]
            return df
        
        def get_heatmap_data():
            df = self.data[(self.data['jahr'].isin(range(self.sel_years[0],self.sel_years[1]+1))) & (self.data['parameter']==self.sel_par)]
            return df
        
        def get_table_data():
            df = self.data[(self.data['jahr'].isin(range(self.sel_years[0],self.sel_years[1]+1))) & \
                (self.data['parameter'] == self.sel_par)]
            if self.type == StatType.MONTHLY.value:
                df = df[df['monat'] == self.sel_month]
            else:
                df = df.groupby(['parameter','jahr']).sum().reset_index()
            df = df[['parameter','jahr', 'wert']]
            df['rang'] = df.groupby('parameter')["wert"].rank("max", ascending=False)
            int_fields = ['wert','rang']
            df[int_fields] = df[int_fields].astype(int)
            return df

        self.sel_par = st.sidebar.selectbox('Parameter', options=self.parameters)
        self.sel_plot = st.sidebar.selectbox('Ausgabe', options=STAT_PLOTS)
        if self.type == StatType.MONTHLY.value:
            idx = STAT_MONTHS.index(self.current_month)
            self.sel_month = st.sidebar.selectbox('Monat', options=STAT_MONTHS, index=idx)
        self.sel_years = st.sidebar.slider('Jahr', min_value=1921, max_value=2022, value =(1921,2022))

        if STAT_PLOTS.index(self.sel_plot) == 0:
            df = get_time_series_data()
            self.show_histogram(df)
        if STAT_PLOTS.index(self.sel_plot) == 1:
            df = get_time_series_data()
            self.show_timeseries(df)
        if STAT_PLOTS.index(self.sel_plot) == 2:
            df = get_heatmap_data()
            self.show_heatmap(df)
        if STAT_PLOTS.index(self.sel_plot) == 3:
            df = get_table_data()
            self.show_table(df)