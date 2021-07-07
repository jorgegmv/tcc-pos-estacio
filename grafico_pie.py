import locale
import os
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.style.use(['seaborn-whitegrid', 'ggplot', 'fast'])
sns.set_theme()
warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_ALL, 'pt_BR')


def get_dataframe():
    lista_df = []
    for dirname, _, filenames in os.walk('D:/data/dataset/covid/', topdown=False):
        for filename in filenames:
            if filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(dirname, filename), sep=';', encoding='utf-8')
                df.rename(columns=str.lower, inplace=True)
                df.rename(columns=str.strip, inplace=True)
                df['evolucao'] = df['evolucao'].fillna(9)
                df['cs_sexo'] = df['cs_sexo'].fillna('I')
                lista_df.append(df)

        if lista_df:
            df = pd.concat(lista_df, axis=0, ignore_index=True)
            df = df.drop_duplicates()
            return df
    return None


def gera_grafico(df):
    # Ajusta os valores no Dataframe.
    df1 = df[['cs_sexo', 'evolucao']]
    df1 = df1.dropna()
    # Ajusta o Sexo.
    df1['cs_sexo'] = df1['cs_sexo'].map({'M': 'Masculino', 'F': 'Feminino', 'I': 'Não Informado'})
    # Monta o índice do gráfico.
    indice = df1['cs_sexo'].unique()
    # Realiza uma contagem das ocorrências por sexo.
    df1 = df1.value_counts().to_frame('contagem').reset_index()
    del df1['evolucao']
    df1 = df1.pivot_table('contagem', [], 'cs_sexo')
    # Monta e gera o gráfico.
    df2 = pd.DataFrame(
        {'Sexo': [df1['Masculino'].to_list()[0], df1['Feminino'].to_list()[0], df1['Não Informado'].to_list()[0]]},
        index=indice)
    ax = df2.plot.pie(y='Sexo')
    fig = ax.get_figure()
    fig.savefig("C:/Users/jorge/Downloads/Imagens/06_grafico_pie.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    # Gera os gráficos.
    gera_grafico(df)


if __name__ == '__main__':
    main()
