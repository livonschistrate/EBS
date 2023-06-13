# EBS Homework

O arhitectura de sistem publish/subscribe, content-based, care sa fie capabila sa proceseze si secvente de publicatii grupate in ferestre, structurata in felul urmator:

Generati un flux de publicatii care sa fie emis de un nod publisher. Publicatiile pot fi generate cu valori aleatoare pentru campuri folosind generatorul de date din tema practica. (5 puncte)
Implementati o retea (overlay) de brokeri (2-3) care sa notifice clienti (subscriberi) in functie de o filtrare bazata pe continutul publicatiilor, cu posibilitatea de a procesa inclusiv ferestre (secvente) de publicatii (exemplu mai jos). (10 puncte)
Simulati 3 noduri subscriber care se conecteaza la reteaua de brokeri si pot inregistra atat susbcriptii simple cat si subscriptii complexe ce necesita o filtrare pe fereastra de publicatii. Subscriptiile pot fi generate cu valori aleatoare pentru campuri folosind generatorul de date din tema practica, modificat pentru a genera si subscriptii pentru ferestre de publicatii (exemplu mai jos). (5 puncte)
Folositi un mecanism de serializare binara (exemplu - Google Protocol Buffers sau Thrift) pentru transmiterea publicatiilor de la nodul publisher la brokers. (5 puncte)
Realizati o evaluare a sistemului, masurand pentru inregistrarea a 10000 de subscriptii simple, urmatoarele statistici: a) cate publicatii se livreaza cu succes prin reteaua de brokeri intr-un interval continuu de feed de 3 minute, b) latenta medie de livrare a unei publicatii (timpul de la emitere pana la primire) pentru publicatiile trimise in acelasi interval, c) rata de potrivire (matching) pentru cazul in care subscriptiile generate contin pe unul dintre campuri doar operator de egalitate (100%) comparata cu situatia in care frecventa operatorului de egalitate pe campul respectiv este aproximativ un sfert (25%). Redactati un scurt raport de evaluare a solutiei. (10 puncte)

# Results

## Tests 
For 1000 publications and subscriptions, the broker takes almost 60 seconds to process the registered subscriptions and match the publications, while the subscriber sends the subscriptions and waits until he receives a response about the filtered publications.

## Commands

        To generate a specific number of pubs/subs:
        py publish.py -n 500
        py subscribe.py -n 500

        To generate pubs/subs with a single thread:
        py parallelworks.py -t 1 -s p -n 100000
        py parallelworks.py -t 1 -s s -n 100000

        To generate only pubs/only subs/both with multiple threads:
        py parallelworks.py -t 5 -s p -n 100000
        py parallelworks.py -t 5 -s s -n 100000
        py parallelworks.py -t 5 -s b -n 100000
