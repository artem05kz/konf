import json
import re
import argparse

class ConfigTranslator:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.variables = {}  # Для хранения констант

    def parse(self):
        """Читает файл конфигурации и выполняет обработку"""
        with open(self.input_file, 'r') as f:
            config = f.read()
        
        # Парсим содержимое файла
        parsed_data = self.process_config(config)
        
        # Сохраняем результат в JSON файл
        self.save_to_json(parsed_data)

    def process_config(self, config):
        """Рекурсивно обрабатывает конфигурацию, переводя её в словари Python"""
        result = {}
        lines = config.splitlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Парсинг константных выражений
            if re.match(r"[a-zA-Z][a-zA-Z0-9]*\s*:", line):  # Только английские буквы и цифры
                key, value = map(str.strip, line.split(":", 1))
                if value.startswith("@(") and value.endswith(")"):
                    result[key] = self.evaluate_expression(value[2:-1].strip())
                else:
                    result[key] = self.parse_value(value.strip(";"))
            
            # Парсинг словарей
            elif line.startswith("{") and line.endswith("}"):
                result.update(self.process_dictionary(line))

        return result

    def process_dictionary(self, dictionary_str):
        """Обрабатывает строку, содержащую словарь"""
        dictionary_str = dictionary_str.strip("{} ")
        dictionary = {}
        
        items = dictionary_str.split(";")
        for item in items:
            if ":" in item:
                key, value = map(str.strip, item.split(":", 1))
                if not re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", key):
                    raise ValueError(f"Некорректное имя переменной: {key}")
                dictionary[key] = self.parse_value(value)

        return dictionary

    def parse_value(self, value):
        """Обрабатывает отдельное значение (число или словарь)"""
        if value.isdigit():
            return int(value)
        elif value.startswith("{") and value.endswith("}"):
            return self.process_dictionary(value)
        elif value in self.variables:
            return self.variables[value]
        else:
            return value  # В случае строки

    def evaluate_expression(self, expression):
        """Вычисляет постфиксное выражение"""
        tokens = re.split(r'\s+', expression)  # Разделяет по пробелам
        stack = []
        
        for token in tokens:
            if token.isdigit():  # Число
                stack.append(int(token))
            elif token in self.variables:  # Переменная
                stack.append(self.variables[token])
            elif token == '+':
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif token == '-':
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token == '*':
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            elif token == 'pow':
                b, a = stack.pop(), stack.pop()
                stack.append(pow(a, b))
            elif token == 'max':
                stack.append(max(stack))
            else:
                raise ValueError(f"Неизвестный токен в выражении: {token}")
        
        return stack.pop()

    def save_to_json(self, data):
        """Сохраняет результат в JSON файл"""
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=4)

# Основной блок программы
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ConfigTranslator: Преобразует конфигурационный файл в JSON.")
    parser.add_argument('input_file', type=str, help="Путь к входному файлу конфигурации")
    parser.add_argument('output_file', type=str, help="Путь к выходному файлу JSON")
    
    args = parser.parse_args()
    
    translator = ConfigTranslator(args.input_file, args.output_file)
    translator.parse()
