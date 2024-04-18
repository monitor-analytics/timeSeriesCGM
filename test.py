import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from streamlit_option_menu import option_menu

with st.sidebar:
    selected=option_menu(
        menu_title = 'Menu',
        options = ['Overview', 'Statistics', 'Forecasting'],
        default_index=0
    )


df_clean = pd.read_csv('./data/cgm_data_clean.csv', usecols=range(3,7))


df_clean['Device Timestamp'] = pd.to_datetime(df_clean['Device Timestamp'])
df_clean_scan = df_clean[df_clean['Record Type'] == 1].drop_duplicates()
df_clean_historic = df_clean[df_clean['Record Type'] == 0].drop_duplicates()

# Line graph of data overtime
st.line_chart(data=df_clean_scan, x='Device Timestamp', y='Scan Glucose mmol/L')
st.line_chart(data=df_clean_historic, x='Device Timestamp', y='Historic Glucose mmol/L')

# Histograms of scanned vs historic glucose
base = alt.Chart(df_clean_scan, title='Distribution of scanned glucose results ')
bar = base.mark_bar().encode(
    x=alt.X('Scan Glucose mmol/L', bin=True, axis=None),
    y='count()'
)

#

rule = base.mark_rule(color='red').encode(
    x='mean(Scan Glucose mmol/L):Q',
    size=alt.value(5)
)

chart = bar + rule
st.altair_chart(chart, use_container_width=True)


# Understanding the statistical properties of the scanned glucose

# average_scanned_glucose = st.slider('Average the scanned readings over x days:', min_value=1, max_value=365)  # 👈 this is a widget
# df_clean_scan['Date'] = df_clean_scan['Device Timestamp'].dt.date
# df_clean_scan_daily_average = df_clean_scan.groupby('Date')['Scan Glucose mmol/L'].mean()
# average_scanned_bs = df_clean_scan_daily_average.rolling(window=average_scanned_glucose).mean().mean()
# st.write(average_scanned_bs)
# st.write('The average scanned glucose over', average_scanned_glucose, 'day(s) is:', average_scanned_bs)

st.write(df_clean_scan)
st.write(df_clean_historic)
