from curses import def_prog_mode
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from email.mime import image
import requests
from deta import Deta
import json
from collections import Counter
import calendar
from datetime import datetime

img_pandas_1 = Image.open("images/Pandas_1.jpg")
img_pandas_2 = Image.open("images/Pandas_2.jpg")
img_html_1 = Image.open("images/html_1.jpg")
img_html_2 = Image.open("images/html_2.jpg")
img_css_1 = Image.open("images/css_1.jpg")
img_css_2 = Image.open("images/css_2.jpg")
img_math = Image.open("images/math.jpg")
img_python_1 = Image.open("images/python_1.jpg")
img_python_2 = Image.open("images/python_2.jpg")
img_python_3 = Image.open("images/python_3.jpg")
img_python_4 = Image.open("images/python_4.jpg")
img_python_5 = Image.open("images/python_5.jpg")
img_python_6 = Image.open("images/python_6.jpg")
img_python_7 = Image.open("images/python_7.jpg")
img_python_8 = Image.open("images/python_8.jpg")
img_python_9 = Image.open("images/python_9.jpg")
img_cli_1 = Image.open("images/CLI_1.jpg")
img_cli_2 = Image.open("images/CLI_2.jpg")

st.set_page_config(page_title="My Dashboard", page_icon=":microscope:", layout="wide")
st.title(":microscope:"+" Data Science and Visualisation")

@st.experimental_memo
def read_csv(path) -> pd.DataFrame:
    return pd.read_csv(path)

# IMPORTING ALL DATA
dfworld1 = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')
df_asean = dfworld1[dfworld1['continent'].notna()]
df_asean = df_asean.loc[df_asean['location'].isin(['Malaysia','Singapore','Thailand','Indonesia','Philippines','Cambodia',
                                                  'Laos','Vietnam','Myanmar','Brunei'])]
df_asean_pop = df_asean.sort_values('population',ascending=False)
df_asean_popdensity = df_asean.sort_values('population_density',ascending=False)
df_asean_gdp = df_asean.sort_values('gdp_per_capita',ascending=False)
df_asean_poverty = df_asean.sort_values('extreme_poverty',ascending=False)
df_asean_hdi = df_asean.sort_values('human_development_index',ascending=False)
df_asean_life = df_asean.sort_values('life_expectancy',ascending=False)
df_asean_hosp_bed = df_asean.sort_values('hospital_beds_per_thousand',ascending=False)
df_asean_cardiovasc = df_asean.sort_values('cardiovasc_death_rate',ascending=False)

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

    page = st.selectbox("", ['Home', '1. Malaysia','2. ASEAN','3. Cheat Sheets','Contact'])

    if page == 'Home':
        st.header("A Quick Fact Sheet")
        #st.subheader("By Zahiruddin Zahidanishah")
        st.write("This website consists of several facts sheet; namely `Malaysia Fact Sheet`, `ASEAN Fact Sheet` and `Cheat Sheets`.")
        st.write("1. `Malaysia Facts Sheets` will shows Malaysia several main statistical information. The site will be updated in progress according to the available dataset retrieved from [Malaysia Informative Data Centre (MysIDC)](https://mysidc.statistics.gov.my).")
        st.write("2. `ASEAN Facts Sheets` will shows several important statistical information on ASEAN countries. Data for this dashboards are retrieved from [Johns Hopkins University CSSE Github pages](https://github.com/CSSEGISandData/COVID-19).")
        st.write("3. :memo: `Cheat Sheets` will shows some of the importants notes on programming languages such as Python, Pandas, HTML, CSS and others.")
        st.write('Other website available are:-')
        st.write(':warning: `Covid19 Dashboard` shows the latest information on the pandemic situation and trends specifically in Malaysia and in other country as generally. Please click on this link for further information :point_right: [Covid19 Dashboard](https://zzahir1978-covid-dashboard-covid-gpsg1z.streamlitapp.com/)')
        st.write(":bar_chart: `Utilities Dashboard` shows main utilities cost and usage for electricity, water and telcos. The utilities are for a typical double storey residential house located in Malaysia. Data for this dashboard is based on the monthly bills from TNB, Air Selangor, DiGi and TM. For electricity, usage is measured in kWh. For water, usage is measured in m3. All cost is measured in RM.")
        
        
        # Logos
        st.write("---")
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <div style="text-align:center">
            <p style="font-family:verdana">Powered By:</p>
            <span class="iconify" data-icon="logos:python"></span> <span class="iconify" data-icon="simple-icons:pandas"></span> <span class="iconify" data-icon="simple-icons:plotly"></span> <span class="iconify" data-icon="icon-park:github"></span> <span class="iconify" data-icon="logos:github"></span> <span class="iconify" data-icon="simple-icons:streamlit"></span>
            <p style="font-family:verdana">zahiruddin.zahidanishah<span class="iconify" data-icon="icon-park:at-sign"></span>2022</p>
            </div>
            """
        )

    elif page == '1. Malaysia':
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <h1 style="font-family:verdana"><span class="iconify" data-icon="openmoji:flag-malaysia"></span> Malaysia Facts Sheets</h1>
            """
        )
        #st.markdown("##")
        with st.expander("Introduction:"):
            st.write(
                """
                Malaysia is a country in Southeast Asia. The federal constitutional monarchy consists of thirteen states and three federal territories, separated by the 
                South China Sea into two regions, Peninsular Malaysia and Borneo's East Malaysia.
                """
                )
            st.write(
                """
                Peninsular Malaysia shares a land and maritime border with Thailand and maritime borders with Singapore, Vietnam, and Indonesia. 
                East Malaysia shares land and maritime borders with Brunei and Indonesia and a maritime border with the Philippines and Vietnam.
                """
                )
            st.write(
                """
                This webpage will shows some of the important statistical information on Malaysia.
                """
                )
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
        with st.expander("Water Treatment Capacity Description:"):
            st.write(
                """
                The increase of water treatment plants design capacity is due to the addition of new plant and expansion of present plant design. 
                The decrease of water treatment plants design capacity is due to the closing of plants and temporary closure of water treatment plant (will be reopened when needed)
                """
                )
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

        with st.expander("Click To Select State(s) For Total Annual Rainfall Graphs:"):
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

    elif page == '2. ASEAN':
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <h1 style="font-family:verdana"><span class="iconify" data-icon="emojione:globe-showing-asia-australia"></span> ASEAN Facts Sheets</h1>
            """
        )
        #st.markdown('##')
        with st.expander("Introduction:"):
            st.write(
                """
                ASEAN is known as the Association of South East Asian Nations is an international organization. 
                It was established on 8 August 1967 which are consists of Malaysia, Thailand, Indonesia, Singapore and Philippines. 
                On 7 January 1984, Brunei joined ASEAN. Vietnam joined in 28 July 1995. Both Laos and Myanmar joined ASEAN on 23 July 1997. 
                While Cambodia joined ASEAN on 30 April 1999.
                """
                )
            st.write(
                """
                The purpose of the organization is political and economic cooperation. The organization headquarter is in Jakarta, Indonesia. 
                This webpage will shows some of the important statistical information on ASEAN countries.
                """
                )
        st.markdown("##")
        st.subheader("ASEAN Population")
        st.markdown("##")
        
        # Charts
        fig_asean_pop = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_pop.add_trace(go.Bar(x = df_asean_pop['location'], y = df_asean_pop['population'],name='population',text=df_asean_pop['population']))
        fig_asean_pop.add_trace(go.Scatter(x = df_asean_pop['location'], y = df_asean_pop['gdp_per_capita'],name='gdp_per_capita',
            mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_asean_pop.update_layout(title_text='Population VS GDP',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_pop.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_pop.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_pop.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_pop.add_hline(y=df_asean_pop['population'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Population", annotation_position="top right")
        # Chart Presentation
        st.plotly_chart(fig_asean_pop, use_container_width=True)

        st.subheader("ASEAN Population Density (Nos. Of People/km2)")
        st.markdown("##")
        # Charts
        fig_asean_popden = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_popden.add_trace(go.Bar(x = df_asean_popdensity['location'], y = df_asean_popdensity['population_density'],
            name='population_density',text=df_asean_popdensity['population_density']))
        fig_asean_popden.add_trace(go.Scatter(x = df_asean_popdensity['location'], y = df_asean_popdensity['population'],name='population',
            mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_asean_popden.update_layout(title_text='Population VS Population Density',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_popden.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_popden.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_popden.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_popden.add_hline(y=df_asean_popdensity['population_density'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Population Density", annotation_position="top right")
        # Chart Presentation
        st.plotly_chart(fig_asean_popden, use_container_width=True)

        st.subheader("ASEAN Gross Domestic Products")
        st.markdown("##")
        # Charts
        fig_asean_gdp = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_gdp.add_trace(go.Bar(x = df_asean_gdp['location'], y = df_asean_gdp['gdp_per_capita'],name='gdp_per_capita',
            text=df_asean_gdp['gdp_per_capita']))
        fig_asean_gdp.add_trace(go.Scatter(x = df_asean_gdp['location'], y = df_asean_gdp['population_density'],name='population_density',
            mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_asean_gdp.update_layout(title_text='GDP VS Population Density',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_gdp.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_gdp.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_gdp.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_gdp.add_hline(y=df_asean_popdensity['gdp_per_capita'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average GDP", annotation_position="top right")
        # Chart Presentation
        st.plotly_chart(fig_asean_gdp, use_container_width=True)

        st.subheader("ASEAN Poverty Index")
        st.markdown("##")
        # Charts
        fig_asean_pov = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_pov.add_trace(go.Bar(x = df_asean_poverty['location'], y = df_asean_poverty['extreme_poverty'],name='extreme_poverty',
            text=df_asean_poverty['extreme_poverty']))
        fig_asean_pov.add_trace(go.Scatter(x = df_asean_poverty['location'], y = df_asean_poverty['gdp_per_capita'],name='gdp_per_capita',
            mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_asean_pov.update_layout(title_text='Poverty Index VS GDP',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_pov.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_pov.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_pov.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_pov.add_hline(y=df_asean_poverty['extreme_poverty'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Poverty Index", annotation_position="top right")
        # Chart Presentation
        st.plotly_chart(fig_asean_pov, use_container_width=True)

        st.subheader("ASEAN Human Development Index")
        st.markdown("##")
        # Charts
        fig_asean_hdi = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_hdi.add_trace(go.Bar(x = df_asean_hdi['location'], y = df_asean_hdi['human_development_index'],name='human_development_index',
            text=df_asean_hdi['human_development_index']))
        fig_asean_hdi.add_trace(go.Scatter(x = df_asean_hdi['location'], y = df_asean_hdi['gdp_per_capita'],name='gdp_per_capita',
            mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_asean_hdi.update_layout(title_text='Human Development Index VS GDP',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_hdi.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_hdi.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_hdi.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_hdi.add_hline(y=df_asean_hdi['human_development_index'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Human Development Index", annotation_position="top right")
        # Chart Presentation
        st.plotly_chart(fig_asean_hdi, use_container_width=True)

        st.subheader("ASEAN Life Expectancy")
        st.markdown("##")
        # Charts
        fig_asean_life = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_life.add_trace(go.Bar(x = df_asean_life['location'], y = df_asean_life['life_expectancy'],name='life_expectancy',
            text=df_asean_life['life_expectancy']))
        fig_asean_life.add_trace(go.Scatter(x = df_asean_life['location'], y = df_asean_life['gdp_per_capita'],name='gdp_per_capita',
            mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_asean_life.update_layout(title_text='Life Expectancy VS GDP',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_life.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_life.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_life.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_life.add_hline(y=df_asean_life['life_expectancy'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Life Expectancy Index", annotation_position="top right")
        # Chart Presentation
        st.plotly_chart(fig_asean_life, use_container_width=True)

        st.subheader("ASEAN Cardiovascular Death Rate")
        st.markdown("##")
        # Charts
        fig_asean_cardiovasc = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_cardiovasc.add_trace(go.Bar(x = df_asean_cardiovasc['location'], y = df_asean_cardiovasc['cardiovasc_death_rate'],
            name='cardiovasc_death_rate',text=df_asean_life['cardiovasc_death_rate']))
        fig_asean_cardiovasc.add_trace(go.Scatter(x = df_asean_cardiovasc['location'], y = df_asean_cardiovasc['population_density'],
            name='population_density',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_asean_cardiovasc.update_layout(title_text='Cardiovascular Death Rate VS Population Density',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_cardiovasc.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_cardiovasc.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_cardiovasc.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_cardiovasc.add_hline(y=df_asean_cardiovasc['cardiovasc_death_rate'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Cardiovascular Death Rate", annotation_position="top right")
        # Chart Presentation
        st.plotly_chart(fig_asean_cardiovasc, use_container_width=True)

        st.subheader("ASEAN Hospital Beds Per Thousand")
        st.markdown("##")
        # Charts
        fig_asean_hosp_bed = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_asean_hosp_bed.add_trace(go.Bar(x = df_asean_hosp_bed['location'], y = df_asean_hosp_bed['hospital_beds_per_thousand'],
            name='hospital_beds_per_thousand',text=df_asean_hosp_bed['hospital_beds_per_thousand']))
        fig_asean_hosp_bed.add_trace(go.Scatter(x = df_asean_hosp_bed['location'], y = df_asean_hosp_bed['population'],
            name='population',mode='lines',line = dict(color='red', width=1)), secondary_y=True)
        fig_asean_hosp_bed.update_layout(title_text='Hospital Beds Per Thousand VS Population',title_x=0.5,
            font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_asean_hosp_bed.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_hosp_bed.update_xaxes(title_text='Country', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_hosp_bed.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_hosp_bed.add_hline(y=df_asean_hosp_bed['hospital_beds_per_thousand'].mean(), line_dash="dot",line_color="red",
              annotation_text="Average Hospital Beds Per Thousand", annotation_position="top right")
        # Chart Presentation
        st.plotly_chart(fig_asean_hosp_bed, use_container_width=True)
        
        st.markdown("""---""")
    
    elif page == '3. Cheat Sheets':
        st.subheader(':memo: Cheat Sheets')
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <h2 style="font-family:verdana"><span class="iconify" data-icon="simple-icons:pandas"></span> Pandas Cheat Sheets</h2>
            """)
        #st.subheader('Pandas Cheat Sheets:')
        with st.expander("About Pandas"):
            st.write("""
            In 2008, pandas development began at AQR Capital Management. By the end of 2009 it had been open sourced, and is actively supported today by 
            a community of like-minded individuals around the world who contribute their valuable time and energy to help make open source pandas possible. 
            Thank you to all of our contributors. Since 2015, pandas is a NumFOCUS sponsored project. This will help ensure the success of development of 
            pandas as a world-class open-source project.
                """
                )
        with st.expander("Sheets 1:"):
            st.image(img_pandas_1)
        with st.expander("Sheets 2:"):
            st.image(img_pandas_2)
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <h2 style="font-family:verdana"><span class="iconify" data-icon="logos:python"></span> Python For Data Science Cheat Sheets</h>

            """
        )
        with st.expander("About Python"):
            st.write("""
            Python is a high-level, interpreted, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant 
            indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), 
            object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library. 
            Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language and first released it in 1991 as Python 0.9.0. 
            Python 2.0 was released in 2000 and introduced new features such as list comprehensions, cycle-detecting garbage collection, reference counting, 
            and Unicode support. Python 3.0, released in 2008, was a major revision that is not completely backward-compatible with earlier versions. 
            Python 2 was discontinued with version 2.7.18 in 2020.
                """
                )
        with st.expander("Sheets 1 (Pyhton Basic):"):
            st.image(img_python_1)
        with st.expander("Sheets 2 (Jupyter Notebook):"):
            st.image(img_python_2)
        with st.expander("Sheets 3 (NumPy Basic):"):
            st.image(img_python_3)
        with st.expander("Sheets 4 (SciPy - Linear Algebra):"):
            st.image(img_python_4)
        with st.expander("Sheets 5 (Pandas Basic):"):
            st.image(img_python_5)
        with st.expander("Sheets 6 (Scikit-Learn):"):
            st.image(img_python_6)
        with st.expander("Sheets 7 (Matplotlib):"):
            st.image(img_python_7)
        with st.expander("Sheets 8 (Seaborn):"):
            st.image(img_python_8)
        with st.expander("Sheets 9 (Bokeh):"):
            st.image(img_python_9)
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <h2 style="font-family:verdana"><span class="iconify" data-icon="logos:html-5"></span> HTML Cheat Sheets</h>

            """
        )
        #st.subheader('HTML Cheat Sheets:')
        with st.expander("About HTML"):
            st.write("""
            The HyperText Markup Language or HTML is the standard markup language for documents designed to be displayed in a web browser. 
            It can be assisted by technologies such as Cascading Style Sheets (CSS) and scripting languages such as JavaScript.
                """
                )
        with st.expander("Sheets 1:"):
            st.image(img_html_1)
        with st.expander("Sheets 2:"):
            st.image(img_html_2)
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <h2 style="font-family:verdana"><span class="iconify" data-icon="logos:css-3"></span> CSS Cheat Sheets</h>

            """
        )
        #st.subheader('CSS Cheat Sheets:')
        with st.expander("About CSS"):
            st.write("""
            Cascading Style Sheets (CSS) is a style sheet language used for describing the presentation of a document written in a markup language 
            such as HTML or XML (including XML dialects such as SVG, MathML or XHTML). CSS is a cornerstone technology of the World Wide Web, alongside HTML and 
            JavaScript.
                """
                )
        with st.expander("Sheets 1:"):
            st.image(img_css_1)
        with st.expander("Sheets 2:"):
            st.image(img_css_2)
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <h2 style="font-family:verdana"><span class="iconify" data-icon="arcticons:math"></span> Math Formula Sheets</h2>
            """
        )   
        with st.expander("Sheets 1:"):
            st.image(img_math)
        components.html(
            """
            <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
            <h2 style="font-family:verdana"><span class="iconify" data-icon="icon-park:terminal"></span> Terminal Cheat Sheets</h>

            """
        )
        with st.expander("Sheets 1:"):
            st.image(img_cli_1)
        with st.expander("Sheets 2:"):
            st.image(img_cli_2)
    
    else:
        st.subheader(':speech_balloon: Contact')
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