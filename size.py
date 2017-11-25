import datetime
import delorean
import arrow
import pendulum
import numpy as np

def get_vm_size():
    with open("/proc/self/status") as file:
        for line in file:
            if line.startswith("VmSize"):
                parts = line.strip().split()
                assert parts[2] == "kB"
                return int(parts[1]) * 1024


_results = []
N = 234567

s0 = get_vm_size()
_results.append([ None for _ in range(N) ])
s1 = get_vm_size()
print("None: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ np.datetime64("now") for _ in range(N) ])
s1 = get_vm_size()
print("datetime64: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ datetime.datetime.now() for _ in range(N) ])
s1 = get_vm_size()
print("datetime: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ delorean.Delorean() for _ in range(N) ])
s1 = get_vm_size()
print("Delorean: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ arrow.now() for _ in range(N) ])
s1 = get_vm_size()
print("Arrow: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ pendulum.now() for _ in range(N) ])
s1 = get_vm_size()
print("Pendulum: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append(np.arange(N).astype("datetime64[ns]"))
s1 = get_vm_size()
print("datetime64: {} bytes each".format((s1 - s0) // N))

N = 567890

s0 = get_vm_size()
_results.append([ pendulum.now() for _ in range(N) ])
s1 = get_vm_size()
print("Pendulum: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ arrow.now() for _ in range(N) ])
s1 = get_vm_size()
print("Arrow: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ delorean.Delorean() for _ in range(N) ])
s1 = get_vm_size()
print("Delorean: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ np.datetime64("now") for _ in range(N) ])
s1 = get_vm_size()
print("datetime64: {} bytes each".format((s1 - s0) // N))

s0 = get_vm_size()
_results.append([ datetime.datetime.now() for _ in range(N) ])
s1 = get_vm_size()
print("datetime: {} bytes each".format((s1 - s0) // N))

