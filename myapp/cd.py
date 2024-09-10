import pandas as pd

def preprocess_cd(df):
    df['Valor do Processo (R$)'] = df['Valor do Processo (R$)'].str.replace(',','.').astype(float)
    df['Data de Aprovação'] =pd.to_datetime(df['Data de Aprovação'], dayfirst=True)
    df['Qtd.'] = df['Qtd.'].str.replace(',','.').astype(float)
    df['Vl. Unitário (R$)'] = df['Vl. Unitário (R$)'].str.replace(',','.').astype(float)
    df_filtrado = df[(df['Valor do Processo (R$)'] >=0)]

    return df_filtrado

def calculate_cd(df):
  df['total'] = df['Qtd.'] * df['Vl. Unitário (R$)']
  total_processos = len(df['ID Processo'].unique())
  valor_total = df['total'].sum()
  processos_total_f = f"{int(total_processos):,}".replace(",", ".")
  valor_total_f = f"{int(valor_total):,}".replace(",", ".")
  return df, processos_total_f, valor_total_f


def formatar(valor):
  return f"{int(valor):,}".replace(",", ".")


def tes(df):
  agrupamento = df.groupby('Afastamento').agg({'total':'sum', 'ID Processo':'nunique'})
  agrupamento = agrupamento.to_dict()
  new_dict = {
    key: {
      'Valor Total': formatar(agrupamento['total'][key]),
      'Quantidade de Processos': formatar(agrupamento['ID Processo'][key])
    }
    
    for key in agrupamento['total']
  }
  return new_dict

def tes_licit(df):
  agrupamento = df.groupby('Modalidade').agg({'Valor Total Homologado (R$)':'sum', 'ID Licitação':'nunique'})
  agrupamento = agrupamento.to_dict()
  new_dict = {
    key: {
      'Valor Total': formatar(agrupamento['Valor Total Homologado (R$)'][key]),
      'Quantidade de Processos': formatar(agrupamento['ID Licitação'][key])
    }
    
    for key in agrupamento['Valor Total Homologado (R$)']
  }
  return new_dict
    
    
def load_data(url):
    return pd.read_csv(url, sep=';', encoding='latin-1')

def preprocess_data(df):
    df['Data de Aprovação'] = pd.to_datetime(df['Data de Aprovação'], dayfirst=True)
    df['Qtd.'] = df['Qtd.'].str.replace(',', '.').astype(float)
    df['Vl. Unitário (R$)'] = df['Vl. Unitário (R$)'].str.replace(',', '.').astype(float)
    df['total'] = df['Qtd.'] * df['Vl. Unitário (R$)']
    return df

def get_year_options(df):
    options = df['Data de Aprovação'].dt.year.unique()
    return options

def filter_data_by_year(df, year):
    start_date = pd.to_datetime(f'{year}-01-01')
    end_date = pd.to_datetime(f'{year}-12-31')
    return df[(df['Data de Aprovação'] >= start_date) & (df['Data de Aprovação'] <= end_date)]

def calculate_totals(df):
    total_processos = len(df['ID Processo'].unique())
    valor_total = df['total'].sum()
    processos_total_f = f"{int(total_processos):,}".replace(",", ".")
    valor_total_f = f"{int(valor_total):,}".replace(",", ".")
    return processos_total_f, valor_total_f

#funções para a tabela licitações

def preprocess_licit(df):
    df['Data/Hora Homologação'] = pd.to_datetime(df['Data/Hora Homologação'], dayfirst=True)
    df['Valor Total Homologado (R$)'] = df['Valor Total Homologado (R$)'].str.replace(',','.').astype(float)
    return df

def filtro_licit(df):
  df_licit = df[df['Status'] == 'Homologado']
  valores_desejados = ['Pregão Eletrônico - Lei 8.666','Pregão Eletrônico - 14.133/2021', 'Pregão Eletrônico - 13.303/2016','Pregão Presencial']
  df_licit_filtrado = df_licit[df_licit['Modalidade'].isin(valores_desejados)]
  return df_licit_filtrado

def calculate_totals_licit(df):
    total_processos = len(df['ID Licitação'].unique())
    valor_total = df['Valor Total Homologado (R$)'].sum()
    processos_total_f = f"{int(total_processos):,}".replace(",", ".")
    valor_total_f = f"{int(valor_total):,}".replace(",", ".")
    return processos_total_f, valor_total_f

def filter_data_by_year_licit(df, year):
    start_date = pd.to_datetime(f'{year}-01-01')
    end_date = pd.to_datetime(f'{year}-12-31')
    return df[(df['Data/Hora Homologação'] >= start_date) & (df['Data/Hora Homologação'] <= end_date)]

def calculate_trad(df):
  valor_total=df['Valor Total Homologado (R$)'].sum() 
  processos_totais=len(df['ID Licitação'].unique())
  valor_total_f = f"{int(valor_total):,}".replace(",", ".")
  processos_totais_f = f"{int(processos_totais):,}".replace(",", ".")
  return valor_total_f, processos_totais_f


def preprocess_trad(df):
   df_filt = df[df['Modalidade'].isin(['Concorrência','Convite','Tomada de Preços','Concorrência Eletrônica - 14.133/2021'])]
   df_filt2 = df_filt[df_filt['Status'].isin(['Adjudicado'])]
   df_filt2['Valor Total Homologado (R$)'] = df_filt2['Valor Total Homologado (R$)'].fillna('0,00')
   df_filt2['Valor Total Homologado (R$)'] = df_filt2['Valor Total Homologado (R$)'].str.replace(',','.').astype(float)
   df_filt2['Valor Total Estimado (R$)'] = df_filt2['Valor Total Estimado (R$)'].str.replace(',','.').astype(float)
   df_filt2['Data/Hora Adjudicação'] = pd.to_datetime(df_filt2['Data/Hora Adjudicação'], dayfirst=True)
   return df_filt2

def filter_data_by_year_licit_trad(df, year):
    start_date = pd.to_datetime(f'{year}-01-01')
    end_date = pd.to_datetime(f'{year}-12-31')
    return df[(df['Data/Hora Adjudicação'] >= start_date) & (df['Data/Hora Adjudicação'] <= end_date)]