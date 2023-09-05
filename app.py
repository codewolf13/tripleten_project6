import pandas as pd
import streamlit as st
import plotly_express as px

# Load the dataset into a DataFrame
df=pd.read_csv(r"C:\Users\oscar\OneDrive\earthquake_data.csv")

st.title("Earthquake Analysis")

df

df.shape

df.info()

### When looking at the info from the graph, the date_time column has nanoseconds for precise measurement data.

#This is great but for the purpose of this analysis, we want only the year in which these eartquakes occurred. So, we'll be changing the type to a datetime type and apply the .apply function to swtich it back to a string for year respectively.

#since column "date_time" has nanoseconds, we want to change it to to just years for a slider effect
df["date_time"]=df["date_time"].apply(pd.to_datetime)

df['date_time'] = df['date_time'].apply(lambda x: x.strftime('%Y'))

df.info()

## This data contains oceanic earthquake information, therefore creating tsunamis. We'll led the user choose whether to include tsunami occurrence in the data.

#creating header with an option to filter the data and the checkbox:
#data set includes 2 options for tsunami: 1=yes an d0=no
#let users decide whether they want to see

st.header('Earthquake effects.')
st.write("""
##### Filter the data below to see how earthquake data is affected by whether a tsunami occured
""")
show_tsunami = st.checkbox('Include tsunami occurence')

show_tsunami

if not show_tsunami:
    df = df[df.tsunami!='1']

#creating options for filter from all servers
country_choice = df['country'].unique()
country_choice_man = st.selectbox('Select country:', country_choice)

country_choice_man

#next let's create a slider for years, so that users can filter earthquakes 
#creating min and max years as limits fro sliders
min_year, max_year=int(df['date_time'].min()), int(df['date_time'].max())

#creating slider
year_range = st.slider(
    "Choose years",
    value=(min_year,max_year),min_value=min_year,max_value=max_year)

year_range

st.header('Earthquake analysis')
st.write("""
###### Let's analyze what influences earthquakes the most. We will check how distribution of earthquakes varies depending on the alert and continent
""")

# Will create 2 histograms with the choice: color and alert, color and continent

#creating list of options to choose from
list_for_hist=['alert', 'continent']

#creating selectbox
choice_for_hist = st.selectbox('Split for magnitude distribution', list_for_hist)

#plotly histogram, where magnitude is split by alert level
fig1 = px.histogram(df, x="magnitude", color=choice_for_hist,
                    color_discrete_map={
                        "green": "green",
                        "yellow": "yellow",
                        "orange": "orange",
                        "red": "red"})
#adding title
fig1.update_layout(title="<b> Split of magnitude by {}</b>".format(choice_for_hist))

#embedding into streamlit
st.plotly_chart(fig1)

fig1.show()
st.write("""
###### Alert Level refers to an assessment of the potential population exposure to earthquakes in proximity to specific ares.

• Green = Litle to no
• Yellow = Limited
• Orange = Significant
• Red = Extensive
""")

# Alert Level Meaning

#Alert Level refers to an assessment of the potential population exposure to earthquakes in proximity to specific ares.

#</p>• Green = Ltle to no</p>
# • Yellow = Limited</p>
# • Orange = Significant</p>
# • Red = Extensive

df['age']=2023-df['date_time'].values.astype(float)
    
def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'
    
df['age_category']= df['age'].apply(age_category)

df['age_category']

st.write("""
###### Now let's check if Earthquake occurrence has increased over the years and if they're becoming more "significant"
""")

fig2 = px.scatter(df, x="magnitude", y="sig", color="age_category", hover_data=['date_time'])

st.plotly_chart(fig2)

fig2.show()

st.write("""
###### The "sig" numbers tend to rise with increasing magnitude numbers. Moreover, the year span doesn't appear to reveal any hidden insights in this graph.
""")

# SIG

# Sig - A number describing how significant the event is. Larger numbers indicate a more significant event. This value is determined on a number of factors, including: magnitude, maximum MMI, felt reports, and estimated impact

# We can see how "sig" numbers increase with magnitude

#streamlit run earthquake_eda.py

