# Piano di avvio per cinque persone

Questo è il piano operativo. Assegnate i nomi a P1–P5 nel kickoff; sono ruoli, non livelli di esperienza. Prima tutti completano [primi_passi.md](primi_passi.md).

La baseline include già build, test, quattro nodi, configurazione YAML e watchdog. La prima settimana serve a comprenderla e aggiungere piccole estensioni. Non dividiamo subito il codice in cinque pacchetti: le aree sono già separabili per file.

## Assegnazioni e prima PR

I percorsi di codice nella tabella sono relativi a `zefiro_autonomy/src/zefiro_demo/`.

| Persona | Responsabilità | File principali | Prima PR, verificabile | Reviewer |
| --- | --- | --- | --- | --- |
| P1 | Missione: cosa si vuole fare | `zefiro_demo/fake_goal_velocity_node.py`, nuovo `test/test_goal_source.py` | Parametro di avvio `goal_vx_mps`, default 1.0; test che 0.4 produca richieste a 0.4; rifiutare negativi/NaN/Inf | P3 |
| P2 | Percezione sintetica: cosa si osserva | `zefiro_demo/fake_front_clearance_node.py`, nuovo `test/test_clearance_source.py` | Modalità di distanza costante parametrica, mantenendo il ciclo attuale come default; a 2.0 m la pipeline rallenta | P1 |
| P3 | Decisione e robustezza | `zefiro_demo/avoidance_core.py`, `test/test_avoidance_core.py` | Test con configurazione non predefinita: stop=1.5, slowdown=3.0, clearance=2.0, goal=1.0 → 1/3 m/s; documentare precedenza stati e limiti in una nota di test | P4 |
| P4 | Consumatore dell'uscita, mock | nuovo `zefiro_demo/output_mock_node.py`, nuovo `test/test_output_mock.py` | Nodo che legge solo `/zefiro/setpoint/velocity` e segnala comando ricevuto / assente / scaduto; test della perdita del publisher; nessun invio a PX4 | P2 |
| P5 | Integrazione, launch, riproducibilità | `launch/`, `config/`, `setup.py`, `package.xml`, `scripts/`, guide | Launch di esercizio con input attivabili/disattivabili; mantenere il launch base; istruzioni e prova di timeout senza modificare sorgenti | P1 + referente dell'area modificata |

Le prime PR sono piccole: un comportamento, un test pertinente, un esempio d'uso. Non assegnare a una sola persona tutta la documentazione: ogni autore aggiorna la propria parte.

## Contratti condivisi

- Nomi e tipi dei topic restano quelli di [architecture.md](architecture.md).
- Velocità in m/s, distanza in metri, frame `base_link`, solo asse x positivo.
- `Float32` negativo o non finito significa input invalido.
- La mancanza di sensore o missione genera rispettivamente `SENSOR_TIMEOUT` o `GOAL_TIMEOUT`.
- Il mock legge l'uscita filtrata; non legge il goal come comando da eseguire.
- I parametri si validano prima di creare timer: frequenze positive, numeri finiti.
- Ogni nodo nuovo deve avere arresto pulito e un test significativo.

P5 integra modifiche a `setup.py`, `package.xml` e launch condivisi dopo aver concordato nome dell'eseguibile e parametri con l'autore. Gli altri possono proporre tali modifiche nella propria PR, ma vanno integrate una alla volta per evitare conflitti.

## Sequenza suggerita: cinque sessioni

| Sessione | Tutti | Risultato |
| --- | --- | --- |
| 1 | Installazione, demo, ispezione topic, timeout manuali | Ognuno esegue la baseline sul proprio ambiente |
| 2 | Lettura del codice, assegnazione P1–P5, branch e prima PR | Cinque PR piccole con input/output atteso |
| 3 | Review incrociata e correzioni | Ciascuno sa leggere anche un'area diversa dalla propria |
| 4 | Integrazione progressiva P1 → P2 → P3 → P4 → P5 | Test verdi dopo ogni merge, demo standard ancora valida |
| 5 | Demo di gruppo e replay, registrazione dei limiti | Checklist compilata e prossime attività scelte |

I ruoli ruotano al ciclo successivo. Chi finisce prima aiuta il reviewer o riproduce una PR su un clone pulito.

## Seconda attività per area

- **P1:** scenari di velocità desiderata, compreso goal zero e interruzione del publisher; mantenere recupero automatico.
- **P2:** sequenza configurabile e pausa pubblicazione per simulare un guasto; test della durata delle fasi. I dati sintetici restano utilizzabili senza camera.
- **P3:** proposta e test per isteresi vicino alle soglie. Definire prima input/output; qualsiasi modifica al comportamento di arresto richiede review dell'intero gruppo.
- **P4:** contratto PX4 in bozza: frame, timestamp, frequenza, watchdog del ricevitore, differenze tra ROS e PX4. Non implementare arm/disarm né conversioni non validate.
- **P5:** matrice di scenari, registrazione/replay e report di integrazione seguendo [observability.md](observability.md).

## Checklist della prima integrazione

- [ ] Cinque ambienti hanno completato la guida e riportato OS, percorso nativo/Docker e risultato.
- [ ] `bash scripts/check.sh` e `python3 scripts/smoke_demo.py` passano.
- [ ] Distanza 5 / 2 / 0.7 / -1 produce CLEAR / SLOWDOWN / STOP / INVALID_INPUT.
- [ ] Stop del sensore e del goal arrestano l'uscita; ripresa degli input recupera.
- [ ] Il mock riceve il setpoint e rileva quando avoidance scompare.
- [ ] Un altro membro riproduce il caso usando solo comandi scritti.
- [ ] Nessun dato generato, credenziale o bag è aggiunto a Git.
- [ ] Le limitazioni sono riportate nella PR, non solo in chat.

## Dopo il primo ciclo: backlog di simulazione

Il piano precedente usava T0–T9. I riferimenti restano utili: T0 setup, T1 bringup/pacchetti, T2 percezione sintetica, T3 camera/replay, T4 avoidance, T5 output mock/PX4, T6 scenari, T7 osservabilità, T8 CI, T9 integrazione.

T0/T8 e parte di T4/T6 sono già preparati nella baseline, ma vanno provati dai nuovi membri. T1/T3/T5/T9 non sono dichiarati completati.

La camera citata nel piano precedente è **Orbbec Gemini 336L**: prima di implementarla confermare dispositivo disponibile, versione del driver, topic effettivi, encoding, unità, frame e calibrazione. Le vecchie ipotesi su range e default non costituiscono misure validate.

PX4/SITL viene dopo una pipeline sintetica riproducibile e un mock con watchdog. Servono prove separate dei frame, dei failsafe e dei limiti dell'hardware. La demo attuale non è un controllore di volo.
