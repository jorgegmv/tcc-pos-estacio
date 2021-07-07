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
                lista_df.append(df)

        if lista_df:
            df = pd.concat(lista_df, axis=0, ignore_index=True)
            df = df.drop_duplicates()
            return df
    return None


def gera_grafico(df):
    # Ajusta os valores no Dataframe.
    df1 = df[['nu_idade_n']]
    df1 = df1.dropna()
    df1.columns = ['Idade (Total de Casos)']
    # Monta e gera o gráfico.
    # df1.plot.box()
    color = {"boxes": "DarkGreen", "whiskers": "DarkOrange", "medians": "DarkBlue", "caps": "Gray"}
    ax = df1.plot.box(color=color, sym="r+")
    fig = ax.get_figure()
    fig.savefig("C:/Users/jorge/Downloads/Imagens/09_grafico_boxplot.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    gera_grafico(df)


if __name__ == '__main__':
    main()
