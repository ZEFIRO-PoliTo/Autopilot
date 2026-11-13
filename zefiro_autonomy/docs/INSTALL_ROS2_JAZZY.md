# Ambiente di sviluppo ROS 2 Jazzy

Percorso nativo del team: **Ubuntu 24.04 + ROS 2 Jazzy + Python di sistema**. Per altri sistemi usate l'ambiente Docker nel [README](../../README.md); l'integrazione con host Windows/macOS non è stata verificata localmente.

## Installare ROS

Seguite la [guida ufficiale Jazzy per Ubuntu](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) per locale UTF-8, repository Universe, `ros2-apt-source` e installazione. La variante `ros-jazzy-ros-base` è sufficiente per la demo; desktop è facoltativa.

La configurazione dei repository APT evolve: usate i comandi ufficiali, senza copiare vecchie chiavi o repository di altre distribuzioni.

Dopo l'installazione:

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install python3-colcon-common-extensions python3-rosdep python3-pytest ros-jazzy-rosbag2
```

Inizializzate rosdep una sola volta sulla macchina:

```bash
sudo rosdep init
rosdep update --rosdistro jazzy
```

Se `rosdep init` dice che esiste già `20-default.list`, proseguite con update senza rimuovere configurazioni esistenti.

## Installare le dipendenze della repo

Dalla radice `Autopilot/`:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths zefiro_autonomy/src --ignore-src --rosdistro jazzy -y
bash scripts/doctor.sh
bash scripts/check.sh
bash scripts/demo.sh
```

Ogni nuova shell di ispezione richiede `source scripts/ros_env.sh` e `source install/local_setup.bash`. Gli script di build/test/demo preparano il proprio ambiente automaticamente.

Non installate con `sudo pip` nuove versioni di pytest o librerie ROS. Se usate conda/venv, disattivatelo per questa guida. Per il conflitto pytest trovato sulla macchina dell'audit, vedere [troubleshooting.md](troubleshooting.md).

Riferimenti verificati anche tramite i sorgenti ufficiali: [installazione](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst), [build con colcon](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.rst).
