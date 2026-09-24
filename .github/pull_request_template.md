## What and why

<!-- One or two sentences. Link the issue if there is one. -->

## Checklist

- [ ] `python3 tools/validate.py` passes
- [ ] `python3 -m unittest discover -s plugins/whole-team/skills/whole-team/scripts` passes
- [ ] `claude plugin validate .` passes (if you have Claude Code)
- [ ] Behaviour change: an eval case in `tools/gen_evals.py` covers it, and the run is in the results table in `evals/README.md`
- [ ] New slash command: listed in `/whole-team:help` and the README
- [ ] User-visible change: `CHANGELOG.md` entry; version bumped in both manifests when releasing
