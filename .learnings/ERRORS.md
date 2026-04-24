## [ERR-20260421-001] zsh-shell-variable-status

**Logged**: 2026-04-21T11:26:00Z
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Used `status` as a shell variable name in zsh, which is read-only and caused the cron command wrapper to fail.

### Error
```
zsh:2: read-only variable: status
```

### Context
- Command/operation attempted: run fetch script, then branch on exit code
- Environment details: zsh on macOS via OpenClaw exec

### Suggested Fix
Use a different variable name like `rc` instead of `status` in zsh shell snippets.

### Metadata
- Reproducible: yes
- Related Files: /Users/vivianashford/.openclaw/workspace/tejas-combined/scripts/fetch_oil_data.py

---
## [ERR-20260423-002] zsh_exec

**Logged**: 2026-04-23T12:25:52Z
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Using  in zsh failed because  is a readonly special variable

### Error


### Context
- Command/operation attempted: conditional git commit/push wrapper after oil data refresh
- Environment: zsh on macOS via OpenClaw exec

### Suggested Fix
Use a different variable name like  instead of  in zsh shell snippets

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

---
