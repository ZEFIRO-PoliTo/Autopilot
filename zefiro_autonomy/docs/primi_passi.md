# Primo giorno: capire ed eseguire la demo

Obiettivo: ciascuna delle cinque persone avvia la demo, legge un topic, interrompe un input e spiega perché il comando si ferma. Riservate una sessione comune di 90–120 minuti; l'installazione può richiedere tempo aggiuntivo.

## 1. Sei concetti da conoscere

| Concetto | Significato | Esempio in questa repo |
| --- | --- | --- |
| Nodo | Programma ROS con una responsabilità | `avoidance_node` |
| Topic | Canale nominato su cui viaggiano messaggi | `/zefiro/safety/state` |
| Messaggio | Struttura e tipo dei dati inviati | `Float32` contiene `data` |
| Publisher / subscriber | Chi invia / chi riceve su un topic | Il sensore finto pubblica, avoidance riceve |
| Pacchetto | Unità di codice e dipendenze installabile da ROS | `zefiro_demo` |
| Launch | File che avvia più nodi e passa configurazione | `demo_fake_avoidance.launch.py` |

`colcon build` prepara il pacchetto. `source` rende disponibile ROS o il pacchetto nella shell corrente. Un **parametro** configura un nodo; non è un flusso di messaggi. Un **callback** è la funzione chiamata quando arriva un messaggio o scade un timer.

## 2. Ottenere il progetto

Serve accesso alla repo GitHub dell'organizzazione. Se clone/push restituisce 403, fate aggiungere il vostro account da chi gestisce la repo.

```bash
git clone https://github.com/ZEFIRO-PoliTo/Autopilot.git
cd Autopilot
```

Queste istruzioni presuppongono che il branch di onboarding sia stato condiviso e integrato; per provarlo prima del merge, dopo il push del responsabile usate `git switch chore/ros-team-onboarding`.

Installate ROS con [INSTALL_ROS2_JAZZY.md](INSTALL_ROS2_JAZZY.md), oppure usate il container descritto nel [README](../../README.md). Tutti i comandi seguenti partono dalla radice `Autopilot/`.

## 3. Compilare e vedere la pipeline

Terminale A:

```bash
bash scripts/doctor.sh
bash scripts/check.sh
bash scripts/demo.sh
```

Aspettate un ciclo completo:

| Tempo indicativo | Distanza | Stato | Velocità in uscita |
| --- | --- | --- | --- |
| 0–8 s | 5 m | CLEAR | 1 m/s |
| 8–14 s | 2 m | SLOWDOWN | 0.5 m/s |
| 14–20 s | 0.7 m | STOP | 0 m/s |
| 20–24 s | -1 (dato invalido) | INVALID_INPUT | 0 m/s |

All'avvio può comparire un timeout finché non arrivano entrambi gli input. Il logger campiona una volta al secondo: non è un registro atomico di tutti i topic.

## 4. Ispezionare il grafo

Terminale B, nella stessa repo (oppure `docker exec` nello stesso container):

```bash
source scripts/ros_env.sh
source install/local_setup.bash
ros2 node list
ros2 node info /avoidance_node
ros2 topic list
ros2 topic info /zefiro/setpoint/velocity --verbose
ros2 interface show geometry_msgs/msg/TwistStamped
ros2 topic echo /zefiro/safety/state
```

Ctrl+C termina solo `echo`. Poi:

```bash
ros2 topic hz /zefiro/setpoint/velocity
ros2 param get /avoidance_node stop_distance_m
```

Atteso: quattro nodi applicativi, i quattro topic descritti in [architecture.md](architecture.md), uscita intorno a 20 Hz e soglia 1.0. ROS può mostrare anche `/rosout`, `/parameter_events` e nodi di servizio.

Tutti i terminali dello stesso esercizio devono usare lo stesso `ROS_DOMAIN_ID`. Gli script scelgono 41 e discovery locale. Per lavorare in cinque assegnate 41, 42, 43, 44, 45 e impostate il valore **prima** di avviare qualsiasi comando, uguale in ogni terminale della persona:

```bash
export ROS_DOMAIN_ID=42
```

## 5. Interrompere un input e osservare il timeout

Chiudete la demo del terminale A con Ctrl+C. Non lasciate i publisher finti attivi insieme ai publisher manuali.

In ogni nuovo terminale eseguite prima:

```bash
source scripts/ros_env.sh
source install/local_setup.bash
```

Terminale A — solo avoidance:

```bash
ros2 run zefiro_demo avoidance_node
```

Terminale B — sensore:

```bash
ros2 topic pub -r 10 /zefiro/perception/front_clearance std_msgs/msg/Float32 "{data: 5.0}"
```

Terminale C — richiesta di moto:

```bash
ros2 topic pub -r 20 /zefiro/mission/goal_velocity geometry_msgs/msg/TwistStamped "{header: {frame_id: base_link}, twist: {linear: {x: 1.0}}}"
```

Terminale D — risultato:

```bash
ros2 topic echo /zefiro/safety/state
```

Provate in ordine:

1. Con entrambi gli input attivi: `CLEAR`.
2. Ctrl+C nel terminale C: `GOAL_TIMEOUT` dopo circa 0.5 s.
3. Riavvio di C: ritorno a `CLEAR`.
4. Ctrl+C nel terminale B: `SENSOR_TIMEOUT` dopo circa 0.5 s.
5. Riavvio di B con `data: 0.7`: `STOP`.
6. Riavvio di B con `data: -1.0`: `INVALID_INPUT`.

Per osservare anche la velocità, usate un altro terminale con `ros2 topic echo /zefiro/setpoint/velocity`: nei quattro stati di arresto `linear.x` deve essere zero. I timeout misurano l'ultimo arrivo locale, non il timestamp del messaggio.

## 6. Leggere e modificare poco codice

Leggete in quest'ordine, sotto `zefiro_autonomy/src/zefiro_demo/`:

1. `zefiro_demo/fake_goal_velocity_node.py`: publisher, timer, messaggio.
2. `zefiro_demo/fake_front_clearance_node.py`: sequenza temporale.
3. `zefiro_demo/avoidance_node.py`: subscriber e watchdog.
4. `zefiro_demo/avoidance_core.py`: decisione senza dipendenze ROS.
5. `test/test_avoidance_core.py`: input e output verificabili.
6. `launch/demo_fake_avoidance.launch.py`: collegamento dei nodi.

Esercizio comune: in un branch personale cambiate temporaneamente `stop_distance_m` a 1.5 nel file `config/demo.yaml`, riavviate la demo e spiegate perché a 2 m l'uscita diventa circa 0.33 m/s. Ripristinate 1.0 prima del test smoke standard. I parametri di avoidance si impostano all'avvio; `ros2 param set` li rifiuta intenzionalmente.

Per provare una configurazione esterna:

```bash
bash scripts/demo.sh config:=/percorso/assoluto/demo.yaml
```

## 7. Uscita dalla sessione

Ogni persona deve saper mostrare:

- Build e test riusciti.
- Un messaggio letto e il suo tipo spiegato.
- `GOAL_TIMEOUT` e `SENSOR_TIMEOUT` provocati e recuperati.
- Il file che decide la velocità e il file che la pubblica.
- Un branch personale e una piccola PR secondo [il workflow](contribution_workflow.md).

Poi scegliete il ruolo nel [piano per cinque persone](task_plan.md). Non occorre studiare tutto ROS prima di iniziare.

Approfondimenti ufficiali: [ambiente ROS](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html), [tutorial CLI](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools.html), [colcon](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html).
