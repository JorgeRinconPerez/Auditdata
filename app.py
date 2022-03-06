import streamlit as st
import pandas as pd

def explore(df):
  # DATA
  st.write("\n")
  st.markdown('####  Data (first 10 records):')
  #st.write(df.head(10))
  st.dataframe(df)
  # AUDIT
  st.write("\n")
  st.markdown('#### Audit:')
  st.write("Number of rows: ", len(df))
  st.write("Number of columns: ", len(df.columns))
  st.write("\n")

  y = pd.DataFrame(columns=["Column Name", "Type", "Cardinality", "Granularity", 'Percentage of Nulls', "Examples"], dtype=object)
  y["Cardinality"] = pd.to_numeric(y["Cardinality"])
  y["Percentage of Nulls"] = pd.to_numeric(y["Percentage of Nulls"])
  longitud = len(df)
  for i in df.columns:
    nombre_variable = df[f"{i}"].name
    tipo_variable = df[f"{i}"].dtype
    cardianalidad_variable = df[f"{i}"].nunique()
    n_nulo_variable = df[f"{i}"].isnull().sum() / longitud
    ejemplo_valores_variable = df[f"{i}"].unique().tolist()[:3]
    nivelgranularidad = cardianalidad_variable / longitud

    x = pd.DataFrame({'Column Name': [nombre_variable],
                      "Type": [tipo_variable],
                      "Cardinality": [cardianalidad_variable],
                      "Granularity": [round(nivelgranularidad*100, 2)],
                      "Percentage of Nulls": [round(n_nulo_variable*100, 2)],
                      "Examples": [ejemplo_valores_variable]})

    y = y.append(x, ignore_index=True)

  st.write(y.astype(str))

  @st.cache
  def convert_y(y):
    return y.to_csv().encode('utf-8')
  csv = convert_y(y)
  st.write("\n")
  st.download_button(
    "Press to Download",
    csv,
    "Audited data.csv",
    "text/csv",
    key='download-csv'
  )

def get_df(file):
  # get extension and read file
  extension = file.name.split('.')[1]
  if extension.upper() == 'CSV':
    df = pd.read_csv(file)
  elif extension.upper() == 'XLSX':
    df = pd.read_excel(file, engine='openpyxl')
  elif extension.upper() == 'PICKLE':
    df = pd.read_pickle(file)
  return df

def main():
  st.title('Audit a dataset ️🕵️‍♂️')
  st.markdown('#### A general purpose data audit app by Jorge Rincón.')
  #st.markdown('# Markdown')
  #st.title('My title')
  #st.header('My header')
  #st.subheader('My sub')
  st.write('\n')
  st.write('\n')
  st.write('\n')
  file = st.file_uploader("Upload a .csv, .xlsx or .pickle file to get started", type=['csv', 'xlsx', 'pickle'])
  if not file:
    #st.write("Upload a .csv, .xlsx or .pickle file to get started")
    #st.text('Jorge Rincón')
    #st.code('')
    return
  df = get_df(file)
  explore(df)

if __name__ == '__main__':
    main()
