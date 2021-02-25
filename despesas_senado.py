#!/usr/bin/env python
# coding: utf-8

# # Bibliotecas

# In[1]:


import pandas as pd


# # Backup arquivo anterior

# In[5]:


backup = pd.read_csv(
    'despesas_senado.csv',
    engine='python',
    delimiter=';'    
)

backup.to_csv(
    'despesas_senado_backup.csv',
    sep=';',
    encoding='utf-8',
    index=False
)


# ## Dados Backup

# In[13]:


data_carga_anterior = backup['data_carga'].unique()[0]
linhas_anterior = backup.shape[0]
colunas_anterior = backup.shape[1]

print(f'DATA CARGA DE DADOS DO BACKUP: {data_carga_anterior}.')
print(f'VOLUME CARGA DE DADOS BACKUP: {linhas_anterior} LINHAS E {colunas_anterior} COLUNAS.')


# # Extração dados da web

# ## Despesas ATUAL

# In[9]:


despesas = pd.read_csv(
    'http://www.senado.gov.br/bi-arqs/Arquimedes/Financeiro/DespesaSenado.csv',
    engine='python',
    delimiter=';',
    encoding='utf-8'
)


# ## Data carga de dados ATUAL

# In[10]:


data_carga_atual = despesas['Data da Carga da Base'].unique()[0]
linhas_atual, colunas_atual = despesas.shape

print(f'DATA CARGA DE DADOS ATUAL: {data_carga_atual}.')
print(f'VOLUME DA CARGA DE DADOS ATUAL: {linhas_atual} LINHAS E {colunas_atual} COLUNAS.')


# ## Informações da base

# In[11]:


print(despesas.info())


# ## Tratamento

# ### Excluir colunas desnecessárias

# In[33]:


despesas.drop(
    columns=[
        'Ação (código)', 
        'Plano Orçamentário (código)', 
        'Grupo de Despesa (código)',
        'Resultado Lei (código)',
        'Resultado Lei (nome)',
        'Modalidade de Aplicação (código)',
        'Fonte (código)'
    ],
    inplace=True
)


# ### Renomear colunas

# In[34]:


#lista com novos nomes de colunas
lista_colunas = ['data_carga', 'exercicio_financeiro', 'acao', 'plano_orcamentario', 'grupo_despesa',
    'modalidade_aplicacao', 'fonte','valor_dotacao_inicial', 'valor_dotacao_atualizado', 'valor_total_empenhado',
    'valor_liquidado','valor_pago']

#iteração entre a lista e as colunas do DataFrame para criar o dicionário com os novos nomes
dicionario_colunas = {}
for i in range(len(despesas.columns)):
    dicionario_temp = {despesas.columns[i]: lista_colunas[i]}
    dicionario_colunas.update(dicionario_temp)

#altera o nome das colunas no DataFrame
despesas.rename(
    columns=dicionario_colunas,
    inplace=True
)


# ### Ajuste da categoria das variáveis

# In[35]:


lista_colunas = ['valor_dotacao_inicial', 'valor_dotacao_atualizado', 'valor_total_empenhado','valor_liquidado','valor_pago']

for coluna in lista_colunas:
    despesas[coluna] = despesas[coluna].str.replace(',', '.')
    despesas[coluna] = despesas[coluna].astype(dtype=float)


# In[15]:


print('DADOS DO ARQUIVO SALVO')
print(despesas.info())


# ## Gravar arquivo modificado

# ### <font color=red>Somente fazer a gravação e sobreposição do arquivo se verificado que o mesmo está OK

# In[40]:


try:   
    despesas.to_csv(
        'despesas_senado.csv',
        sep=';',
        encoding='utf-8',
        index=False
    )
    print('ARQUIVO SALVO NO DIRETÓRIO')
    print('Publicam Data >> Subprojetos >> gastos_publicos >> notebooks')
except:
    print('ERRO AO SALVAR O ARQUIVO.')

