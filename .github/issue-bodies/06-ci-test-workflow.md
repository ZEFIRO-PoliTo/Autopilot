## Goal

Make build and test failures more useful on pull requests.

## Context

A minimal GitHub Actions workflow already builds the workspace and runs `colcon test`. As multiple people start contributing, it should be extended with package-specific tests and clearer failure output.

## Tasks

- [ ] Review the existing GitHub Actions workflow.
- [ ] Keep building the workspace with `colcon build --symlink-install`.
- [ ] Keep running tests with `colcon test`.
- [ ] Upload or print test results in a useful way.
- [ ] Add meaningful tests as package owners add logic.
- [ ] Document the local equivalent commands.

## Expected Outputs

- Reviewed or improved `.github/workflows/ci.yml`.
- Updated setup/test docs.
- Passing CI on the default branch.

## Milestones

- 0-6h: review the minimal CI build.
- 6-12h: improve test result output if needed.
- 12-20h: align CI with Docker/native docs.
- 20-30h: add package-specific tests as they appear.

## Definition of Done

- [ ] Pull requests run CI automatically.
- [ ] CI catches build failures.
- [ ] Contributors know the matching local commands.
