# type: ignore

def convert_base(n_digits, b1, b2):
    result = []
    for d in n_digits:
        result = multiply_by_base(result, b1, b2)
        result = add_digit(result, d, b2)
    return result[::-1] if result else [0]

def multiply_by_base(number, base, target_base):
    carry = 0
    result = []
    for digit in number:
        product = digit * base + carry
        res_digit = product % target_base
        carry = product // target_base
        result.append(res_digit)
    while carry > 0:
        result.append(carry % target_base)
        carry = carry // target_base
    return result

def add_digit(number, digit, target_base):
    carry = digit
    result = []
    for d in number:
        total = d + carry
        res_digit = total % target_base
        carry = total // target_base
        result.append(res_digit)
        if carry == 0:
            result += number[len(result):]
            break
    while carry > 0:
        result.append(carry % target_base)
        carry = carry // target_base
    return result

print(convert_base([2, 1], 3, 2))