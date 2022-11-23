import streamlit as st
import pandas as pd

#local
from const import *
from texts import *
import plots

class Extremas():
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

    
    def show_extremas(self, month, years, param):
        df = self.data[(self.data['jahr'].isin(range(years[0], years[1]+1))) & \
            (self.data['parameter'] == param)]
        if month != ALL_MONTHS_EXPRESSION:
            df = df[df['monat'] == month]
        df = df[['jahr','monat','wert']]
        df['month_expression'] = df['monat'].astype(str) + ' ' + df['jahr'].astype(str)
        
        num_years = len(df['jahr'].unique())
        par_desc = PARAMETER_DESC[param]
        max = int(df['wert'].max())
        df_max = df[df['wert'] == max]
        num_max = len(df_max)
        max_months_csv_list = ', '.join(df_max['month_expression'])
        min = int(df['wert'].min())
        df_min = df[df['wert']==min]
        num_min = len(df_min)
        min_months_csv_list = ', '.join(df_min['month_expression'])
        avg = df['wert'].mean()
        std = df['wert'].std()
        num_within_2std = len(df[(df['wert'] <= avg + std) & (df['wert'] >= avg - std)])

        text = f"### Maxima und Verteilung für Parameter {par_desc} in den Jahren {years[0]} bis {years[1]}"
        if month == ALL_MONTHS_EXPRESSION:
            text +=  " (Ganzes Jahr)"
        else:
            text +=  f" (Monat {month})"
        st.markdown(text, unsafe_allow_html=True)
        text = f"""Der höchste Wert des Parameters `{par_desc}` während {num_years} Jahren beträgt {max}."""
        if num_max == 1:
            text += f" Dieses Maximum wurde im {max_months_csv_list} gemessen."
        elif num_max < 6:
            text += f" Dieses Maximum wurde {num_max} Mal erreicht in den Monaten {max_months_csv_list}."
        else:
            text += f" Dieses Maximum wurde {num_max} Mal gemessen."

        text += f""" Der tiefste Wert für diesen Parameter beträgt {min}."""
        if num_min == 1:
            text += f" Dieses Minimum wurde im {min_months_csv_list} registriert."
        elif num_min < 6:
            text += f" Das Minimum wurde {num_min} Mal erreicht in den Monaten {min_months_csv_list}."
        else:
            text += f" Das Minimum wurde {num_min} Mal erreicht."
        
        text += f""" Der Mittelwert des Parameters beträgt {avg:.1f} und die Standardabweichung {std:.1f}. Die Werte von {num_within_2std} 
        Monaten ({num_within_2std / len(df):.1%}) liegen im Intervall Mittelwert ± Standardabweichung. """
        st.markdown(text, unsafe_allow_html=True)

        with st.expander('Alle Werte'):
            st.write(df[['jahr','monat','wert']].sort_values('wert', ascending=False))

    def show_menu(self):
        sel_par = st.sidebar.selectbox('Parameter', options=self.parameters)
        sel_monat = st.sidebar.selectbox('Monat', options=[ALL_MONTHS_EXPRESSION] + STAT_MONTHS)
        sel_years = st.sidebar.slider('Jahr', min_value=1921, max_value=2022, value =(1921,2022))

        self.show_extremas(sel_monat, sel_years, sel_par)