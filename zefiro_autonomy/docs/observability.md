# Ispezione, registrazione e replay

Avviare la demo nel primo terminale. Negli altri, dalla radice Autopilot:

```bash
source scripts/ros_env.sh
source install/local_setup.bash
ros2 node info /avoidance_node
ros2 topic info /zefiro/setpoint/velocity --verbose
ros2 topic hz /zefiro/setpoint/velocity
```

## Registrare un caso

Serve `ros-jazzy-rosbag2` (incluso nell'immagine Docker). Usare una directory di output che non esiste già:

```bash
mkdir -p bags
ros2 bag record -o bags/demo_01 \
  /zefiro/perception/front_clearance \
  /zefiro/mission/goal_velocity \
  /zefiro/setpoint/velocity \
  /zefiro/safety/state
```

Attendere almeno un ciclo di 24 secondi, poi Ctrl+C. `ros2 bag info bags/demo_01` mostra durata, tipi e numero di messaggi. `bags/` è ignorata da Git; allegare alla PR i comandi e una breve sintesi, non dati voluminosi.

## Rivedere un'esecuzione registrata

Fermare la demo e ogni publisher manuale, quindi:

```bash
ros2 bag play bags/demo_01
```

In un altro terminale osservare `ros2 topic echo /zefiro/safety/state`. Questo ripubblica anche le vecchie uscite: **non dimostra che il codice corrente sia corretto**.

## Ricalcolare le uscite con il codice corrente

Fermare il playback completo. Avviare `ros2 run zefiro_demo avoidance_node` in un terminale e, in un altro:

```bash
ros2 bag play bags/demo_01 --topics \
  /zefiro/perception/front_clearance \
  /zefiro/mission/goal_velocity
```

Così avoidance riceve solo gli input registrati e produce nuove uscite. Non avviare i publisher finti. Alla fine della registrazione deve comparire `SENSOR_TIMEOUT`. I watchdog usano il tempo reale di ricezione: un replay rallentato o sospeso può produrre timeout ed è una prova distinta.

## Evidenza di una prova

```text
Commit:
Ambiente e ROS_DOMAIN_ID:
Launch/comandi:
Input (o bag e velocità di replay):
Stati e velocità osservati:
Interruzione sensore/goal:
Ripresa:
Esito e limiti:
```

I due topic di output non sono sincronizzati atomicamente. Per il confronto numerico usare i test; il logger è uno strumento didattico.
