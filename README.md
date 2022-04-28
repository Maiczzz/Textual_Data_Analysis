# README #

This README would normally document whatever steps are necessary to get your application up and running.

## What is this repository for? ##
### Quick summary:

*Lo scopo di questo progetto è di estrarre dei dati testuali dalle testate economiche "The Economist" e "Financial Times",
in particolare gli articoli che sono stati pubblicati dalle stesse nel periodo che va da marzo 2022 a ottobre 2021.

*Si procede quindi a operare sugli stessi sia una sentiment analysis, così da determinare la percentuale di articoli positivi e negativi
che sono stati pubblicati in un dato mese, sia una topic modelling che restituisca i principali temi trattati.
 
*L'output finale del progetto è un dataframe che contenga per ogni mese il valore dell'inflazione, il valore dell'aggregato monetario
M2, i risultati della sentiment analysis e del topic modelling il tutto riferito ai valori aggregati per i paesi dell' EU
e agli articoli della sezione Europa.


## How do I get set up? ###

!!! IMPORTANTE !!!
Nel commit sono stati inseriti molti file. Il file da aprire e lanciare è " main.py ", da lì è possibile richiamare tutte le operazioni dagli altri file.

### Summary of set up:
* Scaricare da github geckodriver e posizionarlo nella cartella contenente python, accedere con le proprie credenziali sul
browser firefox al Financial Times e installare l'estensione "i don't care about cookies"
* Per funzionare wordcloud ha necessità di un compilatore C++, su windows si può installare visual studio
### Dependencies:
* bs4
* requests
* requests-html
* selenium
* matplotlib
* pandas
* numpy
* sklearn
* urllib.parse
* wordcloud
* nltk

