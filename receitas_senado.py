#!/usr/bin/env python
# coding: utf-8

# # Versões e Bibliotecas

# In[1]:


#versão do Pandas utilizada foi a '1.1.3 / se houver atualização o notebook instalará versão original
import pandas as pd

versao = pd.__version__
if versao != '1.1.3':
    get_ipython().system('pip install pandas==1.1.3')
    print(f'Pandas versão: {versao}')
else:
    print(f'Pandas versão: {versao}')

from datetime import date


# # Backup arquivo anterior

# In[64]:


try:
    backup = pd.read_csv(
        'receitas_senado.csv',
        engine='python',
        delimiter=';',
        encoding='utf-8'
    )

    backup.to_csv(
        'receitas_senado_backup.csv',
        sep=';',
        encoding='utf-8',
        index=False
    )
    print('BACKUP = OK')
except Exception as erro:
    print('BACKUP = ERRO')
    print(erro)


# # Extração dados da web

# In[12]:


try:
    receitas = pd.read_csv(
        'http://www.senado.gov.br/bi-arqs/Arquimedes/Financeiro/ReceitasSenado.csv',
        engine='python',
        delimiter=';',
        encoding='ISO-8859-1'
    )
    data_extracao = date.today()
    print(f'EXTRAÇÃO DE DADOS EM {data_extracao} = OK')
except Exception as erro:
    data_extracao = date.today()
    print(f'EXTRAÇÃO DE DADOS EM {data_extracao} = ERRO')
    print(erro)


# ## Informações da base de dados

# In[14]:


linhas, colunas = receitas.shape

print('-=' * 30)
print(f'ARQUIVOS COM {linhas} LINHAS E {colunas} COLUNAS.')
print('-=' * 30)

print(receitas.info())


# ## Tratamento

# ### Excluir colunas desnecessárias

# In[34]:


try:
    receitas.drop(
        columns=[
            'Categoria econômica', 
            'Alínea / Desdobramento', 
            'Código natureza de receita',
            'Natureza de receita',
        ],
        inplace=True
    )
    print('EXCLUSÃO COLUNAS = OK')
except Exception as erro:
    print('EXCLUSÃO COLUNAS = ERRO')
    print(erro)


# ### Separar os dados das colunas Órgão, origem e Espécie

# In[53]:


try:
    #fazer o split das colunas pelo traço
    orgao = receitas['Órgão'].str.split(' - ', n=1, expand=True)[1]
    origem = receitas['Origem'].str.split(' - ', n=2, expand=True)[1] #opção coluna com mais valores
    especie = receitas['Espécie'].str.split(' - ', n=2, expand=True)[1] #opção coluna com mais valores

    #atribuir os resultados às respectivas colunas
    receitas['Órgão'] = orgao
    receitas['Origem'] = origem
    receitas['Espécie'] = especie
    print('SPLIT DAS COLUNAS = OK')
except Exception as erro:
    print('SPLIT DAS COLUNAS = ERRO')
    print(erro)


# ### Renomear colunas

# In[56]:


#lista com novos nomes de colunas
lista_colunas = ['ano', 'orgao', 'data_carga', 'origam', 'especie', 'receita_prevista', 'receita_arrecadada']

#iteração entre a lista e as colunas do DataFrame para criar o dicionário com os novos nomes
try:
    dicionario_colunas = {}
    for i in range(len(receitas.columns)):
        dicionario_temp = {receitas.columns[i]: lista_colunas[i]}
        dicionario_colunas.update(dicionario_temp)

    #altera o nome das colunas no DataFrame
    receitas.rename(
        columns=dicionario_colunas,
        inplace=True
    )
    print('RENOMEAR COLUNAS = OK')
except Exception as erro:
    print('RENOMEAR COLUNAS = ERRO')
    print(erro)


# ### Ajuste da categoria das variáveis

# In[59]:


lista_colunas = ['receita_prevista', 'receita_arrecadada']

try:
    for coluna in lista_colunas:
        receitas[coluna] = receitas[coluna].str.replace(',', '.')
        receitas[coluna] = receitas[coluna].astype(dtype=float)
    print('ALTERAÇÃO DTYPES = OK')
except Exception as erro:
    print('ALTERAÇÃO DTYPES = ERRO')
    print(erro)


# In[62]:


print('=-' * 30)
print('FORMATO FINAL DO ARQUIVO')
print('=-' * 30)
print(receitas.info())


# ## Gravar arquivo modificado

# ### <font color=red>Somente fazer a gravação e sobreposição do arquivo se verificado que o mesmo está OK

# In[63]:


try:   
    receitas.to_csv(
        'receitas_senado.csv',
        sep=';',
        encoding='utf-8',
        index=False
    )
    print('GRAVAÇÃO ARQUIVO = OK')
    print('ARQUIVO SALVO NO DIRETÓRIO: PUBLICAM DATA >> SUBPROJETOS >> GASTOS_PUBLICOS >> SENADO_FEDERAL')
except Exception as erro:
    print('GRAVAÇÃO ARQUIVO = ERRO')
    print(erro)

