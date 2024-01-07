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

# Adding code to show relation between education/employment and fertility
my_cur.execute('select "States/UTs" ,AREA , "Women (age 15-49)  with 10 or more years of schooling (%)"  as "Educated Women(%)","Women (age 15-49 years) who worked in the last 12 months and were paid in cash (%)" as "Employed Women(%)", "Total Fertility Rate (number of children per woman)" , "Women age 20-24 years married before age 18 years (%)" as "Early Marriage Rate", "Women age 15-19 years who were already mothers or pregnant at the time of the survey (%)" as "Motherhood Rate" from WOMEN_IN_DATA.HYPOTHESIS_1.NHFS ')

result = my_cur.fetchall()

data = pd.DataFrame(result, columns=['States/UTs', 'AREA', 'Educated Women(%)','Employed Women(%)','Total Fertility Rate (number of children per woman)','Early Marriage Rate', 'Motherhood Rate'])
#data = st.dataframe(result)
x_axis_selection = st.sidebar.selectbox('Select X-Axis for relation between education/employment and fertility', ['Educated Women(%)','Employed Women(%)'])
selected_state = st.sidebar.selectbox('Select State', data['States/UTs'].unique())

# Filter the data based on the selected state
filtered_data = data[data['States/UTs'] == selected_state]
 

# Streamlit app
#st.subheader('Relationship between Education and Fertility')

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

# Create a bar chart for Early Marriage Rate vs Motherhood Rate
st.subheader('Education Level vs Early Marriage/Motherhood')

fig_grouped_bar = px.bar(
    data.melt(id_vars=[selected_state, 'AREA'], value_vars=['Educated Women(%)', 'Early Marriage Rate', 'Motherhood Rate']),
    x=selected_state,
    y='value',
    color='variable',
    facet_col='AREA',  # Facet by 'Area'
    barmode='group',
    title='Grouped Bar Chart for Education Level and Early Marriage/Motherhood',
)
# Customize the layout
fig_grouped_bar.update_layout(showlegend=True)

# Customize the layout
fig_grouped_bar.update_layout(showlegend=True)

# Show the plot in the Streamlit app
st.plotly_chart(fig)
st.plotly_chart(fig_grouped_bar)

# Close the Snowflake connection
my_cnx.close()
