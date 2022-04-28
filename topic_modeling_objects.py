from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from tokenization_objects import PreProcessing
from word_cloud import crea_cloud
"""------------------------------------------------------------------------------------------------------------------"""


class ProcessText(object):

    def __init__(self, list_of_text):
        self.list_of_text = list_of_text

    def text_cleaner(self):
        # Questa parte mi permette di pulire gli articoli che gli passo, tokenizzarli, e, successivamente, lemmizzarti.
        articoli_lemmed = []
        for articolo in self.list_of_text:
            articoli_tokenized = PreProcessing(articolo).lemmatize_words()
            articoli_lemmed.append(articoli_tokenized)

        # Questa parte invece mi permette di prendere gli articoli (che sono ancora in forma di token) e riportarli
        # alla forma testuale, chiaramente ogni articolo separato dall'altro. Faccio questo in quanto la funzione
        # 'CountVectorizer' prende in ingresso una lista in cui ogni argomento è un testo (in questo caso un
        # articolo), e non una lista di tokens.
        articoli_def = []
        for token in articoli_lemmed:
            articoli_cleaned = ''
            for tok in token:
                articoli_cleaned += tok + ' '
            articoli_def.append(articoli_cleaned[:-1])
        return articoli_def

    def topic(self):
        # Vettorizzazione: trasformo gli articoli in vettori.
        count_vect = CountVectorizer()
        x_counts = count_vect.fit_transform(self.text_cleaner())

        # tf-idf: Trasformo la matrice dei conteggi delle parole nel testo incrociando le stesse parole in altri
        # documenti
        tfidf_transformer = TfidfTransformer()
        x_tfidf = tfidf_transformer.fit_transform(x_counts)

        # LDA: Con l'LDA (latent dirichlet allocation) calcoliamo la probabilità che ogni articolo appartenga ad uno dei
        # topic (dimension).
        dimension = 3
        lda = LDA(n_components=dimension)
        lda_array = lda.fit_transform(x_tfidf)
        # print(lda_array)
        # Con 'lda array' possiamo vedere la probabilità che ogni articolo appartenga al primo o al secondo topic.
        # nelle prime 2 righe la probabilità è molto alta che appartenga al primo topic e bassissima che appartenga
        # al secondo. per le ultime 3 righe il contrario.
        # print(lda_array)

        # In questa ultima parte si definisce il numero di topic e il numero delle features (il dizionario delle
        # parole). Successivamente si va a  ciclare per il nuemero dei topic 'len(components)' e per ogni componente
        # si vanno a prendere le parole più frequenti per ongi topic, in ordine di frequenza.
        components = [lda.components_[i] for i in range(len(lda.components_))]
        features = count_vect.get_feature_names()
        important_words = [sorted(features, key=lambda x: components[j][features.index(x)], reverse=True)[:3] for j in
                           range(len(components))]
        # L'output sarà dunque una lista di liste in cui ogni lista è un topic e gli elementi sono le parole più
        # importanti quel topic.
        return important_words


"""------------------------------------------------------------------------------------------------------------------"""

# questa funzione mostra l'esito della topic sugli articoli di una mese dopodiché esegue la stessa per altre 10 volte
# ogni volta inserendo in un unica stringa le parole dei diversi topic, su questa stringa viene poi creata una
# wordcloud, questo è stato fatto nella speranza di evidenziare i topic più significativi rispetto quelli secondari i
# quali sarebbero dovuti comparire meno spesso nelle diverse ripetizioni
def mostra_topic():
    # MARZO
    print('\necco i topic per il mese di marzo: ')
    articoli = []
    bag = ''
    with open('6. Marzo_22.md', encoding='utf8') as f:
        for line in f:
            articoli.append(line)
    articoli_def = ProcessText(articoli)
    print(articoli_def.topic())
    for i in range(1, 10):
        topic = articoli_def.topic()
        for lista in topic:
            tmp = ' '.join(lista)
            bag = bag+' '+tmp
    crea_cloud(bag)

    # FEBBRAIO
    print('\necco i topic per il mese di febbraio: ')
    articoli = []
    bag = ''
    with open('5. Febbraio_22.md', encoding='utf8') as f:
        for line in f:
            articoli.append(line)
    articoli_def = ProcessText(articoli)
    print(articoli_def.topic())
    for i in range(1, 10):
        topic = articoli_def.topic()
        for lista in topic:
            tmp = ' '.join(lista)
            bag = bag + ' ' + tmp
    crea_cloud(bag)

    # GENNAIO
    print('\necco i topic per il mese di gennaio: ')
    articoli = []
    bag = ''
    with open('4. Gennaio_22.md', encoding='utf8') as f:
        for line in f:
            articoli.append(line)
    articoli_def = ProcessText(articoli)
    print(articoli_def.topic())
    for i in range(1, 10):
        topic = articoli_def.topic()
        for lista in topic:
            tmp = ' '.join(lista)
            bag = bag + ' ' + tmp
    crea_cloud(bag)

    # DICEMBRE
    print('\necco i topic per il mese di dicembre: ')
    articoli = []
    bag = ''
    with open('3. Dicembre_21.md', encoding='utf8') as f:
        for line in f:
            articoli.append(line)
    articoli_def = ProcessText(articoli)
    print(articoli_def.topic())
    for i in range(1, 10):
        topic = articoli_def.topic()
        for lista in topic:
            tmp = ' '.join(lista)
            bag = bag + ' ' + tmp
    crea_cloud(bag)

    # NOVEMBRE
    print('\necco i topic per il mese di novembre: ')
    articoli = []
    bag = ''
    with open('2. Novembre_21.md', encoding='utf8') as f:
        for line in f:
            articoli.append(line)
    articoli_def = ProcessText(articoli)
    print(articoli_def.topic())
    for i in range(1, 10):
        topic = articoli_def.topic()
        for lista in topic:
            tmp = ' '.join(lista)
            bag = bag + ' ' + tmp
    crea_cloud(bag)

    # OTTOBRE
    print('\necco i topic per il mese di ottobre: ')
    articoli = []
    bag = ''
    with open('1. Ottobre_21.md', encoding='utf8') as f:
        for line in f:
            articoli.append(line)
    articoli_def = ProcessText(articoli)
    print(articoli_def.topic())
    for i in range(1, 10):
        topic = articoli_def.topic()
        for lista in topic:
            tmp = ' '.join(lista)
            bag = bag + ' ' + tmp
    crea_cloud(bag)
