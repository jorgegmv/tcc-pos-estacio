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
    df1 = df[['evolucao', 'classi_out']]
    # Mantém somente óbitos.
    df1 = df1.query('evolucao == 2 or evolucao == 3')
    df1['evolucao'] = df1['evolucao'].fillna(9)
    df1 = df1.dropna()
    df1['classi_out'] = df1['classi_out'].str.strip()
    df1['classi_out'] = df1['classi_out'].str.replace(' ', '_')
    df1['classi_out'] = df1['classi_out'].str.replace('-', '_')
    df1['classi_out'] = df1['classi_out'].str.replace('__', '_')
    df1['classi_out'] = df1['classi_out'].str.replace('___', '_')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_NAO_ESPECIFICADA', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_NAO_ESPECIFICA', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_NAO_ESPEDIFICADA', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_COMUNITARIA', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PEUNOMIA_POR_COVID_19', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA,_COVID_19', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_VIRAL', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_GRAVE', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_VIRAL_P/_COVID', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_BACTERIANA_N/E', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_HOSPITALAR', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEMONIA', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONI_BACTERIANA', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('PNEUMONIA_BACTERIANA', 'PNEUMONIA')
    df1['classi_out'] = df1['classi_out'].str.replace('METASTASE_PULMONAR_E_MEDIASTIN', 'METASTASE_PULMONAR_E_MEDIASTINO')
    df1['classi_out'] = df1['classi_out'].str.replace('TUBERCULOSE_PULMONAR', 'TUBERCULOSE')
    df1['classi_out'] = df1['classi_out'].str.replace('M._TUBERCULOSIS', 'TUBERCULOSE')
    df1['classi_out'] = df1['classi_out'].str.replace('M_TUBERCULOSIS', 'TUBERCULOSE')
    df1['classi_out'] = df1['classi_out'].str.replace('CORONAVIRUS_SAR_COV_2', 'COVID_19')
    causas = df1['classi_out']
    # Junta as palavras.
    palavras = " ".join(s for s in causas)
    # Configura e gera o gráfico.
    stopwords = set(STOPWORDS)
    stopwords.update(['e', 'da', 'meu', 'em', 'você', 'de', 'ao', 'os'])
    wordcloud = WordCloud(stopwords=stopwords,
                          collocations=False,
                          background_color='black', width=1600,
                          height=800).generate(palavras)
    plt.figure(facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    wordcloud.to_file("C:/Users/jorge/Downloads/Imagens/11_grafico_wordcloud.png")
    plt.show()


def main():
    # Obtém os dados da API.
    df = get_dataframe()
    gera_grafico(df)


if __name__ == '__main__':
    main()
