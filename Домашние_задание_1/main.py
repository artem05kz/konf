from tarfile import TarFile
import sys
import tkinter as tk
import time
import os


class Emulator:
    def __init__(self, filesystem: TarFile):
        self.current_dir = ""
        self.filesystem = filesystem

    def __del__(self):
        self.filesystem.close()

    def ls(self) -> str:
        """Команда ls — вывод списка файлов."""
        output = ""
        for i in self.filesystem.getnames():
            output += i + "\n"
        output = output.strip()
        print(output)
        return output

    def cd(self, command: str) -> str:
        """Команда cd — смена текущего каталога."""
        files = self.filesystem.getnames()
        files.append("")
        try:
            path = command.split()[1]
        except IndexError:
            return "cd: Provide additional arguments"

        # Проверка, абсолютный или относительный путь
        if path[0] == '/':
            to_path = path.removeprefix('/')
        else:
            to_path = (self.current_dir + "/" + path).removeprefix('/')

        # Проверка, существует ли путь
        if to_path not in files:
            output = "cd: No such file or directory: /" + to_path
        elif to_path.count('.') != 0:
            output = "cd: Not a directory: /" + to_path
        else:
            output = ""
            self.current_dir = to_path
        return output

    def cal(self) -> str:
        """Команда cal — вывод текущей даты."""
        current_date = time.strftime("%B %Y")  # Вывод месяца и года
        return f"Current month: {current_date}"

    def chmod(self, command: str) -> str:
        """Команда chmod — изменение прав доступа к файлу."""
        try:
            args = command.split()
            mode = int(args[1], 8)
            file_path = args[2]
            # Симуляция chmod: операция не изменяет реальные права, т.к. это эмулятор
            if file_path in self.filesystem.getnames():
                output = f"chmod: Changed mode of '{file_path}' to {oct(mode)}"
            else:
                output = f"chmod: No such file: {file_path}"
        except (IndexError, ValueError):
            output = "chmod: Provide valid mode and file path"
        return output

    def cp(self, command: str) -> str:
        """Команда cp — копирование файлов."""
        try:
            args = command.split()
            src_path = args[1]
            dest_path = args[2]
            if src_path not in self.filesystem.getnames():
                return f"cp: No such file: {src_path}"
            output = f"cp: Copied {src_path} to {dest_path} (simulated)"
        except IndexError:
            output = "cp: Provide source and destination paths"
        return output

    def command_parse(self, command: str) -> str:
        """Функция для парсинга и выполнения команд."""
        output = ""
        if command == 'ls':
            output = self.ls()
        elif command.split()[0] == "cd":
            output = self.cd(command)
        elif command == "cal":
            output = self.cal()
        elif command.split()[0] == "chmod":
            output = self.chmod(command)
        elif command.split()[0] == "cp":
            output = self.cp(command)
        elif command == "exit":
            sys.exit()
        else:
            output = "Unknown command: " + command
        return output


class ConsoleText(tk.Text):
    def __init__(self, master=None, **kw):
        tk.Text.__init__(self, master, **kw)
        self.insert('1.0', '$ ')  # первый приглашение к вводу
        self.mark_set('input', 'insert')
        self.mark_gravity('input', 'left')
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.bind("<Return>", self.enter)

        # Проверка аргумента командной строки и открытие tar-файла
        if len(sys.argv) > 1:
            self.emulator = Emulator(TarFile(sys.argv[1], 'r'))
        else:
            print("Ошибка: Пожалуйста, укажите путь к tar-файлу виртуальной файловой системы в аргументах.")
            sys.exit(1)

    def _proxy(self, *args):
        largs = list(args)
        if args[0] == 'insert':
            if self.compare('insert', '<', 'input'):
                self.mark_set('insert', 'end')
        elif args[0] == "delete":
            if self.compare(largs[1], '<', 'input'):
                if len(largs) == 2:
                    return
                largs[1] = 'input'
        result = self.tk.call((self._orig,) + tuple(largs))
        return result

    def enter(self, event):
        command = self.get('input', 'end').strip()
        # Выполнение команды
        output = self.emulator.command_parse(command)

        # Отображение результата и нового приглашения к вводу
        self.insert('end', f"\n{output}\n$ ")
        self.mark_set('input', 'insert')
        return "break"


if __name__ == "__main__":
    root = tk.Tk()
    tfield = ConsoleText(root, bg='gray10', fg='white', insertbackground='white')
    tfield.pack()
    root.mainloop()
