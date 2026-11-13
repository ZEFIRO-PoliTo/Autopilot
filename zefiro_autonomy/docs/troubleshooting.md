# Problemi frequenti

Partire da `bash scripts/doctor.sh`, dalla radice Autopilot.

| Sintomo | Controllo e soluzione |
| --- | --- |
| `ros2: command not found` | Installare Jazzy, poi `source scripts/ros_env.sh` nel terminale corrente |
| `Package zefiro_demo not found` | `bash scripts/build.sh`, poi `source install/local_setup.bash` |
| Modifico un file ma non cambia nulla | Modificare solo `zefiro_autonomy/src/`; `ros2 pkg prefix zefiro_demo` deve indicare l'installazione nella radice della repo corrente |
| Comandi eseguiti dentro `zefiro_autonomy/` | Tornare alla radice Autopilot; usare gli script |
| Topic vuoti o nodi duplicati | Confrontare dominio in tutte le shell, chiudere demo precedenti; `ros2 topic info TOPIC --verbose` mostra i publisher |
| Grafo CLI rimasto nel dominio precedente | Dopo aver corretto le variabili, eseguire `ros2 daemon stop` e riprovare |
| Docker non mostra i topic | Entrare con `docker exec -it zefiro-dev bash` nello stesso container, poi source ambiente e install |
| `GOAL_TIMEOUT` | Il goal non arriva da oltre 0.5 s; il publisher deve continuare a pubblicare |
| `INVALID_INPUT` con goal apparentemente corretto | Frame deve essere `base_link`, solo linear.x ≥ 0 finito, tutti gli altri assi zero |
| `ros2 param set` rifiutato | Parametri avoidance di solo avvio: modificare YAML e rilanciare |
| Test smoke fallisce dopo aver cambiato soglie | Ripristinare `config/demo.yaml` standard prima dello smoke; per scenari diversi scrivere prove dedicate |
| Permessi GitHub | Verificare accesso dell'account all'organizzazione e credenziali; non inserire token nella repo |

## Conflitto pytest / plugin launch_testing

Durante l'audit, il Python di sistema caricava pytest 9.2 da `/usr/local` invece della versione Ubuntu 7.4.4. Il risultato era un errore del plugin `launch_testing` su `pytest_pycollect_makemodule(path, parent)`, prima dell'esecuzione dei test.

Per riprodurre i controlli usando i pacchetti APT **solo nella shell corrente**, su Ubuntu 24.04:

```bash
export PATH="/usr/bin:/bin:$PATH"
export PYTHONNOUSERSITE=1
export PYTHONPATH="/usr/lib/python3/dist-packages:${PYTHONPATH:-}"
bash scripts/check.sh
python3 scripts/smoke_demo.py
```

Non disinstallare alla cieca pacchetti usati da altri progetti. Il container fornisce un'altra strada per isolare l'ambiente.

## Vecchi build/install locali

I file generati precedentemente sotto `zefiro_autonomy/build`, `install`, `log` sono stati tolti da Git ma possono essere ancora presenti sulla macchina originale. Non vanno copiati o caricati con `source`. Gli script usano solo i sorgenti espliciti e il workspace alla radice.

Per verificare un problema di cache, preferire un clone pulito o un nuovo worktree a cancellazioni indiscriminate. Ricompilare dopo modifiche a `setup.py`, nuove dipendenze, nuovi eseguibili o nuovi file launch/config.
