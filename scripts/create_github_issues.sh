#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh is not installed. Install GitHub CLI and run: gh auth login"
  exit 1
fi

gh auth status >/dev/null

create_or_update_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  if gh label view "${name}" >/dev/null 2>&1; then
    gh label edit "${name}" --color "${color}" --description "${description}"
  else
    gh label create "${name}" --color "${color}" --description "${description}"
  fi
}

create_issue() {
  local title="$1"
  local body_file="$2"
  local labels="$3"

  gh issue create \
    --title "${title}" \
    --body-file "${repo_root}/${body_file}" \
    --label "${labels}"
}

create_or_update_label "area:setup" "5319e7" "Development environment and repo workflow"
create_or_update_label "area:input" "1d76db" "Camera, synthetic depth, and perception input"
create_or_update_label "area:avoidance" "d93f0b" "Safety and avoidance behavior"
create_or_update_label "area:output" "0052cc" "PX4, micro XRCE-DDS, and output adapters"
create_or_update_label "area:bringup" "0e8a16" "ROS 2 package layout and launch files"
create_or_update_label "area:simulation" "bfd4f2" "Simulation scenarios and rehearsal"
create_or_update_label "area:hardware" "c5def5" "Hardware-facing contracts and preparation"
create_or_update_label "area:test" "fbca04" "Automated tests, smoke tests, and CI"
create_or_update_label "area:docs" "006b75" "Documentation and demo instructions"
create_or_update_label "area:integration" "5319e7" "Cross-package integration and rehearsals"
create_or_update_label "priority:high" "b60205" "Must be handled in the first work block"
create_or_update_label "priority:medium" "fbca04" "Important but can follow high-priority work"

create_issue "T0 Setup and acceptance checklist" ".github/issue-bodies/01-setup.md" "area:setup,area:docs,priority:high"
create_issue "T1 Package boundaries and bringup" ".github/issue-bodies/02-package-boundaries-bringup.md" "area:bringup,priority:high"
create_issue "T2 Synthetic perception node" ".github/issue-bodies/03-synthetic-perception.md" "area:input,area:simulation,priority:high"
create_issue "T3 Camera interface specification and replay path" ".github/issue-bodies/04-camera-contract-replay.md" "area:input,area:hardware,area:docs,priority:high"
create_issue "T4 Avoidance core and safety tests" ".github/issue-bodies/05-avoidance-core.md" "area:avoidance,area:test,priority:high"
create_issue "T5 PX4 output mock and micro XRCE-DDS study" ".github/issue-bodies/06-px4-output-mock.md" "area:output,area:hardware,priority:high"
create_issue "T6 Simulation scenario harness" ".github/issue-bodies/07-simulation-scenarios.md" "area:simulation,area:test,priority:medium"
create_issue "T7 Observability and rosbag workflow" ".github/issue-bodies/08-observability-rosbag.md" "area:docs,area:test,priority:medium"
create_issue "T8 CI and contributor workflow" ".github/issue-bodies/09-ci-contributor-workflow.md" "area:test,area:setup,priority:medium"
create_issue "T9 Integration rehearsal" ".github/issue-bodies/10-integration-rehearsal.md" "area:integration,area:simulation,priority:high"
