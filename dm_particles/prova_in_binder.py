import threading

def printit():
  threading.Timer(5.0, printit).start()
  print("Hello, World!")

def writeit():
  threading.Timer(5.0, writeit).start()
  with open("./data.dat", "a") as f:
    f.write("Hello world :)")

writeit()