# Progetto per il corso di Data Protection & Privacy
#### Prof. Alessio Merlo, Unige
Il progetto si pone come obiettivo l'anonimizzazione di **dati transazionali**.

Il database di riferimento è reperibile liberamente a questo [link](http://www.philippe-fournier-viger.com/spmf/index.php?link=datasets.php).
Nello specifico, sono stati utilizzati i dataset: 
* [BMSWebView1 (Gazelle) ( KDD CUP 2000)](http://www.philippe-fournier-viger.com/spmf/datasets/BMS1_spmf)
* [BMSWebView2 (Gazelle) ( KDD CUP 2000)](http://www.philippe-fournier-viger.com/spmf/datasets/BMS2.txt)

### Funzionamento:
All'interno del progetto sono presenti tre main: main.py, main_test.py e main_testRCM.py. Il primo prevede un utilizzo più lineare dell'algoritmo, ovvero dato un singolo grado di privacy desiderabile esegue il CAHD e al termine stampa il tempo di esecuzione e la KL-divergence. Con il secondo è possibile eseguire più iterazioni sullo stesso dataset ma con gradi di privacy differenti, al fine di poter confrontare le prestazioni dell'algoritmo stesso. Al termine verrà visualizzato un grafico in cui in ascissa è presente il tempo di esecuzione mentre nell'ordinata il grado di Privacy. Con il terzo main è possibile verificare la differenza prestazionale in termini di tempo d'esecuzione d KL-divergence utilizzando o meno l'algoritmo RCM all'interno del CAHD.
