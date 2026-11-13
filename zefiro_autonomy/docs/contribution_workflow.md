# Lavorare insieme senza sovrapporsi

Ogni attività ha un owner e un reviewer nel [piano](task_plan.md). Prima di scrivere codice riportate nella issue: input, output atteso, file coinvolti e una prova di accettazione.

## Branch e PR

Dalla radice della repo, con working tree pulito:

```bash
git switch main
git pull --ff-only
git switch -c task/p1-goal-parameter
# Modifica piccola, poi:
bash scripts/check.sh
python3 scripts/smoke_demo.py
git status --short
git add percorso/del/file.py percorso/del/test.py
git commit -m "Add configurable mission velocity"
git push -u origin task/p1-goal-parameter
```

Sostituite nome del branch e percorsi con quelli della vostra attività. Aprite una PR verso `main`; il template chiede comportamento, prova riproducibile e limiti. Evitate `git add .` finché non sapete spiegare ogni file nella lista.

La prima PR può essere una correzione della guida scoperta durante l'esercizio, purché descriva il comando fallito e quello verificato.

## Comandi condivisi

- `bash scripts/build.sh`: compila dai soli sorgenti.
- `bash scripts/check.sh`: build, test, lettura dei risultati; fallisce se fallisce un test.
- `python3 scripts/smoke_demo.py`: avvia il launch per un intero ciclo; richiede prima la build e il YAML standard.
- `bash scripts/doctor.sh`: mostra ambiente, dipendenze e pacchetto trovato.

Chiudete la demo prima dei test: publisher concorrenti nello stesso dominio alterano i risultati. La CI usa un ambiente Jazzy e verifica anche il percorso Docker. Non vengono eseguiti controlli su hardware.

## Review e merge

Il reviewer deve poter rifare l'esempio senza istruzioni private. Controlla che i nomi dei topic siano compatibili, i parametri invalidi siano rifiutati e le nuove dipendenze siano dichiarate in `package.xml`.

Una approvazione e CI verde prima del merge. Per logica di arresto, contratti e output chiedete anche la review del referente dell'area. P5 coordina le modifiche condivise a packaging e launch e integra una PR alla volta.

Sono regole del team; **non è stato verificato né configurato** che GitHub le imponga. Il maintainer può impostare branch protection e controlli richiesti dopo il primo run CI.

Dopo un merge, aggiornate `main` e riallineate i branch aperti. Se c'è un conflitto su un file condiviso risolvetelo con il suo owner, poi rieseguite i test.

## Cosa resta fuori da Git

`build/`, `install/`, `log/`, cache Python/pytest e registrazioni in `bags/`. Non modificare copie di codice dentro build/install: i sorgenti sono in `zefiro_autonomy/src/`.

## Quando qualcosa blocca il lavoro

Dopo un tentativo ragionato, condividete nella issue:

```text
Ambiente: Ubuntu/Docker, versione ROS, dominio
Branch e commit:
Comando esatto:
Risultato atteso:
Errore osservato:
Tentativi già fatti:
```

Per i problemi comuni vedere [troubleshooting.md](troubleshooting.md).
