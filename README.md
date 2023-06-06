# Tesi Magistrale: Matrici di Fisher tramite Scattering Transform

###### di Gervasoni Riccardo

</br>

La tesi ha come obbittivo il calcolo di informazione portato dai coefficienti di scattering ottenuti tramite Wavelet Scattering Transform, un innovativo metodo statistico inizialmente usato in ambito di trasmissione dati che sta diffondendosi nel tempo anche ad altre discipline che studiano la distribuzione di grandi dati (p.e. chimica fisica).

Il primo passo è stato utilizzare le simulazioni n-body di Quijote:

- usare la libreria `kymatio` su una semplice distribuzione di densità di materia oscura -> Try;
- usare la libreria `kymatio` su distribuzioni di aloni, ottenue dalle pprecedenti tramite metodo FoF;
  - è stato necessario creare un algoritmo Cloud In a Cell per generare una matrice densità da una serie di punti discreti;
    - alla fine uso metodo di MAS_library che una Chyton, estremamente più veloce;
- creare funzioni per calcolare le matrici di Fisher dai coefficienti di scattering.

</br>

## Utilizzo

Per poter calcolare i coefficientidi scattering è necessario modificare la variabile `root` (nella funzione `CALCULUS`, in `calc_WST_halos.py`) per indicare la posizione della cartella contenente i file degli aloni (e.g. fino a .../Halos/FoF); assicurarsi inoltre di aver selezionato il redshift (`snapnum`) desiderato.
Avviare lo script da line di comando; ci sono le seguenti opzioni:

- ```$ python ./calc_WST_halos.py``` avvia il programma con i parametri di default (vedi sotto per i valori di default);
- ```$ python ./calc_WST_halos.py -h``` dà informazioni per come passare gli argomenti opzionali modificabili:
  - ```-o <one file>```: scrive i risultati su un file se `True`, su due se `False` (default. True);
  - ```-g <cell density grid>```: modifica il numero di celle per lato della matrice densità (default: 256);
  - ```-w <cell WST coeff>```: modifica il numero di celle per lato della griglia per il calcolo dei coefficienti di scattering (default: 256);
  - ```-r <realizations>```: modifica il numero di realizzazoni sucui calcolare i coefficienti di scattering  (default: 350);
  - ```-F <folder1 folder2 ...>```: modifica le cosmologie su cui calcolare i coefficienti di scattering, ```ALL``` dà da eseguire tutte le cosmologie (default: fiducial);
  - ```-v <verbose opt>```: metodo esteso che chiede uno alla volta i valori precedenti, "Invio" dà il valore di default.

### Output

I file di output contenti i coefficienti WST saranno contenuti in una cartella nella directory principale, chiamata `WST-files` e avranno la seguente struttura:

'nome cosmologia' _ coefficients _ 'celle per lato della griglia' _ 'celle per lato per i coeff. WST' _ 'numero realizzazioni' . wst"

Esempio: fiducial_coefficients_256_512_1000.wst

- 'fiducial' -> cosmologia fiduciale;
- 256 -> griglia di densità con 256 celle per lato;
- 512 -> griglia per calcolo coefficienti WST con 512 celle per lato;
- 1000 -> numero di realizzazioni di cui sono stati calcolati  icoefficienti.

</br>

## Cartelle

### Principale

Contiene:

- i file in output contenenti i coefficienti di scattering, divisi per cosomologia e ordine;
- `calc_WST_halos.py`: calcola i coefficienti di scattering partendo da cataloghi di aloni (usando nel mentre un algoritmo CiC);
- `README`, `CHANGELOG` e `profileroutput.out`; file di "servizio".

### MyFunc

Contiene librerie create per facilitare i calcoli nei notebook jupyter.

- `CalcWST`: funzione che ritorna i coefficienti di scattering dando una matrice densità;
- `downloader-globus`: script in python per scaricare da Globus le simulazioni di aloni;
- `Fisher`: contiene funzioni per calcolare la matrice di Fischer e un vettore contenente gli errori minimi sui parametri cosmologici dai coefficienti di scattering;
- `myCIC` [...]: contiene vari algoritmi per provare il multithreading;
- `Try_pickle`: cartella con relativi file per proivare la libreria pickle.

### Try_01-density field

Contiene prove per la manipolazione dati delle simulaizoni di materia oscura.

### Try_02-HaloCatalogue

Contine notebook per l'analisi dati di un catalogo di aloni e un altro per testare l'iterazione su più file.

### WST-files

Contiene i file su cui sono scritti i coefficienti WST, per maggiori informazioni vedi [qui](#output).
