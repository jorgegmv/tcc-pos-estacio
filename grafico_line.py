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
                # Ajusta o nome das colunas para minúsculo e sem espaços.
                df.rename(columns=str.lower, inplace=True)
                df.rename(columns=str.strip, inplace=True)
                lista_df.append(df)

        if lista_df:
            df = pd.concat(lista_df, axis=0, ignore_index=True)
            df = df.drop_duplicates()
            return df
    return None


def gera_grafico(df):
    # Seleciona as colunas do Dataframe a serem trabalhadas.
    df1 = df[['hospital', 'uti', 'dt_notific']]
    # Formata a Data para Dia/Mês/Ano.
    df1['dt_notific'] = pd.to_datetime(df1['dt_notific'], format="%d/%m/%Y")
    # Trata valores nulo como sendo indefinidos, que é id 9.
    df1['hospital'] = df1['hospital'].fillna(9)
    df1['uti'] = df1['uti'].fillna(9)
    # Mantém somente linhas não nulas.
    df1 = df1.dropna()
    # Ajusta os dados.
    # Data para o formato Ano/Mês
    df1['dt_notific'] = df1['dt_notific'].dt.strftime('%Y/%m')
    # Internação para número inteiro.
    df1['hospital'] = df1['hospital'].astype('int32')
    df1['uti'] = df1['uti'].astype('int32')
    # Para aplicar a soma das internações em Hospital considera o que não contiver o valor 1 como sendo zero.
    df1['hospital'] = df1['hospital'].map({1: 1, 2: 0, 9: 0})
    # Para aplicar a soma das internações em UTI considera o que não contiver o valor 1 como sendo zero.
    df1['uti'] = df1['uti'].map({1: 1, 2: 0, 9: 0})
    df1.columns = ['hospital', 'uti', 'Ano/Mês']
    df1 = df1.groupby(['Ano/Mês']).agg(total=pd.NamedAgg(column='hospital', aggfunc='count'),
                                       hospital=pd.NamedAgg(column='hospital', aggfunc='sum'),
                                       uti=pd.NamedAgg(column='uti', aggfunc='sum'))
    df1 = df1.sort_index()
    df1.columns = ['Casos (Total)', 'Internações (Hospital)', 'Internações (UTI)']
    # Monta e gera o gráfico.
    ax = df1.plot(kind="line", marker='o', legend=True)
    fig = ax.get_figure()
    fig.savefig("C:/Users/jorge/Downloads/Imagens/01_grafico_line.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    # Gera os gráficos.
    gera_grafico(df)


if __name__ == '__main__':
    main()
