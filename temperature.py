import streamlit as st
import pandas as pd

#local
from const import *
from texts import *
import plots
import locale
from utils import get_max_month_name

class MonthlyAverage():
    def __init__(self):
        self.data = self.get_data()
        self.avg_data = self.get_avg_pre_indust()
        self.sel_par = 'Temperature'
        self.min_jahr =  int(self.data['Year'].min())
        self.max_jahr =  int(self.data['Year'].max())
        

    def get_avg_pre_indust(self):
        df = self.data[self.data['Year']< START_INDUSTRIAL_PERIOD]
        fields = ['Month', 'Temperature', 'Precipitation']
        group_fields = ['Month']
        df = df[fields].groupby(group_fields)['Temperature', 'Precipitation'].agg(['min', 'max', 'mean']).reset_index()
        df.columns = ['Month','Temperature_min', 'Temperature_max', 'Temperature_mean', 'Precipitation_min', 'Precipitation_max', 'Precipitation_mean']
        return(df)

    def get_data(self):
        # years = list(range(1910,2031,10))
        # group = pd.cut(s, bins=years, labels=years[:-1])
        # grouped = data.groupby([group, 'type']).size()
        col_widths = [6, 13, 17, 13]
        df = pd.read_fwf(TEMPERATUR_LONG, col_widths=col_widths)
        df['Day'] = 15
        df['Date'] = pd.to_datetime(df[['Year','Month','Day']])
        df[['Temperature', 'Precipitation']] = df[['Temperature', 'Precipitation']].astype(float)
        df[['Year', 'Month']] = df[['Year', 'Month']].astype(int)
        return df
    
    def show_heatmap(self, df):
        settings = {'width': 800, 'height': 800, 'x': 'Month:N', 'y': 'Year:N', 'color': 'Temperature', 'tooltip':['Year', 'Month', 'Temperature']}
        settings['title'] = f"Heatmap {self.sel_par}" 
        settings['color_scheme'] = "viridis" 
        settings['show_numbers'] = st.sidebar.checkbox('Zeige Werte in Zelle')
        plots.heatmap(df, settings)
    
    def show_timeseries(self, df):
        
        settings = {'width': 800, 'height': 400, 'x': 'Date', 'y': 'Temperature', 'x_title': 'Jahr', 
            'y_title': f"{self.sel_par}°C", 'tooltip':['Year', 'Month', self.sel_par]}
        settings['y_domain'] = [df[self.sel_par].min(), df[self.sel_par].max()]
        all_years = [self.min_jahr, self.max_jahr]
        years_sel =  st.sidebar.slider('Jahr von/bis', min_value=self.min_jahr, max_value=self.max_jahr, value=all_years)
        settings['show_regression'] = st.sidebar.checkbox('Zeige Regressionslinie')
        settings['show_average'] = st.sidebar.checkbox('Zeige Mittelwert')
        settings['rolling_avg_window'] = st.sidebar.number_input('Gleitendes Mittel Fenster (Mt)', min_value=0, max_value=1000)
        settings['title'] = f"Zeitreihe" 
        if years_sel != all_years:
            df = df[(df['Year']>= years_sel[0]) & (df['Year']<= years_sel[1])]
        plots.time_series_chart(df, settings)

        df = df.join(self.avg_data[['Month', 'Temperature_mean']].set_index('Month'), on='Month', how='inner',  lsuffix='', rsuffix='_agg')
        df['Temperature_diff'] = (df['Temperature'] - df['Temperature_mean']).astype(float)
        settings['y'] = "Temperature_diff"
        settings['y_domain'] = [df[settings['y']].min(), df[settings['y']].max()]
        settings['title']='Abweichungen des Monatsmittels vom Monatsmittel der Referenzperiode vor 1901'
        #print(df.dtypes)
        #settings['tooltip'] = ['Year', 'Month', settings['y']],
        plots.time_series_chart(df, settings)

        df = df[['Year', 'Temperature', 'Precipitation']].groupby(['Year'])[['Temperature', 'Precipitation']].agg('mean').reset_index()
        df['Month'] = 7
        df['Day'] = 1
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        settings['y'] = "Temperature"
        settings['x'] = 'Date'
        settings['x_dt'] = 'T'
        settings['y_domain'] = [df[settings['y']].min(), df[settings['y']].max()]
        settings['title']='Jahresmittel'
        #print(df.dtypes)
        #settings['tooltip'] = ['Year', 'Month', settings['y']],
        plots.time_series_chart(df, settings)

    
    def show_month_superposed(self, df):
        settings = {'width': 800, 'height': 400, 'x': 'Month', 'x_dt': 'N', 'y': 'Temperature', 'x_title': 'Jahr', 
            'y_title': f"{self.sel_par}°C", 'tooltip':['Year', 'Month', self.sel_par], 'color': 'Year', 'x_domain':list(range(1,13))}
        settings['y_domain'] = [df[self.sel_par].min(), df[self.sel_par].max()]
        settings['title'] = f"Zeitreihe, Monate" 
        plots.line_chart(df, settings)
        
        df = self.data.join(self.avg_data[['Month', 'Temperature_mean']].set_index('Month'), on='Month', how='inner',  lsuffix='', rsuffix='_agg')
        df['Temperature_diff'] = (df['Temperature'] - df['Temperature_mean']).astype(float)
        settings['y'] = 'Temperature_diff'
        settings['y_domain'] = [df[settings['y']].min(), df[settings['y']].max()]
        settings['title'] = 'Differenz Monatsmittel vom Monatsmittel der Referenzperiode vor 1901'

        plots.line_chart(df, settings)
        

    def show_menu(self):
        plot_options = ['Heatmap', 'Monate überlagert', 'Zeitreihe']
        plot_type = st.sidebar.selectbox('Darstellung', options=plot_options)
        if plot_options.index(plot_type) == 0:
            self.show_heatmap(self.data)
        if plot_options.index(plot_type) == 1:
            self.show_month_superposed(self.data)
        if plot_options.index(plot_type) == 2:
            self.show_timeseries(self.data)
