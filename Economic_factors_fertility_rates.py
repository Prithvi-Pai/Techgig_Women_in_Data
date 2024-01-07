import streamlit as st
import snowflake.connector
import plotly.express as px
import pandas as pd

st.title('TechGig Women in Data')
st.header('Hypothesis on Economic factors and Fertility rates')

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# st.text("Hello from Snowflake:")
# st.text(my_data_row)

# Adding code to show relation between education and fertility
my_cur.execute('select "States/UTs" ,AREA , "Women (age 15-49)  with 10 or more years of schooling (%)"  as "Educated Women(%)","Women (age 15-49 years) who worked in the last 12 months and were paid in cash (%)" as "Employed Women(%)", "Total Fertility Rate (number of children per woman)" from WOMEN_IN_DATA.HYPOTHESIS_1.NHFS ')

result = my_cur.fetchall()

data = pd.DataFrame(result, columns=['States/UTs', 'AREA', 'Educated Women(%)','Employed Women(%)','Total Fertility Rate (number of children per woman)'])
#data = st.dataframe(result)
x_axis_selection = st.sidebar.selectbox('Select X-Axis', ['Educated Women(%)','Employed Women(%)'])
 

# Streamlit app
#st.text('Relationship between Education and Fertility')

# Create a scatter plot to visualize the inverse relationship

fig = px.scatter(
    data,
    x=x_axis_selection,
    y='Total Fertility Rate (number of children per woman)',
    color='States/UTs',
    facet_col='AREA',  # Facet by 'Area'
    title='Impact of Employment and Education in Women and Fertility',
    labels={'EducationLevel': 'Education Level', 'FertilityRate': 'Fertility Rate'},
)
# Customize the layout
fig.update_layout(showlegend=True)

#Early Marriage and Motherhood Data Analysis
st.title('Early Marriage and Motherhood Data Analysis')
selected_state = st.selectbox('Select State/UT:', data['States/UTs'].unique())
selected_area = st.selectbox('Select Area:', ['Rural', 'Urban', 'Total'])

# Filter data based on user selection
filtered_data = data[(data['States/UTs'] == selected_state) & (data['AREA'] == selected_area)]

# Bar Chart for Early Marriage Rate
st.subheader('Early Marriage Rate')
fig_marriage = px.bar(filtered_data, x='States/UTs', y='Women age 20-24 years married before age 18 years (%)', text='Women age 20-24 years married before age 18 years (%)')
st.plotly_chart(fig_marriage)

# Bar Chart for Motherhood Rate
st.subheader('Motherhood Rate')
fig_motherhood = px.bar(filtered_data, x='States/UTs', y='Women age 15-19 years who were already mothers or pregnant at the time of the survey (%)', text='Women age 15-19 years who were already mothers or pregnant at the time of the survey (%)')
st.plotly_chart(fig_motherhood)

st.subheader('Education Level vs Early Marriage/Motherhood')
fig_education = px.bar(filtered_data, x='States/UTs', y=['Women age 20-24 years married before age 18 years (%)', 'Women age 15-19 years who were already mothers or pregnant at the time of the survey (%)'], text=['Women age 20-24 years married before age 18 years (%)', 'Women age 15-19 years who were already mothers or pregnant at the time of the survey (%)'])


# Show the plot in the Streamlit app
st.plotly_chart(fig)
st.plotly_chart(fig_education)
# Close the Snowflake connection
my_cnx.close()
