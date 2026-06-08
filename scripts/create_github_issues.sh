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
create_or_update_label "area:test" "fbca04" "Automated tests, smoke tests, and CI"
create_or_update_label "area:docs" "006b75" "Documentation and demo instructions"
create_or_update_label "priority:high" "b60205" "Must be handled in the first work block"
create_or_update_label "priority:medium" "fbca04" "Important but can follow high-priority work"

create_issue "Stabilize local and Docker setup" ".github/issue-bodies/01-setup.md" "area:setup,area:docs,priority:high"
create_issue "Implement synthetic depth input and clearance node" ".github/issue-bodies/02-synthetic-depth-input.md" "area:input,priority:high"
create_issue "Refactor and test avoidance core" ".github/issue-bodies/03-avoidance-core.md" "area:avoidance,area:test,priority:high"
create_issue "Design and implement PX4 output mock adapter" ".github/issue-bodies/04-px4-output-mock.md" "area:output,priority:high"
create_issue "Split packages and create bringup launches" ".github/issue-bodies/05-package-split-bringup.md" "area:bringup,priority:high"
create_issue "Harden CI and test workflow" ".github/issue-bodies/06-ci-test-workflow.md" "area:test,area:setup,priority:medium"
create_issue "Improve demo logging and troubleshooting" ".github/issue-bodies/07-demo-docs.md" "area:docs,priority:medium"
