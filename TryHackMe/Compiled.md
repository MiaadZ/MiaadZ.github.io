---
layout: default
title: Compiled
parent: TryHackMe
---
# CTF Writeup: [Compiled](https://tryhackme.com/room/compiled)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Easy |
> **Date:** 11.11.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/SeZaR)

---
## 1. Explanation
After downloading the Compiled file we need to use `gdb` to see the functions and registers inside and find the flag.

* **Tip:** You can install [**Gef**](https://hugsy.github.io/gef/install/) which is a plugin for `gdb`.

First open the file in `gdb`:
```bash
gdb Compiled-1688545393558.Compiled
```
We will see `gdb>` or `gef>` if you installed it. ()

```bash
gef➤  checksec
[+] checksec for 'Compiled-1688545393558.Compiled'
Canary                        : ✘
NX                            : ✓
PIE                           : ✓
Fortify                       : ✘
RelRO                         : Partial
```
What it means:
* **Canary:** A check value on the stack to detect buffer overflows before they hijack control flow.
* **NX:** Marks the stack and heap as non-executable, preventing injected shellcode from running.
* **PIE:** Randomizes the main program's memory address each time it runs (part of ASLR).
* **Fortify:** Compiler checks that make functions like `strcpy` safer by detecting overflows at runtime.
* **RelRO:** A mitigation to make program data sections (like the Global Offset Table - GOT) read-only.

As a result of checking the security of the program, we have two approaches to take:
* Try buffer overflow using a generated input (Usually `scanf` or `printf` commands in the program)
* Try exploiting the compare functions which compare input with the real password (Usually `strcmp` function)

## 2. Buffer Overflow
Starting the `BoF` we will start the program as explained. Using the below command we get an overview of functions:
```bash
gef➤  info functions
All defined functions:

Non-debugging symbols:
0x0000000000001000  _init
0x0000000000001030  printf@plt
0x0000000000001040  strcmp@plt
0x0000000000001050  __isoc99_scanf@plt
0x0000000000001060  fwrite@plt
0x0000000000001070  __cxa_finalize@plt
0x0000000000001080  _start
0x00000000000010b0  deregister_tm_clones
0x00000000000010e0  register_tm_clones
0x0000000000001120  __do_global_dtors_aux
0x0000000000001160  frame_dummy
0x0000000000001169  main
0x0000000000001268  _fini
```
To exploit the `BoF` we can focus on `printf` and `scanf`, but to know more details and which one to focus on, we should `disassemble main` function as below:

```bash
gef➤  disassemble main
Dump of assembler code for function main:
. . .
   0x00000000000011b6 <+77>:    lea    rax,[rbp-0x20]
   0x00000000000011ba <+81>:    mov    rsi,rax
   0x00000000000011bd <+84>:    lea    rax,[rip+0xe4b]        # 0x200f
   0x00000000000011c4 <+91>:    mov    rdi,rax
   0x00000000000011c7 <+94>:    mov    eax,0x0
   0x00000000000011cc <+99>:    call   0x1050 <__isoc99_scanf@plt>
. . . 
End of assembler dump.
```
Inside `disassemble main` we can find `scanf` so we know that the input can be vulnerable. Let's test the input with a custom pattern.
We can generate a custom pattern using the `pattern` command in `gef`as below:
```bash
gef➤  pattern create 100
[+] Generating a pattern of 100 bytes (n=8)
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
[+] Saved as '$_gef0'
```
Then we should copy the pattern generated and paste it when the password is asked. We can test it when running the program:
```bash
gef➤  run
Starting program: Compiled-1688545393558.Compiled
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
Password: aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
Try again![Inferior 1 (process 49857) exited normally]
```
As we see, the program `exited normally`, even with `100` inputs the `scanf` function seems to be secured and can handle the input very well.

There is one single thing in `disassemble main` that we missed. As you saw in the command, there were information on the right side of the `gef` where we noticed the program is writing something to `0x200f`. This was visible on this line:
```bash
disassemble main
. . . 
0x00000000000011bd <+84>:    lea    rax,[rip+0xe4b]        # 0x200f
. . .
```
This means that the program is writing something into `0x200f`. Maybe this is the reason that the `Buffer Overflow` is not working? That remains to be seen, let's see what is inside the mentioned address:
```bash
gef➤  x/s 0x200f
0x200f: "DoYouEven%sCTF"
```
Well, what is happening?! Let me explain... The input we entered (`100 characters`) first matches `DoYouEven`. Then, the `%s` reads everything after that (until a space or newline) into the buffer at `[rbp-0x20]`. This makes it a bit more tricky!

### Crafting a Payload
In order to use this information we can come up with a new pattern starting with `DoYouEven`. Let's do that:
```bash
gef➤  pattern create 40
[+] Generating a pattern of 40 bytes (n=8)
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaa
[+] Saved as '$_gef0'
```
Copy the pattern then add `DoYouEven` to the start of it:
```
DoYouEvenaaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaa
```
Combining the two of them, now we have crafted a new input which should work perfectly fine. The moment of truth!
```bash
gef➤ run
Starting program: Compiled-1688545393558.Compiled
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
Password: DoYouEvenaaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaa

Program received signal SIGSEGV, Segmentation fault.
0x00007fffffffd430 in ?? ()
```
There it is, the `Segmentation fault` is what we needed all this time. That means we successfully failed the program and it crashed!

Now there are a lot of information printed out from our dear `gef`, but we focus on what is important. Looking at the output we can see a familiar pattern:
```bash
. . . 
$rbp   : 0x00007fffffffd658  →  "eaaaaaaa"
. . . 
```
Isn't that the input we crafted? Yes it is!

### Offset
Let's find the offset of the input we used.

* **Offset:** When a function is called, the program saves its `return address` on the stack. This address is the `golden ticket` it tells the CPU where to go next after the function is finished.

How can we find the offset? We can count it from the beginning, but we don't wanna make `gef` upset do we? So let's find it the `gef` way:
```bash
gef➤  pattern search 0x00007fffffffd658     # register address
[+] Searching for '6561616161616161'/'6161616161616165' with period=8
[+] Found at offset 32 (little-endian search) likely
```
So, this means that in the pattern `gef` created, the offset is `32` plus the `period=8` sums up to `40`. Thank you Gef!

### Return Address
Let's see what we've got:
* A Prefix: `DoYouEven`
* Offset: `40 Bytes`
Up until here, we smashed the stacks! Now it's time to show them whos the Boss by instructing it where to go next! This address is called `Return Address`.

#### Jump if Not Equal!
OK, Let's look into the main function again:
```bash
   0x000000000000121b <+178>:   test   eax,eax
   0x000000000000121d <+180>:   jne    0x1235 <main+204>
   0x000000000000121f <+182>:   lea    rax,[rip+0xe0b]
```
This part of main function seems interesting!
Let me translate it for you. Ehemm! By looking at this part, we can see that there is a `jne`, this is an Assembly Code for `Jump if Not Equal`. So if the input is not equal when compared to the real password, then it jumps to `<main+204>`. This is a **Failure**!

We need to bypass this function. But what would be the next thing we will deal with afterwards? Let's see a few more lines:
```bash
   0x000000000000121f <+182>:   lea    rax,[rip+0xe0b]        # 0x2031
   0x0000000000001226 <+189>:   mov    rdi,rax
   0x0000000000001229 <+192>:   mov    eax,0x0
   0x000000000000122e <+197>:   call   0x1030 <printf@plt>
```
Apparently the program is `loading the effective address` (`lea`) and then `copies the the data 
from rax to rdi and null to eax` (`mov`). This feels correct!

Ok let's do it, we will use the `0x000000000000121f` as our `Return Address` at the end of our payload. First of all, we need to write it in `Little Endian` (Little end first) as below:
```bash
\x1f\x12\x00\x00\x00\x00\x00\x00
```

* **Little Endian:** It is a method of storing data in computer memory where the least significant byte (the little end) is stored first, which is the lowest memory address.

Now let's add the ingredients and make the final payload. We can add them together in Notepad! But since we are trying to get professional let's generate it using Assembly Language, Ehemmm, Python i meant!
```python
❯ python3 -c 'import sys; sys.stdout.buffer.write(b"DoYouEven" + b"A"*40 + b"\x1f\x12\x00\x00\x00\x00\x00\x00")' > payload.txt
```
This creates the perfect payload that we need and writes it into the `payload.txt` file.
We can then use this inside `gef` with the command `r < payload.txt`.

What are we waiting for, let's do it!
```bash
. . . 
$rsi : 0x2174636572726f43 ("Correct!"?)
$rdi : 0x00007fffffffd4c0 → ... ("Correct!"?)
. . .
[!] Cannot access memory at address 0x121f
. . . 
```
Woah! Correct! That's it! But wait! This doesn't feel like Victory! why!?

That's because it was all a big mistake! Just kidding! The address we had for the offset `0x000000000000121f` was a relative address in `disassemble main`! We need the `Base Address` too.

This can be a bit tricky! When the code crashed the output had this line:
```bash
0x00007fffffffd6b8│+0x0018: 0x0000555555555169  →  <main+0000> push rbp
```
Getting back to the `disassemble main` we also had this line:
```bash
0x0000000000001169 <+0>:     push   rbp
```
Basically the first one was the memory address of the second relative address!
Alright let's make it simple math:
```bash
Absolute Address - Relative Address = Base Address
0x0000555555555169 - 0x0000000000001169 = 0x555555554000
```
See? *Simp el Math!*
So `0x555555554000` is what we call `Base Address`.

**Base Address:** The start of virtual memory address where the operating system randomly generates to load your program.

Now we can add our `Relative Address` to the `Base Address` to get the `Absolute Address`:

```bash
0x555555554000 (Base) + 0x121f (Offset) = 0x55555555521f
```
Next is the `Little Endian`:
```bash
\x1f\x52\x55\x55\x55\x55\x00\x00
```
And now we can replace this with the last python command we used to generate the payload:
```python
python3 -c 'import sys; sys.stdout.buffer.write(b"DoYouEven" + b"A"*40 + b"\x1f\x52\x55\x55\x55\x55\x00\x00")' > payload.txt
```
There we go! Now we demand the password!!!
Let's see the output:
```bash
gef➤  r < payload.txt
Starting program: Compiled-1688545393558.Compiled < payload.txt
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".

Program received signal SIGBUS, Bus error.
0x0000555555555264 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0x0
$rdx   : 0x0
$rsp   : 0x00007fffffffd670  →  0x00007ffff7fc7000  →  0x03010102464c457f
$rbp   : 0x4141414141414141 ("AAAAAAAA"?)
$rsi   : 0x2174636572726f43 ("Correct!"?)
$rdi   : 0x00007fffffffd490  →  0x00007fffffffd4c0  →  "Correct!"
$rip   : 0x0000555555555264  →  <main+00fb> leave
$r8    : 0x0
$r9    : 0x00007ffff7f90ec0  →  0x0000000000000000
$r10   : 0x0000555555556031  →  "Correct!"
$r11   : 0x00007ffff7de0040  →  <printf+0000> endbr64
$r12   : 0x00007fffffffd788  →  0x00007fffffffdc20  →  "Compiled-1688545393[...]"
$r13   : 0x1
$r14   : 0x00007ffff7ffd000  →  0x00007ffff7ffe5f0  →  0x0000555555554000  →   jg 0x555555554047
$r15   : 0x0000555555557dd8  →  0x0000555555555120  →  <__do_global_dtors_aux+0000> endbr64
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00
────────────────────────────────────────────────────────────── stack ────
0x00007fffffffd670│+0x0000: 0x00007ffff7fc7000  →  0x03010102464c457f    ← $rsp
0x00007fffffffd678│+0x0008: 0x00007fffffffd788  →  0x00007fffffffdc20  →  "Compiled-1688545393[...]"
0x00007fffffffd680│+0x0010: 0x00000001ffffd6c0
0x00007fffffffd688│+0x0018: 0x0000555555555169  →  <main+0000> push rbp
0x00007fffffffd690│+0x0020: 0x0000000000000000
0x00007fffffffd698│+0x0028: 0xa5ef5ecff35fd68f
0x00007fffffffd6a0│+0x0030: 0x00007fffffffd788  →  0x00007fffffffdc20  →  "Compiled-1688545393[...]"
0x00007fffffffd6a8│+0x0038: 0x0000000000000001
──────────────────────────────────────────────────────── code:x86:64 ────
   0x555555555255 <main+00ec>      mov    eax, 0x0
   0x55555555525a <main+00f1>      call   0x555555555030 <printf@plt>
   0x55555555525f <main+00f6>      mov    eax, 0x0
 → 0x555555555264 <main+00fb>      leave
   0x555555555265 <main+00fc>      ret
   0x555555555266                  add    BYTE PTR [rax], al
   0x555555555268 <_fini+0000>     sub    rsp, 0x8
   0x55555555526c <_fini+0004>     add    rsp, 0x8
   0x555555555270 <_fini+0008>     ret
──────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "Compiled-168854", stopped 0x555555555264 in main (), reason: SIGBUS
────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555264 → main()
```
OK! Normally at this point we should get the flag printed out, but this time we can't see it! Is it `gef`? Is it us? Maybe there is no flag? None of them! This time the program is taunting us! It's hiding the answers. But . . .

#### <p style="color: red;"> Failure is not an option! </p>

Let's analyze `main` function we had earlier. With a bit of Caffeine `main` will spill the beans!
```diff
gef➤  disassemble main
Dump of assembler code for function main:

    Section 1: Standard function setup that creates the stack frame.
+   0x0000000000001169 <+0>:     push   rbp
+   0x000000000000116a <+1>:     mov    rbp,rsp
+   0x000000000000116d <+4>:     sub    rsp,0x40

    Section 2: A misdirection that manually builds the string "StringsIsForNoobs" on the stack. The rabbit hole!
+   0x0000000000001171 <+8>:     movabs rax,0x4973676e69727453
+   0x000000000000117b <+18>:    movabs rdx,0x626f6f4e726f4673
+   0x0000000000001185 <+28>:    mov    QWORD PTR [rbp-0x40],rax
+   0x0000000000001189 <+32>:    mov    QWORD PTR [rbp-0x38],rdx
+   0x000000000000118d <+36>:    mov    WORD PTR [rbp-0x30],0x73

    Section 3: Calls fwrite to print the Password prompt to the screen.
+   0x0000000000001193 <+42>:    mov    rax,QWORD PTR [rip+0x2e96]        # 0x4030 <stdout@GLIBC_2.2.5>
+   0x000000000000119a <+49>:    mov    rcx,rax
+   0x000000000000119d <+52>:    mov    edx,0xa
+   0x00000000000011a2 <+57>:    mov    esi,0x1
+   0x00000000000011a7 <+62>:    lea    rax,[rip+0xe56]        # 0x2004
+   0x00000000000011ae <+69>:    mov    rdi,rax
+   0x00000000000011b1 <+72>:    call   0x1060 <fwrite@plt>

    Section 4: Calls 'scanf' to get user input, using the vulnerable format string "DoYouEven%sCTF".
    Already Checked!
+   0x00000000000011b6 <+77>:    lea    rax,[rbp-0x20]
+   0x00000000000011ba <+81>:    mov    rsi,rax
+   0x00000000000011bd <+84>:    lea    rax,[rip+0xe4b]        # 0x200f
+   0x00000000000011c4 <+91>:    mov    rdi,rax
+   0x00000000000011c7 <+94>:    mov    eax,0x0
+   0x00000000000011cc <+99>:    call   0x1050 <__isoc99_scanf@plt>

    Section 5: Two 'strcmp' checks against junk data (at 0x201e) meant to be a rabbit hole.
    We Successfully avoided it!
+   0x00000000000011d1 <+104>:   lea    rax,[rbp-0x20]
+   0x00000000000011d5 <+108>:   lea    rdx,[rip+0xe42]        # 0x201e
+   0x00000000000011dc <+115>:   mov    rsi,rdx
+   0x00000000000011df <+118>:   mov    rdi,rax
+   0x00000000000011e2 <+121>:   call   0x1040 <strcmp@plt>
+   0x00000000000011e7 <+126>:   test   eax,eax
+   0x00000000000011e9 <+128>:   js     0x1205 <main+156>
+   0x00000000000011eb <+130>:   lea    rax,[rbp-0x20]
+   0x00000000000011ef <+134>:   lea    rdx,[rip+0xe28]        # 0x201e
+   0x00000000000011f6 <+141>:   mov    rsi,rdx
+   0x00000000000011f9 <+144>:   mov    rdi,rax
+   0x00000000000011fc <+147>:   call   0x1040 <strcmp@plt>
+   0x0000000000001201 <+152>:   test   eax,eax
-   0x0000000000001203 <+154>:   jle    0x124b <main+226>

    Section 6: Another strcmp check, comparing input to what!?
    A suspicious one! We should look into this one too!
+   0x0000000000001205 <+156>:   lea    rax,[rbp-0x20]
+   0x0000000000001209 <+160>:   lea    rdx,[rip+0xe1b]        # 0x202b
+   0x0000000000001210 <+167>:   mov    rsi,rdx
+   0x0000000000001213 <+170>:   mov    rdi,rax
+   0x0000000000001216 <+173>:   call   0x1040 <strcmp@plt>

    Section 7: Failure path if the password was not equal.
+   0x000000000000121b <+178>:   test   eax,eax
-   0x000000000000121d <+180>:   jne    0x1235 <main+204>
    We bypassed this jne and started Section 8 below.

    Section 8: The success path which loads to Correct! and calls printf.
    We successfully jumped here by crashing the program with our payload!
+   0x000000000000121f <+182>:   lea    rax,[rip+0xe0b]        # 0x2031
+   0x0000000000001226 <+189>:   mov    rdi,rax
+   0x0000000000001229 <+192>:   mov    eax,0x0
+   0x000000000000122e <+197>:   call   0x1030 <printf@plt>
+   0x0000000000001233 <+202>:   jmp    0x125f <main+246>

    Section 9: The failure printing Try again!.
+   0x0000000000001235 <+204>:   lea    rax,[rip+0xdfe]        # 0x203a
+   0x000000000000123c <+211>:   mov    rdi,rax
+   0x000000000000123f <+214>:   mov    eax,0x0
+   0x0000000000001244 <+219>:   call   0x1030 <printf@plt>
+   0x0000000000001249 <+224>:   jmp    0x125f <main+246>
+   0x000000000000124b <+226>:   lea    rax,[rip+0xde8]        # 0x203a
+   0x0000000000001252 <+233>:   mov    rdi,rax
+   0x0000000000001255 <+236>:   mov    eax,0x0
+   0x000000000000125a <+241>:   call   0x1030 <printf@plt>

    Section 10: Standard function cleanup that restores the stack and returns.
+   0x000000000000125f <+246>:   mov    eax,0x0
+   0x0000000000001264 <+251>:   leave
+   0x0000000000001265 <+252>:   ret
End of assembler dump.
```
To sum it up, if we follow the execution of the program, we notice that on our first catch `jne` got our attention and we bypassed it. But the password was not there. So now we are looking for another section to execute to find the password.

The next one is the `jle` which is `Jump if Less Than or Equal` and is not letting us to execute the line after that. But we are the Boss now remember?!

#### Jump if Less Than or Equal
Since we already Crashed the program we don't need to do it again for `jle`, we can just read the registers when the program crashed.

So let's run the program again with `r < payload.txt` as we did before for `jne`. And then we see what is inside Section 6 above.

We should add the `Relative Addresses` we have in `disassemble main` to our `Base Address`:
```bash
0x555555554000 (Base) + 0x1209f (Offset) = 0x555555555209 (Absolute)
```
Ok let's see what's inside the `rdx,[rip+0xe1b]`:
```bash
gef➤  x/s 0x555555555209
0x555555555209 <main+160>:      "H\215\025\033\016"
```
That is not what we were expecting! (This is just the raw machine code bytes for the `lea` instruction)

Well, look at Section 6 again, anything suspicious? You gussed it! Thanks to `Gef!` the `0x202b` is staring at us! 
Let's do the math for this:
```bash
0x555555554000 (Base) + 0x202b (Offset) = 0x55555555602b (Absolute)
```
Let's check this one:
```bash
gef➤  x/s 0x55555555602b
0x55555555602b: "_init"
```
Well! At least something readable!!!
```bash
0x555555555209 is the address of the INSTRUCTION (the code).
0x55555555602b is the address of the DATA (the string) that the instruction points to.
```

You might ask yourself what the hell ! We looked everywhere ! But where is the password ?!

This is where we sit down and try to put the pieces of the puzzle together!

## 3. Final Flag
Let's review eveything we had:
* We found three separate `strcmp` (string compare) functions, but the first two were misdirections.
* The third and final strcmp (at `<main+173>`) was the only one that could lead to the `Correct!` message.
* Right before this call, the assembly code at `<main+160>` loads a pointer to a string from the relative address `0x202b`.
* This string, which it compares our input against, is must be the real password!
* By examining the data at that specific address using `gef` (`x/s [base_address] + 0x202b`), we found it contained the string `_init`. 
* This proves `_init` should be the secret we were looking for.
* Our discoveries also explain the purpose of the unusual scanf format string, `DoYouEven%sCTF` which we found earlier.
* The program isn't just checking for `_init`. It's parsing the input based on that specific format.
* The `DoYouEven` part acts as a required prefix. The `%s` then reads the next block of text.
* Our `_init` was inside the buffer at `[rbp-0x20]`. This is the same buffer that the crucial `strcmp` check reads from.
* Therefore! The complete and correct input to solve the challenge isn't an exploit, but simply adding the secret to the prefix needed.
* `DoYouEven` plus `_init`! This perfectly satisfies both the scanf format and the final password check.

---
<details>
  <summary>The Final Flag:</summary>

  * `DoYouEven` + `_init` = **`DoYouEven_init`**

</details>

---
Running the program:
```bash
❯ ./Compiled-1688545393558.Compiled
Password: [Final Flag]
Correct!
```

That's it!

---

There are other methods to solve the challenge using `Ghidra`, `ltrace` or a weapon of your choice!

But i tried to explain it with the help of `Gef` which is a plugin installed on `Gdb`.

<p style="color: green;"> Hope you learned something new! GL! </p>

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
