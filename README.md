# Zefiro Autopilot — partire con ROS 2

Questa repo contiene una demo didattica **ROS 2 Jazzy / Python** per imparare a costruire una pipeline di autonomia. Funziona sul portatile, con dati finti e un logger: non comanda un drone.

```text
distanza frontale finta ─┐
                        ├─ avoidance ─ velocità filtrata + stato ─ logger
velocità desiderata ─────┘
```

## Parti da qui

1. [Primo giorno: concetti, avvio ed esercizi](zefiro_autonomy/docs/primi_passi.md).
2. [Piano per cinque persone](zefiro_autonomy/docs/task_plan.md): prime PR, file, reviewer e risultati attesi.
3. [Contratti e architettura](zefiro_autonomy/docs/architecture.md).
4. [Come contribuire](zefiro_autonomy/docs/contribution_workflow.md).

## Avvio su Ubuntu 24.04

Installa ROS seguendo [la guida](zefiro_autonomy/docs/INSTALL_ROS2_JAZZY.md). Poi, **dalla radice di questa repo**:

```bash
bash scripts/doctor.sh
bash scripts/check.sh
bash scripts/demo.sh
```

La demo ripete un ciclo di 24 secondi: `CLEAR → SLOWDOWN → STOP → INVALID_INPUT`.
Chiudila con Ctrl+C. Per verificarla automaticamente:

```bash
python3 scripts/smoke_demo.py
```

Il test dura circa 27 secondi. Build, installazione e log vengono prodotti solo nelle cartelle `build/`, `install/`, `log/` della radice e non vanno in Git.

## Alternativa Docker

Richiede Docker Engine e Compose v2. Il percorso Docker viene controllato dalla CI; vedi i limiti della verifica locale nell'[audit](zefiro_autonomy/docs/audit.md).

```bash
docker compose build
docker compose run --rm --name zefiro-dev autonomy
# Dentro il container, dalla cartella /workspace/autopilot:
bash scripts/check.sh
bash scripts/demo.sh
```

Per un secondo terminale nello **stesso container**:

```bash
docker exec -it zefiro-dev bash
source scripts/ros_env.sh
source install/local_setup.bash
ros2 topic echo /zefiro/safety/state
```

I sorgenti sono condivisi con l'editor dell'host; build/install/log usano volumi Docker separati. Non lanciare un altro `compose run` per osservare la demo: la discovery è limitata al singolo container.

## Mappa della repo

| Percorso | Contenuto |
| --- | --- |
| `zefiro_autonomy/src/zefiro_demo/zefiro_demo/` | Nodi Python e logica di avoidance |
| `zefiro_autonomy/src/zefiro_demo/config/demo.yaml` | Parametri della demo |
| `zefiro_autonomy/src/zefiro_demo/launch/` | Avvio dei quattro nodi |
| `zefiro_autonomy/src/zefiro_demo/test/` | Test della logica e del collegamento ROS |
| `scripts/` | Diagnostica, build, test e demo |
| `zefiro_autonomy/docs/` | Guide e piano di lavoro |

Altre guide: [problemi frequenti](zefiro_autonomy/docs/troubleshooting.md), [registrazione e replay](zefiro_autonomy/docs/observability.md), [audit e verifiche](zefiro_autonomy/docs/audit.md).

La directory del progetto si chiama **Autopilot** con A maiuscola. Il vecchio percorso locale `zefiro/autopilot` è un'altra cartella e non è questa repo.
