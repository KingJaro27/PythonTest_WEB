def add_numbers(a, b):
    return a + b


input_str = input()
a, b = map(int, input_str.split(','))
print(add_numbers(a, b))