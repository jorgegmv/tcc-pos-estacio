import locale
import os
import warnings

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

plt.style.use(['seaborn-whitegrid', 'ggplot', 'fast'])
warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_ALL, 'pt_BR')


def get_dataframe():
    dt = {15: str, 60: str, 62: str, 63: str, 64: str, 92: str, 94: str, 106: str, 115: str, 117: str, 118: str,
          119: str, 123: str}
    lista_df = []
    for dirname, _, filenames in os.walk('D:/data/dataset/covid/', topdown=False):
        for filename in filenames:
            if filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(dirname, filename), sep=';', encoding='utf-8', dtype=dt)
                df.rename(columns=str.lower, inplace=True)
                df.rename(columns=str.strip, inplace=True)
                df['evolucao'] = df['evolucao'].fillna(9)
                df['sg_uf_not'] = df['sg_uf_not'].fillna('N/I')
                lista_df.append(df)

        if lista_df:
            df = pd.concat(lista_df, axis=0, ignore_index=True)
            df = df.drop_duplicates()
            return df
    return None


def gera_grafico(df):
    df1 = df[['sg_uf_not', 'evolucao']]
    # Mantém somente óbitos.
    df1 = df1.query('evolucao == 2 or evolucao == 3')
    df1 = df1.dropna()
    del df1['evolucao']
    df1['sg_uf_not'] = df1['sg_uf_not'].str.upper()
    df1.columns = ['uf']
    uf = df1['uf']
    # Junta as palavras.
    palavras = " ".join(s for s in uf)
    # Configura e gera o gráfico.
    stopwords = set(STOPWORDS)
    stopwords.update(['da', 'meu', 'em', 'você', 'de', 'ao', 'os'])
    wordcloud = WordCloud(stopwords=stopwords,
                          collocations=False,
                          background_color='black', width=1600,
                          height=800).generate(palavras)
    plt.figure(facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    wordcloud.to_file("C:/Users/jorge/Downloads/Imagens/12_grafico_wordcloud.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    gera_grafico(df)


if __name__ == '__main__':
    main()
