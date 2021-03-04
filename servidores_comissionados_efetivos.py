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

#importar date do módulo daterime para obter o dia da extração
from datetime import date


# # Backup arquivo anterior

# In[2]:


try:
    backup = pd.read_csv(
        'servidores_senado.csv',
        engine='python',
        delimiter=';',
        encoding='utf-8'
    )

    backup.to_csv(
        'servidores_senado_backup.csv',
        sep=';',
        encoding='utf-8',
        index=False
    )
    print('BACKUP = OK')
except Exception as erro:
    print('BACKUP = ERRO')
    print(erro)


# # Extração do arquivo web

# In[3]:


try:
    servidores = pd.read_csv(
        'http://www.senado.gov.br/transparencia/LAI/secrh/todos_csv.csv',
        engine='python',
        encoding='ISO-8859-1',
        delimiter=';',
        header=1
    )
    data_extracao = date.today()
    print(f'EXTRAÇÃO DE DADOS EM {data_extracao} = OK')
except Exception as erro:
    data_extracao = date.today()
    print(f'EXTRAÇÃO DE DADOS EM {data_extracao} = ERRO')
    print(erro)


# ## Informações da base de dados

# In[11]:


linhas, colunas = servidores.shape

print('-=' * 30)
print(f'ARQUIVO COM {linhas} LINHAS E {colunas} COLUNAS.')
print('-=' * 30)

print(servidores.info())


# # Tratamento

# ## Excluir colunas

# In[5]:


try:
    servidores.drop(
        columns=[
            'SETOR1',
            'SETOR3',
            'SETOR4',
            'SETOR5',
            'SETOR6',
            'SETOR7',
            'CARGO',
            'CATEGORIA',
            'AFASTAMENTO',
            'ISENÇÃO DO PONTO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      '
        ],
        inplace=True
    )
    print('EXTRAÇÃO DE COLUNAS = OK')
except Exception as erro:
    print('EXTRAÇÃO DE COLUNAS = ERRO')
    print(erro)


# ## Separar colunas SETOR2 e SETOR_EXERCICIO

# In[7]:


try:
    #fazer o split da coluna SETOR2 pelo traço
    setor2 = servidores['SETOR2'].str.split(' - ', n=1, expand=True)[1]
    servidores['SETOR2'] = setor2

    #fazer o split da coluna SETOR_EXERCICIO pelo traço/espaço
    setor_exercicio = servidores['SETOR_EXERCICIO'].str.split(' - ', n=1, expand=True)[1]
    servidores['SETOR_EXERCICIO'] = setor_exercicio
    print('SEPARAÇÃO DE COLUNAS = OK')
except Exception as erro:
    print('SEPARAÇÃO DE COLUNAS = ERRO')
    print(erro)


# ## Renomear colunas

# In[8]:


#lista com novos nomes de colunas
lista_colunas = ['setor', 'setor_exercicio', 'nome', 'tipo_vinculo', 'data_admissao', 'funcao']

#iteração entre a lista e as colunas do DataFrame para criar o dicionário com os novos nomes
try:
    dicionario_colunas = {}
    for i in range(len(servidores.columns)):
        dicionario_temp = {servidores.columns[i]: lista_colunas[i]}
        dicionario_colunas.update(dicionario_temp)

    #altera o nome das colunas no DataFrame
    servidores.rename(
        columns=dicionario_colunas,
        inplace=True
    )
    print('RENOMEAR COLUNAS = OK')
except Exception as erro:
    print('RENOMEAR COLUNAS = ERRO')
    print(erro)


# ## Formato do arquivo

# In[9]:


print('=-' * 30)
print('FORMATO FINAL DO ARQUIVO')
print('=-' * 30)

print(servidores.info())


# # Gravação

# In[12]:


try:
    servidores.to_csv(
        'servidores_senado.csv',
        sep=';',
        encoding='utf-8',
        index=False
    )
    print('GRAVAÇÃO ARQUIVO = OK')
    print('ARQUIVO SALVO NO DIRETÓRIO: PUBLICAM DATA >> SUBPROJETOS >> GASTOS_PUBLICOS >> SENADO_FEDERAL')
except Exception as erro:
    print('GRAVAÇÃO ARQUIVO = ERRO')
    print(erro)

