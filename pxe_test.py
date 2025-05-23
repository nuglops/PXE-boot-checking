import subprocess
import time
import re

dhcp_log_path = "/var/log/syslog"

blade_nodes = [
    {"name": "blade01", "mac": "00:11:22:33:44:55"},
    {"name": "blade02", "mac": "00:11:22:33:44:66"},
]

def run_ansible_playbook():
    print("Running Ansible reboot playbook...")
    subprocess.run(["ansible-playbook", "playbooks/reboot_and_wait.yml"], check=True)

def get_dhcp_log_entries(mac_address, since_timestamp):
    with open(dhcp_log_path, "r") as f:
        lines = f.readlines()
    mac_regex = re.compile(mac_address.replace(":", "").lower())
    matching = [
        line for line in lines
        if mac_regex.search(line.replace(":", "").lower()) and "DHCPDISCOVER" in line or "PXE" in line
    ]
    return matching

def main():
    timestamp_before = time.time()
    run_ansible_playbook()
    print("Waiting 60s for PXE boot attempts...")
    time.sleep(60)
    print("\n--- PXE Boot Results ---")
    for node in blade_nodes:
        log_entries = get_dhcp_log_entries(node["mac"], timestamp_before)
        if log_entries:
            print(f"{node['name']}: ✅ PXE boot seen")
            for entry in log_entries:
                print(f"  → {entry.strip()}")
        else:
            print(f"{node['name']}: ❌ No PXE boot seen")

if __name__ == "__main__":
    main()
