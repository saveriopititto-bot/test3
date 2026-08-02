# Dashboard per ETF e Commodities Agricole

Una dashboard moderna, scalabile e rigorosamente tipizzata sviluppata in Python con Streamlit per l'analisi di ETF e commodities agricole. 
Questo progetto è strutturato seguendo i principi della **Clean Architecture**, assicurando una chiara separazione delle responsabilità tra il livello di acquisizione dati/logica di calcolo (Business Logic) e il livello di presentazione (UI).

## Struttura delle Directory

```text
.
├── app.py                  # Entry point dell'applicazione (orchestratore)
├── engine/                 # Livello di Business Logic
│   ├── config.py           # Costanti e dizionari di configurazione
│   └── data_fetcher.py     # Logica di acquisizione dati (yfinance) e calcoli DataFrame
├── ui/                     # Livello di Presentazione (User Interface)
│   ├── charts.py           # Generazione dei grafici con Plotly Express/Graph Objects
│   ├── style.css           # Framework CSS Milligram e palette personalizzata
│   └── views.py            # Componenti layout di Streamlit (Tabs, Sidebar)
├── requirements.txt        # Dipendenze di progetto
└── README.md               # Documentazione
```

## Architettura e Clean Code
Il progetto applica le seguenti regole di design:
1. **Separation of Concerns**: Il modulo `engine` non contiene alcuna dipendenza da `streamlit` e si occupa unicamente della manipolazione dati. La UI si limita ad eseguire il rendering dei dati ricevuti.
2. **Type Hints Strict**: Ogni funzione utilizza `Type Hints` di Python (`Callable`, `Dict`, `pd.DataFrame`) migliorando la leggibilità e riducendo bug.
3. **Funzioni Pure**: Vengono privilegiate funzioni stateless nella elaborazione dati per facilitare unit testing futuri.
4. **Stile Milligram**: L'app inietta programmaticamente la libreria CSS Milligram sovrascrivendo la palette con i toni personalizzati del **Blu Petrolio (HEX #035158)**.

## Installazione ed Esecuzione

### Prerequisiti
- Python 3.9 o superiore

### Setup Ambiente Locale
1. Clona il repository o spostati nella cartella del progetto.
2. (Opzionale ma consigliato) Crea un virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   ```
3. Installa le librerie richieste:
   ```bash
   pip install -r requirements.txt
   ```
4. Avvia l'applicazione Streamlit:
   ```bash
   streamlit run app.py
   ```

## Sviluppi Futuri (Roadmap)

- [ ] **Database Relazionale**: Integrazione di un database PostgreSQL tramite container Docker per storicizzare le serie storiche evitando chiamate API ripetute.
- [ ] **Migrazioni DB**: Sviluppo di un sistema di migrazioni (es. Alembic) per la gestione dello schema del database.
- [ ] **Nuovi Indicatori**: Integrazione di API esterne aggiuntive (es. FRED) per correlazioni con dati di macroeconomia.
- [ ] **Gestione State Avanzata**: Sfruttare appieno la gestione avanzata dello State tramite `st.session_state` per mantenere preferenze utente complesse e caching tra sessioni.
