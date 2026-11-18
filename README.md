# Zefiro Autopilot

A small **ROS 2 Jazzy / Python** demo for learning how an autonomy pipeline fits together. It runs on a laptop with synthetic inputs. It does not control a drone.

```text
synthetic front distance ─┐
                          ├─ avoidance ─ filtered velocity + state ─ logger
requested velocity ───────┘
```

## Start here

1. [Exercise: run and inspect the demo](zefiro_autonomy/docs/getting_started.md).
2. [Plan for five contributors](zefiro_autonomy/docs/task_plan.md).
3. [Architecture and topic contracts](zefiro_autonomy/docs/architecture.md).
4. [Contribution workflow](zefiro_autonomy/docs/contribution_workflow.md).

## Run on Ubuntu 24.04

Install ROS 2 Jazzy using the [installation guide](zefiro_autonomy/docs/install_ros2_jazzy.md). From the **Autopilot repository root**:

```bash
bash scripts/doctor.sh
bash scripts/check.sh
bash scripts/demo.sh
```

The demo cycles through `CLEAR → SLOWDOWN → STOP → INVALID_INPUT` every 24 seconds. Stop it with Ctrl+C. An automated launch check takes about 27 seconds:

```bash
python3 scripts/smoke_demo.py
```

Build files and logs go into `build/`, `install/`, and `log/` at the repository root and are ignored by Git.

## Docker alternative

Requires Docker Engine and Compose v2. See the [audit](zefiro_autonomy/docs/audit.md) for local verification limits.

```bash
docker compose build
docker compose run --rm --name zefiro-dev autonomy
# Inside the container, from /workspace/autopilot:
bash scripts/check.sh
bash scripts/demo.sh
```

To inspect topics from a second shell in the **same container**:

```bash
docker exec -it zefiro-dev bash
source scripts/ros_env.sh
source install/local_setup.bash
ros2 topic echo /zefiro/safety/state
```

The source files are shared with the host editor; Docker uses separate volumes for build artifacts. A second `compose run` starts another container and cannot observe this local-only ROS graph.

## Repository map

| Path | Purpose |
| --- | --- |
| `zefiro_autonomy/src/zefiro_demo/zefiro_demo/` | Python nodes and avoidance logic |
| `zefiro_autonomy/src/zefiro_demo/config/demo.yaml` | Demo parameters |
| `zefiro_autonomy/src/zefiro_demo/launch/` | Starts all four nodes |
| `zefiro_autonomy/src/zefiro_demo/test/` | Logic and ROS integration tests |
| `scripts/` | Diagnosis, build, checks, and demo |
| `zefiro_autonomy/docs/` | Exercise, architecture, and work plan |

Further reading: [troubleshooting](zefiro_autonomy/docs/troubleshooting.md), [recording and replay](zefiro_autonomy/docs/observability.md), [audit](zefiro_autonomy/docs/audit.md).

The repository is named **Autopilot** with a capital A. The older local `zefiro/autopilot` directory is a separate project.
