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
                df['dt_notific'] = pd.to_datetime(df['dt_notific'], format="%d/%m/%Y")
                df['dt_sin_pri'] = pd.to_datetime(df['dt_sin_pri'], format="%d/%m/%Y")
                df['dt_nasc'] = pd.to_datetime(df['dt_nasc'], format="%d/%m/%Y")
                df['dt_evoluca'] = pd.to_datetime(df['dt_evoluca'], format="%d/%m/%Y")
                df['dt_encerra'] = pd.to_datetime(df['dt_encerra'], format="%d/%m/%Y")
                df['sem_not'] = df['sem_not'].fillna(0)
                df['sem_pri'] = df['sem_pri'].fillna(0)
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
    df1.columns = ['UF', 'evolucao']
    df1 = df1.dropna()
    df1 = df1.groupby(['UF']).agg(total=pd.NamedAgg(column='evolucao', aggfunc='count'))
    df1 = df1.pivot_table('total', [], 'UF')
    ax = df1.plot.bar(rot=0)
    ax.legend(loc='lower left')
    for p in ax.patches:
        ax.annotate("{:.0f}".format(np.round(p.get_height(), decimals=2)),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    fig = ax.get_figure()
    fig.savefig("C:/Users/jorge/Downloads/Imagens/07_grafico_bar.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    # Gera os gráficos.
    gera_grafico(df)


if __name__ == '__main__':
    main()
