from enum import Enum

URL_CLIMATE = "https://data.bs.ch/explore/dataset/100227/download/?format=csv&timezone=Europe/Berlin&lang=de&use_labels_for_header=false&csv_separator=%3B"
LOTTIE_URL="https://assets9.lottiefiles.com/temp/lf20_rpC1Rd.json"

class StatType(Enum):
    MONTHLY = 1
    YEARLY = 2

STAT_PLOTS = ['Histogramm', 'Zeitreihe', 'Heatmap', 'Tabelle']
STAT_MONTHS = ['Januar', 'Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
MONTHS_REV_DICT = {'Januar':1, 'Februar':2, 'März':3, 'April':4, 'Mai':5, 'Juni':6, 'Juli':7, 'August':8, 'September':9,'Oktober':10,'November':11,'Dezember':12}
COMPARE_TIME_INTERVALS = ['1921 bis heute', '1900-1910']

PARAMETER_DESC = {'frosttag': 'Anzahl Tage mit Minimaltemperatur unter 0° Celsius',
    'eistag': 'Anzahl Tage mit Maximaltemperatur unter 0° Celsius',
    'sommertag': 'Anzahl Tage mit Maximaltemperatur über 25° Celsius',
    'hitzetag':'Anzahl Tage mit Maximaltemperatur über 30° Celsius',
    'sonnenlos':'Anzahl Tage mit 0 Sonnenstunden',
    'regen1':'Anzahl Tage mit höchstens 0.1 mm Niederschlag',
    'regen2':'Anzahl Tage mit höchstens 0.3 mm Niederschlag',
    'regen3':'Anzahl Tage mit mindestens 1.0 mm Niederschlag',
    'schneefall':'Anzahl Tage mit Schneefall',
    'schneedecke':'Anzahl Tage mit geschlossener Schneedecke',
    'reif': 'Anzahl Tage mit Reif',
    'nebel': 'Anzahl Tage mit Nebel',
    'gewitter1':'Anzahl Tage mit Nah- oder Ferngewitter',
    'gewitter2': 'Anzahl Tage mit Nahgewitter (<15 km Entfernung)',
    'hagel': 'Anzahl Tage mit Hagel',
    'hell': 'Anzahl Tage mit höchstens 20% Bewölkung',
    'trueb': 'Anzahl Tage mit mindestens 80% Bewölkung',
    'wind1': 'Anzahl Tage mit Windgeschwindigkeiten über 15 m/sec',
    'wind2': 'Anzahl Tage mit Windgeschwindigkeiten über 26 m/sec',
    'heizgradtage': 'Anzahl Tage mit einer mittleren Aussentemperatur unter 12°C'
}



ALL_MONTHS_EXPRESSION = 'Alle Monate'