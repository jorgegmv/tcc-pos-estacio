import locale
import os
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

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
    # Remove linhas com valores nulos.
    df1.dropna()
    # Ajusta o Sexo.
    df1['cs_sexo'] = df1['cs_sexo'].map({'M': 'Masculino', 'F': 'Feminino', 'I': 'Não Informado'})
    # Monta o índice do gráfico.
    indice = df1['cs_sexo'].unique()
    # Realiza uma contagem das ocorrências por sexo.
    df1 = df1.value_counts().to_frame('contagem').reset_index()
    # Ajusta a Evolução.
    df1['evolucao'] = df1['evolucao'].map({1: 'cura', 2: 'obito', 3: 'obito_outros', 9: 'ignorado'})
    # Transpõe as linhas em colunas.
    df1 = df1.pivot_table('contagem', ['cs_sexo'], 'evolucao')
    # Monta e gera o gráfico.
    df2 = pd.DataFrame({'Cura': df1['cura'], 'Óbito': df1['obito'], 'Óbito (Outros)': df1['obito_outros'],
                        'Não Informado': df1['ignorado']}, index=indice)
    ax = df2.plot.bar(rot=0)
    for p in ax.patches:
        ax.annotate("{:.0f}".format(np.round(p.get_height(), decimals=2)),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    fig = ax.get_figure()
    fig.savefig("C:/Users/jorge/Downloads/Imagens/06_grafico_bar.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    # Gera os gráficos.
    gera_grafico(df)


if __name__ == '__main__':
    main()
