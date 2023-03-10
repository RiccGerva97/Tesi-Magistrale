# Sul calcolo delle matrici di Fisher

Ora devo stimare le derivate per calcolare la matrice di Fisher
ogni elemento della matrice di F. ha fissi i parametri cosmologici e somma su
tutte le possibili diverse permutazioni dei coeff WST.
Come devo però trattare le derivate? Le varie cosmologie disponibili hanno tutte
almeno un parametro cosmologico che devia da quella fiduciale o in eccesso o in
difetto.

## IDEA:
calcolo i rapporti incrementali di tutte le cosmologie non fiduciali con
quella fiduciale e poi ne faccio la media, perché utilizzo la matrice di
covarianza della fiduciale e sono interessato ai costrains sui parametri
cosmologici della stessa.

## OSS:
quando faccio la media, devo dividere per il numero totale di rapporti
incrementali che calcolo o solo quelli che mi danno un effettivo valore (ossia
quelli che hanno parametri cosmologici diversi)?

## DOMANDA:
a questo punto non potrei fare diretamente il rapporto incrementale
tra le cosmologie che hanno il parametro cosmologico in considerazione una
aumentato e l'altra diminuito (sempre rispetto alla fiduciale)

## NOVITA':
i ricercatori Quijote per calcolare le derivate di un parametro fanno:
d/dx S_i = (S_i(x+dx)-S_i(x-dx)) / 2dx
quindi poteri pensare di valutare le deirvate facendo le differenze tra 
cosmologie _p e _m (dei coefficienti e dei parametri)
Conviene calcolare già gli step o utilizzare le percentuali come da paper?

> NOTA: essendoci 4 variazioni sulla densità di barioni, considero solo le coppie 
(+, -) e (++, --) o posso/conviene calcolare anche le altre (aggiustanto la formula),
che sono (++, -), (+, --), (++, +), (-, --)?
Sono sensate solo quelle che hanno i termini fiduciali all'interno? E basterebbe
aggiustare o bisogna aggingere dei possibili pesi?

</br>

In quasi tutte le cosmologie ci sono tre tipologie di realizzazioni:
- standard -> 500
- fisse -> 250
- fisse accoppiate -> 250
cioè dipende come vengono generati (aka con quale distribuzione vengono calcolati) i
parametri iniziali delle simulazioni.
Il sig. Navarro ci informa che possono essere utulizzate tutte e 1000 solo per il
computo delle derivate, mentre per quello della matrice di covarianza solo quelle standard.

Ora ho due strade:
- a) usare 350/500 standard e basta;
- b) usare standard e fisse (/accoppiate) -> quante? Perché l'importante è usarne >= 350 standard
    per avere una matrice di covar.sufficientemente bendefinita

Problema:
- 1) "Ob_" ha solo realizzazioni non standard -> posso supperire con "Ob2_"
- 2) "w_" ha solo realizzazioni standard

Come posso mettere insieme a), b) e 1), 2)?
La facile soluzione sarebbe calcolare il tutto solo con realizzazioni standard e non usare
le cosmologie varianti "Ob_".

SOLUZIONE PIU' ARTICOLATA
Si potrebbe invece pensare di calcolare la matrice di covarianza con le realizzazioni standard,
le derivate anche con quelle fisse.
Bisogna però:
- pensare a come (e se si deve) riportare che le derivare -> Fisher per cosmologie "w_"
hanno una precisione minore;
- come "unire" le derivate fatte su variazione di Omega_b (perché è quella con ++, +, -, --) 
