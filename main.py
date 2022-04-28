def crea_file():
    titolo = str(input('\nInserire nome per il file: '))
    file = pd.concat([ft_df, te_df], ignore_index=True)
    file.to_markdown(titolo + '.md')


"""------------------------------------------------------------------------------------------------------------------"""
if __name__ == '__main__':
    try:
        selettore = int(input("selezionare l'attività da svolgere:\n"
                              "1. Estrarre gli articoli\n"
                              "2. Generare una wordcloud per gli articoli\n"
                              "3. Applicare il topic modelling agli articoli\n"
                              "4. Applicare la sentiment analysis agli articoli\n"
                              ">> "))
        if selettore == 1:
            import pandas as pd
            from ft_lettura import ft_df
            from economist_lettura import te_df

            crea_file()

        elif selettore == 2:
            from word_cloud import crea_cloud

            nome_file = str(input('Scegliere il file per il quale si vuole visionare la wordcloud: '))
            crea_cloud(nome_file + ".md")

        elif selettore == 3:
            from topic_modeling_objects import mostra_topic

            mostra_topic()

        elif selettore == 4:
            from sentiment_articles import Sentiment

            Sentiment.esegui_sentiment()

    except ValueError:
        print('selezionare con un numero')
