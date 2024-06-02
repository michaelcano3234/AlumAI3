from app_secrets import OPENAI_API_KEY
from app_secrets import PASSWORD

import os
import streamlit as st
from sql_execution import execute_sf_query
from langchain_community.llms import OpenAI
from langchain.prompts import load_prompt
import json
import hmac


#Authenticate user
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():

        """Checks whether a password entered by the user is correct."""
        entered_password = st.session_state.get("password", "")
        if hmac.compare_digest(entered_password, PASSWORD):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


#setup env variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

#frontend
st.set_page_config(
    page_title="Query Assistant",
    page_icon="🌄"
)

tab_titles=[
    "Results",
    "Query",
]

#Centering the image
st.markdown(
    """
    <style>
        [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)


st.image("aiLogo.jpg", width=200)  

st.title("AlumAI")
#Request from the user
prompt = st.text_input("Enter your query")
tabs = st.tabs(tab_titles)

csv = None

prompt_template = load_prompt("prompt2.yaml")

# Load the contents of the dict.json file
with open('dict.json', 'r') as json_file:
    dict_data = json.load(json_file)

# Convert the dict_data to a string
dict_string = json.dumps(dict_data)

#Clean query_text
def clean_query_text(input_string):
    return input_string.split(";", 1)[0]





#Final prompt to be used for the llm
final_prompt = prompt_template.format(input=prompt, json_data=dict_string)

llm = OpenAI(temperature=0)


if prompt:
    #Getting the SQL query
    query_text = llm(prompt=final_prompt)
    query_text = clean_query_text(query_text)

    #Getting the results as a dataframe
    output = execute_sf_query(query_text)
    if output is not None and not output.empty:
        csv = output.to_csv(index=False).encode('utf-8')


    with tabs[0]:
        st.write(output)
        
        if csv is not None:

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='alumni_data.csv',
                mime='text/csv',
            )
        else:
            st.write("CSV data is not available yet. Please wait for it to be generated.")




    with tabs[1]:
        st.write(query_text)

