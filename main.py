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
    dt = {15: str, 60: str, 62: str, 63: str, 64: str, 92: str, 94: str, 106: str, 115: str, 117: str, 118: str,
          119: str, 123: str}
    lista_df = []
    for dirname, _, filenames in os.walk('C:/Users/jorge/Downloads/dataset/', topdown=False):
        for filename in filenames:
            if filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(dirname, filename), sep=';', encoding='utf-8', dtype=dt)
                df.rename(columns=str.lower, inplace=True)
                df.rename(columns=str.strip, inplace=True)
                df['dt_notific'] = pd.to_datetime(df['dt_notific'], format="%d/%m/%Y")
                df['dt_sin_pri'] = pd.to_datetime(df['dt_sin_pri'], format="%d/%m/%Y")
                df['dt_nasc'] = pd.to_datetime(df['dt_nasc'], format="%d/%m/%Y")
                df['dt_evoluca'] = pd.to_datetime(df['dt_evoluca'], format="%d/%m/%Y")
                df['dt_encerra'] = pd.to_datetime(df['dt_encerra'], format="%d/%m/%Y")
                df['evolucao'] = df['evolucao'].fillna(9)
                lista_df.append(df)

        if lista_df:
            df = pd.concat(lista_df, axis=0, ignore_index=True)
            df = df.drop_duplicates()
            return df
    return None


def gera_grafico_evolucao_por_ano_mes(df):
    # Ajusta os valores no Dataframe.
    df1 = df[['dt_notific', 'evolucao']]
    # Remove linhas com valores nulos.
    df1.dropna()
    # Ajusta a data para Ano/Mês.
    df1['dt_notific'] = df1['dt_notific'].dt.strftime('%Y/%b')
    # Monta o índice do gráfico.
    indice = df1['dt_notific'].unique()
    # Junta os tipos de óbito.
    df1['evolucao'] = df1['evolucao'].replace(3, 2)
    # Realiza uma contagem das ocorrências por evolução.
    df1 = df1.value_counts().to_frame('contagem').reset_index()
    # Ajusta a Evolução.
    df1['evolucao'] = df1['evolucao'].map({1: 'cura', 2: 'obito', 9: 'ignorado'})
    # Transpõe as linhas em colunas.
    df1 = df1.pivot_table('contagem', ['dt_notific'], 'evolucao')
    df1['total'] = df1['cura'] + df1['obito'] + df1['ignorado']
    # Monta e gera o gráfico.
    df2 = pd.DataFrame({'Total': df1['total'], 'Cura': df1['cura'],
                        'Óbito': df1['obito'], 'Não Informado': df1['ignorado']}, index=indice)
    df2.plot(style='.-')
    plt.show()


def gera_grafico_por_uf(df):
    # Ajusta os valores no Dataframe.
    df1 = df[['sg_uf_not', 'evolucao']]
    df1.columns = ['uf', 'evolucao']
    # Remove linhas com valores nulos.
    df1 = df1.dropna()
    # Conta as ocorrências por UF.
    cura = df1[df['evolucao'] == 1].groupby(['uf']).agg(total=pd.NamedAgg(column='evolucao', aggfunc='count'))
    cura = cura.sort_values(by=['uf'])
    cura = cura.pivot_table('total', [], 'uf')
    obito = df1[np.logical_or(df['evolucao'] == 2, df['evolucao'] == 3)].groupby(['uf']).agg(
        total=pd.NamedAgg(column='evolucao', aggfunc='count'))
    obito = obito.sort_values(by=['uf'])
    obito = obito.pivot_table('total', [], 'uf')
    ignorado = df1[df['evolucao'] == 9].groupby(['uf']).agg(total=pd.NamedAgg(column='evolucao', aggfunc='count'))
    ignorado = ignorado.sort_values(by=['uf'])
    ignorado = ignorado.pivot_table('total', [], 'uf')
    # Une as linhas dos dataframes.
    dff = cura
    dff = dff.append(obito)
    dff = dff.append(ignorado)
    dff = dff.reset_index()
    print(dff)
    # Monta e gera o gráfico.
    color = {"boxes": "DarkGreen", "whiskers": "DarkOrange", "medians": "DarkBlue", "caps": "Gray"}
    dff.plot.box(color=color, sym="r+")
    plt.show()


def gera_grafico_por_sexo(df):
    # Ajusta os valores no Dataframe.
    df1 = df[['cs_sexo', 'evolucao']]
    # Remove linhas com valores nulos.
    df1.dropna()
    # Ajusta o Sexo.
    df1['cs_sexo'] = df1['cs_sexo'].map({'M': 'Masculino', 'F': 'Feminino', 'I': 'Indefinido'})
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
                        'Ignorado': df1['ignorado']}, index=indice)
    ax = df2.plot.bar(rot=0)
    for p in ax.patches:
        ax.annotate("{:.0f}".format(np.round(p.get_height(), decimals=2)),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    plt.show()


def gera_grafico_tempo_internacao_por_faixa_etaria(df):
    # Ajusta os valores no Dataframe.
    df1 = df[['nu_idade_n', 'hospital', 'dt_notific', 'dt_evoluca', 'dt_encerra']]
    # Mantém somente linhas com internação.
    df1 = df1.query('(hospital == 1) and (dt_evoluca == dt_evoluca or dt_encerra == dt_encerra)')
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
    df1.plot.area(stacked=False)
    # sns.heatmap(df1, cmap='RdYlGn_r', linewidths=0.5, annot=True, fmt='d')
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    # Gera os gráficos.
    gera_grafico_por_uf(df)


if __name__ == '__main__':
    main()
