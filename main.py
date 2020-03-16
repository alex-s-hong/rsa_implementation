"""
Author: Alex Sung-Min Hong
This version has been submitted to Himani Shah directly as NYU Classes does not allow me to resubmit.
"""

import random


# line 133
def line133_generator(num, printing=False):
    random_bits = bin(random.randint(2**31, 2**32))[2:]
    least = random_bits[-1]
    if printing:
        print("b_{}|{}|{}".format(num, random_bits, least))
    return least


def n_generator(printing=False):
    binary = '0' * 25 + '1'
    for i in range(5, 0, -1):
        binary += line133_generator(i, printing=printing)
    binary += '1'
    if printing:
        print("Number|{}|{}".format(int(binary, 2), binary))
    return int(binary, 2)


print("line:133")
n_generator(printing=True)
print()


# line 149 and 155
# 149 for non prime, 155 for prime
def mydivmod(num, divisor):
    # Handle divisor equals to 0 case
    if divisor == 0:
        return False

    if divisor < 0:
        divisor = -divisor
    if num < 0:
        num = -num

    times = 0
    product = 0
    while product + divisor <= num:
        product = divisor * times
        times += 1
    return times-1, num - product


def primality(n: int, a: int, printing=False) -> bool:
    """
    n is decimal representation
    n-1 should be used for miller-robin algorithm
    """
    k = bin(n-1)[2:]
    y = 1
    res = True
    decision_message = ''
    if printing:
        print("{0:<2}|{1:<3}|{2:<4}|{3:<4}|y".format('i', 'xi', 'z','y'))
    for i in range(len(k)):
        if res:
            z = y
            y = mydivmod(y * y, n)[1]
            y1 = y
            # early stopping
            if y == 1 and z != 1 and z != n - 1:
                res = False
                y = ''
                decision_message = '{0} is not a prime because {1}^{2} mod {0} = 1 and {1} != 1 and {1} != {0} - 1'.format(n, z, 2)
            if res and k[i] == '1':
                y = mydivmod(y * a, n)[1]
        if printing:
            print("{0:<2}|{1:<3}|{2:<4}|{3:<4}|{4}".format(len(k)-i-1, k[i], z, y1, y))
        if not res:
            z = y1 = ''

    if res and y != 1:
        res = False
        decision_message = '{0} is not a prime because {1}^{2} mod {0} != 1'.format(n, a, n-1)
    elif res:
        decision_message = '{} is perhaps a prime'.format(n)
    if printing:
        print(decision_message)
    return res


def get_prime(want_prime=True) -> (int, int):
    # create 20 unique 'a's
    a_set = set()
    while True:
        n = n_generator()
        while len(a_set) < 20:
            a = random.randint(1, n - 1)
            a_set.add(a)

        is_prime = True
        for a in iter(a_set):
            is_prime = is_prime and primality(n, a)
            if not want_prime and not is_prime:
                return n, a

        if want_prime and is_prime:
            return n, a


# print line 149: non prime
print("line:149")
(non_prime, non_a) = get_prime(want_prime=False)
print("n = {}, a = {}".format(non_prime, non_a))
primality(non_prime, non_a, printing=True)
print()

# print line 155: prime
print("line:155")
(prime_n, a) = get_prime()
print("n = {}, a = {}".format(prime_n, a))
primality(prime_n, a, printing=True)
print()


# print line 174
def extend_euclidean(p1, p2, printing=True):
    # force p1 > p2
    if p2 > p1:
        p1, p2 = p2, p1
    if printing:
        print("e = ", p2)
        print("{0:<2}|{1:<7}|{2:<7}|{3:<7}|{4:<7}|{5:<6}|ti".format("i","qi","r","ri+1","ri+2","si"))
    i = 0
    r = None
    ri1 = p1
    ri2 = p2
    q = []
    s = [1, 0]
    t = [0, 1]

    def get_s(n):
        if n > 2:
            s.append(s[-2] - q[-2]*s[-1])

    def get_t(n):
        if n > 2:
            t.append(t[-2] - q[-2]*t[-1])

    while ri2 != 0:
        i += 1
        r = ri1
        ri1 = ri2
        qi, ri2 = mydivmod(r, ri1)
        get_s(i)
        get_t(i)
        q.append(qi)
        if printing:
            print("{0:<2}|{1:<7}|{2:<7}|{3:<7}|{4:<7}|{5:<6}|{6}".format(i, qi, r, ri1, ri2, s[i-1], t[i-1]))

    i += 1
    r = ri1
    get_s(i)
    get_t(i)
    if printing:
        print("{0:<2}|{1:<7}|{2:<7}|{3:<7}|{4:<7}|{5:<6}|{6}".format(i, "", r, "", "", s[i - 1], t[i - 1]))

    # 1 = s * n + t * e
    return (s[-1], t[-1]) if r == 1 else False

# print line 174 and line 186
# first, get unique p and q then run it on extended Euclidean algorithm
# pick e, and get d from t of eEa. (if negative, put it in 0 < d < n)


# get p and q
# reuse the prime_n that has been calculated to p
p = prime_n
q, _ = get_prime()

while p == q:
    q, _ = get_prime()

#p = 71
#q = 79
n = p * q
pin = (p-1)*(q-1)
e = 3
print("line:174")
while not extend_euclidean(pin, e):
    e += 1
print()

# line 186: get d
s,t = extend_euclidean(pin, e, printing=False)
while t < 0:
    t += pin
print("line:186")
print("d = {}".format(t))
print()

# line 190, organize well which binary representation
print("line:190")
print("p = {}, q = {}, n = {}, e = {}, d = {}".format(p, q, n, e, t))
print("p = {:032}".format(int(bin(p)[2:])))
print("q = {:032}".format(int(bin(q)[2:])))
print("n = {:032}".format(int(bin(n)[2:])))
print("e = {:032}".format(int(bin(e)[2:])))
print("d = {:032}".format(int(bin(t)[2:])))
print()

# line 198 public and private key for Trent

p2, _ = get_prime()
q2, _ = get_prime()

while p2 == q2:
    q2, _ = get_prime()

n2 = p2 * q2
pin2 = (p2-1)*(q2-1)
e2 = 3
while not extend_euclidean(pin2, e2, printing=False):
    e2 += 1

# line 186: get d
s2, t2 = extend_euclidean(pin2, e2, printing=False)
while t2 < 0:
    t2 += pin2

print("line:198")
print("p = {}, q = {}, n = {}, e = {}, d = {}".format(p2, q2, n2, e2, t2))
print("p = {:032}".format(int(bin(p2)[2:])))
print("q = {:032}".format(int(bin(q2)[2:])))
print("n = {:032}".format(int(bin(n2)[2:])))
print("e = {:032}".format(int(bin(e2)[2:])))
print("d = {:032}".format(int(bin(t2)[2:])))
print()

# line 222

########################
#p = 109
#q = 73
#n = 8611
#e = 5
#d = 1685

# r
# 1. get binary representation of ' Alice'
alice = bin(int.from_bytes(' Alice'.encode(), 'big'))[2:]
alice = alice.rjust(48, '0')

# 2. n from Alice's public key
nbin = bin(n)[2:].rjust(32, '0')

# 3. e from Alice's public key
ebin = bin(e)[2:].rjust(32, '0')

r = alice + nbin + ebin


# signature s : h(r) decrypted with Trent’s private key (using fast exponentiation)
# 1. h(r): XOR operation on each bit in 14 bytes of r (even 1 -> 0 else 1)
def one_way_hash(r: str) -> int:
    bit = ''
    for i in range(8):
        tmp = 0
        for j in range(len(r)//8):
            tmp += int(r[j*8 + i])
        if tmp & 1:
            bit += '1'
        else:
            bit += '0'

    return int(bit, 2)


hr = one_way_hash(r) # type: str
#print(int(hr, 2))

def fast_exponent(a, x, n, printing= False): # a^x mod n
    y0 = y = 1
    num = bin(x)[2:]
    if printing:
        print("{0:<2}|{1:<3}|{2:<6}|{3}".format("i", "xi", "y", "y"))
    for k in range(len(num)):
        y0 = y = mydivmod(y*y, n)[1]
        if num[k] == '1':
            y = mydivmod(a*y, n)[1]
        if printing:
            print("{0:<2}|{1:<3}|{2:<6}|{3}".format(len(num) - k -1,  num[k], y0, y))

    return y


signature = fast_exponent(hr, t2, n2)

# signature #############
#n2 = 7957
#e2 = 5
#t2 = 6221

#line 222
print("line:222")
print("r = {}".format(r))
print("h(r) = {}".format(bin(hr)[2:].rjust(32, '0')))
# s should be obtained from h(r) ** d2 (=t2) % n, but it's not as same as the e.g.
print("s = {}".format(bin(signature)[2:].rjust(32, '0')))
print()

# line 224

print("line:224")
print("h(r) = {}, s = {}".format(hr, signature))
# print("recreation through encryption", fast_exponent(signature, e2, n2))
print()


# line 246
# k should be the length of binary representation of n, - 1
k = len(bin(n)[2:])-1


# create random u
def make_u(k):
    res = ''
    for i in range(k):
        res +=line133_generator(i)

    return res

# u should be, 4096 <= u <= 8191
# Choose uk−2, ..., u0 randomly, bit by bit
u = '1' + make_u(k-1) #+ str(random.randint(0,1))

### THIS PROBLEM HAS ERROR, IF K EQUALS TO 12, U CANNOT BE IN 4096 AND 8191, K MUST BE 13 DETERMINISTICALLY
### I'll JUST IGNORE THE RANGE
# make sure u is in the bound
# while not 4096 <= int(u, 2) <= 8191:
#     #print(int(u, 2))
#     u = '1' + make_u(12)


u = u.rjust(32, '0')


print("line:246")
print("k = {}, u = {}".format(k, int(u,2)))
print()

# line 248
print("line:248")
print("u = {}".format(u))
print()

# line 254
hu = one_way_hash(u)
v = fast_exponent(hu, t, n)

print("line:254")
print("u = {}, h(u) = {}, v = {}, Ev = {}".format(int(u, 2), hu, v, fast_exponent(v, e, n)))
print()

print("line:257")
fast_exponent(v, e, n, printing=True)
