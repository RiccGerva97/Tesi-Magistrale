# Tesi Magistrale: Matrici di Fisher tramite Scattering Transform
###### di Gervasoni Riccardo

La tesi ha come obbittivo il calcolo di informazione portato dai coefficienti di scattering ottenuti tramite Wavelet Scattering Transform, un innovativo metodo statistico inizialmente usato in ambito di trasmissione dati che sta diffondendosi nel tempo anche ad altre discipline che studiano la distribuzione di grandi dati (p.e. chimica fisica).

Il primo passo è stato utilizzare le simulazioni n-body di Quijote:
- usare la libreria 'kymatio' su una semplice distribuzione di densità di materia oscura -> Try;
- usare la libreria 'kymatio' su distribuzioni di aloni, ottenue dalle pprecedenti tramite metodo FoF;
    * è stato necessario creare un algoritmo Cloud In a Cell per generare una matrice densità da una serie di punti .discreti

## Cartelle

### MyFunc
Contiene librerie create per facilitare i calcoli nei notebook jupyter.
- CalcWST: funzione che ritorna i coefficienti di scattering dando una matrice densità;
- downloader-globus: script in python per scaricare da Globus le simulazioni di aloni;
- myCIC [...]: contiene vari algoritmi per provare il multithreading;
- Try_pickle: cartella con relativi file per proivare la libreria pickle.

### Try_01-density field
Contiene prove per la manipolazione dati delle simulaizoni di materia oscura.

### Try_02-HaloCatalogue
Contine notebook per l'analisi dati di un catalogo di aloni e un altro per testare l'iterazione su più file.