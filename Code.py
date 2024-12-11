def sum_of_digits(number):
    # Convert the number to its absolute value to handle negative numbers
    number = abs(number)
    # Calculate the sum of digits
    return sum(int(digit) for digit in str(number))


num = int(input("Enter a number: "))
print(f"The sum of the digits is: {sum_of_digits(num)}")