# Offline / Air-gapped Install

On an internet-connected machine:

```bash
./scripts/bootstrap/create_wheelhouse.sh
```

Copy these to the offline machine:

```text
project folder
wheelhouse.tar.gz
```

On offline machine:

```bash
tar -xzf wheelhouse.tar.gz
./scripts/bootstrap/install_from_wheelhouse.sh
```

Windows equivalent:

```powershell
python -m pip download -r requirements.txt -d wheelhouse
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-index --find-links wheelhouse -r requirements.txt
```
