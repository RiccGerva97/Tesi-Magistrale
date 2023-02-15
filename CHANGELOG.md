# CHANGELOG

### 02/15
Modificato il file per il download da Globus:
- errori nei path per l'indirizzo della cartella locale (c'erano alcune "//")
- errore con Globus: modificato il file 'accessPaths.tcl' per permettere alla cartella di destinazione i diritti di lettura/scrittura (vedi [qui](https://docs.globus.org/how-to/globus-connect-personal-linux/#config-paths))
    <a href="https://docs.globus.org/how-to/globus-connect-personal-linux/#config-paths" target="_blank">qui</a>

- aggiunta documentazione per "downloader-prova.py"
- modificato nome "downloader-prova.py" $\rightarrow$ "downloader-globus.py"


### 01/27
#### Primo aggiornamento di changelog 
Ad oggi creati:
- notebook per analisi di distribuzione di DM da simulazioni Quijote
- notebook per analisi di cataloghi di aloni sempre da simulazioni Quijote
- funzione per costruire matrici densità da cataloghi di aloni con metodo CIC, conrelativo test
- funzione per calcolare direttamente i coefficienti di scattering da cataloghi di aloni
- creato branch "multithread" per prove di multithreading su funzione myCIC
- ottimizzata funzione myCIC (3m 10 $\rightarrow$ 1m 10s)
- creato file per scaricare da globus i cataloghi di aloni necessari per l'analisi