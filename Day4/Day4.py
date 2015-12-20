
from hashlib import md5
import time


#%%

input_string = "bgvyzdsv"
print("Input: {}".format(input_string))

def get_hash(inputstring):
    input_raw = inputstring.encode("utf-8")
    input_hash = md5(input_raw)
    input_hash_readable = input_hash.hexdigest()
    return input_hash_readable
    
def check_ready_5(input_hash_readable):
    return input_hash_readable[:5] == "00000"
    
def check_ready_6(input_hash_readable):
    return input_hash_readable[:6] == "000000"

#%% part 1

print("Part 1, 5 zeroes")
print(time.ctime())

check = False
i=0
while check == False:
    i+=1
    input_hash_readable = get_hash(input_string+str(i))
    check = check_ready(input_hash_readable)
    
    #print(input_string+str(i), input_hash_readable, check)

print(input_string+str(i), input_hash_readable, check)
print(time.ctime())
print("====")

#%% bug preventing pause

time.sleep(5)

#%% part 2

print("Part 2, 6 zeroes")
print(time.ctime())

check2 = False
i2=0
while check2 == False:
    i2+=1
    input_hash_readable2 = get_hash(input_string+str(i2))
    check2 = check_ready_6(input_hash_readable2)
    #print(input_string+str(i), input_hash_readable, check)

print(input_string+str(i2), input_hash_readable2, check2)
print(time.ctime())
