Per eseguire il codice presente nel file .ipynb è necessario prima di tutto avere accesso alla cartella drive con i dataset.
Il link alla cartella drive è il seguente: https://drive.google.com/drive/folders/1GcyVdhKStRl0S3j0O96cFKH95NZIEGCs?usp=sharing
Se il file .ipynb viene aperto in google colab, per caricare i dataset bisognerà portare la suddetta cartella nel proprio drive.
Basterà poi farvi l'accesso eseguendo il codice nella seconda cella e seguendo le istruzioni.
Sarà eventualmente necessario modificare il percorso dei file al momento del caricamento.
Se il file .ipynb non viene aperto in google colab, bisognerà probabilmente scaricare i dataset dalla cartella drive.
Una volta scaricati, basterà cambiare il percorso dei file al momento del caricamento.
Il codice è adeguatamente commentato e permette una semplice esecuzione.
I tempi computazionali potrebbero essere abbastanza lunghi.
Nel caso in cui il codice venga eseguito su google colab, non dovrebbe essere necessario installare nessuna libreria aggiuntiva.
Nel caso di esecuzione locale (o altro), se le librerie richieste non sono già installate, basta eseguire da command line il seguente comando:
pip install pandas numpy gzip-reader nltk textblob scikit-learn joblib keras matplotlib
Sempre nel caso di esecuzione locale, bisogna commentare nella prima cella la seguente riga di codice: from google.colab import drive
Ovviamente, in caso di esecuzione locale, non va eseguita la seconda cella in cui si effettua il login in google drive.