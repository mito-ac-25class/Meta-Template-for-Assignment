# Flow and Context Issues

| Category | Scope | Location/Related Files | Issue | Improvement |
| --- | --- | --- | --- | --- |
| Overall flow | Student-facing deliverables | `release/README.md` (missing) | The student README is absent, so the release output is incomplete. | Run `/readme.admin` to generate `release/README.md` from `templates/template.README.md` and restore it to the release flow. |
| Overall flow | Plan → README/TUTORIAL chain | `agent-output/plan.md` (missing) | Without a plan file, `/readme.admin` and `/tutorial.admin` prerequisites are unmet and the flow stalls. | Generate a plan from `agent-input/topics.md` or place a placeholder `agent-output/plan.md` so downstream steps can proceed. |
| Step workflow | CI autograding | `.github/workflows/classroom.yml` and `tests/stages/stage-01` to `stage-05` | The workflow runs stage01–05, but the corresponding tests are empty comments, so grading is ineffective. | Add minimal RED tests for each stage or temporarily disable those workflow steps until real tests exist. |
| Context duplication | Repository overview | `AGENTS.md` and `README.md` | Structure/flow explanations are duplicated, inflating the context window during support. | Keep one canonical description and replace the other with a short pointer/link. |
| Context duplication | Admin prompt footers | `.github/prompts/*.admin.prompt.md` | Branch/push instructions repeat in every prompt, drowning the core guidance. | Centralize workflow/branch rules in one doc and link to it from each prompt. |
| Step workflow | Local test setup | Local dev environment | Running `pytest` locally fails with `command not found` because dependencies are not installed by default. | Document a quick-start install step (e.g., `pip install -r requirements-dev.txt` or at minimum `pip install pytest`) before running tests locally. |
