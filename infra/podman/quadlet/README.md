# Podman Quadlet

Quadlet lets systemd manage Podman containers without Docker.

Install rootless for a Linux user:

```bash
mkdir -p ~/.config/containers/systemd
cp infra/podman/quadlet/* ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user enable --now indomarket-network.service indomarket-frontend.service indomarket-api.service
loginctl enable-linger $USER
```

Build image first:

```bash
podman build -f Containerfile -t localhost/indomarket-insight:latest .
```

Check logs:

```bash
journalctl --user -u indomarket-api -f
journalctl --user -u indomarket-frontend -f
```
