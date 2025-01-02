# ICON Course Project 2024/2025

## Introduzione
Questo repository raccoglie il progetto realizzato per il corso di ICON 2024/2025, tenuto dal Professore **Nicola Fanizzi** presso l'Università degli Studi di Bari Aldo Moro.

L'obiettivo principale è dimostrare le conoscenze acquisite durante il corso attraverso un'analisi dettagliata e applicazioni pratiche su un dataset tratto dal videogioco online competitivo **Valorant**.

[Valorant](https://it.wikipedia.org/wiki/Valorant) è un videogioco multiplayer FPS (First-Person Shooter) dove due squadre da cinque giocatori si affrontano in due tempi da 12 round ciascuno, alternandosi tra le fasi di attacco e difesa. Ogni giocatore sceglie un personaggio, chiamato "agente", con abilità uniche e un arsenale di armi a disposizione.

---

## Struttura del Progetto
```plaintext
C:.
├───bayes                # Ragionamento probabilistico
├───datasets            # Dataset pre e post processing
├───displayers          # Funzioni per visualizzare i risultati
├───img
│   ├───ANN            # Reti neurali artificiali
│   ├───DT             # Decision tree
│   ├───LR             # Logistic regression
│   ├───RF             # Random forest
│   ├───SVM            # Support vector machine
│   └───_general       # Immagini generali del progetto
├───pre_processing      # Funzioni per il preprocessing
├───prolog              # Rappresentazione relazionale
│   └───pl_files       # File .pl (Prolog)
└───supervised_training # Apprendimento supervisionato
```
---

## Setup del Progetto

1. Clona il repository:
   ```bash
   git clone https://github.com/<tuo-username>/icon-course-project.git
   ```

2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Esegui gli script:
   - Per preprocessing: `python pre_processing/main.py`
   - Per il training: `python supervised_training/main.py`
   - per l'apprendimento della struttura `python bayes/bayes.py`
   - per prolog `python prolog/prolog_dialog.py`

---

## Contributi
Contributi sono benvenuti! Sentiti libero di aprire una [issue](https://github.com/<tuo-username>/icon-course-project/issues) o una pull request.

---

## Licenza
Questo progetto è distribuito sotto la licenza MIT. Consulta il file [LICENSE](LICENSE) per maggiori dettagli.

---

## Crediti
Progetto sviluppato da **[Porcelli andrea]**, Università degli Studi di Bari Aldo Moro.
