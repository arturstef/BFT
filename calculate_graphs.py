import math

def falling_factorial_1(n, k): # n! / (n - k)!
    result = 1
    for i in range(k):
        result *= (n - i)
    return result


#number of set opinions in the Lamport algorithm
def calculate_Op(n, d):
    result = 2 * (n - 1)
    for k in range(2, d + 1):
        result += falling_factorial_1(N - 1, k)
    return result

#number of messages in the Lamport algorithm
def calculate_Mes(n, d): 
    result = n-1
    for k in range(1, d + 1):
        result += falling_factorial_1(n - 1, k + 1)
    return result

#number of steps in the Lamport algorithm
def calculate_St(n, d):
    result = 1
    for k in range(1, d + 1):
        result += falling_factorial_1(n - 1, k)
    return result

def calculate_Lamport(n, d):
    if(n-d < 2 or n < 3 or d < 1):
        print('Error: Bad parameters for Lamport algorithm.')
        return 
    messages, opinions, steps = calculate_Mes(n, d), calculate_Op(n, d), calculate_St(n, d)
    print(f'Lamport algorithm: Number of messages: {messages}, number of set opinions: {opinions}, number of steps: {steps}')

def calculate_King(n, k):
    if(n < 3 or k < 1):
        print('Error: Bad parameters for King algorithm.')
        return
    messages, opinions, steps = n* (n-1) * k, n * k, k
    print(f'King algorithm: Number of messages: {messages}, number of set opinions: {opinions}, number of steps: {steps}')

def calculate_PBFT(n, k):
    if(n < 3 or k < 1):
        print('Error: Bad parameters for PBFT algorithm.')
        return
    steps = 5 * k
    messages = k * (1 + (n-2) + (n-2)*(n-3) + (n-1)*(n-2)+ (n-1))
    opinions = k * ((n-1) + (n-1)) + 1
    print(f'PBFT algorithm: Number of messages: {messages}, number of set opinions: {opinions}, number of steps: {steps}')

# compare number of operations on a full graph with n nodes and t max traitors
def compare_operations_number(n, t):
    calculate_Lamport(n, 2)
    calculate_King(n, t)
    calculate_PBFT(n, t)

# data
N = 50
t = 12

compare_operations_number(N, t)