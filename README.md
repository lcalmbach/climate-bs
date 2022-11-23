# climate-bs
This [application](https://lcalmbach-climate-bs-app-c6nya9.streamlit.app/) allows to compare weather data with historic data since 1921. Data is used from https://data.bs. The app is written in python using the framework [streamlit](https://streamlit.io/) and the library [altair](https://altair-viz.github.io/). To install the app llocally proceed as follwos:
```
> git clone https://github.com/lcalmbach/climate-bs.git
> cd climate-bs
> python -m venv env
> env\scripts\activate
> pip install -r requirements.txt
> streamlit run app.py
```