import time
a = 0
b = 1
while True:
    c = a + b
    a = b
    b = c
    print(b%50)
    # time.sleep(0.1)
