from flask import Flask, render_template, request
import pandas as pd
from cd import preprocess_cd, calculate_cd,tes, tes_licit, load_data, preprocess_data, get_year_options, filter_data_by_year, calculate_totals, preprocess_licit, filtro_licit, calculate_totals_licit,filter_data_by_year_licit, calculate_trad, preprocess_trad, filter_data_by_year_licit_trad




url = ['https://www.compras.rj.gov.br/siga/imagens/OUTRAS_COMPRAS.CSV',
       'https://www.compras.rj.gov.br/siga/imagens/COMPRAS_DIRETAS.CSV',
       'https://www.compras.rj.gov.br/siga/imagens/LICITACOES.CSV'
]

#outras compras
df_outras_compras = load_data(url[0])
df_outras_compras = preprocess_data(df_outras_compras)
years = get_year_options(df_outras_compras)

#compras diretas

df_cd = load_data(url[1])
df_cd_filtrado = preprocess_cd(df_cd)
df_filtrado_cd = calculate_cd(df_cd_filtrado)[0]

#pregoes

df_licitacao = load_data(url[2])
df_licitao_tratado = preprocess_licit(df_licitacao)
df_filtrado = filtro_licit(df_licitao_tratado)

#tradicionais
df_tratado = load_data(url[2])
df_tratado2 = preprocess_trad(df_tratado)

app = Flask(__name__)


@app.route('/')
def index():
    cd = 'Compras Diretas'
    oc = 'Outras Compras'
    pregoes = 'Pregões - Elet. e Pres.'
    modalidades_trad = 'Modalidades Trad.'
    
    df_cd = load_data(url[1])
    df_cd_filtrado = preprocess_cd(df_cd)
    total_compras_diretas = calculate_cd(df_cd_filtrado)
    total_compras_diretas_p = total_compras_diretas[1] 
    total_compras_diretas_v = total_compras_diretas[2] 
    total_compras_diretas_v = total_compras_diretas_v.replace('.','')
    total_compras_diretas_v = int(total_compras_diretas_v)
    
    total_outras_compras = calculate_totals(df_outras_compras)
    total_outras_compras_p = total_outras_compras[0]
    total_outras_compras_v = total_outras_compras[1]
    total_outras_compras_v = total_outras_compras_v.replace('.','')
    total_outras_compras_v = int(total_outras_compras_v)
    
    
    #total compras publicas
    
    valor_total_compras_publicas = total_outras_compras_v + total_compras_diretas_v
    valor_total_compras_publicas = f"Total de compras feita pelo Estado do Rio de Janeiro: R$ {valor_total_compras_publicas:,}".replace(',','.')
    
    
    #selecionando apenas as modalidades dentro de cada DataFrame tratado e filtrado
    
    
    
    return render_template('index.html', message_cd =cd,message_oc= oc,message_pr=pregoes,message_tr=modalidades_trad, total_valor_cp = valor_total_compras_publicas)


@app.route('/outras_compras', methods = ['GET','POST'])
def index2():
    ano_filt =''
    resultado= ['','']
    processos_t=''
    valor_t=''
    valor1 = ''
    valor2 = ''
    dictio = {}

    if request.method == 'POST':
        ano_filt = request.form.get("ano")
        if ano_filt == 'todos_anos':
            total_processos = calculate_totals(df_outras_compras)
            processos_t = f"Total de processos aprovados: {total_processos[0]}"
            valor_t = f"Valor total aprovado: R$ {total_processos[1]}"
            dictio = tes(df_outras_compras)
        else:
            ano_filt = request.form.get("ano")
            filter = filter_data_by_year(df_outras_compras, ano_filt)
            resultado = calculate_totals(filter) 
            valor1 = f"Processos aprovados em {ano_filt}: {resultado[0]}"
            valor2 = f"Valor total aprovado em {ano_filt}: R$ {resultado[1]}" 
            dictio = tes(filter)  
   
    return render_template('outras_compras.html', teste=years, oi = ano_filt, num1 = valor1, num2 = valor2, processos_t= processos_t, valor_t = valor_t, dictio = dictio)

@app.route('/compras_diretas', methods = ['GET', 'POST'])
def index3():
    ano_filt =''
    resultado= ['','']
    processos_t_cd=''
    valor_t_cd=''
    valor1 = ''
    valor2 = ''
    dictio = {}

    

    if request.method == 'POST':
        ano_filt = request.form.get("ano")
        if ano_filt == 'todos_anos':
            total_processos = calculate_cd(df_cd_filtrado)
            processos_t_cd = f"Total de processos aprovados: {total_processos[1]}"
            valor_t_cd = f"Total de valor aprovado: R$ {total_processos[2]}"
            dictio = tes(df_filtrado_cd)


        else:
            ano_filt = request.form.get("ano")
            filter = filter_data_by_year(df_filtrado_cd, ano_filt)
            resultado = calculate_totals(filter) 
            valor1 = f"Processos aprovados em {ano_filt}: {resultado[0]}"
            valor2 = f"Valor total aprovado em {ano_filt}: R$ {resultado[1]}"
            df_test = filter.drop_duplicates(subset='ID Processo')
            dictio = tes(filter)
    
    return render_template('compras_diretas.html', processos_t_cd=processos_t_cd,valor_t_cd=valor_t_cd, anos = years,valor1=valor1,valor2=valor2, dictio = dictio)
@app.route('/pregoes', methods = ['GET', 'POST'])
def index4():

    ano_filt =''
    resultado= ['','']
    processos_t_cd=''
    valor_t_cd=''
    valor1 = ''
    valor2 = ''
    dictio = {}

    if request.method == 'POST':
        ano_filt = request.form.get("ano")
        if ano_filt == 'todos_anos':
            total_processos = calculate_totals_licit(df_filtrado)
            processos_t_cd = f"Total de processos aprovados: {total_processos[0]}"
            valor_t_cd = f"Valor total aprovado: R$ {total_processos[1]}"
            dictio = tes_licit(df_filtrado)
        else:
            ano_filt = request.form.get("ano")
            filter = filter_data_by_year_licit(df_filtrado, ano_filt)
            resultado = calculate_totals_licit(filter) 
            valor1 = f"Processos aprovados em {ano_filt}: {resultado[0]}"
            valor2 = f"Valor total aprovado em {ano_filt}: R$ {resultado[1]}"
            dictio = tes_licit(filter)   
    
    return render_template('pregoes.html', processos_t_cd=processos_t_cd,valor_t_cd=valor_t_cd, anos = years,valor1=valor1,valor2=valor2, dictio = dictio )
    
@app.route('/tradicionais', methods = ['GET', 'POST'])
def index5():
    ano_filt =''
    resultado= ['','']
    processos_t_cd=''
    valor_t_cd=''
    valor1 = ''
    valor2 = ''
    dictio = {}

    if request.method == 'POST':
        ano_filt = request.form.get("ano")
        if ano_filt == 'todos_anos':
            resultado = calculate_trad(df_tratado2)
            processos_t_cd = f"Total de processos aprovados: {resultado[1]}"
            valor_t_cd = f"Total de valor aprovado: R$ {resultado[0]}"
            dictio = tes_licit(df_tratado2)
        else:
            ano_filt = request.form.get("ano")
            df_filtrado = filter_data_by_year_licit_trad(df_tratado2, ano_filt)
            calculo = calculate_trad(df_filtrado)
            valor1 = f"Processos aprovados em {ano_filt}: {calculo[1]}"
            valor2 = f"Valor total aprovado em  {ano_filt}: R$ {calculo[0]}"
            dictio = tes_licit(df_filtrado)   
    
    return render_template('trad.html', processos_t_cd=processos_t_cd,valor_t_cd=valor_t_cd, anos = years,valor1=valor1,valor2=valor2, dictio = dictio)
if __name__ == '__main__':
    app.run(debug=True)

