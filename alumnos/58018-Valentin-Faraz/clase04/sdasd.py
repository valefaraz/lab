import os

pid = os.fork()
if pid == 0:
    print("soy el hijo")

print(pid)
