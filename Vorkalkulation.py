import streamlit as st
import pandas as pd
import io
from PIL import Image
# from google.cloud import firestore
# import os
#
# # Initialize Firestore client
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "anlagentechnik-aschersleben-firebase-adminsdk-sfoug-5eb13936b2.json"
# db = firestore.Client()
#
#
# # Function to get all collection names from Firestore database
# def get_all_collections(db):
#     excluded_collections = {'operators', 'posts', 'projects'}  # Set of collections to exclude
#     collections = db.collections()
#     return [collection.id for collection in collections if collection.id not in excluded_collections]
#
#
# # Function to get all document IDs from a Firestore collection
# def get_all_document_ids(collection_name):
#     docs = db.collection(collection_name).stream()
#     return [doc.id for doc in docs]
#
#
# # Function to get data from Firestore for a specific document in a collection
# def get_data_from_firestore(collection_name, document_id):
#     doc_ref = db.collection(collection_name).document(document_id)
#     doc = doc_ref.get()
#     return doc.to_dict() if doc.exists else None
#

image = Image.open('logo_ata.png')
st.image(image, caption='Ata Logo', use_column_width=True)

# Define data types and properties
properties = {
    'Brennen': float,
    'Richten': float,
    'Heften_Zussamenb_Verputzen': float,
    'Anzeichnen': float,
    'Schweißen': float,
}

units = {
    'Brennen': 'min',
    'Richten': 'min',
    'Heften_Zussamenb_Verputzen': 'min',
    'Anzeichnen': 'min',
    'Schweißen': 'min',
}
# firestore_data = {}
#
# # Display a select box with all collection names
# collection_names = get_all_collections(db)
# selected_collection = st.selectbox('Select Collection:', options=collection_names)
#
# # Fetch and display the data for a known document ID ('Details') from the selected collection
# if selected_collection:
#     firestore_data = get_data_from_firestore(selected_collection, 'Details')

field_mapping = {
    'Brennen': 'Brennen',
    'Richten': 'Richten',
    'Heften_Zussamenb_Verputzen': 'Heften_Zussamenb_Verputzen',
    'Anzeichnen': 'Anzeichnen',
    'Schweißen': 'Schweißen'
}

st.title("Vorkalkulation")

# Initialize session state for each property
if "data" not in st.session_state:
    st.session_state.data = {prop: "" for prop in properties}

# # If firestore_data is fetched, update the session state
# if firestore_data:
#     for app_field, firestore_field in field_mapping.items():
#         # Assuming 'Gegenstand' should map to 'Benennung' in Firestore
#         if app_field == 'Gegenstand':
#             firestore_field = 'Benennung'
#         st.session_state.data[app_field] = firestore_data.get(firestore_field, "")

col1, col2 = st.columns(2)

props_col1 = list(properties.keys())[:len(properties) // 2]
props_col2 = list(properties.keys())[len(properties) // 2:]

for prop in props_col1:
    prompt = f"{prop} ({units.get(prop, '')})"
    # Use the session state data to populate the fields
    st.session_state.data[prop] = col1.text_input(prompt, value=st.session_state.data[prop]).strip()

for prop in props_col2:
    prompt = f"{prop} ({units.get(prop, '')})"
    # Use the session state data to populate the fields
    st.session_state.data[prop] = col2.text_input(prompt, value=st.session_state.data[prop]).strip()


# Convert the user input data dictionary to a pandas DataFrame
df = pd.DataFrame([st.session_state.data])


# Function to download DataFrame as Excel
def download_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    return output.getvalue()


# Function to download DataFrame as JSON
def download_json(df):
    return df.to_json(orient="records")


# Provide download options
if st.button("Download as Excel"):
    excel_data = download_excel(df)
    st.download_button("Download Excel File", excel_data, file_name="data.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if st.button("Download as JSON"):
    json_data = download_json(df)
    st.download_button("Download JSON File", json_data, file_name="data.json", mime="application/json")