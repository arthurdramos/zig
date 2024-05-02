from google.colab import auth
import gspread
from google.auth import default
import pandas as pd
import re
import fuzzy_pandas as fpd

def authenticate():
    auth.authenticate_user()

def authorize():
    credentials, _ = default()
    return gspread.authorize(credentials)

def get_spreadsheet_data(sheet_key, worksheet_name):
    gc = authorize()
    ss = gc.open_by_key(sheet_key)
    ws = ss.worksheet(worksheet_name)
    rows = ws.get_all_values()
    return pd.DataFrame.from_records(rows[1:], columns=rows[0])

def clean_produtores(series):
    return series.str.lower().str.replace('[^a-z\s]','').str.replace(r"eventos|producoes|produtora|produtor|entretenimento|producoes e eventos|produções|promocoes|promocao|produes artisticas|participacoes|ltda|servicos|shows|locacoes|produes",'', regex=True).str.replace(' e ','')

def apply_clean_produtores(df, column):
    df['prodClean'] = clean_produtores(df[column])
    return df

def clean_produtor_column(df, column):
    df[column] = df[column].str.lower().str.replace('[^a-z\s]','').str.replace(r"eventos|producoes|produtora|produtor|entretenimento|producoes e eventos!|produções|promocoes|promocao|stage music|ltda",'', regex=True).str.replace(' e','').str.replace(' e ','')
    df[column] = df[column].str.strip()
    print(df[column].tail(50))

def clean_producer_name_column(df, column):
    df[column] = df[column].str.lower().str.replace('[^a-z\s]','').str.replace(r"eventos|producoes|produtora|produtor|entretenimento|producoes e eventos!|produções|promocoes|promocao|stage music|ltda|music|club|beach club|produçoes|brasil|ticket|promo",'', regex=True).str.replace(' e','').str.replace(' e ','')
    df[column] = df[column].str.strip()
    print(df[column].tail(50))

def fuzzy_merge_df(df1, df2, left_on, right_on):
    matches = fpd.fuzzy_merge(df1, df2,
                               left_on=left_on,
                               right_on=right_on,
                               ignore_case=True,
                               method="levenshtein",
                               threshold=0.6,
                               keep='match')
    return matches
