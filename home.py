import streamlit as st
from const import *
import pandas as pd
import locale
from datetime import datetime

#local
from const import *
from texts import *
import plots
from utils import get_max_month_name

class Home():
    def __init__(self):
        self.data = self.get_data()
        self.parameters = list(self.data['parameter'].unique())
        self.years = list(self.data['jahr'].unique())
        self.min_year, self.max_year = min(self.years), max(self.years)
        
    def get_data(self):
        df = pd.read_csv(URL_CLIMATE, sep=';')
        df['datum'] = pd.to_datetime(df['datum'])
        df['jahrzent'] = (df['jahr'] / 10).astype(int) * 10
        id_vars=['datum','jahr', 'monat', 'jahrzent']
        value_vars = [i for i in df.columns if i not in id_vars]

        df = df.melt(id_vars=id_vars,value_vars=value_vars,
            var_name='parameter', 
            value_name='wert')
        return df

    def show_menu(self):
        st.title('Witterung-bs')
        st.markdown(HOME_INFO)
        locale.setlocale(locale.LC_TIME, 'de_DE')
        max_date = self.data['datum'].max()
        max_month_name = max_date.strftime('%B')
        month = get_max_month_name(self.data, 'datum')
        current_year = datetime.now().year
        (sel_year_from, sel_year_to) = st.slider(f'Vergleich {max_month_name}-Daten aktuell mit den {max_month_name} Werten der Jahre', min_value=1921, max_value=2022, value = (1921,2022))
        # df = pd.DataFrame({'Parameter':[2],'Oktober 2022':[1], 'Vergleichperiode Mittel':[2],'Rekord':[1]})
        df = self.data
        df_last_month = df[ df['datum'] == max_date][['parameter', 'wert']]
        df_all_months = df[(df['monat'] == max_month_name) & (df['jahr'].isin(range(sel_year_from, sel_year_to+1)))]
        df_all_months = df_all_months[['parameter', 'wert']]
        #df_all_months['rank'] = df.groupby('parameter')["wert"].rank("max", ascending=False)
        df_last_month = df_last_month.rename(columns={'wert': f"{max_month_name} {current_year}"})
        df_average = df_all_months[['parameter', 'wert']].groupby(['parameter']).agg(['mean', 'min', 'max', 'std']).reset_index()
        df_average.columns = ['parameter', 'mittelwert', 'minimum', 'maximum', 'standardabweichung']
        
        df = df_last_month.join(df_average.set_index('parameter'), on='parameter')
        
        st.write(df.set_index('parameter'))
        st.write(TABLE_LEGEND.format(max_month_name))

        with st.expander('Beschreibung der Parameter'):
            st.write(PARAMETER_DESC)
        