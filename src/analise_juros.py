import pandas as pd
from pathlib import Path

#Localiza a pasta principal do projeto, acima da src
PASTA_PROJETO = Path(__file__).resolve().parent.parent

#Define onde ficam os arquivos de dados
PASTA_DADOS = PASTA_PROJETO / 'dados'

#Lê o arquivo e guarda a tabela na variável df
df = pd.read_csv(
    PASTA_DADOS / 'historicotaxajurosdiario_TodosCampos.csv',
    sep=';',
    decimal=',',
    dtype={'cnpj8': 'string'}
)

#Mostra as 5 primeiras linhas
print(df.head())

#Mostra a quantidade de linhas e colunas
print('Dimensões: ', df.shape)

#Mostra os nomes de todas as colunas
print('Colunas: ', df.columns.tolist())

#Mostra quais públicos e modalidades no arquivo
print('Públicos: ', df['Segmento'].unique())
print('Modalidades: ', df['Modalidade'].unique())

#Exibe o tipo de dado de cada coluna
print(df.dtypes)

#Conta os valores ausentes em cada coluna
print(df.isna().sum())

#Conta linhas totalmente iguais a uma linha anterior
print('Linhas duplicadas:', df.duplicated().sum())

#Conta repetições do identificador após sua primeira ocorrência
print('Identificadores repetidos:', df['cnpj8'].duplicated().sum())

#Seleciona registros com taxa mensal ou anual menor ou igual a 0
taxas_suspeitas = df[
    (df['TaxaJurosAoMes'] <= 0) |
    (df['TaxaJurosAoAno'] <= 0)
]

print(taxas_suspeitas)

#Compara nomes originais com nomes sem espaços nas extremidades
nomes = df['InstituicaoFinanceira']
tem_espaco_extra = nomes != nomes.str.strip()

print('Nomes com espaços extras:', tem_espaco_extra.sum())

#Registra o período de referência em todas as linhas
df['PeriodoInicio'] = '2026-09-21'
df['PeriodoFim'] = '2026-09-25'

#Confere novas colunas
print(df[['InstituicaoFinanceira', 'PeriodoInicio', 'PeriodoFim']].head())

#Salva a tabela com as colunas de período
df.to_csv(
    'juros_tratados.csv',
    sep=';',
    decimal=',',
    index=False,
    encoding='utf-8-sig'
)

print('Arquivo juros_tratados.csv salvo.')

#Seleciona a coluna de taxas mensais
taxas = df['TaxaJurosAoMes']

#Obtém os extremos e calcula a diferença
menor_taxa = taxas.min()
maior_taxa = taxas.max()
amplitude = maior_taxa - menor_taxa

#Formata apenas a exibição com duas casas decimais
print(f'Menor taxa: {menor_taxa:.2f}% ao mês')
print(f'Maior taxa: {maior_taxa:.2f}% ao mês')
print(f'Amplitude: {amplitude:.2f} pontos percentuais')

#Seleciona todas as instituições com a menor taxa
menores = df[df['TaxaJurosAoMes'] == menor_taxa]

#Seleciona todas as instituições com a maior taxa
maiores = df[df['TaxaJurosAoMes'] == maior_taxa]

#Mostra nome e taxa mensal
colunas = ['InstituicaoFinanceira', 'TaxaJurosAoMes']

print('Instituições com a menor taxa:')
print(menores[colunas].to_string(index=False))

print('Instituições com a maior taxa:')
print(maiores[colunas].to_string(index=False))

#Calcula o centro da sequência de taxas mensais
mediana = df['TaxaJurosAoMes'].median()

print(f'Mediana das taxas: {mediana:.2f}% ao mês')

#Calcula a média simples das taxas das instituições
media = df['TaxaJurosAoMes'].mean()

print(f'Média das taxas das instituições: {media:.2f}% ao mês')

#Define os limites das faixas de taxas mensais
limites = [0, 5, 10, 15, 20, 25]

#Classifica cada taxa em uma faixa
faixas = pd.cut(
    df['TaxaJurosAoMes'],
    bins=limites,
    right=False
)

#Conta as instituições por faixa e mantém a ordem dos intervalos
frequencias = faixas.value_counts(sort=False)

print(frequencias)

#Divide a contagem de cada faixa pelo total de registros
percentuais = frequencias / len(df) * 100

print(percentuais.round(2))

#Ordena a tabela pela taxa mensal, em ordem crescente
ordenado = df.sort_values('TaxaJurosAoMes')

#Seleciona as 5 primeiras linhas da tabela ordenada
cinco_menores = ordenado.head(5)

#Mostra apenas as informações necessárias para comparação
colunas = ['InstituicaoFinanceira', 'TaxaJurosAoMes']
print(cinco_menores[colunas].to_string(index=False))

#Obtém a taxa da quinta linha da tabela ordenada
taxa_corte = cinco_menores['TaxaJurosAoMes'].max()

#Inclui todas as instituições com taxa até esse limite
menores_com_empates = ordenado[
    ordenado['TaxaJurosAoMes'] <= taxa_corte
]

colunas = ['InstituicaoFinanceira', 'TaxaJurosAoMes']
print(menores_com_empates[colunas].to_string(index=False))

#Ordena da maior taxa para a menor
ordem_decrescente = df.sort_values(
    'TaxaJurosAoMes',
    ascending=False
)

#Obtém as 5 primeiras linhas e encontra a taxa de corte
cinco_maiores = ordem_decrescente.head(5)
corte_maiores = cinco_maiores['TaxaJurosAoMes'].min()

#Inclui todas as instituições com taxa igual ou superior ao corte
maiores_com_empates = ordem_decrescente[
    ordem_decrescente['TaxaJurosAoMes'] >= corte_maiores
]

print(maiores_com_empates[colunas].to_string(index=False))

#Calcula a distância de cada taxa mensal em relação à mediana
df['DiferencaMedianaPP'] = df['TaxaJurosAoMes'] - mediana

#Seleciona nome, taxa e diferença para conferência
colunas_comparacao = [
    'InstituicaoFinanceira',
    'TaxaJurosAoMes',
    'DiferencaMedianaPP',
]

#Mostra as 5 maiores taxas com a nova informação
comparacao = df.sort_values('TaxaJurosAoMes', ascending=False)

print(
    comparacao[colunas_comparacao]
    .head(5)
    .round(2)
    .to_string(index=False)
)

#Exporta a base com todas as colunas criadas
df.to_csv(
    'juros_tratados.csv',
    sep=';',
    decimal=',',
    index=False,
    encoding='utf-8-sig'
)
print('Arquivo juros_tratados.csv salvo.')
print(f"Base tratada salva em: {PASTA_DADOS / 'juros_tratados.csv'}")
