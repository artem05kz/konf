import json
import re
import sys
from math import pow

# Функция для вычисления выражений в постфиксной нотации
def calculate_expression(tokens, variables):
    stack = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in variables:
            stack.append(variables[token])
        elif token == '+':
            stack.append(stack.pop() + stack.pop())
        elif token == '-':
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif token == '*':
            stack.append(stack.pop() * stack.pop())
        elif token == 'pow':
            exponent = stack.pop()
            base = stack.pop()
            stack.append(pow(base, exponent))
        elif token == 'max':
            stack.append(max(stack.pop(), stack.pop()))
    return stack[0]

# Функция для обработки значений с проверкой на постфиксное выражение
def process_value(value, variables):
    # Если значение начинается с "@", то это постфиксное выражение
    if value.startswith("@(") and value.endswith(")"):
        # Убираем "@(" и ")" и разбиваем на части
        expression = value[2:-1].split()
        # Вычисляем значение выражения
        return calculate_expression(expression, variables)
    else:
        # Возвращаем числовое значение, если это число
        return int(value)

# Функция для обработки входного файла
def parse_file(input_file_path):
    variables = {}

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            # Парсим строки с объявлением переменной и выражением
            if re.match(r'[_a-zA-Z][_a-zA-Z0-9]*:', line):
                name, value = line.split(':', 1)
                name = name.strip()
                value = value.strip().strip(';')

                # Обрабатываем значение переменной (с проверкой на постфиксное выражение)
                variables[name] = process_value(value, variables)

    return variables

# Запись данных в JSON
def write_to_json(output_file_path, data):
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Основная программа
def main():
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    # Парсим входной файл и выполняем вычисления
    output_data = parse_file(input_file_path)

    # Записываем данные в JSON
    write_to_json(output_file_path, output_data)

if __name__ == "__main__":
    main()
