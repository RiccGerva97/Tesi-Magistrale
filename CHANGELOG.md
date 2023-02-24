# CHANGELOG

### 02/24
- modificato downloader per scaricare dal server di San Diego
- aggiornato dizionario 'COSMOPAR'


### 02/22
- spostate le funzioni CALCULUS in CalcWST.py e line_parser in arg_parser.py
- dizionario per associare nome cosmologia(/cartella) -> parametri
- trovato ERRORE: dovevo passare a HarmonicScattering3D nel calcolodelle WST non la matrice densità ma sovradensità
- PROBLEMA RISCONTRATO: i dati che stavo fin ora utilizzando non sembrano essere adatti ai nostri scopi!

### 02/21
- aggiunto dizionario delle cosmologie per iterare su queste e poterle associare a un valore numerico da 0 a 10 per i cicli for
- spostato il dizionario in un file a sé stante in MyFunc
- sistemato il formato di output nella scrittura dei file (ora sono array di numpy)
- creata una funzione per il calcolo di WST che utilizza MAS library al posto dell'algoritmo CIC da me creato (impiega circa 2/9 del tempo!)
- progresso nel codice, cicli for per il calcolo delle derivare e calcolo matrice Hartlap

</br>

### 02/20
- Modificato il metodo di avvio del programma: aggiunta la possibilità di modificare attraverso linea di comando il numero di celle (per lato) della griglia di densità, della griglia per la stima dei coefficienti WST, del numero di realizzazioni da utilizzare per cosmologia e le cosmologie da usare.
- Aggiunte funzioni per scrivere su un solo file o ritornare in un'unica variabile i coefficienti WST. 

</br>

### 02/18
- implemented progress bar in 'calc_WST_halos.py'
- aggiunta variabile 'i' alla funzione 'HaloWST_f' (in 'CalcWST.py') per possibilità di stampa a schermo dei tempi
- nuovo script-bozza "Fisher.py" per calcoalre le matricidi Fisher per i coefficienti WST

</br>

### 02/15
- modificato il file per il download da Globus:
    * errori nei path per l'indirizzo della cartella locale (c'erano alcune "//")
    * errore con Globus: modificato il file 'accessPaths.tcl' per permettere alla cartella di destinazione i diritti di lettura/scrittura (vedi [qui](https://docs.globus.org/how-to/globus-connect-personal-linux/#config-paths))
    * aggiunta documentazione per "downloader-prova.py"
    * modificato nome "downloader-prova.py" $\rightarrow$ "downloader-globus.py"
- creata cartella con relativo file per testare la libreria 'pickle'
- creato file per calcolare i coefficienti di scattering per una cosmologia (estendibile a più) ("calc_WST_halo.py")
- migliorati indirizzi cartelle nei file per uso generico per pull da GitHub

</br>

### 01/27
#### Primo aggiornamento di changelog 
Ad oggi creati:
- notebook per analisi di distribuzione di DM da simulazioni Quijote (nella cartella "Try_01-densityfield")
- notebook per analisi di cataloghi di aloni sempre da simulazioni Quijote (nella cartella "Try_02-HaloCatalogue")
- funzione per costruire matrici densità da cataloghi di aloni con metodo CIC, conrelativo test (nella cartella "My_func", "myCIC.py" e "test_CIC.py")
- funzione per calcolare direttamente i coefficienti di scattering da cataloghi di aloni (nella cartella "My_func, nel file "CalcWST.py")
- creato branch "multithread" per prove di multithreading su funzione myCIC
- ottimizzata funzione myCIC (3m 10 $\rightarrow$ 1m 10s)
- creato file per scaricare da globus i cataloghi di aloni necessari per l'analisi ("downloader-prova.py")