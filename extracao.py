#!/usr/bin/env python
# coding: utf-8

# # Versão e Bibliotecas

# In[ ]:


#versão do Pandas utilizada foi a '1.1.3 / se houver atualização o notebook instalará versão original
import pandas as pd

versao = pd.__version__
if versao != '1.1.3':
    get_ipython().system('pip install pandas==1.1.3')
    print(f'Pandas versão: {versao}')
else:
    print(f'Pandas versão: {versao}')


# # Funções

# ## título

# In[ ]:


def titulo(titulo):
    print('=-' * 40)
    print(f'{titulo:^80}')
    print('=-' * 40)


# ## backup

# In[ ]:


def backup(nome_arquivo, nome_backup):
    from pandas import read_csv
    try:
        backup = read_csv(
            nome_arquivo,
            engine='python',
            delimiter=';',
            encoding='utf-8'
        )

        backup.to_csv(
            nome_backup,
            sep=';',
            encoding='utf-8',
            index=False
        )
        print('BACKUP = OK')
    except Exception as erro:
        print(f'BACKUP = ERRO {erro}')


# ## informações do arquivo

# In[ ]:


def informacoes_arquivo(tabela):
    linhas, colunas = tabela.shape
    print(f'ARQUIVO CARREGADO COM {linhas} LINHAS E {colunas} COLUNAS.')
    print(f'DETALHE DO ARQUIVO:')
    print(tabela.info())


# ## exclui_coluna

# In[ ]:


def exclui_colunas(*colunas, tabela):
    #lista de colunas a serem excluídas
    lista_coluna = list(colunas)

    #exclusão das colunas selecionadas
    try:
        from pandas import DataFrame
        DataFrame(tabela)
        tabela.drop(
            columns=lista_coluna,
            inplace=True
        )
        print('EXCLUSÃO DAS COLUNAS = OK')
    except Exception as erro:
        print(f'EXCLUSÃO DAS COLUNAS = ERRO ({erro})')


# ## renomeia_colunas

# In[ ]:


def renomeia_colunas(*colunas, tabela):
    #lista com novos nomes de colunas
    lista_colunas = list(colunas)

    #iteração entre a lista e as colunas do DataFrame para criar o dicionário com os novos nomes
    try:
        dicionario_colunas = {}
        for item in range(len(lista_colunas)):
            dicionario_temp = {tabela.columns[item]: lista_colunas[item]}
            dicionario_colunas.update(dicionario_temp)

    #altera o nome das colunas no DataFrame
        tabela.rename(
            columns=dicionario_colunas,
            inplace=True
        )
        print('RENOMEAR COLUNAS = OK')
    except Exception as erro:
        print(f'RENOMEAR COLUNAS = ERRO {erro}')


# ## alteração de dtype

# In[ ]:


def altera_dtypes(*colunas, tabela):
     #lista com as colunas a serem alteradas
    lista_colunas = list(colunas)

    #iteração para alterar as característica de cada coluna
    try:
        for coluna in lista_colunas:
            tabela[coluna] = tabela[coluna].str.replace(',', '.')
            tabela[coluna] = tabela[coluna].astype(dtype=float)
        print('ALTERAÇÃO DTYPES = OK')
        print('DESCRIÇÃO DO ARQUIVO ALTERADO:')
        print(tabela.info())
    except Exception as erro:
        print(f'ALTERAÇÃO DTYPES = ERRO {erro}')


# ## salva o arquivo

# In[ ]:


def salva_arquivo(arquivo, nome_arquivo):
    try:
        arquivo.to_csv(
            nome_arquivo,
            sep=';',
            encoding='utf-8',
            index=False
        )
        print('GRAVAÇÃO ARQUIVO = OK')
        print('ARQUIVO SALVO NO DIRETÓRIO: PUBLICAM DATA >> SUBPROJETOS >> GASTOS_PUBLICOS >> SENADO_FEDERAL')
    except Exception as erro:
        print('GRAVAÇÃO ARQUIVO = ERRO')
        print(erro)


# # Tratamento dos arquivos

# ## Despesas

# In[ ]:


titulo('PROCESSAMENTO DESPESAS')


# ### Backup

# In[ ]:


backup('despesas_senado.csv', 'despesas_senado.backup.csv')


# ### Extração da Web

# In[ ]:


try:
    despesas = pd.read_csv(
        'http://www.senado.gov.br/bi-arqs/Arquimedes/Financeiro/DespesaSenado.csv',
        engine='python',
        delimiter=';',
        encoding='utf-8'
    )
    print('EXTRAÇÃO WEB = OK')
except Exception as erro:
    print(f'EXTRAÇÃO WEB = ERRO {erro}')


# In[ ]:


informacoes_arquivo(despesas)


# ### Exclusão de colunas

# In[ ]:


exclui_colunas(
    'Ação (código)', 
    'Plano Orçamentário (código)', 
    'Grupo de Despesa (código)',
    'Resultado Lei (código)',
    'Resultado Lei (nome)',
    'Modalidade de Aplicação (código)',
    'Fonte (código)',
    tabela=despesas
)


# ### Renomeação das colunas

# In[ ]:


renomeia_colunas(
    'data_carga',
    'exercicio_financeiro',
    'acao',
    'plano_orcamentario', 
    'grupo_despesa',
    'modalidade_aplicacao',
    'fonte',
    'valor_dotacao_inicial', 
    'valor_dotacao_atualizado',
    'valor_total_empenhado',
    'valor_liquidado',
    'valor_pago',
    tabela=despesas                 
)


# ### Alteração dos dtypes

# In[ ]:


altera_dtypes(
    'valor_dotacao_inicial',
    'valor_dotacao_atualizado',
    'valor_total_empenhado',
    'valor_liquidado',
    'valor_pago',
    tabela=despesas
)


# In[ ]:


salva_arquivo(despesas, 'despesas_senado.csv')


# ## Receitas

# In[ ]:


titulo('Processamento Receitas')


# In[ ]:


#backup('receitas_senado.csv', 'receitas_senado_backup.csv')


# ### Backup

# In[ ]:


backup('receitas_senado.csv', 'receitas_senado_backup.csv')


# ### Extração da web

# In[ ]:


try:
    receitas = pd.read_csv(
        'http://www.senado.gov.br/bi-arqs/Arquimedes/Financeiro/ReceitasSenado.csv',
        engine='python',
        delimiter=';',
        encoding='ISO-8859-1'
    )
    print(f'EXTRAÇÃO DE DADOS = OK')
except Exception as erro:
    data_extracao = date.today()
    print(f'EXTRAÇÃO DE DADOS = ERRO {erro}')


# In[ ]:


informacoes_arquivo(receitas)


# ### Exclusão de colunas

# In[ ]:


exclui_colunas(
    'Categoria econômica', 
    'Alínea / Desdobramento', 
    'Código natureza de receita',
    'Natureza de receita',
    tabela=receitas
)


# ### Separação das colunas Órgão, Origem e Espécie

# In[ ]:


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

# In[ ]:


renomeia_colunas(
    'ano', 
    'orgao',
    'data_carga',
    'origem', 
    'especie',
    'receita_prevista',
    'receita_arrecadada',
    tabela=receitas
)


# ### Alterar dtypes

# In[ ]:


altera_dtypes(
    'receita_prevista',
    'receita_arrecadada',
    tabela=receitas
)


# ### Gravação do arquivo

# In[ ]:


salva_arquivo(receitas, 'receitas_senado.csv')


# ## Servidores

# In[ ]:


titulo('PROCESSAMENTO SERVIDORES COMISSIONADOS E EFETIVOS')


# In[ ]:


backup('servidores_senado.csv', 'servidores_senado_backup.csv')


# ### Extração da web

# In[ ]:


try:
    servidores = pd.read_csv(
        'http://www.senado.gov.br/transparencia/LAI/secrh/todos_csv.csv',
        engine='python',
        encoding='ISO-8859-1',
        delimiter=';',
        header=1
    )
    print(f'EXTRAÇÃO DE DADOS = OK')
except Exception as erro:
    data_extracao = date.today()
    print(f'EXTRAÇÃO DE DADOS = ERRO {erro}')


# In[ ]:


informacoes_arquivo(servidores)


# ### Excluir colunas

# In[ ]:


exclui_colunas(
    'SETOR1',
    'SETOR3',
    'SETOR4',
    'SETOR5',
    'SETOR6',
    'SETOR7',
    'CARGO',
    'CATEGORIA',
    'AFASTAMENTO',
    'ISENÇÃO DO PONTO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      ',
    tabela=servidores                
)


# ### Separação das colunas SETOR2, SETOR_EXERCICIO e FUNÇÃO

# In[ ]:


try:
    #fazer o split da coluna SETOR2 pelo traço
    setor2 = servidores['SETOR2'].str.split(' - ', n=1, expand=True)[1]
    servidores['SETOR2'] = setor2
    
    #fazer o split da coluna SETOR_EXERCICIO pelo traço/espaço
    setor_exercicio = servidores['SETOR_EXERCICIO'].str.split(' - ', n=1, expand=True)[1]
    servidores['SETOR_EXERCICIO'] = setor_exercicio
    
    #fazer o split da coluna FUNÇÃO pelo espaço
    funcao = servidores['FUNÇÃO'].str.split(' ', n=1, expand=True)
    servidores['FUNÇÃO'] = funcao

    #dicionário para armazenar iteração
    dicionario_funcao = {}
    #iteração para concatenar o valor CHeFE DE GABIENTE
    for i in funcao[0].unique():
        if i == 'CHEFE':
            dicionario_temp = {i: 'CHEFE DE GABINETE'}
            dicionario_funcao.update(dicionario_temp)
        else:
            dicionario_temp = {i: i}
            dicionario_funcao.update(dicionario_temp)
    #altera os valores da coluna no DataFrame
    servidores['FUNÇÃO'] = servidores['FUNÇÃO'].map(dicionario_funcao)
    print('SEPARAÇÃO DE COLUNAS = OK')
except Exception as erro:
    print('SEPARAÇÃO DE COLUNAS = ERRO')
    print(erro)


# ### Renomear colunas

# In[ ]:


renomeia_colunas(
    'setor',
    'setor_exercicio',
    'nome',
    'tipo_vinculo',
    'data_admissao',
    'funcao',
    tabela=servidores                 
)


# ### Informações do arquivo

# In[ ]:


#arquivo dos Servidores do senado não precisa alterar dtypes
informacoes_arquivo(servidores)


# ### Salvar arquivo

# In[ ]:


salva_arquivo(servidores, 'servidores_senado.csv')


# # Encerramento

# In[ ]:


titulo('EXTRAÇÃO E TRATAMENTO DOS ARQUIVOS ENCERRADA')

