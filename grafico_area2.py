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
    for dirname, _, filenames in os.walk('C:/Users/jorge/Downloads/dataset/', topdown=False):
        for filename in filenames:
            if filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(dirname, filename), sep=';', encoding='utf-8')
                df.rename(columns=str.lower, inplace=True)
                df.rename(columns=str.strip, inplace=True)
                df['dt_notific'] = pd.to_datetime(df['dt_notific'], format="%d/%m/%Y")
                df['dt_evoluca'] = pd.to_datetime(df['dt_evoluca'], format="%d/%m/%Y")
                df['dt_encerra'] = pd.to_datetime(df['dt_encerra'], format="%d/%m/%Y")
                df['evolucao'] = df['evolucao'].fillna(9)
                df['hospital'] = df['hospital'].fillna(9)
                lista_df.append(df)

        if lista_df:
            df = pd.concat(lista_df, axis=0, ignore_index=True)
            df = df.drop_duplicates()
            return df
    return None


def gera_grafico(df):
    # Ajusta os valores no Dataframe.
    df1 = df[['nu_idade_n', 'hospital', 'dt_notific', 'dt_evoluca', 'dt_encerra', 'evolucao']]
    # Mantém somente linhas com internação.
    query = '(hospital == 1) and (dt_evoluca == dt_evoluca or dt_encerra == dt_encerra) and (evolucao == 2 or ' \
            'evolucao == 3) '
    df1 = df1.query(query)
    # Remove linhas com valores nulos.
    df1 = df1.dropna()
    # Ajustando as faixas etárias.
    df1.loc[df1['nu_idade_n'] < 20, 'faixa_etaria'] = '0-19 anos'
    df1.loc[np.logical_and(df1['nu_idade_n'] > 19, df1['nu_idade_n'] < 60), 'faixa_etaria'] = '20-59 anos'
    df1.loc[df1['nu_idade_n'] > 59, 'faixa_etaria'] = '60+ anos'
    # Calcula o número de dias internado.
    df1['dt_fim'] = np.where(df1['dt_evoluca'].notnull(), df1['dt_evoluca'], df1['dt_encerra'])
    df1['dias_internacao'] = (df1['dt_fim'] - df1['dt_notific'])
    df1['dias_internacao'] = df1['dias_internacao'].dt.days.astype('int16')
    # Criando as colunas de faixas de internação.
    df1['Até 14 dias'] = np.where(df1['dias_internacao'] < 15, 1, 0)
    df1['15-30 dias'] = np.where(np.logical_and(df1['dias_internacao'] > 14, df1['dias_internacao'] < 31), 1, 0)
    df1['31-60 dias'] = np.where(np.logical_and(df1['dias_internacao'] > 30, df1['dias_internacao'] < 61), 1, 0)
    df1['Mais de 60 dias'] = np.where(df1['dias_internacao'] > 60, 1, 0)
    df1 = df1.drop(['nu_idade_n', 'hospital', 'dt_notific', 'dt_evoluca', 'dt_encerra', 'dt_fim', 'dias_internacao'],
                   axis=1)
    df1 = df1.groupby('faixa_etaria').agg(soma1=pd.NamedAgg(column='Até 14 dias', aggfunc=sum),
                                          soma2=pd.NamedAgg(column='15-30 dias', aggfunc=sum),
                                          soma3=pd.NamedAgg(column='31-60 dias', aggfunc=sum),
                                          soma4=pd.NamedAgg(column='Mais de 60 dias', aggfunc=sum)).reset_index()
    df1.columns = ['Faixa etária', '1-14 dias', '15-30 dias', '31-60 dias', '61+ dias']
    df1 = df1.set_index('Faixa etária')
    # Monta e gera o gráfico.
    ax = df1.plot.area(stacked=False)
    fig = ax.get_figure()
    fig.savefig("C:/Users/jorge/Downloads/Imagens/05_grafico_area.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    # Gera os gráficos.
    gera_grafico(df)


if __name__ == '__main__':
    main()
