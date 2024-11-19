import struct
import csv

class Assembler:
    def __init__(self, path_to_program: str, path_to_binary: str, path_to_log_file: str):
        self.FREE_MEMORY_ADDRESS = -1
        self.NAMESPACE = {}
        self.INPUT_FILE = path_to_program
        self.OUTPUT_FILE = path_to_binary
        self.LOG_FILE = path_to_log_file
        open(self.OUTPUT_FILE, 'wb').close()
        open(self.LOG_FILE, 'w').close()
        self.LOG_ARRAY = []

    def get_free_address(self):
        self.FREE_MEMORY_ADDRESS += 1
        return self.FREE_MEMORY_ADDRESS

    def add_var_to_namespace(self, var: str) -> int:
        address = self.get_free_address()
        self.NAMESPACE[var] = address
        return address

    def paginate(self, num: int, length: int) -> str:
        return bin(num)[2:].zfill(length)

    def write_to_binary(self, bytes_data: bytes):
        logged = ", ".join([("0x" + hex(i)[2:]).zfill(4) for i in bytes_data])
        self.log({"bin": logged}, method="append")
        with open(self.OUTPUT_FILE, 'ab') as f:
            f.write(bytes_data)

    # Команда для загрузки константы
    def bin_load_const(self, a: int, b: int, c: int) -> bytes:
        self.log({"A": a, "B": b, "C": c})
        binary_command = f"{self.paginate(a, 5)}{self.paginate(b, 5)}{self.paginate(c, 15)}{'0' * 15}"
        return int(binary_command, 2).to_bytes(5, byteorder="big")

    # Команда для чтения значения из памяти
    def bin_load_from_memory(self, a: int, b: int, c: int) -> bytes:
        self.log({"A": a, "B": b, "C": c})
        binary_command = f"{self.paginate(a, 5)}{self.paginate(b, 5)}{self.paginate(c, 5)}{'0' * 25}"
        return int(binary_command, 2).to_bytes(5, byteorder="big")

    # Команда для записи значения в память
    def bin_store_to_memory(self, a: int, b: int, c: int) -> bytes:
        self.log({"A": a, "B": b, "C": c})
        binary_command = f"{self.paginate(a, 5)}{self.paginate(b, 5)}{self.paginate(c, 15)}{'0' * 10}"
        return int(binary_command, 2).to_bytes(5, byteorder="big")

    # Команда для проверки равенства
    def bin_equality(self, a: int, b: int, c: int, d: int) -> bytes:
        self.log({"A": a, "B": b, "C": c, "D": d})
        binary_command = f"{self.paginate(a, 5)}{self.paginate(b, 5)}{self.paginate(c, 5)}{self.paginate(d, 7)}{'0' * 18}"
        return int(binary_command, 2).to_bytes(5, byteorder="big")

    def log(self, text: dict, method="last"):
        if method == "last":
            self.LOG_ARRAY.append(text)
        elif method == "append":
            self.LOG_ARRAY[-1].update(text)

    def dump_log_csv(self):
        with open(self.LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Command", "Details"])
            for entry in self.LOG_ARRAY:
                for key, value in entry.items():
                    writer.writerow([key, value])

    def run(self):
        with open(self.INPUT_FILE, 'r') as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if parts[0] == "load_const" and len(parts) == 3:
                _, var, value = parts
                address = self.add_var_to_namespace(var)
                binary = self.bin_load_const(12, address, int(value))
                self.write_to_binary(binary)
                
            elif parts[0] == "load_from_memory" and len(parts) == 3:
                _, var1, var2 = parts
                address1 = self.NAMESPACE.get(var1, self.add_var_to_namespace(var1))
                address2 = self.NAMESPACE[var2]
                binary = self.bin_load_from_memory(17, address1, address2)
                self.write_to_binary(binary)
                
            elif parts[0] == "store_to_memory" and len(parts) == 3:
                _, var1, var2 = parts
                address1 = self.NAMESPACE.get(var1, self.add_var_to_namespace(var1))
                address2 = self.NAMESPACE[var2]
                binary = self.bin_store_to_memory(15, address1, address2)
                self.write_to_binary(binary)
                
            elif parts[0] == "equality" and len(parts) == 4:
                _, var1, offset, var2 = parts
                address1 = self.NAMESPACE.get(var1, self.add_var_to_namespace(var1))
                address2 = self.NAMESPACE[var2]
                binary = self.bin_equality(26, address1, address2, int(offset))
                self.write_to_binary(binary)

        self.dump_log_csv()

class Interpreter:
    def __init__(self, path_to_binary: str, path_to_result: str, memory_range: tuple):
        with open(path_to_binary, 'rb') as f:
            self.BINARY = f.read()
        self.MEMORY = [0 for _ in range(32)]
        self.RESULT_FILE = path_to_result
        self.MEMORY_RANGE = memory_range
        open(self.RESULT_FILE, 'w').close()

    def run(self):
        commands = [self.BINARY[i:i+5] for i in range(0, len(self.BINARY), 5)]
        
        for command in commands:
            command_bits = bin(int.from_bytes(command, 'big'))[2:].zfill(40)
            command_type = int(command_bits[:5], 2)
            B = int(command_bits[5:10], 2)
            
            if command_type == 12:
                C = int(command_bits[10:25], 2)
                self.MEMORY[B] = C
            elif command_type == 17:
                C = int(command_bits[10:15], 2)
                self.MEMORY[B] = self.MEMORY[C]
            elif command_type == 15:
                C = int(command_bits[10:25], 2)
                self.MEMORY[C] = self.MEMORY[B]
            elif command_type == 26:  # equality
                C = int(command_bits[10:15], 2)  # Адрес первого операнда
                D = int(command_bits[15:22], 2)  # Смещение
                target_address = C + D
                if target_address < len(self.MEMORY):  # Проверяем, что адрес допустимый
                    self.MEMORY[B] = int(self.MEMORY[C] == self.MEMORY[target_address])
                else:
                    print(f"Error: Address out of range - C + D = {target_address}")



        self.log_result_csv()

    def log_result_csv(self):
        with open(self.RESULT_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Address", "Value"])
            for i in range(self.MEMORY_RANGE[0], self.MEMORY_RANGE[1] + 1):
                writer.writerow([f"0b{bin(i)[2:].zfill(4)}", self.MEMORY[i]])

def main():
    assembler = Assembler("programm.txt", "assembled.bin", "assembler_log.csv")
    assembler.run()

    interpreter = Interpreter("assembled.bin", "result.csv", (0, 31))
    interpreter.run()


if __name__ == '__main__':
    main()
