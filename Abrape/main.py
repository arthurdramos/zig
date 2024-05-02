from functions import *

def main():
    authenticate()
    
    sheet_key = '1KW6OP2bYIpy0igl2eJb7-qEU2svCxrYtjz45-x98yDU'
    
    df_abrape = get_spreadsheet_data(sheet_key, "Abrape")
    df_balada_app = get_spreadsheet_data(sheet_key, "Scrapping BaladApp")
    df_outgo = get_spreadsheet_data(sheet_key, "Outgo - Eventos")
    
    df_abrape = apply_clean_produtores(df_abrape, 'Produtor')
    df_balada_app = apply_clean_produtores(df_balada_app, 'anuncio_auxiliar.informacoes_descritivas.produtor.value')
    df_outgo = apply_clean_produtores(df_outgo, 'Producer Name')
    
    clean_produtor_column(df_abrape, 'Produtor')
    clean_producer_name_column(df_outgo, 'Producer Name')
    
    matches_abrape_outgo = fuzzy_merge_df(df_abrape, df_outgo, 'Produtor', 'Producer Name')
    matches_abrape_balada = fuzzy_merge_df(df_abrape, df_balada_app, 'Produtor', 'anuncio_auxiliar.informacoes_descritivas.produtor.value')
    
    return matches_abrape_outgo, matches_abrape_balada

if __name__ == "__main__":
    main()
