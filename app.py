import streamlit as st 
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import requests
from const import *
from stats import Stats
from home import Home
from extremas import Extremas

__version__ = '0.0.2'
__author__ = 'Lukas Calmbach'
__author_email__ = 'lcalmbach@gmail.com'
VERSION_DATE = '2022-22-11'
my_name = 'Witterung-bs'
my_kuerzel = "WEx"
SOURCE_URL = 'https://data.bs.ch/explore/dataset/100227'
GIT_REPO = 'https://github.com/lcalmbach/climate-bs'


@st.experimental_memo()
def get_lottie():
    ok=True
    r=''
    try:
        r = requests.get(LOTTIE_URL).json()
    except:
        ok = False
    return r,ok

def get_info():
    text = f"""<div style="background-color:#34282C; padding: 10px;border-radius: 15px; border:solid 1px white;">
    <small>App von <a href="mailto:{__author_email__}">{__author__}</a><br>
    Version: {__version__} ({VERSION_DATE})<br>
    Quelle: <a href="{SOURCE_URL}">OpenData Kanton Basel-Stadt</a><br>
    <a href="{GIT_REPO}">git-repo</a></small></div>
    """
    return text

def main():
    st.set_page_config(
        page_title=my_name,
        layout="wide",
        page_icon='⛈️', )
    # load_css()
    lottie_search_names, ok = get_lottie()
    if ok:
        with st.sidebar:
            st_lottie(lottie_search_names,height=80, loop=20)
    else:
        pass
    
    menu_options = ['Home','Monats-Statistik', 'Rekorde']
    # https://icons.getbootstrap.com/
    with st.sidebar:
        st.markdown(f"## {my_name}")
        menu_action = option_menu(None, menu_options, 
            icons=['house', 'calendar-month', 'calendar'], 
            menu_icon="cast", default_index=0)

    if menu_action == menu_options[0]:
        app = Home()
    elif menu_action == menu_options[1]:
        app = Stats(StatType.MONTHLY.value)
    elif menu_action == menu_options[2]:
        app = Extremas(StatType.YEARLY.value)
    app.show_menu()
    st.sidebar.markdown(get_info(), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
