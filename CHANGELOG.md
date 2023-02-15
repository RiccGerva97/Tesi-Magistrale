# CHANGELOG

### 02/15
Modificato il file per il download da Globus:
- errori nei path per l'indirizzo della cartella locale (c'erano alcune "//")
- errore con Globus: modificato il file 'accessPaths.tcl' per permettere alla cartella di destinazione i diritti di lettura/scrittura (vedi [qui](https://docs.globus.org/how-to/globus-connect-personal-linux/#config-paths))
- aggiunta documentazione per "downloader-prova.py"
- modificato nome "downloader-prova.py" $\rightarrow$ "downloader-globus.py"
- creata cartella con relativo file per testare la libreria 'pickle'
- creato file per calcolare i coefficienti di scattering per una cosmologia (estendibile a più) ("calc_WST_halo.py")
- migliorati indirizzi cartelle nei file per uso generico per pull da GitHub


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