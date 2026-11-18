# Working together

Each task has an owner and reviewer in the [work plan](task_plan.md). Before coding, write the input, expected output, affected files, and acceptance check in the issue.

## Branch and PR

From a clean `Autopilot/` root:

```bash
git switch main
git pull --ff-only
git switch -c task/p1-goal-parameter
# Make one small change, then:
bash scripts/check.sh
python3 scripts/smoke_demo.py
git status --short
git add path/to/file.py path/to/test.py
git commit -m "Add configurable mission velocity"
git push -u origin task/p1-goal-parameter
```

Replace the branch and paths with your own task. Open a PR into `main`; the template asks for the changed behavior, a reproducible check, and limits. Review `git status` before adding files. A useful first PR can also fix an exercise instruction if it documents the failing and verified commands.

## Shared checks

- `bash scripts/build.sh`: build from source.
- `bash scripts/check.sh`: build, test, and show results; fails on test failure.
- `python3 scripts/smoke_demo.py`: run a full launch cycle; first build and use the standard YAML.
- `bash scripts/doctor.sh`: show the environment, dependencies, and installed package.

Stop the demo before tests, since competing publishers can alter results. CI checks Jazzy and the Docker path, not hardware.

## Review and merge

A reviewer should reproduce the result from written commands. Check topic names, invalid parameters, and new dependencies in `package.xml`. Team practice is one approval and green CI before merge, with an additional area review for stopping logic, contracts, or output. P5 coordinates shared packaging and launch edits. These are team rules; GitHub enforcement has not been verified or configured.

After a merge, update `main`, rebase open branches if needed, and rerun checks after resolving conflicts with the file owner.

## Keep generated files out of Git

Ignore `build/`, `install/`, `log/`, Python/pytest caches, and `bags/`. Edit source under `zefiro_autonomy/src/`, never copies in build/install.

## If work is blocked

Share this information in the issue after a reasonable attempt:

```text
Environment: Ubuntu/Docker, ROS version, domain
Branch and commit:
Exact command:
Expected result:
Observed error:
Attempts so far:
```

See [troubleshooting.md](troubleshooting.md) for common problems.
