import streamlit
import snowflake.connector
import plotly.express as px

streamlit.title('TechGig Women in Data')
streamlit.header('Hypothesis on Economic Empowerment and Marital Status')

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

# Adding code to show relation between education and fertility
my_cur.execute("select '"States/UTs"' ,AREA , '"Women (age 15-49)  with 10 or more years of schooling (%)"' ,'"Total Fertility Rate (number of children per woman)"' from NHFS ")

result = my_cur.fetchall()

data = my_cur.DataFrame(result, columns=['"States/UTs"', 'AREA', '"Women (age 15-49)  with 10 or more years of schooling (%)"','"Total Fertility Rate (number of children per woman)"'])

# Streamlit app
streamlit.title('Inverse Relationship between Education and Fertility')

# Create a scatter plot to visualize the inverse relationship

fig = px.scatter(
    data,
    x='"Women (age 15-49)  with 10 or more years of schooling (%)"',
    y='"Total Fertility Rate (number of children per woman)"',
    color='"States/UTs"',
    facet_col='Area',  # Facet by 'Area'
    title='Inverse Relationship between Education and Fertility',
    labels={'EducationLevel': 'Education Level', 'FertilityRate': 'Fertility Rate'},
)
# Customize the layout
fig.update_layout(showlegend=True)

# Show the plot in the Streamlit app
st.plotly_chart(fig)

# Close the Snowflake connection
my_cnx.close()
