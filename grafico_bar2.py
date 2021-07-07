import locale
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
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
                df['sg_uf_not'] = df['sg_uf_not'].fillna('N/I')
                df['evolucao'] = df['evolucao'].fillna(9)
                lista_df.append(df)

        if lista_df:
            df = pd.concat(lista_df, axis=0, ignore_index=True)
            df = df.drop_duplicates()
            return df
    return None


def gera_grafico(df):
    # Ajusta os valores no Dataframe.
    df1 = df[['sg_uf_not', 'evolucao']]
    df1.columns = ['uf', 'evolucao']
    df1['uf'] = df1['uf'].str.upper()
    df1 = df1.dropna()
    df1['Região'] = df1['uf'].map(
        {'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MS': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'AL': 'Nordeste',
         'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste',
         'RN': 'Nordeste', 'SE': 'Nordeste', 'AC': 'Norte', 'AM': 'Norte', 'AP': 'Norte', 'PA': 'Norte', 'RO': 'Norte',
         'RR': 'Norte', 'TO': 'Norte', 'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste', 'PR': 'Sul',
         'RS': 'Sul', 'SC': 'Sul', 'N/I': 'Não Informado'})
    df1 = df1.groupby(['Região']).agg(total=pd.NamedAgg(column='evolucao', aggfunc='count'))
    df1 = df1.pivot_table('total', [], 'Região')
    ax = df1.plot.bar(rot=0)
    for p in ax.patches:
        ax.annotate("{:.0f}".format(np.round(p.get_height(), decimals=2)),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    fig = ax.get_figure()
    fig.savefig("C:/Users/jorge/Downloads/Imagens/08_grafico_bar.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    # Gera os gráficos.
    gera_grafico(df)


if __name__ == '__main__':
    main()
