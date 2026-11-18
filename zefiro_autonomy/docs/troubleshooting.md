# Troubleshooting

Start with `bash scripts/doctor.sh` from the `Autopilot/` root.

| Symptom | Check |
| --- | --- |
| `ros2: command not found` | Install Jazzy, then `source scripts/ros_env.sh` in this shell. |
| `Package zefiro_demo not found` | Run `bash scripts/build.sh`, then `source install/local_setup.bash`. |
| Edited code has no effect | Edit only `zefiro_autonomy/src/`; `ros2 pkg prefix zefiro_demo` should point to this repository's root `install/`. |
| Commands run inside `zefiro_autonomy/` | Return to the outer `Autopilot/` root and use the scripts. |
| Empty topics or duplicate nodes | Match the domain across shells; close older demos. Check `ros2 topic info TOPIC --verbose`. |
| CLI graph uses an old domain | After changing environment variables, run `ros2 daemon stop` and retry. |
| Docker cannot see topics | Use `docker exec -it zefiro-dev bash` in the same container and source the ROS and install environments. |
| `GOAL_TIMEOUT` | No goal arrived for over 0.5 s; the publisher must keep sending. |
| `INVALID_INPUT` for an apparently valid goal | Frame must be `base_link`; only finite forward `linear.x` ≥ 0 is allowed, all other axes zero. |
| `ros2 param set` rejected | Avoidance parameters are start-up only; edit YAML and relaunch. |
| Smoke fails after changing thresholds | Restore the standard YAML; write a separate test for other scenarios. |
| GitHub access denied | Check organization access and credentials; do not commit tokens. |

## pytest / launch_testing plugin conflict

On the audit machine, global pytest 9.2 from `/usr/local` took precedence over Ubuntu pytest 7.4.4 and broke the ROS `launch_testing` plugin before tests started. To use APT packages **in the current shell only** on Ubuntu 24.04:

```bash
export PATH="/usr/bin:/bin:$PATH"
export PYTHONNOUSERSITE=1
export PYTHONPATH="/usr/lib/python3/dist-packages:${PYTHONPATH:-}"
bash scripts/check.sh
python3 scripts/smoke_demo.py
```

Do not uninstall packages used by other projects without checking. The container provides an isolated alternative.

## Old local build artifacts

Older `build/`, `install/`, or `log/` directories inside `zefiro_autonomy/` may still exist locally but are no longer tracked. Do not source or copy them. The scripts build from explicit source paths and install at the repository root. For cache issues, use a clean clone or worktree rather than deleting files blindly. Rebuild after changes to `setup.py`, dependencies, executables, launch files, or configuration.
