import nmap


def scan_network():

    scanner = nmap.PortScanner()

    scanner.scan(
        hosts="127.0.0.1",
        arguments="-sV"
    )

    devices = []

    for host in scanner.all_hosts():

        device = {
            "hostname": scanner[host].hostname(),
            "ip": host,
            "mac": "",
            "os": "",
            "ports": []
        }

        # Collect ports
        for protocol in scanner[host].all_protocols():

            ports = scanner[host][protocol].keys()

            for port in ports:
                device["ports"].append(port)

        devices.append(device)

    return devices