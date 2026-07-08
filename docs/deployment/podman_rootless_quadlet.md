# Rootless Podman with Quadlet

Quadlet is a systemd integration for Podman. It is open-source and works well on cloud Linux VMs.

## Install

```bash
sudo apt-get update
sudo apt-get install -y podman
./scripts/podman_quadlet_install.sh
```

## Check status

```bash
systemctl --user status indomarket-api
systemctl --user status indomarket-frontend
journalctl --user -u indomarket-api -f
```

## Enable after logout/reboot

```bash
loginctl enable-linger $USER
```

## Uninstall

```bash
systemctl --user disable --now indomarket-api indomarket-frontend
rm -f ~/.config/containers/systemd/indomarket-*.container ~/.config/containers/systemd/indomarket.network
systemctl --user daemon-reload
```
