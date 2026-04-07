# Deploying Schema Changes to schema.ocsflab.com

## Prerequisites

- Python 3.14+ (`brew install python@3.14`)
- SSH access to the Hetzner server (configured as `hetzner` in `~/.ssh/config`)
- `ocsf-schema-compiler` installed in a venv

## One-time setup

```bash
# Create a venv with the compiler
/opt/homebrew/bin/python3.14 -m venv /tmp/ocsf-venv
/tmp/ocsf-venv/bin/pip install ocsf-schema-compiler

# Patch the compiler (v2.0 removed the datetime profile but still uses datetime_t)
/tmp/ocsf-venv/bin/python3.14 patch_compiler.py
```

> The patch changes the compiler to warn instead of crash when `datetime_t` exists without a `datetime` profile. Re-run after recreating the venv or upgrading the compiler.

## Deploy steps

Run these from the `ocsf-schema` repo root:

```bash
# 1. Compile the schema (browser mode)
mkdir -p build/schema
/tmp/ocsf-venv/bin/ocsf-schema-compiler . -b 2>/dev/null > build/schema/schema.json

# 2. Transfer to server
scp build/schema/schema.json hetzner:~/schema/schema.json

# 3. Restart the service
ssh hetzner "sudo systemctl restart ocsf-schema"

# 4. Verify
curl -s -o /dev/null -w '%{http_code}' https://schema.ocsflab.com/
# Should return 200
```

## Troubleshooting

**Compiler fails?** Check the error output:
```bash
/tmp/ocsf-venv/bin/ocsf-schema-compiler . -b 2>&1 | tail -20
```

**Service won't start?** Check logs:
```bash
ssh hetzner "sudo journalctl -u ocsf-schema -n 50 --no-pager"
```

**Venv gone?** (e.g. after reboot — `/tmp` is cleared) Recreate it:
```bash
/opt/homebrew/bin/python3.14 -m venv /tmp/ocsf-venv
/tmp/ocsf-venv/bin/pip install ocsf-schema-compiler
/tmp/ocsf-venv/bin/python3.14 patch_compiler.py
```
