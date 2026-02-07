---
layout: single
title: "Advent of Cyber 2025"
link: "https://tryhackme.com/adventofcyber25"
parent: TryHackMe
os: Linux
difficulty: Easy
tags: [Docker, AWS Cli, Burp Suite]
starred: true
date: 2025-12-24
toc: true
toc_sticky: true
toc_label: "Mission Log"
toc_icon: "crosshairs"
---

# Event Log: [{{ page.title }}]({{ page.link }})
{% include ctf-badges.html %}

> **Event:** TryHackMe Advent of Cyber 2025 |
> **Focus:** Blue/Red Team |
> **Duration:** 24 Days |
> **Date:** Dec 2025 |
> **Status:** Completed (24/24)

---

## 📝 Event Overview
The Advent of Cyber is a 24-day capture-the-flag event covering the full spectrum of defensive and offensive security. I used this event to specifically sharpen my skills in **Cloud Security (AWS)**, **Web Exploitation**, and **Container Forensics**.

### 🛠️ Key Tools Used
* **Network:** Wireshark, Nmap, Burp Suite
* **Cloud/Infra:** Docker, AWS CLI, Kubernetes
* **Forensics:** Splunk, Volatility

---

## 🏆 Top 3 Highlights

### 1. Day 14: DoorDasher's Demise (Containers)
* **Topic:** Docker Misconfigurations
* **Technique:** Analyzed a compromised container environment. Identified privileges that allowed for interacting with the host system.
* **Takeaway:** Container isolation is not guaranteed. Misconfigured capabilities can easily lead to full host compromise.

### 2. Day 20: Race Conditions (Web)
* **Topic:** Web Application Logic Flaws
* **Technique:** Used **Burp Suite** (Repeater/Intruder) to send simultaneous requests, manipulating a coupon/credit system before the database could update the balance.
* **Takeaway:** Even secure code can be vulnerable if it doesn't handle concurrency correctly.

### 3. Day 23: S3cret Santa (AWS Cloud)
* **Topic:** AWS S3 Enumeration
* **Technique:** Configured `aws-cli` to interact with a target bucket. Enumerated file lists and downloaded sensitive data that was improperly secured.
* **Takeaway:** Publicly accessible S3 buckets remain a critical low-hanging fruit in cloud security assessments.

---

## 📅 Daily Log (Summary)

| Day | Category | Topic |
|:--- |:--- |:--- |
| **1-5** | **Web & AI** | Prompt Injection, IDOR, SQL Injection |
| **6-10** | **Forensics** | Memory Analysis, Registry Forensics, Splunk Basics |
| **11-15** | **Cloud & Infra** | **Docker Escapes (Day 14)**, Azure Blob Attacks |
| **16-20** | **Network/Web** | Active Directory, **Race Conditions (Day 20)** |
| **21-24** | **Red Team** | C2 Beacons, Malware Analysis, **AWS S3 (Day 23)** |

---

### 🚀 Conclusion
This event reinforced the importance of **hybrid skills**. Being able to pivot from Web (Burp Suite) to Infrastructure (Docker) and Cloud (AWS) is essential for a modern Penetration Tester.

---

{% comment %}

[Technique]: Docker Capabilities Check
[Command]: capsh --print
[Why]: Checks container capabilities to identify if privilege escalation to host is possible.

[Technique]: AWS S3 Bucket List
[Command]: aws s3 ls s3://<bucket-name> --no-sign-request
[Why]: Lists contents of a public bucket without authentication headers.

[Technique]: Powershell Encoded Command
[Command]: powershell -EncodedCommand <Base64String>
[Why]: Common method to execute obfuscated Powershell scripts in Windows environments.

{% endcomment %}