#https://towardsdatascience.com/deploy-a-public-streamlit-web-app-for-free-heres-how-bf56d46b2abe
import streamlit as st
import pandas as pd

st.write("My First Streamlit Web App")

# df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
df = pd.read_excel("07012022/0000000015e46514 Range Test 07012022.xlsx",sheet_name="combined-csv-files",engine="openpyxl")
# st.write(df)
st.line_chart(df)
