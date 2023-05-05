import numpy as np

arc = 12

generated_numbers = np.array([])
allowed_numbers = np.array([])
allowed_numbers_corrected = np.array([])

def arc_generator(arc, generated_numbers):
    for i in range(2**arc):
        number = i
        number = bin(number).replace('0b', '')
        number = int(number)
        number = f"{number:012}"
        generated_numbers = np.append(generated_numbers, number)
    return generated_numbers

# 2) отсортировать все числа
#   б) сумма всех цифр == 0
#   в) первая цифра == 1, последняя цифра == 0
#   г) последовательная сумма не превосходит 3
#   д) заменить все -1 на 0

def Is_Katalan_Number(generated_numbers, allowed_numbers):
    test = np.array([])
    for number in generated_numbers:
        # number = generated_numbers[i]
        number = list(map(int, str(number)))
        number = np.array([-1 if elem == 0 else elem for elem in number])

        if sum(number) == 0:
            test = np.append(test, number)
            if check_sum_is_correct(number) == True:
                number = np.array([0 if elem == -1 else elem for elem in number])
                number = str(''.join(map(str, number)))
                allowed_numbers = np.append(allowed_numbers, number)

    return allowed_numbers

def check_sum_is_correct(number):
    summ = 0
    for digit in number:
        if summ > 3 or summ < 0:
            return False
        else:
            summ += digit
    return True

def beautiful_number(number):
    counter = 0
    new_number = []
    # summ = number[counter]
    summ = 0
    for digit in number:
        if summ != 0:
            summ += digit
            new_number.append(digit)
        else:
            new_number.append(' | ')
            new_number.append(digit)
            summ = number[counter]
    return new_number

generated_numbers = arc_generator(arc, generated_numbers)

allowed_numbers = Is_Katalan_Number(generated_numbers, allowed_numbers)

for number in allowed_numbers:
    number = list(map(int, str(number)))
    number = np.array([-1 if elem == 0 else elem for elem in number])

    number = beautiful_number(number)

    number = np.array([0 if elem == -1 else elem for elem in number])
    number = str(''.join(map(str, number)))

    allowed_numbers_corrected = np.append(allowed_numbers_corrected, number)

# print(allowed_numbers_corrected)

numbers_with_zero = []
numbers_with_one = []
numbers_with_two = []
numbers_with_three = []
numbers_with_four = []
numbers_with_five = []
numbers_with_six = []

def numbers_sort(allowed_numbers_corrected):
    for number in allowed_numbers_corrected:
        if str(number).count('|') == 0:
            numbers_with_zero.append(number)
        elif str(number).count('|') == 1:
            numbers_with_one.append(number)
        elif str(number).count('|') == 2:
            numbers_with_two.append(number)
        elif str(number).count('|') == 3:
            numbers_with_three.append(number)
        elif str(number).count('|') == 4:
            numbers_with_four.append(number)
        elif str(number).count('|') == 5:
            numbers_with_five.append(number)
        elif str(number).count('|') == 6:
            numbers_with_six.append(number)

numbers_sort(allowed_numbers_corrected)

for number in numbers_with_zero:
    print(str(number))
for number in numbers_with_one:
    print(str(number))
for number in numbers_with_two:
    print(str(number))
for number in numbers_with_three:
    print(str(number))
for number in numbers_with_four:
    print(str(number))
for number in numbers_with_five:
    print(str(number))
for number in numbers_with_six:
    print(str(number))