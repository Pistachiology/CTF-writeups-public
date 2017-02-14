
import struct

def p64(mm):
    return struct.pack("<Q", mm)

A = ['0111','0000','0100', '0101', '0100', '0111', '0111', '0000', '0100', '0010', '0111', '0101']

def do_enc(st):
    storage = [0, 0, 0]
    o = []
    f = ''.join(map(lambda x: "{:08b}".format(ord(x)), st))
    for b in f:
        o.append( "{0}{1}{2}{3}".format(0 ,int(b) ^ 1,  storage[0] ^ storage[1] ^ storage[2] ^ 1 ^ int(b), int(b) ^ storage[0] ^ storage[2] ^ 1))
        storage = [int(b)] +  storage[:2]
    return o
    
data = p64(0x0007070405040007) + p64(0x0504030606000204) + p64(0x0106000106030004) + p64(0x0305070106000207) + p64(0x0501000106000204) + p64(0x0707070405040306) + p64(0x0103000405040007) + p64(0x0704060603030605) 

d = map(lambda x: "{:04b}".format(ord(x)), data)
d = ''.join(d)
user = ''
temp = ''
for i in range(0, len(d), 4):
    temp += str(int(d[i+1]) ^ 1)
    if len(temp) == 8:
        user += chr(int(temp, 2))
        temp = ''

print ((user))

pw = p64(0x5d6a345c1b2e5612) + p64(0x6f34671c5b0f2973) + p64(0x543570193a1e5011) + p64(0x0000002e472d453f)
pw = pw.rstrip('\x00')
pas =''
i = 0
for p in pw:
        pas += chr(ord(p) ^ ord(user[i % len(user)])) 
        i += 1
print pas
