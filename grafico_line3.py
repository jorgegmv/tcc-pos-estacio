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
                # Formata a Data para Dia/Mês/Ano.
                df['dt_notific'] = pd.to_datetime(df['dt_notific'], format="%d/%m/%Y")
                # Internação em Hospital:
                # 1 -> Sim, invasivo
                # 2 -> Sim, não invasivo
                # 3 -> Não
                # 9 -> Ignorado
                # Os registros que possuem valores nulo serão convertidos para 9.
                df['suport_ven'] = df['suport_ven'].fillna(9)
                lista_df.append(df)

        if lista_df:
            df = pd.concat(lista_df, axis=0, ignore_index=True)
            df = df.drop_duplicates()
            return df
    return None


def gera_grafico(df):
    # Seleciona as colunas do Dataframe a serem trabalhadas.
    df1 = df[['suport_ven', 'dt_notific']]
    # Mantém somente linhas não nulas.
    df1 = df1.dropna()
    # Ajusta os dados.
    # Data para o formato Ano/Mês
    df1['dt_notific'] = df1['dt_notific'].dt.strftime('%Y/%m')
    # Uso do Suporte Ventilatório.
    df1['suport_ven'] = df1['suport_ven'].astype('int32')
    # Para aplicar a soma das mortes considera o que não contiver o valor 2, 3 ou 9 como sendo zero.
    df1['suport_ven'] = df1['suport_ven'].map({1: 1, 2: 1, 3: 0, 9: 0})
    df1.columns = ['suport_ven', 'Ano/Mês']
    df1 = df1.groupby(['Ano/Mês']).agg(total=pd.NamedAgg(column='suport_ven', aggfunc='count'),
                                       obito=pd.NamedAgg(column='suport_ven', aggfunc='sum'))
    df1 = df1.sort_index()
    df1.columns = ['Casos (Total)', 'Uso de Suporte Ventilatório (Total)']
    # Monta e gera o gráfico.
    ax = df1.plot(kind="line", marker='o', legend=True)
    fig = ax.get_figure()
    fig.savefig("C:/Users/jorge/Downloads/Imagens/03_grafico_line.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    # Gera os gráficos.
    gera_grafico(df)


if __name__ == '__main__':
    main()
