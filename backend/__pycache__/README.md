Module 4 - SHAP Features

Input Features:

1. unknown_device
   - 1 = Shadow IT device
   - 0 = Authorized device

2. open_port_count
   - Number of open network ports

3. critical_cve_count
   - Number of critical vulnerabilities

4. patch_status
   - 1 = Updated
   - 0 = Outdated

5. os_version
   - Operating system version

6. sensitive_network_access
   - 1 = Has sensitive access
   - 0 = No sensitive access


SHAP Explanation Examples:

Feature: unknown_device
Value: 1
Meaning:
Unknown device increases risk


Feature: open_port_count
Value: 5
Meaning:
Many open ports increase attack surface


Feature: critical_cve_count
Value: 2
Meaning:
Critical vulnerabilities increase risk


Feature: patch_status
Value: 0
Meaning:
Outdated patches increase risk