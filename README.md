# PXE-boot-checking

Uses Ansible to power cycle blade servers via IPMI.

Parses DHCP/boot server logs (e.g., dhcpd.log, syslog, or journalctl) to verify PXE boot requests.

Returns a pass/fail result per server.

🔧 Requirements
Ansible installed and properly configured.

DHCP logs accessible on the Ansible control node or a centralized log server.

dhcp_log_path set to your actual DHCP server log file.

Your Ansible inventory has a [blades] group with variables for IPMI.

pxe_test/
├── pxe_test.py
├── ansible.cfg
├── inventory.ini
└── playbooks/
    └── reboot_and_wait.yml

When you run:
  python3 pxe_test.py

You’ll see:
Whether PXE boot requests were observed for each server (by MAC).
Optional DHCP log lines that prove PXE occurred.
