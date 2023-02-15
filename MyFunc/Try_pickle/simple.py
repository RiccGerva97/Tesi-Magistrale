import numpy as np
import pickle
import os

# def read_function(in_file, N):
#     file = open(in_file, 'rb')
#     i = 0
#     # while True:
#     #     i+=1
#     #     print("i: ", i)
#     #     try:
#     #         print(pickle.load(file), "\n")
#     #     except EOFError:
#     #         break

#     # data = pickle.load(file)

#     for i in range(N):
#         print(pickle.load(file), "\n")

#     file.close()
#     # print("RESULTS:\n", data, "\n")

def write_function(out_file, a):
    A = a**2
    file = open(out_file, 'ab')
    pickle.dump(A, file)
    file.close()
    print(a, " ", A)
    #read_function(out_file)

def Load(in_file, N):
    print(N)
    d = np.zeros(N+1)
    with open(in_file, 'rb') as f:
        while True:
            try:
                a = pickle.load(f)
                # print(np.shape(a))
                d += a
            except EOFError:
                break
            # else:
            #    d += a
    print("\nHERE d:\n",  d)


os.remove('out_file')
results = 'out_file'
dat = np.arange(6)
dats = np.array((dat, dat+1, dat+2, dat+3, dat+4))
print(dats, "\n")

for i in range(len(dats)):
    write_function(results, dats[i])
print("\n\n")
# read_function(results, len(dats))
Load(results, len(dats))