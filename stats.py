import math

def mean(numbers):
    return sum(numbers) / len(numbers)

def median(numbers):
    length = len(numbers)
    mid = (length // 2) - 1
    
    if length % 2 == 0:
        sum = numbers[mid] + numbers[mid + 1]
        return sum / 2
    else:
        return numbers[mid + 1]
    
def typical(numbers):
    numbers_set = set()
    duplicates = {}
    for n in numbers:
        duplicates[n] = 1

    for n in numbers:
        length = len(numbers_set)
        numbers_set.add(n)

        if len(numbers_set) == length:
            duplicates[n] = duplicates[n] + 1

    if len(numbers_set) == len(numbers):
        return None

    typical_values = []
    i = 0
    for value in duplicates:
        i += 1
        if i == 1:
            typical_values.append(value)
            continue

        if duplicates[value] > duplicates[typical_values[0]]:
            typical_values.clear()
            typical_values.append(value)
        elif duplicates[value] == duplicates[typical_values[0]]:
            typical_values.append(value)
    
    return typical_values

def width(numbers):
    return max(numbers) - min(numbers)

def varians(numbers):
    average = mean(numbers)
    
    sum = 0
    for n in numbers:
        sum += (n - average) ** 2
    
    return sum / (len(numbers) - 1)

def stdev(numbers):
    var = varians(numbers)
    return math.sqrt(var)

def get_dataset(dataset):
    print(f"{GREENBLUE}Input dataset:{RESET}")

    while True:
        user_in = input()
        if user_in == '':
            if len(dataset) > 2:
                break
            else:
                print("Please enter at least three numbers.", 
                    f"You have entered {len(dataset)} numbers.")
                
        if user_in.isdigit():
           dataset.append(float(user_in))
        else:
            user_in += ','
            d = {"value": '', "frequency": ''}
            key = "value"

            for c in user_in:
                if c.isdigit() or c == '.' or c =='-':
                    d[key] += c
                elif c == ',' or c == ';':
                    data = float(d["value"])

                    if key == "frequency":
                        freq = int(d["frequency"])
                        d["frequency"] = ''
                        key = "value"
                    else:
                        freq = 1
                        data = float(d["value"])

                    for _ in range(freq):
                        dataset.append(data)
                    
                    d["value"] = ''
                elif c == 'x':
                    key = "frequency"
    
    if user_in != '\n' and user_in != '':
        print()

def boxplot(numbers):
    length = len(numbers)
    mid = length // 2
 
    if length % 2 == 0:
        lower_half = numbers[:mid]
        upper_half = numbers[mid:]
    else:
        lower_half = numbers[:mid]
        upper_half = numbers[mid + 1:]

    q1 = median(lower_half)
    q2 = median(numbers)
    q3 = median(upper_half)

    outlier_limit = 1.5 * (q3 - q1)
    outliers = []
    min_n = None
    for n in lower_half:
        if (q2 - n) > outlier_limit:
            outliers.append(n)
        else:
            min_n = n
            break

    upper_half.reverse()
    max_n = None
    for n in upper_half:
        if (n - q3) > outlier_limit:
            outliers.append(n)
        else:
            max_n = n
            break
    
    if not min_n:
        min_n = numbers[0]
    if not max_n:
        max_n = numbers[-1]

    return min_n, q1, q2, q3, max_n, outliers

def gauss(numbers, st_dev=0):    
    '''
    Returns a normal distributed list of values based on the mean
    and standard deviation of the values provided or the mean and 
    standard deviation provided explicitly.

    takes either:
        - a list of int/float
        - one mean as int/float and a standard deviation int/float.
    '''
    mu = mean(numbers) if isinstance(numbers, list) else numbers
    sigma = stdev(numbers) if st_dev == 0 else st_dev
    
    return [mu + sigma * i for i in range(-2, 3)]

def print_gauss(numbers):
    values = []
    max_length = 0
    for n in numbers:
        num_string = str(round(n, 2))

        values.append(num_string)

        length = len(num_string)
        max_length = length if length > max_length else max_length

    top_padding = 22   
    if max_length > 6:
        top_padding += 30
    if max_length > 12:
        top_padding += 30
    if max_length > 15:
        for i, value in enumerate(values):
            values[i] = value[:4] + '..'
        top_padding = 22
    
    padding = 4
    print(PURPLE)
    print(" " * (top_padding + padding), "__")
    x = top_padding - 7
    iterations = math.ceil((x) / 3)
    y = 4
    z = 3
    for i in range(iterations):
        print(" " * (x + padding), "_" * (2 + z), " " * y, "_" * (2 + z))
        x -= 3
        y += 4
        z += 1

    left = " " * (x + padding)
    neg2_to_neg1 = " " * (2 + z - 1 - len(values[0]))
    mid1 = " " * ((y//2) - len(values[1]) - (len(values[2]) // 2) - 3) 
    mid2 = " " * ((y//2) - (len(values[2]) // 2) - 3) 
    pos1_to_pos2 = " " * (2 + z - len(values[3]) - 3)
    print(left, values[0], neg2_to_neg1, values[1], mid1, values[2], mid2, values[3], pos1_to_pos2, values[4])

    neg2_left = " " * (((2 + z - 1) //2) - 4 + padding)
    print(LBLUE, end='')
    print("2.3%", neg2_left, "13.6%")
    print(f'{RESET}\n')
    
def main():
    dataset = []
    get_dataset(dataset)
    dataset.sort()

    print(f"{LBLUE}Dataset:{RESET}", dataset)
    print(f"{LBLUE}Average:{RESET}", mean(dataset))
    print(f"{LBLUE}Median:{RESET}", median(dataset))
    print(f"{LBLUE}Typical Value:{RESET}", typical(dataset))
    print(f"{LBLUE}Variation Width:{RESET}", width(dataset))
    print(f"{LBLUE}Variance:{RESET}", varians(dataset))
    print(f"{LBLUE}Standard Deviation:{RESET}", stdev(dataset))
    
    min_n, q1, q2, q3, max_n, outliers = boxplot(dataset)
    print('\n')
    print(f"{LBLUE}Boxplot:{RESET} {min_n}--[ {q1} ]{q2}[ {q3} ]--{max_n} \n\tOutliers: {outliers}\n")
    
    gauss_curve = gauss(dataset)
    if gauss_curve:
        print("\t\t\tWARNING! Data may not actually be evenly distributable.\n")
        print(f"{LBLUE}Gauss Curve:{RESET} {gauss_curve}")
        print_gauss(gauss_curve)
    print(LBLUE, end='')

if __name__ == '__main__':
    LBLUE = "\033[38;2;10;50;200m"
    GREENBLUE = "\033[38;2;10;180;170m"
    RESET = "\033[0m"
    PURPLE = "\033[38;2;200;50;100m"
    main()