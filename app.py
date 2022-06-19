from curses import def_prog_mode
import streamlit as st
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from email.mime import image
import requests

img_mas = Image.open("images/malaysia.jpg")
img_python = Image.open("logo/python.jpg")
img_pandas = Image.open("logo/pandas.jpg")
img_plotly = Image.open("logo/plotly.jpg")
img_github = Image.open("logo/GitHub.jpg")
img_streamlit = Image.open("logo/streamlit.jpg")
st.set_page_config(page_title="My Dashboard", page_icon=":bar_chart:", layout="wide")
st.title('Data Science and Visualisation')

@st.experimental_memo
def read_csv(path) -> pd.DataFrame:
    return pd.read_csv(path)

# Covid Dataframe
# ---- READ DATA 1----
df_mas_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')
df_mas_deaths = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_malaysia.csv')
df_mas_vaksin = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv')
df_mas_pop = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/static/population.csv')
# Creating new columns
df_mas_cases['cum_cases'] = df_mas_cases['cases_new'].cumsum()
df_mas_cases['cum_recover'] = df_mas_cases['cases_recovered'].cumsum()
df_mas_deaths['cum_deaths'] = df_mas_deaths['deaths_new'].cumsum()
df_mas_vaksin['cum_vax'] = df_mas_vaksin['daily'].cumsum()
df_mas_cases_graph = pd.merge(df_mas_cases,df_mas_vaksin,on='date')
df_mas_cases_graph['vax_perc'] = (df_mas_cases_graph["daily_full"].cumsum()/df_mas_pop.at[df_mas_pop.index[0],'pop'])*100
df_mas_deaths_graph = pd.merge(df_mas_deaths, df_mas_vaksin,on='date')
df_mas_deaths_graph['vax_perc'] = (df_mas_deaths_graph["daily_full"].cumsum()/df_mas_pop.at[df_mas_pop.index[0],'pop'])*100
#st.dataframe(df_mas_cases)
# Creating New Date + Information
df_date_end = df_mas_cases.tail(1)
new_cases = df_mas_cases.tail(1)
new_recover = df_mas_cases.tail(1)
new_deaths = df_mas_deaths.tail(1)
new_vaksin = df_mas_vaksin.tail(1)
# Creating Yearly Data Tables
df1 = pd.merge(df_mas_cases,df_mas_deaths,on='date')
df1['frate'] = (df1['deaths_new']/df1['cases_new'])*100
new_frate = df1.tail(1)
df_covid = df_mas_cases.append(df_mas_deaths)
df_covid = df_covid.append(df_mas_vaksin)

def getYear(s):
  return s.split("-")[0]

def getMonth(s):
  return s.split("-")[1]

df_covid['Year']= df_covid['date'].apply(lambda x: getYear(x))
df_covid['Month']= df_covid['date'].apply(lambda x: getMonth(x))
df_covid = df_covid.groupby('Year').sum().reset_index()
# ---- READ DATA 2----
dfworld1 = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')
dfworld_top = dfworld1[dfworld1['continent'].notna()]
dfworld_top_cases = dfworld_top.sort_values('total_cases',ascending=False)
dfworld_top_cases = dfworld_top_cases.head(10)
dfworld_top_deaths = dfworld_top.sort_values('total_deaths',ascending=False)
dfworld_top_deaths = dfworld_top_deaths.head(10)
dfworld_top_vax = dfworld_top.sort_values('people_fully_vaccinated',ascending=False)
dfworld_top_vax = dfworld_top_vax.head(10)

df_asean = dfworld1[dfworld1['continent'].notna()]
df_asean = df_asean.loc[df_asean['location'].isin(['Malaysia','Singapore','Thailand','Indonesia','Philippines','Cambodia',
                                                  'Laos','Vietnam','Myanmar','Brunei'])]
df_asean_cases = df_asean.sort_values('total_cases',ascending=False)
df_asean_cases = df_asean_cases.head(10)
df_asean_deaths = df_asean.sort_values('total_deaths',ascending=False)
df_asean_deaths = df_asean_deaths.head(10)
df_asean_vax = df_asean.sort_values('people_fully_vaccinated',ascending=False)
df_asean_vax = df_asean_vax.head(10)
df_asean_pop = df_asean.sort_values('population',ascending=False)
df_asean_popdensity = df_asean.sort_values('population_density',ascending=False)
df_asean_gdp = df_asean.sort_values('gdp_per_capita',ascending=False)
df_asean_poverty = df_asean.sort_values('extreme_poverty',ascending=False)
df_asean_hdi = df_asean.sort_values('human_development_index',ascending=False)
df_asean_life = df_asean.sort_values('life_expectancy',ascending=False)

# ---- READ DATA 3----
dfworld2 = dfworld1.groupby('continent').sum().reset_index()
dfworld2['vaccination_percentage'] = (dfworld2['people_fully_vaccinated']/dfworld2['population'])*100
dfworld2 = dfworld2.sort_values('total_cases',ascending=False)

total_cases = int(df_covid["cases_new"].sum())
new_cases = int(new_cases.at[new_cases.index[0],'cases_new'])
total_recover = int(df_covid["cases_recovered"].sum())
new_recover = int(new_recover.at[new_recover.index[0],'cases_recovered'])
total_death = int(df_covid["deaths_new"].sum())
new_deaths = int(new_deaths.at[new_deaths.index[0],'deaths_new'])
total_full = int(df_covid["daily_full"].sum())
vax_perc = int((df_covid["daily_full"].sum()/df_mas_pop.at[df_mas_pop.index[0],'pop'])*100)
fatal_rate = new_frate.at[new_frate.index[0],'frate']

# ---- READ STATES DATA ----
df_states_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv')
df_states_deaths = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_state.csv')
df_states_vaksin = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv')
df_cases = df_states_cases.groupby('state').sum()
df_deaths = df_states_deaths.groupby('state').sum()
df_vaksin = df_states_vaksin.groupby('state').sum()
df_states = pd.merge(df_cases,df_deaths,on='state')
df_states = pd.merge(df_states,df_vaksin,on='state')
df_states = df_states.reset_index()

# Electricity Dataframe
df_e = pd.read_csv('./data/electric.csv')
df_e_main = df_e.groupby('Year').sum().reset_index()

df_e2014 = df_e[df_e.Year == 2014]
df_e2015 = df_e[df_e.Year == 2015]
df_e2016 = df_e[df_e.Year == 2016]
df_e2017 = df_e[df_e.Year == 2017]
df_e2018 = df_e[df_e.Year == 2018]
df_e2019 = df_e[df_e.Year == 2019]
df_e2020 = df_e[df_e.Year == 2020]
df_e2021 = df_e[df_e.Year == 2021]
df_e2022 = df_e[df_e.Year == 2022]

df_e2014 = df_e2014[['Month','Usage (kWh)','Cost (RM)']]
df_e2015 = df_e2015[['Month','Usage (kWh)','Cost (RM)']]
df_e2016 = df_e2016[['Month','Usage (kWh)','Cost (RM)']]
df_e2017 = df_e2017[['Month','Usage (kWh)','Cost (RM)']]
df_e2018 = df_e2018[['Month','Usage (kWh)','Cost (RM)']]
df_e2019 = df_e2019[['Month','Usage (kWh)','Cost (RM)']]
df_e2020 = df_e2020[['Month','Usage (kWh)','Cost (RM)']]
df_e2021 = df_e2021[['Month','Usage (kWh)','Cost (RM)']]
df_e2022 = df_e2022[['Month','Usage (kWh)','Cost (RM)']]

df_e2014.rename(columns={'Usage (kWh)':'2014 (kWh)','Cost (RM)':'2014 (RM)'},inplace=True)
df_e2015.rename(columns={'Usage (kWh)':'2015 (kWh)','Cost (RM)':'2015 (RM)'},inplace=True)
df_e2016.rename(columns={'Usage (kWh)':'2016 (kWh)','Cost (RM)':'2016 (RM)'},inplace=True)
df_e2017.rename(columns={'Usage (kWh)':'2017 (kWh)','Cost (RM)':'2017 (RM)'},inplace=True)
df_e2018.rename(columns={'Usage (kWh)':'2018 (kWh)','Cost (RM)':'2018 (RM)'},inplace=True)
df_e2019.rename(columns={'Usage (kWh)':'2019 (kWh)','Cost (RM)':'2019 (RM)'},inplace=True)
df_e2020.rename(columns={'Usage (kWh)':'2020 (kWh)','Cost (RM)':'2020 (RM)'},inplace=True)
df_e2021.rename(columns={'Usage (kWh)':'2021 (kWh)','Cost (RM)':'2021 (RM)'},inplace=True)
df_e2022.rename(columns={'Usage (kWh)':'2022 (kWh)','Cost (RM)':'2022 (RM)'},inplace=True)

df_etable = pd.merge(df_e2014,df_e2015, on='Month')
df_etable = pd.merge(df_etable,df_e2016, on='Month')
df_etable = pd.merge(df_etable,df_e2017, on='Month')
df_etable = pd.merge(df_etable,df_e2018, on='Month')
df_etable = pd.merge(df_etable,df_e2019, on='Month')
df_etable = pd.merge(df_etable,df_e2020, on='Month')
df_etable = pd.merge(df_etable,df_e2021, on='Month')
df_etable = pd.merge(df_etable,df_e2022, on='Month')

df_eusage = df_etable[['Month','2014 (kWh)','2015 (kWh)','2016 (kWh)','2017 (kWh)','2018 (kWh)','2019 (kWh)',
'2020 (kWh)','2021 (kWh)','2022 (kWh)']]
df_eusage.rename(columns={'2014 (kWh)':'2014','2015 (kWh)':'2015','2016 (kWh)':'2016','2017 (kWh)':'2017',
'2018 (kWh)':'2018','2019 (kWh)':'2019','2020 (kWh)':'2020','2021 (kWh)':'2021','2022 (kWh)':'2022'},inplace=True)
df_eusage = df_eusage.fillna(0)
df_eusage = df_eusage.astype({'2014':'int','2015':'int','2016':'int','2017':'int','2018':'int',
                           '2019':'int','2020':'int','2021':'int','2022':'int'})
df_eusage = df_eusage.round(2)

df_ecost = df_etable[['Month','2014 (RM)','2015 (RM)','2016 (RM)','2017 (RM)','2018 (RM)','2019 (RM)',
'2020 (RM)','2021 (RM)','2022 (RM)']]
df_ecost.rename(columns={'2014 (RM)':'2014','2015 (RM)':'2015','2016 (RM)':'2016','2017 (RM)':'2017',
'2018 (RM)':'2018','2019 (RM)':'2019','2020 (RM)':'2020','2021 (RM)':'2021','2022 (RM)':'2022'},inplace=True)
df_ecost = df_ecost.fillna(0)
df_ecost = df_ecost.astype({'2014':'int','2015':'int','2016':'int','2017':'int','2018':'int',
                           '2019':'int','2020':'int','2021':'int','2022':'int'})
df_ecost = df_ecost.round(2)

# Water Dataframe
df_w = pd.read_csv('./data/water.csv')

df_w2019 = df_w[df_w.Year == 2019]
df_w2020 = df_w[df_w.Year == 2020]
df_w2021 = df_w[df_w.Year == 2021]
df_w2022 = df_w[df_w.Year == 2022]

df_w2019 = df_w2019[['Month','Usage (m3)','Cost (RM)']]
df_w2020 = df_w2020[['Month','Usage (m3)','Cost (RM)']]
df_w2021 = df_w2021[['Month','Usage (m3)','Cost (RM)']]
df_w2022 = df_w2022[['Month','Usage (m3)','Cost (RM)']]

df_w2019.rename(columns={'Usage (m3)':'2019 (m3)','Cost (RM)':'2019 (RM)'},inplace=True)
df_w2020.rename(columns={'Usage (m3)':'2020 (m3)','Cost (RM)':'2020 (RM)'},inplace=True)
df_w2021.rename(columns={'Usage (m3)':'2021 (m3)','Cost (RM)':'2021 (RM)'},inplace=True)
df_w2022.rename(columns={'Usage (m3)':'2022 (m3)','Cost (RM)':'2022 (RM)'},inplace=True)

df_wtable = pd.merge(df_w2019,df_w2020, on='Month')
df_wtable = pd.merge(df_wtable,df_w2021, on='Month')
df_wtable = pd.merge(df_wtable,df_w2022, on='Month')

df_wusage = df_wtable[['Month','2019 (m3)','2020 (m3)','2021 (m3)','2022 (m3)']]
df_wusage.rename(columns={'2019 (m3)':'2019','2020 (m3)':'2020','2021 (m3)':'2021','2022 (m3)':'2022'},inplace=True)
df_wusage = df_wusage.fillna(0)
df_wusage = df_wusage.astype({'2019':'int','2020':'int','2021':'int','2022':'int'})
df_wusage = df_wusage.round(2)

df_wcost = df_wtable[['Month','2019 (RM)','2020 (RM)','2021 (RM)','2022 (RM)']]
df_wcost.rename(columns={'2019 (RM)':'2019','2020 (RM)':'2020','2021 (RM)':'2021','2022 (RM)':'2022'},inplace=True)
df_wcost = df_wcost.fillna(0)
df_wcost = df_wcost.astype({'2019':'int','2020':'int','2021':'int','2022':'int'})
df_wcost = df_wcost.round(2)

df_w_main = df_w.groupby('Year').sum().reset_index()

# ---Malaysia Fact Sheets---
# ---Malaysia Income---
df_mas_income = pd.read_csv('./data/Federal Government Revenue 2000 - 2020_dataset.csv')
df_income_year = df_mas_income.groupby('Year').sum()
df_income_year['Cumulative'] = df_income_year['RM Million'].cumsum()
df_income_year = df_income_year.reset_index()
df_2020 = df_mas_income[df_mas_income.Year == 2020].sort_values('RM Million',ascending=False)

# ---Malaysia Population---
df_mas_pop =  pd.read_csv('./data/Malaysia_Population_dataset.csv')
df_mas_total = df_mas_pop[df_mas_pop.Age_Group == 'Total Age Group']
df_mas_total = df_mas_total[df_mas_total.Ethnic_Group == 'Total Ethnic Group']
df_mas_total = df_mas_total[df_mas_total.Sex == 'Total Sex']
df_mas_total['Cumulative'] = df_mas_total['Value'].cumsum()

df_mas_ethnic = df_mas_pop[df_mas_pop.Sex == 'Total Sex']
df_mas_ethnic = df_mas_ethnic[df_mas_ethnic.Age_Group == 'Total Age Group']
df_mas_ethnic = df_mas_ethnic[df_mas_ethnic.Ethnic_Group != 'Total Ethnic Group']
df_mas_ethnic = df_mas_ethnic[df_mas_ethnic.Year == 2020].sort_values('Value',ascending=False)

# ---Water Treatment Plant---
df_water_treat = pd.read_csv('./data/Water treatment plants design capacity by state Malaysia 2000 - 2020_dataset.csv')

df_water_state = df_water_treat[df_water_treat.Year == 2020]
df_water_state = df_water_state.sort_values('Total',ascending=False)
df_water_state['Population'] = [(6555100+1746600+116100),3794200,2824700,2509000,1774200,2193600,3832500,1684700,1128900,1275200,
                                937800,1928900,255500,100100]

df_water_year = df_water_treat.groupby('Year').sum().reset_index()
df_water_year['Cumulative'] = df_water_year['Total'].cumsum()

df_econ = pd.read_csv('./data/Electricity Consumption - 2018-2022 (Jan-Mar)  Malaysia (Monthly)_dataset.csv')
df_egen = pd.read_csv('./data/Electricity Generation 2018-2022 (Jan-Mar) Malaysia (Monthly)_dataset.csv')
df_econ = df_econ.groupby('Year').sum()
df_econ['Total Local Consumption (Million kilowatt-hours)'] = df_econ['Local consumption-Industrial, commercial and mining (Million kilowatt-hours)']+df_econ['Local consumption- Domestic and public lighting (Million kilowatt-hours)']
df_econ['Total Consumption'] = df_econ['Local consumption-Industrial, commercial and mining (Million kilowatt-hours)']+df_econ['Local consumption- Domestic and public lighting (Million kilowatt-hours)']+df_econ['Exports (Million kilowatt-hours)']+df_econ['Losses (Million kilowatt-hours)']
df_egen = df_egen.groupby('Year').sum()
df_egen['Revenue (RM Million)'] = [50392.5,50939.7,43976,52629.5,0]
df_energy_table = pd.merge(df_egen,df_econ,on='Year')
df_energy_table = df_energy_table.reset_index()
df_energy_table = df_energy_table[df_energy_table.Year != 2022]

# ---Malaysia Annual Rainfall---
df_rainfall = pd.read_csv('./data/Mean temperature rainfall volume and mean relative humidity Malaysia 2000 - 2020_dataset.csv')
df_rainfall[["Mean temperature-Min (oC)", "Mean temperature-Max (oC)","Rainfall-Total (mm)","Rainfall-No. of days",
            "Mean relative humidity (%)"]] = df_rainfall[["Mean temperature-Min (oC)", "Mean temperature-Max (oC)","Rainfall-Total (mm)",
            "Rainfall-No. of days","Mean relative humidity (%)"]].apply(pd.to_numeric, errors='coerce')
df_rainfall_year = df_rainfall.groupby('Year').sum().reset_index()
df_rainfall_year['Cumulative'] = df_rainfall_year['Rainfall-Total (mm)'].cumsum()
df_rainfall_state = df_rainfall[df_rainfall.Year == 2020]
df_rainfall_state = df_rainfall_state.groupby('State').sum().reset_index()

df_state_2000 = df_rainfall[df_rainfall.Year == 2000]
df_state_2000 = df_state_2000.groupby('State').sum().reset_index()
df_state_2000 = df_state_2000[['State','Rainfall-Total (mm)']]
df_state_2000.rename(columns={'Rainfall-Total (mm)':'2000'},inplace=True)
df_state_2001 = df_rainfall[df_rainfall.Year == 2001]
df_state_2001 = df_state_2001.groupby('State').sum().reset_index()
df_state_2001 = df_state_2001[['State','Rainfall-Total (mm)']]
df_state_2001.rename(columns={'Rainfall-Total (mm)':'2001'},inplace=True)
df_state_2002 = df_rainfall[df_rainfall.Year == 2002]
df_state_2002 = df_state_2002.groupby('State').sum().reset_index()
df_state_2002 = df_state_2002[['State','Rainfall-Total (mm)']]
df_state_2002.rename(columns={'Rainfall-Total (mm)':'2002'},inplace=True)
df_state_2003 = df_rainfall[df_rainfall.Year == 2003]
df_state_2003 = df_state_2003.groupby('State').sum().reset_index()
df_state_2003 = df_state_2003[['State','Rainfall-Total (mm)']]
df_state_2003.rename(columns={'Rainfall-Total (mm)':'2003'},inplace=True)
df_state_2004 = df_rainfall[df_rainfall.Year == 2004]
df_state_2004 = df_state_2004.groupby('State').sum().reset_index()
df_state_2004 = df_state_2004[['State','Rainfall-Total (mm)']]
df_state_2004.rename(columns={'Rainfall-Total (mm)':'2004'},inplace=True)
df_state_2005 = df_rainfall[df_rainfall.Year == 2005]
df_state_2005 = df_state_2005.groupby('State').sum().reset_index()
df_state_2005 = df_state_2005[['State','Rainfall-Total (mm)']]
df_state_2005.rename(columns={'Rainfall-Total (mm)':'2005'},inplace=True)
df_state_2006 = df_rainfall[df_rainfall.Year == 2006]
df_state_2006 = df_state_2006.groupby('State').sum().reset_index()
df_state_2006 = df_state_2006[['State','Rainfall-Total (mm)']]
df_state_2006.rename(columns={'Rainfall-Total (mm)':'2006'},inplace=True)
df_state_2007 = df_rainfall[df_rainfall.Year == 2007]
df_state_2007 = df_state_2007.groupby('State').sum().reset_index()
df_state_2007 = df_state_2007[['State','Rainfall-Total (mm)']]
df_state_2007.rename(columns={'Rainfall-Total (mm)':'2007'},inplace=True)
df_state_2008 = df_rainfall[df_rainfall.Year == 2008]
df_state_2008 = df_state_2008.groupby('State').sum().reset_index()
df_state_2008 = df_state_2008[['State','Rainfall-Total (mm)']]
df_state_2008.rename(columns={'Rainfall-Total (mm)':'2008'},inplace=True)
df_state_2009 = df_rainfall[df_rainfall.Year == 2009]
df_state_2009 = df_state_2009.groupby('State').sum().reset_index()
df_state_2009 = df_state_2009[['State','Rainfall-Total (mm)']]
df_state_2009.rename(columns={'Rainfall-Total (mm)':'2009'},inplace=True)
df_state_2010 = df_rainfall[df_rainfall.Year == 2010]
df_state_2010 = df_state_2010.groupby('State').sum().reset_index()
df_state_2010 = df_state_2010[['State','Rainfall-Total (mm)']]
df_state_2010.rename(columns={'Rainfall-Total (mm)':'2010'},inplace=True)
df_state_2011 = df_rainfall[df_rainfall.Year == 2011]
df_state_2011 = df_state_2011.groupby('State').sum().reset_index()
df_state_2011 = df_state_2011[['State','Rainfall-Total (mm)']]
df_state_2011.rename(columns={'Rainfall-Total (mm)':'2011'},inplace=True)
df_state_2012 = df_rainfall[df_rainfall.Year == 2012]
df_state_2012 = df_state_2012.groupby('State').sum().reset_index()
df_state_2012 = df_state_2012[['State','Rainfall-Total (mm)']]
df_state_2012.rename(columns={'Rainfall-Total (mm)':'2012'},inplace=True)
df_state_2013 = df_rainfall[df_rainfall.Year == 2013]
df_state_2013 = df_state_2013.groupby('State').sum().reset_index()
df_state_2013 = df_state_2013[['State','Rainfall-Total (mm)']]
df_state_2013.rename(columns={'Rainfall-Total (mm)':'2013'},inplace=True)
df_state_2014 = df_rainfall[df_rainfall.Year == 2014]
df_state_2014 = df_state_2014.groupby('State').sum().reset_index()
df_state_2014 = df_state_2014[['State','Rainfall-Total (mm)']]
df_state_2014.rename(columns={'Rainfall-Total (mm)':'2014'},inplace=True)
df_state_2015 = df_rainfall[df_rainfall.Year == 2015]
df_state_2015 = df_state_2015.groupby('State').sum().reset_index()
df_state_2015 = df_state_2015[['State','Rainfall-Total (mm)']]
df_state_2015.rename(columns={'Rainfall-Total (mm)':'2015'},inplace=True)
df_state_2016 = df_rainfall[df_rainfall.Year == 2016]
df_state_2016 = df_state_2016.groupby('State').sum().reset_index()
df_state_2016 = df_state_2016[['State','Rainfall-Total (mm)']]
df_state_2016.rename(columns={'Rainfall-Total (mm)':'2016'},inplace=True)
df_state_2017 = df_rainfall[df_rainfall.Year == 2017]
df_state_2017 = df_state_2017.groupby('State').sum().reset_index()
df_state_2017 = df_state_2017[['State','Rainfall-Total (mm)']]
df_state_2017.rename(columns={'Rainfall-Total (mm)':'2017'},inplace=True)
df_state_2018 = df_rainfall[df_rainfall.Year == 2018]
df_state_2018 = df_state_2018.groupby('State').sum().reset_index()
df_state_2018 = df_state_2018[['State','Rainfall-Total (mm)']]
df_state_2018.rename(columns={'Rainfall-Total (mm)':'2018'},inplace=True)
df_state_2019 = df_rainfall[df_rainfall.Year == 2019]
df_state_2019 = df_state_2019.groupby('State').sum().reset_index()
df_state_2019 = df_state_2019[['State','Rainfall-Total (mm)']]
df_state_2019.rename(columns={'Rainfall-Total (mm)':'2019'},inplace=True)
df_state_2020 = df_rainfall[df_rainfall.Year == 2020]
df_state_2020 = df_state_2020.groupby('State').sum().reset_index()
df_state_2020 = df_state_2020[['State','Rainfall-Total (mm)']]
df_state_2020.rename(columns={'Rainfall-Total (mm)':'2020'},inplace=True)

df_state_rainfall_table = pd.merge(df_state_2000, df_state_2001, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2002, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2003, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2004, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2005, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2006, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2007, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2008, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2009, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2010, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2011, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2012, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2013, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2014, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2015, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2016, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2017, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2018, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2019, on='State')
df_state_rainfall_table = pd.merge(df_state_rainfall_table, df_state_2020, on='State')

df_currency = pd.read_csv('./data/Commercial Banks  Exchange Rates Of Ringgit Malaysia 2000 - 2020_dataset.csv')
df_euro = df_currency[df_currency.Currency == 'Euro'].reset_index()
df_euro['Cumulative'] = df_euro['Exchange rates (Average for period)'].cumsum()
df_dollar = df_currency[df_currency.Currency == 'U.S.  dollar'].reset_index()
df_dollar['Cumulative'] = df_dollar['Exchange rates (Average for period)'].cumsum()
df_sing = df_currency[df_currency.Currency == 'Singapore  Dollar'].reset_index()
df_sing['Cumulative'] = df_sing['Exchange rates (Average for period)'].cumsum()
df_pound = df_currency[df_currency.Currency == 'Pound  Sterling'].reset_index()
df_pound['Cumulative'] = df_pound['Exchange rates (Average for period)'].cumsum()
df_indo = df_currency[df_currency.Currency == 'Indonesia  Rupiahs '].reset_index()
df_indo['Cumulative'] = df_indo['Exchange rates (Average for period)'].cumsum()
df_thai = df_currency[df_currency.Currency == 'Thai  Bahts'].reset_index()
df_thai['Cumulative'] = df_thai['Exchange rates (Average for period)'].cumsum()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

def main():

    page = st.selectbox("", ['Home','Covid19 Dashboard', 'Electricity Dashboard', 'Water Dashboard','Malaysia','ASEAN'])

    if page == 'Home':
        st.header("Main Dashboard Pages")
        #st.subheader("By Zahiruddin Zahidanishah")
        st.write("This website consists of several dashboards; namely Covid19 Dashboard, Electricity Dashboard, Water Dashboard and Malaysia Fact Sheets.")
        st.write("1. Covid19 Dashboard shows the current cases and trends focusing in Malaysia and also selected countries around the world. Data for this dashboards are retrieved from [KKM Github pages](https://github.com/MoH-Malaysia/covid19-public) and from [Johns Hopkins University CSSE Github pages](https://github.com/CSSEGISandData/COVID-19). More details on the Covid19 reports can be view at [Covid19 Full Report](https://zzahir1978.github.io/projects/Covid19MalaysiaNow.html) ")
        st.write("2. Electricity Dashboard shows the electricity usage and cost for a typical double storey residential house located in Malaysia. Data for this dashboard is based on the monthly TNB meter billing. The electricity usage is measured in kWh and cost is measured in RM.")
        st.write("3. Water Dashboard shows the water usage and cost for a typical double storey residential house located in Malaysia. Data for this dashboard is based on the monthly Air Selangor meter billing. Water usage is measured in m3 and cost is measured in RM.")
        st.write("4. Malaysia Facts Sheets will shows Malaysia several main statistical information. The site will be updated in progress according to the available dataset retrieved from [Malaysia Informative Data Centre (MysIDC)](https://mysidc.statistics.gov.my).")
        st.write("This website is created by Zahiruddin Zahidanishah using open source application such as Python, Pandas, Plotly, Streamlit and Github.")
        st.write("Please feels free to contact me via [Email](mailto:zahiruddin.zahidanishah@gmail.com) or [WhatsApp](https://wa.me/60103647801?) for any inquiries or recommendation at any time.")
        st.write("To get more details on my knowledge and experience, please click on [My Resume](https://zzahir1978.github.io/resume/resume.html).")
        
        # ---- CONTACT ----
        with st.container():
            st.write("---")
            st.subheader("Get In Touch With Me!")
            st.write("##")

        # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
            contact_form = """
            <form action="https://formsubmit.co/bf85918df6af8e2139d0a995ae42c37a" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
            st.empty()

        # Logos
        st.write("---")
        st.write("##")
        st.write("Powered By:")
        with st.container():
            #st.write("---")
            first_column, second_column, third_column, fourth_column, fifth_column = st.columns(5)
            with first_column:
                st.image(img_python)
            with second_column:
                st.image(img_pandas)
            with third_column:
                st.image(img_plotly)
            with fourth_column:
                st.image(img_streamlit)
            with fifth_column:
                st.image(img_github)

    elif page == 'Covid19 Dashboard':
        st.header(":bar_chart: Malaysia Covid19 Dashboard")
        st.subheader(f"Updated On: {df_date_end.at[df_date_end.index[0],'date']}")
        st.markdown("##")
        first_column, second_column, third_column, fourth_column = st.columns(4)
        with first_column:
            st.subheader(":red_circle: Total Cases:")
            st.subheader(f"{total_cases:,}")
        with second_column:
            st.subheader(":large_blue_circle: Total Recover:")
            st.subheader(f"{total_recover:,}")
        with third_column:
            st.subheader(":black_circle: Total Deaths:")
            st.subheader(f"{total_death:,}")
        with fourth_column:
            st.subheader(":syringe: Full Vax.:")
            st.subheader(f"{vax_perc:,}%")

        first_column, second_column, third_column, fourth_column = st.columns(4)
        with first_column:
            st.subheader(":red_circle: New Cases:")
            st.subheader(f"{new_cases:,}")
        with second_column:
            st.subheader(":large_blue_circle: New Recover:")
            st.subheader(f"{new_recover:,}")
        with third_column:
            st.subheader(":black_circle: New Deaths:")
            st.subheader(f"{new_deaths:,}")
        with fourth_column:
            st.subheader("Fatality Rate:")
            #st.subheader(f"{fatal_rate:,.2f}%")
            st.subheader(f"{(new_cases/new_cases):,.0f} : "f"{(new_deaths/new_cases):,.3f}")
        
        st.markdown("""---""")
        st.subheader('Malaysia Covid19 Cases') 
        #Year = st.multiselect("Select the Year:",options=df_covid["Year"].unique(),default=df_covid["Year"].unique())
        #df_selection = df_covid.query("Year == @Year")
        df_selection = df_covid
        # Malaysia Charts 
        # New Cases Bar Chart
        fig_cases = px.bar(
            df_selection,x="Year",y=["cases_new","cases_fvax"],barmode="group",
            title="Total Cases by Year",template="plotly_white")
        fig_cases.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_cases.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_cases.add_hline(y=df_selection['cases_new'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Cases", annotation_position="bottom left")

        # Deaths Cases Bar Chart
        fig_deaths = px.bar(
            df_selection,x="Year",y=["deaths_new",'deaths_fvax'],barmode='group',
            title="Total Deaths by Year",template="plotly_white")
        fig_deaths.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_deaths.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_deaths.add_hline(y=df_selection['deaths_new'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Deaths", annotation_position="bottom left")

        # Vaccination Bar Chart
        fig_vax = px.bar(
            df_selection,x="Year",y=["daily_full",'daily_booster'],barmode='group',
            title="Total Vaccination by Year",template="plotly_white")
        fig_vax.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_vax.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph Layout
        # First Row Graph
        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(fig_cases, use_container_width=True)
        middle_column.plotly_chart(fig_deaths, use_container_width=True)
        right_column.plotly_chart(fig_vax, use_container_width=True)

        # Daily Cases Chart
        fig_cases_daily = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_cases_daily.add_trace(go.Scatter(x = df_mas_cases_graph['date'], y = df_mas_cases_graph['cases_new'],name='New Cases',
            fill='tozeroy',mode='lines', line = dict(color='blue', width=1)), secondary_y=True)
        fig_cases_daily.add_trace(go.Scatter(x = df_mas_cases_graph['date'], y = df_mas_cases_graph['vax_perc'],name='Vax %',
            fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=False)
        fig_cases_daily.update_layout(height=350,title_text='Daily New Cases VS Vax %',title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_cases_daily.update_annotations(font=dict(family="Helvetica", size=10))
        fig_cases_daily.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_cases_daily.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Daily Deaths Chart
        fig_deaths_daily = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_deaths_daily.add_trace(go.Scatter(x = df_mas_deaths_graph['date'], y = df_mas_deaths_graph['deaths_new'],name='Deaths Cases',
            fill='tozeroy',mode='lines', line = dict(color='blue', width=1)), secondary_y=True)
        fig_deaths_daily.add_trace(go.Scatter(x = df_mas_deaths_graph['date'], y = df_mas_deaths_graph['vax_perc'],name='Vax %',
            fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=False)
        fig_deaths_daily.update_layout(height=350,title_text='Daily Deaths Cases VS Vax %',title_x=0.5,font=dict(family="Helvetica", 
            size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,
            showlegend=False)
        fig_deaths_daily.update_annotations(font=dict(family="Helvetica", size=10))
        fig_deaths_daily.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_deaths_daily.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Daily Vaksin Chart
        fig_vax_daily = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_vax_daily.add_trace(go.Scatter(x = df_mas_vaksin['date'], y = df_mas_vaksin['daily'],name='Daily Vax',fill='tozeroy',
            mode='lines', line = dict(color='blue', width=1)), secondary_y=True)
        fig_vax_daily.add_trace(go.Scatter(x = df_mas_vaksin['date'], y = df_mas_vaksin['cum_vax'],name='Cum. Vax',fill='tozeroy',
            mode='lines',line = dict(color='red', width=1)), secondary_y=False)
        fig_vax_daily.update_layout(height=350,title_text='Daily Vaccination',title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_vax_daily.update_annotations(font=dict(family="Helvetica", size=10))
        fig_vax_daily.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_vax_daily.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Second Row Graph
        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(fig_cases_daily, use_container_width=True)
        middle_column.plotly_chart(fig_deaths_daily, use_container_width=True)
        right_column.plotly_chart(fig_vax_daily, use_container_width=True)

        st.subheader('Malaysia States Covid19 Cases')
        # States Graphs
        # States Cases [PIE CHART]
        fig_states_cases = make_subplots(specs=[[{"type": "domain"}]])
        fig_states_cases.add_trace(go.Pie(
            values=df_states['cases_new'],labels=df_states['state'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_states_cases.update_layout(height=350, showlegend=False,title_text='States Positive Cases',title_x=0.5)
        fig_states_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_states_cases.update_layout(font=dict(family="Helvetica", size=10))

        # States Deaths [PIE CHART]
        fig_states_deaths = make_subplots(specs=[[{"type": "domain"}]])
        fig_states_deaths.add_trace(go.Pie(
            values=df_states['deaths_new'],labels=df_states['state'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_states_deaths.update_layout(height=350, showlegend=False,title_text='States Deaths Cases',title_x=0.5)
        fig_states_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_states_deaths.update_layout(font=dict(family="Helvetica", size=10))

        # States Vaccination [PIE CHART]
        fig_states_vax = make_subplots(specs=[[{"type": "domain"}]])
        fig_states_vax.add_trace(go.Pie(
            values=df_states['daily'],labels=df_states['state'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_states_vax.update_layout(height=350, showlegend=False,title_text='States Vaccination',title_x=0.5)
        fig_states_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_states_vax.update_layout(font=dict(family="Helvetica", size=10))

        # Graph layout
        # Second Row Graph
        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(fig_states_cases, use_container_width=True)
        middle_column.plotly_chart(fig_states_deaths, use_container_width=True)
        right_column.plotly_chart(fig_states_vax, use_container_width=True)

        st.subheader('ASEAN Covid19 Cases')
        # ASEAN Bar Chart
        # ASEAN Total Cases
        fig_asean_cases = px.bar(
            df_asean_cases,x="location",y="total_cases",title="Total Positive Cases",template="plotly_white")
        fig_asean_cases.update_layout(
        height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_asean_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_cases.update_xaxes(title_text='ASEAN Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_asean_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # ASEAN Deaths Cases
        fig_asean_deaths = px.bar(
            df_asean_deaths,x="location",y="total_deaths",title="Total Deaths Cases",template="plotly_white")
        fig_asean_deaths.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_asean_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_deaths.update_xaxes(title_text='ASEAN Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_asean_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # ASEAN Vaccination
        fig_asean_vax = px.bar(
            df_asean_vax,x="location",y="people_fully_vaccinated",title="Total Vaccination",template="plotly_white")
        fig_asean_vax.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_asean_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_vax.update_xaxes(title_text='ASEAN Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_asean_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Third Row Graph
        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(fig_asean_cases, use_container_width=True)
        middle_column.plotly_chart(fig_asean_deaths, use_container_width=True)
        right_column.plotly_chart(fig_asean_vax, use_container_width=True)

        st.subheader('World Countries Covid19 Cases')
        # World Top Bar Chart
        # World Top Total Cases
        fig_world_top_cases = px.bar(
            dfworld_top_cases,x="location",y="total_cases",title="Total Positive Cases",template="plotly_white")
        fig_world_top_cases.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_world_top_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_world_top_cases.update_xaxes(title_text='World Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_world_top_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # World Top Deaths Cases
        fig_world_top_deaths = px.bar(
            dfworld_top_deaths,x="location",y="total_deaths",title="Total Deaths Cases",template="plotly_white")
        fig_world_top_deaths.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_world_top_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_world_top_deaths.update_xaxes(title_text='World Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_world_top_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # World Top Vaccination
        fig_world_top_vax = px.bar(
            dfworld_top_vax,x="location",y="people_fully_vaccinated",title="Total Vaccination",template="plotly_white")
        fig_world_top_vax.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_world_top_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_world_top_vax.update_xaxes(title_text='World Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_world_top_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Fourth Row Graph
        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(fig_world_top_cases, use_container_width=True)
        middle_column.plotly_chart(fig_world_top_deaths, use_container_width=True)
        right_column.plotly_chart(fig_world_top_vax, use_container_width=True)

        # Selection Options
        #Continent = st.multiselect("Select the Continent:",options=dfworld2["continent"].unique(),default=dfworld2["continent"].unique())
        #df_selection_continent = dfworld2.query("continent == @Continent")
        df_selection_continent = dfworld2
        
        st.subheader('World Continent Covid19 Cases')
        # Continent Bar Chart
        # Continent Positive Cases Bar Chart
        fig_con_cases = px.bar(
            df_selection_continent,x="continent",y="total_cases",title="Total Positive Cases",template="plotly_white")
        fig_con_cases.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_con_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_con_cases.update_xaxes(title_text='World Continent',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_con_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Continent Deaths Cases Bar Chart
        fig_con_deaths = px.bar(
            df_selection_continent,x="continent",y="total_deaths",title="Total Deaths Cases",template="plotly_white")
        fig_con_deaths.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_con_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_con_deaths.update_xaxes(title_text='World Continent',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_con_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Continent Vaccination Bar Chart
        fig_con_vax = px.bar(
            df_selection_continent,x="continent",y="people_fully_vaccinated",title="Total Vaccinations",template="plotly_white")
        fig_con_vax.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_con_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_con_vax.update_xaxes(title_text='World Continent',showgrid=False, zeroline=False, showline=True, linewidth=2, 
            linecolor='black')
        fig_con_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Fifth Row Graph
        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(fig_con_cases, use_container_width=True)
        middle_column.plotly_chart(fig_con_deaths, use_container_width=True)
        right_column.plotly_chart(fig_con_vax, use_container_width=True)
        
        st.subheader('Covid19 Cases By Selected Country:')
        # Selection Options
        Location = st.multiselect("Select the Country:",options=dfworld1["location"].unique(),default=None)
        df_selection_country = dfworld1.query("location == @Location")

        # Country Selection Bar Chart
        # Country Positive Cases Bar Chart
        fig_country_cases = px.bar(
            df_selection_country,x="location",y="total_cases",title="Total Positive Cases",template="plotly_white")
        fig_country_cases.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_country_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_country_cases.update_xaxes(title_text='Country',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_country_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Country Deaths Cases Bar Chart
        fig_country_deaths = px.bar(
            df_selection_country,x="location",y="total_deaths",title="Total Deaths Cases",template="plotly_white")
        fig_country_deaths.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_country_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_country_deaths.update_xaxes(title_text='Country',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_country_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Country Vaccination Bar Chart
        fig_country_vax = px.bar(
            df_selection_country,x="location",y="people_fully_vaccinated",title="Total Vaccinations",template="plotly_white")
        fig_country_vax.update_layout(
            height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_country_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_country_vax.update_xaxes(title_text='Country',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_country_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Sixth Row Graph
        left_column, middle_column, right_column = st.columns(3)
        left_column.plotly_chart(fig_country_cases, use_container_width=True)
        middle_column.plotly_chart(fig_country_deaths, use_container_width=True)
        right_column.plotly_chart(fig_country_vax, use_container_width=True)

        st.markdown("""---""")
    
    elif page == 'Electricity Dashboard':
        st.header(":bar_chart: Electricity Dashboard")
        st.markdown("##")
        

        first_column, second_column, third_column = st.columns(3)
        with first_column:
            st.subheader(":bulb: Total Usage:")
            st.subheader(f"{df_e['Usage (kWh)'].sum():,.0f}kWh")
        with second_column:
            st.subheader(":bulb: Average Usage:")
            st.subheader(f"{df_e['Usage (kWh)'].mean():,.2f}kWh")
        with third_column:
            st.subheader(":bulb: Build Up Usage:")
            st.subheader(f"RM{df_e['Usage (kWh)'].mean()/180.4:,.1f}kWh/m2")
        first_column, second_column, third_column = st.columns(3)
        with first_column:
            st.subheader(":moneybag: Total Cost:")
            st.subheader(f"RM{df_e['Cost (RM)'].sum():,.2f}")
        with second_column:
            st.subheader(":moneybag: Average Cost:")
            st.subheader(f"RM{df_e['Cost (RM)'].mean():,.2f}")
        with third_column:
            st.subheader(":moneybag: Average Rate:")
            st.subheader(f"RM{df_e['Cost (RM)'].mean()/df_e['Usage (kWh)'].mean():,.2f}/kWh")
       
        st.markdown("""---""")

        # Annual Electricity Usage [BAR CHART]
        fig_eusage = px.bar(
            df_e_main,x="Year",y="Usage (kWh)",title="<b>Annual Electricity Usage (kWh)</b>",template="plotly_white")
        fig_eusage.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_eusage.update_annotations(font=dict(family="Helvetica", size=10))
        fig_eusage.update_xaxes(title_text='Year',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_eusage.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Annual Electricity Cost [BAR CHART]
        fig_ecost = px.bar(
            df_e_main,x="Year",y="Cost (RM)",title="<b>Annual Electricity Cost (RM)</b>",template="plotly_white")
        fig_ecost.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_ecost.update_annotations(font=dict(family="Helvetica", size=10))
        fig_ecost.update_xaxes(title_text='Year',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_ecost.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Annual Electricity Usage [PIE CHART]
        fig_eusage_pie = make_subplots(specs=[[{"type": "domain"}]])
        fig_eusage_pie.add_trace(go.Pie(
            values=df_e_main['Usage (kWh)'],labels=df_e_main['Year'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_eusage_pie.update_layout(height=350, showlegend=False,title_text='Annual Electricity Usage Percentage',title_x=0.5)
        fig_eusage_pie.update_annotations(font=dict(family="Helvetica", size=10))
        fig_eusage_pie.update_layout(font=dict(family="Helvetica", size=10))

        # Annual Electricity Cost [PIE CHART]
        fig_ecost_pie = make_subplots(specs=[[{"type": "domain"}]])
        fig_ecost_pie.add_trace(go.Pie(
            values=df_e_main['Cost (RM)'],labels=df_e_main['Year'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_ecost_pie.update_layout(height=350, showlegend=False,title_text='Annual Electricity Cost Percentage',title_x=0.5)
        fig_ecost_pie.update_annotations(font=dict(family="Helvetica", size=10))
        fig_ecost_pie.update_layout(font=dict(family="Helvetica", size=10))

        # Creating Graph Layout
        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_ecost, use_container_width=True)
        left_column.plotly_chart(fig_eusage, use_container_width=True)

        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_ecost_pie, use_container_width=True)
        left_column.plotly_chart(fig_eusage_pie, use_container_width=True)

        if st.checkbox('Show Table Dataframes'):
            # CSS to inject contained in a string
            hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            tr:nth-child(even) {background-color: #f2f2f2;}
            th {
                background-color: #04AA6D;
                color: white;
                }
            </style>
            """
            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.subheader('Electricity Usage (kWh)')
            st.table(df_eusage)
            st.markdown("""---""") 
            st.subheader('Electricity Cost (RM)') 
            st.table(df_ecost)
        
        st.markdown("""---""")

    elif page == 'Water Dashboard':
        st.header(":bar_chart: Water Usage Dashboard")
        st.markdown("##")

        first_column, second_column, third_column = st.columns(3)
        with first_column:
            st.subheader(":droplet: Total Usage:")
            st.subheader(f"{df_w['Usage (m3)'].sum():,.0f}m3")
        with second_column:
            st.subheader(":droplet: Average Usage:")
            st.subheader(f"{df_w['Usage (m3)'].mean():,.1f}m3")
        with third_column:
            st.subheader(":droplet: Build Up Usage:")
            st.subheader(f"{df_w['Usage (m3)'].mean()/180.4:,.1f}m3/m2")
        first_column, second_column, third_column = st.columns(3)
        with first_column:
            st.subheader(":moneybag: Total Cost:")
            st.subheader(f"RM{df_w['Cost (RM)'].sum():,.2f}")
        with second_column:
            st.subheader(":moneybag: Average Cost:")
            st.subheader(f"RM{df_w['Cost (RM)'].mean():,.2f}")
        with third_column:
            st.subheader(":moneybag: Average Rate:")
            st.subheader(f"RM{df_w['Cost (RM)'].mean()/df_w['Usage (m3)'].mean():,.2f}/m3")

        st.markdown("""---""")

        # Annual Water Usage [BAR CHART]
        fig_wusage = px.bar(
            df_w_main,x="Year",y="Usage (m3)",title="<b>Annual Water Usage (m3)</b>",template="plotly_white")
        fig_wusage.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_wusage.update_annotations(font=dict(family="Helvetica", size=10))
        fig_wusage.update_xaxes(title_text='Year', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_wusage.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Annual Water Cost [BAR CHART]
        fig_wcost = px.bar(
            df_w_main,x="Year",y="Cost (RM)",title="<b>Annual Water Cost (RM)</b>",template="plotly_white")
        fig_wcost.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_wcost.update_annotations(font=dict(family="Helvetica", size=10))
        fig_wcost.update_xaxes(title_text='Year', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_wcost.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Annual Water Usage [PIE CHART]
        fig_wusage_pie = make_subplots(specs=[[{"type": "domain"}]])
        fig_wusage_pie.add_trace(go.Pie(
            values=df_w['Usage (m3)'],labels=df_w['Year'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_wusage_pie.update_layout(height=350, showlegend=False,title_text='Annual Water Usage Percentage',title_x=0.5)
        fig_wusage_pie.update_annotations(font=dict(family="Helvetica", size=10))
        fig_wusage_pie.update_layout(font=dict(family="Helvetica", size=10))

        # Annual Water Cost [PIE CHART]
        fig_wcost_pie = make_subplots(specs=[[{"type": "domain"}]])
        fig_wcost_pie.add_trace(go.Pie(
            values=df_w['Cost (RM)'],labels=df_w['Year'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_wcost_pie.update_layout(height=350, showlegend=False,title_text='Annual Water Cost Percentage',title_x=0.5)
        fig_wcost_pie.update_annotations(font=dict(family="Helvetica", size=10))
        fig_wcost_pie.update_layout(font=dict(family="Helvetica", size=10))

        # Monthly Water Usage [BAR CHART]
        fig_wusage_monthly = px.bar(
            df_wusage,x="Month",y=['2019','2020','2021','2022'],barmode="group",title="<b>Monthly Water Usage (m3)</b>",
            template="plotly_white")
        fig_wusage_monthly.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_wusage_monthly.update_annotations(font=dict(family="Helvetica", size=10))
        fig_wusage_monthly.update_xaxes(title_text='Month', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_wusage_monthly.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Monthly Water Cost [BAR CHART]
        fig_wcost_monthly = px.bar(
            df_wcost,x="Month",y=['2019','2020','2021','2022'],barmode="group",title="<b>Monthly Water Cost (RM)</b>",
            template="plotly_white")
        fig_wcost_monthly.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_wcost_monthly.update_annotations(font=dict(family="Helvetica", size=10))
        fig_wcost_monthly.update_xaxes(title_text='Month', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_wcost_monthly.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Chart Presentation
        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_wcost, use_container_width=True)
        left_column.plotly_chart(fig_wusage, use_container_width=True)

        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_wcost_pie, use_container_width=True)
        left_column.plotly_chart(fig_wusage_pie, use_container_width=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_wusage_monthly, use_container_width=True)
        right_column.plotly_chart(fig_wcost_monthly, use_container_width=True)

        if st.checkbox('Show Table Dataframes'):
            # CSS to inject contained in a string
            hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            tr:nth-child(even) {background-color: #f2f2f2;}
            th {
                background-color: #04AA6D;
                color: white;
                }
            </style>
            """
            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.subheader('Water Usage (m3)') 
            st.table(df_wusage)
            st.markdown("""---""")  
            st.subheader('Water Cost (RM)') 
            st.table(df_wcost)

        st.markdown("""---""")
    
    elif page == 'Malaysia':
        st.header("Malaysia Facts Sheets")
        st.markdown("##")
        st.write("Malaysia is a country in Southeast Asia. The federal constitutional monarchy consists of thirteen states and three federal territories, separated by the South China Sea into two regions, Peninsular Malaysia and Borneo's East Malaysia.")
        st.write("Peninsular Malaysia shares a land and maritime border with Thailand and maritime borders with Singapore, Vietnam, and Indonesia. East Malaysia shares land and maritime borders with Brunei and Indonesia and a maritime border with the Philippines and Vietnam.")
        st.write("This webpage will shows some of the important statistical information on Malaysia.")
        st.markdown("##")
        st.subheader("Malaysia Federal Government Annual Main Incomes")
        st.markdown("##")
        # First Charts
        fig_mas_income = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_mas_income.add_trace(go.Bar(x = df_income_year['Year'], y = df_income_year['RM Million'],name='Total'))
        fig_mas_income.add_trace(go.Scatter(x = df_income_year['Year'], y = df_income_year['Cumulative'],name='Cumulative',
            fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_mas_income.update_layout(height=350,title_text='Malaysia Annual Income (in RM Million)',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_mas_income.update_annotations(font=dict(family="Helvetica", size=10))
        fig_mas_income.update_xaxes(title_text='Year', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_mas_income.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Second Charts
        fig_income_2020 = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_income_2020.add_trace(go.Bar(x = df_2020['Taxes_category'], y = df_2020['RM Million'],name='Taxes_category',
            text=df_2020['Taxes_category']))
        fig_income_2020.update_layout(height=350,title_text='Annual Income By Category Year 2020 (in RM Million)',
            title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_income_2020.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
        fig_income_2020.update_annotations(font=dict(family="Helvetica", size=10))
        fig_income_2020.update_xaxes(title_text='Category', showticklabels=False, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_income_2020.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Chart Presentation
        #st.plotly_chart(fig_mas_income, use_container_width=True)
        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_income_2020, use_container_width=True)
        left_column.plotly_chart(fig_mas_income, use_container_width=True)
        
        st.subheader("Malaysia Population")
        st.markdown("##")
        # First Charts
        fig_mas_pop = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_mas_pop.add_trace(go.Bar(x = df_mas_total['Year'], y = df_mas_total['Value'],name='Total'))
        fig_mas_pop.add_trace(go.Scatter(x = df_mas_total['Year'], y = df_mas_total['Cumulative'],name='Cumulative',
            fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_mas_pop.update_layout(height=350,title_text='Malaysia Population (,000)',title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_mas_pop.update_annotations(font=dict(family="Helvetica", size=10))
        fig_mas_pop.update_xaxes(title_text='Year', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_mas_pop.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Second Charts
        fig_pop_ethnic = make_subplots(specs=[[{"type": "domain"}]])
        fig_pop_ethnic.add_trace(go.Pie(
            values=df_mas_ethnic['Value'],labels=df_mas_ethnic['Ethnic_Group'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_pop_ethnic.update_layout(height=350, showlegend=False,title_text='Malaysia Population By Ethnic Year 2020',title_x=0.5)
        fig_pop_ethnic.update_annotations(font=dict(family="Helvetica", size=10))
        fig_pop_ethnic.update_layout(font=dict(family="Helvetica", size=10))

        # Chart Presentation
        #first_column = st.columns(1)
        #st.plotly_chart(fig_mas_pop, use_container_width=True)
        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_pop_ethnic, use_container_width=True)
        left_column.plotly_chart(fig_mas_pop, use_container_width=True)

        st.subheader("Malaysia Water Treatment Capacity")
        st.write('The increase of water treatment plants design capacity is due to the addition of new plant and expansion of present plant design. The decrease of water treatment plants design capacity is due to the closing of plants and temporary closure of water treatment plant (will be reopened when needed)')
        st.write('Unit for Value is Million litres per day (MLD) ')
        st.markdown("##")
        # First Charts
        fig_water_state = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_water_state.add_trace(go.Bar(x = df_water_state['State'], y = df_water_state['Total'],name='Total',
            text=df_water_state['State']))
        fig_water_state.add_trace(go.Scatter(x = df_water_state['State'], y = df_water_state['Population'],name='Population',
            fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_water_state.update_layout(height=350,title_text='Malaysia Water Treatment Capacity By States (MLD)',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        #fig_water_state.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
        fig_water_state.update_annotations(font=dict(family="Helvetica", size=10))
        fig_water_state.update_xaxes(title_text='States',   showticklabels=False, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_water_state.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Second Charts
        fig_water_year = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_water_year.add_trace(go.Bar(x = df_water_year['Year'], y = df_water_year['Total'],name='Total',
            text=df_water_year['Total']))
        fig_water_year.add_trace(go.Scatter(x = df_water_year['Year'], y = df_water_year['Cumulative'],name='Cumulative',
            fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_water_year.update_layout(height=350,title_text='Malaysia Water Treatment Capacity Annually (MLD)',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_water_year.update_annotations(font=dict(family="Helvetica", size=10))
        fig_water_year.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_water_year.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Charts Presentation
        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_water_state, use_container_width=True)
        left_column.plotly_chart(fig_water_year, use_container_width=True)

        st.subheader("Malaysia Power Generation Consumption & Generation")
        st.markdown("##")
        # First Charts
        fig_energy_con = px.bar(
            df_energy_table,x="Year",
                y=["Total Local Consumption (Million kilowatt-hours)",
                'Total supply (Million kilowatt-hours)',
                'Imports (Million kilowatt-hours)',
                "Losses (Million kilowatt-hours)"],
                barmode="group",title="Malaysia Annual Power Consumption & Generation",template="plotly_white")
        fig_energy_con.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_energy_con.update_annotations(font=dict(family="Helvetica", size=10))
        fig_energy_con.update_xaxes(title_text='Year', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_energy_con.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Second Charts
        fig_energy_revenue = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_energy_revenue.add_trace(go.Bar(x = df_energy_table['Year'], y = df_energy_table['Revenue (RM Million)'],
            name='Revenue (RM Million)',text=df_energy_table['Revenue (RM Million)']))
        fig_energy_revenue.update_layout(height=350,title_text='Malaysia Power Generation Revenue (RM Million)',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_energy_revenue.update_annotations(font=dict(family="Helvetica", size=10))
        fig_energy_revenue.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_energy_revenue.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Charts Presentation
        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_energy_revenue, use_container_width=True)
        left_column.plotly_chart(fig_energy_con, use_container_width=True)

        st.subheader("Malaysia Annual Rainfall")
        st.write('Malaysia Rainfall Year 2000 - 2020')
        st.markdown("##")
        # First Chart
        fig_rainfall_year = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_rainfall_year.add_trace(go.Bar(x = df_rainfall_year['Year'], y = df_rainfall_year['Rainfall-Total (mm)'],name='Total',
            text=df_rainfall_year['Rainfall-Total (mm)']))
        fig_rainfall_year.add_trace(go.Scatter(x = df_rainfall_year['Year'], y = df_rainfall_year['Cumulative'],name='Cumulative',
            fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_rainfall_year.update_layout(height=350,title_text='Malaysia Annual Rainfall (mm)',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_rainfall_year.update_annotations(font=dict(family="Helvetica", size=10))
        fig_rainfall_year.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_rainfall_year.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Second Charts
        fig_rainfall_state = make_subplots(specs=[[{"type": "domain"}]])
        fig_rainfall_state.add_trace(go.Pie(
            values=df_rainfall_state['Rainfall-Total (mm)'],labels=df_rainfall_state['State'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_rainfall_state.update_layout(height=350, showlegend=False,title_text='Malaysia Annual Rainfall By State Year 2020',title_x=0.5)
        fig_rainfall_state.update_annotations(font=dict(family="Helvetica", size=10))
        fig_rainfall_state.update_layout(font=dict(family="Helvetica", size=10))
        # Charts Presentation
        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_rainfall_state, use_container_width=True)
        left_column.plotly_chart(fig_rainfall_year, use_container_width=True)

        # Selection Options
        State = st.multiselect("Select the State(s):",options=df_state_rainfall_table["State"].unique(),default=None)
        df_selection_state = df_state_rainfall_table.query("State == @State")

        # Country Selection Bar Chart
        # Country Positive Cases Bar Chart
        fig = px.bar(
            df_selection_state,x="State",
            y=['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016',
            '2017','2018','2019','2020'],barmode="group",title="Total Annual Rainfall (mm)",template="plotly_white")
        fig.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig.update_annotations(font=dict(family="Helvetica", size=10))
        fig.update_xaxes(title_text='State(s)', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Malaysia Currency Exchange")
        st.write('Currency Exchange Between MYR & USD, GBP, EUR, SGD, THB, IDR')
        st.markdown("##")
        
        # First Chart
        fig_euro = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_euro.add_trace(go.Scatter(x = df_euro['Year'], y = df_euro['Exchange rates (Average for period)'],
            name='Exchange rates (Average for period)',fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_euro.add_trace(go.Scatter(x = df_euro['Year'], y = df_euro['Cumulative'],
            name='Cumulative',fill='tozeroy',mode='lines',line = dict(color='blue', width=1)), secondary_y=False)
        fig_euro.update_layout(height=350,title_text='MYR VS EUR',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_euro.update_annotations(font=dict(family="Helvetica", size=10))
        fig_euro.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_euro.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Second Charts
        fig_dollar = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_dollar.add_trace(go.Scatter(x = df_dollar['Year'], y = df_dollar['Exchange rates (Average for period)'],
            name='Exchange rates (Average for period)',fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_dollar.add_trace(go.Scatter(x = df_dollar['Year'], y = df_dollar['Cumulative'],
            name='Cumulative',fill='tozeroy',mode='lines',line = dict(color='blue', width=1)), secondary_y=False)
        fig_dollar.update_layout(height=350,title_text='MYR VS USD',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_dollar.update_annotations(font=dict(family="Helvetica", size=10))
        fig_dollar.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_dollar.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Third Charts
        fig_pound = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_pound.add_trace(go.Scatter(x = df_pound['Year'], y = df_pound['Exchange rates (Average for period)'],
            name='Exchange rates (Average for period)',fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_pound.add_trace(go.Scatter(x = df_pound['Year'], y = df_pound['Cumulative'],
            name='Cumulative',fill='tozeroy',mode='lines',line = dict(color='blue', width=1)), secondary_y=False)
        fig_pound.update_layout(height=350,title_text='MYR VS GBP',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_pound.update_annotations(font=dict(family="Helvetica", size=10))
        fig_pound.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_pound.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Fourth Charts
        fig_sing = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_sing.add_trace(go.Scatter(x = df_sing['Year'], y = df_sing['Exchange rates (Average for period)'],
            name='Exchange rates (Average for period)',fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_sing.add_trace(go.Scatter(x = df_sing['Year'], y = df_sing['Cumulative'],
            name='Cumulative',fill='tozeroy',mode='lines',line = dict(color='blue', width=1)), secondary_y=False)
        fig_sing.update_layout(height=350,title_text='MYR VS SGD',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_sing.update_annotations(font=dict(family="Helvetica", size=10))
        fig_sing.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_sing.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Fifth Charts
        fig_thai = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_thai.add_trace(go.Scatter(x = df_thai['Year'], y = df_thai['Exchange rates (Average for period)'],
            name='Exchange rates (Average for period)',fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_thai.add_trace(go.Scatter(x = df_thai['Year'], y = df_thai['Cumulative'],
            name='Cumulative',fill='tozeroy',mode='lines',line = dict(color='blue', width=1)), secondary_y=False)
        fig_thai.update_layout(height=350,title_text='MYR VS THB',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_thai.update_annotations(font=dict(family="Helvetica", size=10))
        fig_thai.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_thai.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Sixth Charts
        fig_indo = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_indo.add_trace(go.Scatter(x = df_indo['Year'], y = df_indo['Exchange rates (Average for period)'],
            name='Exchange rates (Average for period)',fill='tozeroy',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_indo.add_trace(go.Scatter(x = df_indo['Year'], y = df_indo['Cumulative'],
            name='Cumulative',fill='tozeroy',mode='lines',line = dict(color='blue', width=1)), secondary_y=False)
        fig_indo.update_layout(height=350,title_text='MYR VS IDR',
            title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_indo.update_annotations(font=dict(family="Helvetica", size=10))
        fig_indo.update_xaxes(title_text='Year',  showticklabels=True, showgrid=False, zeroline=False, showline=True, 
            linewidth=2, linecolor='black')
        fig_indo.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Charts Presentation
        left_column, middle_column, right_column = st.columns(3)
        right_column.plotly_chart(fig_dollar, use_container_width=True)
        middle_column.plotly_chart(fig_pound, use_container_width=True)
        left_column.plotly_chart(fig_euro, use_container_width=True)
        # Charts Presentation
        left_column, middle_column, right_column = st.columns(3)
        right_column.plotly_chart(fig_sing, use_container_width=True)
        middle_column.plotly_chart(fig_indo, use_container_width=True)
        left_column.plotly_chart(fig_thai, use_container_width=True)

        st.markdown("""---""")

    else:
        st.header("ASEAN Facts Sheets")
        st.markdown('##')
        st.write("ASEAN is known as the Association of South East Asian Nations is an international organization. It was established on 8 August 1967 which are consists of Malaysia, Thailand, Indonesia, Singapore and Philippines. On 7 January 1984, Brunei joined ASEAN. Vietnam joined in 28 July 1995. Both Laos and Myanmar joined ASEAN on 23 July 1997. While Cambodia joined ASEAN on 30 April 1999.")
        st.write("The purpose of the organization is political and economic cooperation. The organization headquarter is in Jakarta, Indonesia. This webpage will shows some of the important statistical information on ASEAN countries.")
        st.markdown("##")
        st.subheader("Population")
        st.markdown("##")
        # Charts
        fig_asean_pop = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_pop.add_trace(go.Bar(x = df_asean_pop['location'], y = df_asean_pop['population'],name='population',
            text=df_asean_pop['population']))
        fig_asean_pop.update_layout(title_text='ASEAN Countries Population',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_pop.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
        fig_asean_pop.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_pop.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_pop.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Chart Presentation
        st.plotly_chart(fig_asean_pop, use_container_width=True)

        st.subheader("Population Density")
        st.markdown("##")
        # Charts
        fig_asean_popden = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_popden.add_trace(go.Bar(x = df_asean_popdensity['location'], y = df_asean_popdensity['population_density'],
            name='population_density',text=df_asean_popdensity['population_density']))
        fig_asean_popden.update_layout(title_text='ASEAN Countries Population Density',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_popden.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
        fig_asean_popden.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_popden.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_popden.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Chart Presentation
        st.plotly_chart(fig_asean_popden, use_container_width=True)

        st.subheader("Gross Domestic Products")
        st.markdown("##")
        # Charts
        fig_asean_gdp = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_gdp.add_trace(go.Bar(x = df_asean_gdp['location'], y = df_asean_gdp['gdp_per_capita'],name='gdp_per_capita',
            text=df_asean_gdp['gdp_per_capita']))
        fig_asean_gdp.update_layout(title_text='ASEAN Countries GDP Per Capita',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_gdp.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
        fig_asean_gdp.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_gdp.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_gdp.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Chart Presentation
        st.plotly_chart(fig_asean_gdp, use_container_width=True)

        st.subheader("Poverty")
        st.markdown("##")
        # Charts
        fig_asean_pov = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_pov.add_trace(go.Bar(x = df_asean_poverty['location'], y = df_asean_poverty['extreme_poverty'],name='extreme_poverty',
            text=df_asean_poverty['extreme_poverty']))
        fig_asean_pov.update_layout(title_text='ASEAN Countries Poverty',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_pov.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
        fig_asean_pov.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_pov.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_pov.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Chart Presentation
        st.plotly_chart(fig_asean_pov, use_container_width=True)

        st.subheader("Human Development Index")
        st.markdown("##")
        # Charts
        fig_asean_hdi = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_hdi.add_trace(go.Bar(x = df_asean_hdi['location'], y = df_asean_hdi['human_development_index'],
            name='human_development_index',text=df_asean_hdi['human_development_index']))
        fig_asean_hdi.update_layout(title_text='ASEAN Countries Human Development Index',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_hdi.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
        fig_asean_hdi.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_hdi.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_hdi.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Chart Presentation
        st.plotly_chart(fig_asean_hdi, use_container_width=True)

        st.subheader("Life Expectancy")
        st.markdown("##")
        # Charts
        fig_asean_life = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_life.add_trace(go.Bar(x = df_asean_life['location'], y = df_asean_life['life_expectancy'],name='life_expectancy',
            text=df_asean_life['life_expectancy']))
        fig_asean_life.update_layout(title_text='ASEAN Countries Life Expectancy',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_life.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
        fig_asean_life.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_life.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_life.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Chart Presentation
        st.plotly_chart(fig_asean_life, use_container_width=True)
        
        st.markdown("""---""")

        

if __name__ == '__main__':
    main()

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)