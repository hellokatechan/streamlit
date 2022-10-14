from curses.ascii import alt
from itsdangerous import encoding
from soupsieve import select
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import Sum
from tomlkit import key
import altair as alt

###
header=st.container()

with header:
    st.title("🏠 Airbnb Gross Earnings Dashboard")

st.sidebar.markdown('**Owner and Airbnb Co-Host Gross Earnings Dashboard**')
st.sidebar.markdown('''Definitions: 

Owners: The property owner. 

Airbnb Co-Host: Co-Hosts help listing owners take care of their home and guests.A portion of the reservation income goes to the Co-Host.

Motivation: 

As of date, the offical Airbnb dashboard does not include a graphical representation of gross earning broken down by user type(Owner and Airbnb Co-Host).

Design by: **Kate Chan**''' )

###


url="https://raw.githubusercontent.com/hellokatechan/airbnb_streamlit/main/airbnb_01_2016-02_2022.csv"
airbnb = pd.read_csv(url)

airbnb=airbnb[airbnb.columns.difference(['Start Date','Listing','Nights'])]
airbnb['Date'] = pd.to_datetime(airbnb['Date'])
airbnb['Year'] = airbnb['Date'].dt.year
airbnb['Month'] = airbnb['Date'].dt.month
airbnb_co = airbnb.groupby(['Confirmation Code'], as_index=False).min()
airbnb_host = airbnb.groupby(['Confirmation Code'], as_index=False).max()


###
st.header('Select the your role')
role = st.selectbox('I am a',('Owner','Airbnb Co-Host'))


st.header(f'Monthly Gross Earnings for {role}')
year= airbnb.Year.unique()
select_year = st.selectbox('I want to see year',year)

co = alt.Chart(airbnb_co[airbnb_co["Year"]==select_year],width=700,height=400).encode(x="Month",y="Gross Earnings", tooltip=['Gross Earnings']).interactive()
host = alt.Chart(airbnb_host[airbnb_host["Year"]==select_year],width=700,height=400).encode(x="Month",y="Gross Earnings", tooltip=['Gross Earnings']).interactive()

if role == "Airbnb Host":
        st.altair_chart(co.mark_bar(color='#8da0cb', size=20))
else:
        st.altair_chart(host.mark_bar(color='#8da0cb',size=20))