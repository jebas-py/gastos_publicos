#!/usr/bin/env python
# coding: utf-8

# # Bibliotecas

# In[1]:


import pandas as pd
from datetime import date


# # Backup

# ## Dados Backup

# In[2]:


try:
    backup = pd.read_csv(
        'remuneracao_servidores_senado.csv',
        delimiter=';'
    )
    backup.to_csv(
        'remuneracao_servidores_senado_backup.csv',
        sep=';',
        index=False
    )
    print('BACKUP = OK')
except Exception as erro:
    print('BACKUP = ERRO')
    print(erro)


# # Extração dados da web

# In[3]:


try:
    remuneracao = pd.read_csv(
        'http://www.senado.leg.br/transparencia/LAI/secrh/SF_ConsultaRemuneracaoServidoresParlamentares_202101.csv',
        engine='python',
        delimiter=';',
        encoding='ISO-8859-1',
        header=1
    )
    print('EXTRAÇÃO WEB = OK')
except Exception as erro:
    print('EXTRAÇÃO WEB = ERRO')
    print(erro)


# ## Data carga de dados ATUAL

# In[4]:


dia = date.today()
linhas_atual, colunas_atual = remuneracao.shape

print(f'DATA CARGA DE DADOS ATUAL: {dia}.')
print(f'VOLUME DA ÚLTIMA CARGA DE DADOS: {linhas_atual} LINHAS E {colunas_atual} COLUNAS.')


# ## Tratamento

# ### Excluir colunas desnecessárias

# In[5]:


try:
    remuneracao.drop(
        columns=[
            'REFERÊNCIA CARGO', 
            'SÍMBOLO FUNÇÃO',
            'LOTAÇÃO EXERCÍCIO', 
            ' TIPO FOLHA'
        ],
        inplace=True
    )
    print('EXCLUSÃO COLUNAS = OK')
except Exception as erro:
    print('EXCLUSÃO COLUNAS = ERRO')
    print(erro)


# ### Renomear colunas

# In[6]:


#lista com novos nomes de colunas
lista_colunas = ['vinculo', 'categoria', 'cargo', 'ano_exercicio', 'remuneracao_basica','vantagens_pessoais', 'funcao_comissionada',
                'gratificacao_natalina', 'horas_extras', 'horas_eventuais','abono','reversao_teto', 'IR', 'INSS', 'falta', 
                'remuneracao_liquida', 'diarias', 'auxilios', 'vantagens_indenizadoras'
               ]

#iteração entre a lista e as colunas do DataFrame para criar o dicionário com os novos nomes
try:
    dicionario_colunas = {}
    for i in range(len(remuneracao.columns)):
        dicionario_temp = {remuneracao.columns[i]: lista_colunas[i]}
        dicionario_colunas.update(dicionario_temp)

    #altera o nome das colunas no DataFrame
    remuneracao.rename(
        columns=dicionario_colunas,
        inplace=True
    )
    print('RENOMEAR COLUNAS = OK')
except Exception as erro:
    print('RENOMEAR COLUNAS = ERRO')
    print(erro)


# ### Ajuste da categoria das variáveis

# In[29]:


lista_colunas = [
    'remuneracao_basica','vantagens_pessoais', 'funcao_comissionada', 'gratificacao_natalina', 'horas_extras', 
    'horas_eventuais','abono','reversao_teto', 'IR', 'INSS', 'falta', 'remuneracao_liquida', 'diarias', 'auxilios'
]
try:
    for coluna in lista_colunas:
        remuneracao[coluna] = remuneracao[coluna].str.replace(',', '.')
        remuneracao[coluna] = remuneracao[coluna].astype(dtype=float)
    print('ALTERAÇÃO DTYPES = OK')
except Exception as erro:
    print('ALTERAÇÃO DTYPES = ERRO')
    print(erro)


# In[30]:


print(remuneracao.info())


# ## Filtrar registros de 2013 em diante

# In[31]:


try:
    remuneracao = remuneracao.query(
        'ano_exercicio >= 2013'
    )
    linhas_filtro, colunas_filtro = remuneracao.shape
    
    print('FILTRO DOS REGISTROS = OK')
    print(f'VOLUME DE DADOS APÓS FILTRO: {linhas_filtro} LINHAS E {colunas_filtro} COLUNAS.')
    print(f'TOTAL DE REGISTROS DESCARTADOS {linhas_atual - linhas_filtro}.')
except Exception as erro:
    print('FILTRO DOS REGISTROS = ERRO')
    print(erro)


# ## Gravar arquivo modificado

# In[32]:


try:
    remuneracao.to_csv(
        'remuneracao_servidores_senado.csv',
        sep=';',
        index=False
    )
    print('GRAVAÇÃO ARQUIVO = OK')
    print('ARQUIVO SALVO NO DIRETÓRIO: PUBLICAM DATA >> SUBPROJETOS >> GASTOS_PUBLICOS >> SENADO_FEDERAL')
except Exception as erro:
    print('GRAVAÇÃO ARQUIVO = ERRO')
    print(erro)


# In[ ]:




