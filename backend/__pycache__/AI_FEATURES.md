# Module 3 – AI Risk Classification

## Purpose

This module predicts the security risk of each discovered device using a Machine Learning model.

---

## Input Features

| Feature | Source | Description |
|---------|--------|-------------|
| unknown_device | Module 2 | Whether the device is Shadow IT (Yes/No) |
| open_port_count | Module 1 | Total number of open ports |
| critical_cve_count | Dataset | Number of known critical vulnerabilities |
| patch_status | Dataset | Updated or Outdated |
| os_version | Module 1 | Operating system detected by Nmap |
| sensitive_network_access | Dataset | Whether the device can access sensitive systems |

---

## Target

The AI model predicts:

- Low
- Medium
- High
- Critical

This value is stored in the `risk` column of the training dataset.