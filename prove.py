import pickle
import torch

with open("fiducial_first_order", "rb") as f:
    for i in range(3):
        x = pickle.load(f)
        print(f"{i}:{x}")
print(x)