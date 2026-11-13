# Audit della repo e preparazione del team

Audit locale iniziato il 12 novembre 2026, completamento delle verifiche il 13 novembre 2026.

## Identificazione

- Repo: `git@github.com:ZEFIRO-PoliTo/Autopilot.git`.
- Checkout: `/home/evang/projects/zefiro/Autopilot`.
- Baseline osservata: `f86a6bb`, branch `main`, working tree inizialmente pulito.
- Branch di lavoro: `chore/ros-team-onboarding`.
- La cartella sorella `zefiro/autopilot` è materiale separato, non il checkout Git individuato.
- Il firmware in `projects/PX4-Autopilot` non è il pacchetto ROS didattico cercato.
- L'audit riguarda il checkout locale; sincronizzazione remota e impostazioni GitHub non sono state verificate.

## Problemi e correzioni

| Priorità | Evidenza nella baseline | Correzione |
| --- | --- | --- |
| Alta | 107 file generati in build/install/log annidati erano versionati, comprese copie Python e percorsi della macchina | Rimossi dall'indice mantenendo le copie locali; CI controlla che non rientrino; un solo workspace alla radice |
| Alta | Solo test di import | Test delle decisioni, dei limiti e degli input invalidi; test ROS con publisher/subscriber reali; smoke del launch |
| Alta | Clearance NaN non veniva rifiutata; goal non finito poteva interagire male con il clamp | Validazione esplicita dei numeri e arresto con INVALID_INPUT |
| Alta | Ultimo goal restava valido indefinitamente | Watchdog del goal, stato GOAL_TIMEOUT e test di recupero |
| Alta | Saturazione dopo rallentamento: goal molto alto annullava la riduzione attesa | Saturazione prima della scala; caso 2 m / 100 m/s → 0.75 m/s |
| Media | Parametri senza validazione, possibili divisioni per zero; cambi live non recepiti dalla logica | Configurazione validata e parametri di solo avvio, YAML installato |
| Media | Timestamp ROS usato per freschezza | Ricezione monotona e timer steady, test con clock simulato fermo |
| Media | Assi extra e frame del goal ignorati | Contratto forward-only esplicito e rifiuto degli input fuori contratto |
| Media | Docker con bind mount dell'intero workspace e fallback all'install annidata | Volumi separati per artefatti, avvio esplicito e immagine ROS base ufficiale; test Docker in CI |
| Media | Piano avanzato T0–T9 senza percorso comune per principianti | Guida italiana, esercizi riproducibili, cinque aree con prima PR e reviewer |
| Media | Installazione e diagnosi incomplete per il team | Dipendenze da manifest, script comuni, guida a domini e replay |

## Validazione

Verifiche eseguite su Ubuntu 24.04, Python 3.12 e ROS 2 Jazzy:

| Prova | Esito |
| --- | --- |
| Build del workspace locale | PASS |
| Suite pytest attraverso colcon | 45 test, 0 errori, 0 fallimenti, 0 skip |
| Copia pulita dei soli file sorgente, senza build/install/log precedenti | PASS: `/tmp/zefiro-onboarding-sx54pdpq` |
| `bash scripts/doctor.sh` e `bash scripts/check.sh` nella copia pulita | PASS, stessi 45 test |
| `python3 scripts/smoke_demo.py` nella copia pulita | PASS: quattro stati/velocità attesi e chiusura pulita di tutti e quattro i nodi |
| Sintassi Python/shell/YAML e collegamenti Markdown locali | PASS |
| Artefatti generati ancora nell'indice Git | 0 |
| Docker e GitHub Actions | NON ESEGUITI localmente/remotamente |

Per la verifica locale sono stati anteposti `/usr/bin` e i pacchetti APT Python; il pytest globale 9.2 non era compatibile con il plugin ROS installato. Procedura in [troubleshooting.md](troubleshooting.md). Rimane un warning locale setuptools su metadati `pytest-repeat`; non ha causato test saltati o falliti. Non sono stati modificati i pacchetti di sistema.

Il primo smoke ha rilevato un doppio SIGINT nel test stesso: corretto inviando il segnale al solo processo launch, che gestisce i figli. La prova successiva verifica anche la chiusura pulita.

I test della demo non attestano idoneità al volo.

## Limiti e lavoro residuo del gruppo

- La demo resta 1D senza camera, PX4, simulatore fisico, frenata dinamica o watchdog esterno.
- Installazione da zero dei pacchetti APT non ripetuta: sulla macchina è già presente Jazzy.
- Docker non è installato su questa macchina: build e runtime Docker non verificati localmente; il workflow include un job dedicato da eseguire su GitHub.
- Nessun push, issue, PR o modifica alle protezioni GitHub eseguita durante l'audit locale.
- Nomi e account delle cinque persone non forniti: assegnazioni P1–P5 da compilare nel kickoff.
- I contratti camera e PX4 restano attività successive da validare su versioni e hardware effettivi.

Immagine Docker verificata nel [catalogo ufficiale](https://github.com/docker-library/official-images/blob/master/library/ros): `ros:jazzy-ros-base`.

Fonti ROS consultate: [installazione Jazzy](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst), [ambiente](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.rst), [colcon](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.rst).
