#!/usr/bin/env python
# coding: utf-8

# # Versão e Bibliotecas

# In[9]:


#versão do Pandas utilizada foi a '1.1.3 / se houver atualização o notebook instalará versão original
import pandas as pd

versao = pd.__version__

if versao != '1.1.3':
    get_ipython().system('pip install pandas==1.1.3')
    print(f'Pandas versão alterada para {versao}')
else:
    print(f'Pandas versão: {versao}')


# # Backup arquivo anterior

# In[2]:


try:
    backup = pd.read_csv(
        'despesas_senado.csv',
        engine='python',
        delimiter=';',
        encoding='utf-8'
    )

    backup.to_csv(
        'despesas_senado_backup.csv',
        sep=';',
        encoding='utf-8',
        index=False
    )
    print('BACKUP = OK')
except Exception as erro:
    print('BACKUP = ERRO')
    print(erro)


# # Extração dados da web

# ## Despesas ATUAL

# In[3]:


try:
    despesas = pd.read_csv(
        'http://www.senado.gov.br/bi-arqs/Arquimedes/Financeiro/DespesaSenado.csv',
        engine='python',
        delimiter=';',
        encoding='utf-8'
    )
    print('EXTRAÇÃO WEB = OK')
except Exception as erro:
    print('extração web = erro')
    print(erro)


# ## Data carga de dados ATUAL

# In[5]:


data_carga_atual = despesas['Data da Carga da Base'].unique()[0]
linhas_atual, colunas_atual = despesas.shape

print(f'DATA CARGA DE DADOS ATUAL: {data_carga_atual}.')
print(f'VOLUME DA CARGA DE DADOS: {linhas_atual} LINHAS E {colunas_atual} COLUNAS.')


# ## Informações da base

# In[8]:


print('INFORMAÇÕES DA BASE DE DADOS')
print( '=-' * 30)
despesas.info()


# ## Tratamento

# ### Excluir colunas desnecessárias

# In[9]:


try:
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
    print('EXCLUSÃO COLUNAS = OK')
except Exception as erro:
    print('EXCLUSÃO COLUNAS = ERRO')
    print(erro)


# ### Renomear colunas

# In[10]:


#lista com novos nomes de colunas
lista_colunas = ['data_carga', 'exercicio_financeiro', 'acao', 'plano_orcamentario', 'grupo_despesa',
    'modalidade_aplicacao', 'fonte','valor_dotacao_inicial', 'valor_dotacao_atualizado', 'valor_total_empenhado',
    'valor_liquidado','valor_pago']

#iteração entre a lista e as colunas do DataFrame para criar o dicionário com os novos nomes
try:
    dicionario_colunas = {}
    for i in range(len(despesas.columns)):
        dicionario_temp = {despesas.columns[i]: lista_colunas[i]}
        dicionario_colunas.update(dicionario_temp)

    #altera o nome das colunas no DataFrame
    despesas.rename(
        columns=dicionario_colunas,
        inplace=True
    )
    print('RENOMEAR COLUNAS = OK')
except Exception as erro:
    print('RENOMEAR COLUNAS = ERRO')
    print(erro)


# ### Ajuste da categoria das variáveis

# In[11]:


lista_colunas = ['valor_dotacao_inicial', 'valor_dotacao_atualizado', 'valor_total_empenhado','valor_liquidado','valor_pago']

try:
    for coluna in lista_colunas:
        despesas[coluna] = despesas[coluna].str.replace(',', '.')
        despesas[coluna] = despesas[coluna].astype(dtype=float)
    print('ALTERAÇÃO DTYPES = OK')
except Exception as erro:
    print('ALTERAÇÃO DTYPES = ERRO')
    print(erro)


# ## Informações Final da Base

# In[1]:


print('INFORMAÇÕES FINAL DA BASE DE DADOS')
print( '=-' * 30)
despesas.info()


# ## Gravar arquivo modificado

# ### <font color=red>Somente fazer a gravação e sobreposição do arquivo se verificado que o mesmo está OK

# In[13]:


try:   
    despesas.to_csv(
        'despesas_senado.csv',
        sep=';',
        encoding='utf-8',
        index=False
    )
    print('GRAVAÇÃO ARQUIVO = OK')
    print('ARQUIVO SALVO NO DIRETÓRIO: PUBLICAM DATA >> SUBPROJETOS >> GASTOS_PUBLICOS >> SENADO_FEDERAL')
except Exception as erro:
    print('GRAVAÇÃO ARQUIVO = ERRO')
    print(erro)


# In[ ]:




