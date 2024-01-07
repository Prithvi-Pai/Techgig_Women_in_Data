import streamlit as st
import snowflake.connector
import plotly.express as px
import pandas as pd

st.title('TechGig Women in Data')
st.header('Hypothesis on Economic Empowerment and Marital Status')

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# st.text("Hello from Snowflake:")
# st.text(my_data_row)

# Adding code to show relation between education and fertility
my_cur.execute('select "States/UTs" ,AREA , "Women (age 15-49)  with 10 or more years of schooling (%)"  as "Educated Women(%)","Women (age 15-49 years) who worked in the last 12 months and were paid in cash (%)" as "Employed Women(%)","Total Fertility Rate (number of children per woman)" from WOMEN_IN_DATA.HYPOTHESIS_1.NHFS ')

result = my_cur.fetchall()

data = pd.DataFrame(result, columns=['"States/UTs"', 'AREA', '"Educated Women(%)"','"Employed Women(%)"','"Total Fertility Rate (number of children per woman)"'])
#data = st.dataframe(result)
x_axis_selection = st.sidebar.selectbox('Select X-Axis', ['Education_Level', 'Employment_Level'])
 

# Streamlit app
st.title('Inverse Relationship between Education and Fertility')

# Create a scatter plot to visualize the inverse relationship

fig = px.scatter(
    data,
    x=x_axis_selection,
    y='"Total Fertility Rate (number of children per woman)"',
    color='"States/UTs"',
    facet_col='AREA',  # Facet by 'Area'
    title='Inverse Relationship between Education and Fertility',
    labels={'EducationLevel': 'Education Level', 'FertilityRate': 'Fertility Rate'},
)
# Customize the layout
fig.update_layout(showlegend=True)

# Show the plot in the Streamlit app
st.plotly_chart(fig)

# Close the Snowflake connection
my_cnx.close()
