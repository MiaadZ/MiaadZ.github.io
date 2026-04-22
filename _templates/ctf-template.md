---
layout: single
title: "Title"
link: "Url"
parent: TryHackMe
os: Linux
difficulty: Easy
tags: [Nmap, Technique1, Technique2]
starred: false
date: YYYY-MM-DD
toc: true
toc_sticky: true
toc_label: "Contents"
toc_icon: "crosshairs"
---
# Writeup: [{{ page.title }}]({{ page.machine_url }})
{% include ctf-badges.html %}

> **Platform:** [**{{ page.parent }}**]({{ page.link }}) |
> **OS:** {{ page.os }} |
> **Difficulty:** {{ page.difficulty }} |
> **Operator:** [*S3Z4R*](https://tryhackme.com/p/S3Z4R)

---
## 🔗 Attack Chain
*A high-level overview of the attack path or incident.*
* 🔍 **Reconnaissance:** (e.g., Port 80, 445, SMB Enumeration)
* 🚪 **Initial Access:** (e.g., CVE-2024-25600 -> Bricks Builder RCE)
* 🔓 **Privilege Escalation:** (e.g., Misconfigured SUID `/bin/cat` -> Shadow Hash Cracking)
* 🛡️ **Remediation:** (e.g., Patch WordPress Theme, Remove SUID bit)

---
## 1. Reconnaissance & Enumeration (or "Incident Discovery")
### Network Scanning / Log Analysis
*Open ports, Services, or Initial malicious indicators.*
```bash
# Nmap output here
# Only relevant ports.
```
### Service Enumeration
*Analyze the discovered services or network traffic. What is the entry point?*

---
## 2. Initial Access (or "Attack Vector Identification")
### Vulnerability Analysis
*Briefly explain the flaw.*
### Exploitation / Execution
*Execution of the attack or exact log entry showing the breach.*
```bash
# Exploit command or payload
```
*Result: Gained a reverse shell as `username` (or "Attacker gained access via compromised credentials").*

---
## 3. Privilege Escalation (or "Persistence & Lateral Movement")
### Internal Enumeration
*(Misconfigurationon the system? (e.g., SUID binary, weak cronjob, kernel exploit).)*
### Exploitation
*How you leveraged the misconfiguration to get root/SYSTEM.*
```bash
# Insert PrivEsc commands here
```
*Result: System compromised.*

---
## 4. Remediation & Threat Intelligence
*How would a blue team detect or prevent this attack path? List 2-3 actionable fixes.*
* **Patching**: Update [Software] to version X to close CVE-XXXX-XXXX.
* **Configuration**: Disable [Feature], restrict permissions on [File], or enforce MFA.
* **Detection**: Monitor SIEM for anomalous child processes spawning from the web server or unauthorized modifications to `authorized_keys`.

---

{% comment %}

[Technique]: Log Analysis (Ripgrep)
[Command]: rg --glob '*.md' --fixed-strings 'Command: Example'
[Why]: Used to quickly grep through my own writeups to find where I used a specific command before.

{% endcomment %}
