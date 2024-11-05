from main import Emulator
from tarfile import TarFile
import os
import time


def test_ls():
    # Ожидаемый результат выполнения команды ls
    expected_output = """filesys
filesys/2.txt
filesys/1.txt
filesys/vfg
filesys/vfg/conf.conf"""
    
    # Создание экземпляра эмулятора с файлом archive.tar
    emulator = Emulator(TarFile("virtual_filesystem.tar", 'r'))
    ls_output = emulator.command_parse("ls")
    
    # Сравнение реального и ожидаемого результата
    assert ls_output == expected_output


def test_cd():
    # Тест на команду cd с проверкой, что переход к папкам корректен
    emulator = Emulator(TarFile("virtual_filesystem.tar", 'r'))
    
    cd_result1 = emulator.command_parse("cd filesys")
    ls_output1 = emulator.command_parse("ls")
    
    cd_result2 = emulator.command_parse("cd vfg")
    ls_output2 = emulator.command_parse("ls")
    
    cd_result3 = emulator.command_parse("cd /")
    ls_output3 = emulator.command_parse("ls")

    # Проверяем, что ошибки не возвращаются и результат команды ls корректен
    assert cd_result1 == ""
    assert "filesys/2.txt" in ls_output1
    assert cd_result2 == ""
    assert "filesys/vfg/conf.conf" in ls_output2
    assert cd_result3 == ""
    assert ls_output3 == "filesys\nfilesys/2.txt\nfilesys/1.txt\nfilesys/vfg\nfilesys/vfg/conf.conf"


def test_cal():
    # Тест для команды cal, проверяет вывод текущего календаря
    emulator = Emulator(TarFile("virtual_filesystem.tar", 'r'))
    cal_output = emulator.command_parse("cal")
    
    # Проверка, что вывод содержит текущий месяц и год
    current_month_year = time.strftime("%B %Y")
    assert current_month_year in cal_output


def test_chmod():
    # Тест для команды chmod, которая симулирует изменение прав доступа
    emulator = Emulator(TarFile("virtual_filesystem.tar", 'r'))
    
    chmod_output1 = emulator.command_parse("chmod 644 filesys/1.txt")
    chmod_output2 = emulator.command_parse("chmod 755 nonexistent_file.txt")
    
    # Проверяем, что вывод соответствует ожидаемому результату
    assert chmod_output1 == "chmod: Changed mode of 'filesys/1.txt' to 0o644"
    assert chmod_output2 == "chmod: No such file: nonexistent_file.txt"


def test_cp():
    # Тест для команды cp, которая симулирует копирование файлов
    emulator = Emulator(TarFile("virtual_filesystem.tar", 'r'))
    
    cp_output1 = emulator.command_parse("cp filesys/1.txt filesys/1_copy.txt")
    cp_output2 = emulator.command_parse("cp nonexistent_file.txt filesys/another.txt")
    
    # Проверка на симулированное копирование файла и попытку скопировать несуществующий файл
    assert cp_output1 == "cp: Copied filesys/1.txt to filesys/1_copy.txt (simulated)"
    assert cp_output2 == "cp: No such file: nonexistent_file.txt"


if __name__ == "__main__":
    test_ls()
    test_cd()
    test_cal()
    test_chmod()
    test_cp()
    print("Все тесты пройдены успешно.")
