import numpy as np
import matplotlib.pyplot as plt

""" 
# Basic Tutorial
plt.scatter([1, 2, 3, 4], [1, 4, 9, 16])

x = np.arange(0, 10, 0.01)
y = np.sin(2 * np.pi * x)
plt.plot(x, y)

plt.show() """

# prints parity of a number
def parity(number):
    if number % 2 == 0:
        print("Deine Zahl ist gerade!")
    else:
        print("Deine Zahl ist ungerade.")

# prints sin & plots cos of an input scale
def sinAndCos(scale):
    range = np.arange(0, scale, 0.01)
    sin = np.sin(scale)
    cos = np.cos(2 * np.pi * range)

    print(f"The sinus of your scale is: {sin}")
    plt.plot(range, cos)
    plt.show()

# returns n numbers of the fibonacci sequence
def fibonacci(n: int):
    range = np.arange(1, n+1)

    sqrt_five = np.sqrt(5)
    alpha = (1 + sqrt_five) / 2
    beta = (1- sqrt_five) / 2

    fib = np.rint(((alpha ** n ) - (beta ** n)) / sqrt_five)

    print(f"The first {n} numbers of the Fibonacci sequence are {fib}")

# prints the biggest number in a list
def biggestNumber(in_list: list):
    sorted = list.sort
    print(f"The biggest number in your list is {sorted[-1]}")

################################

parity(382)
sinAndCos(4)
fibonacci(382)
random_list = np.random.randint(0, 382, 20)
biggestNumber(random_list)