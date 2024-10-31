# Задача 1 
Байткод:
```
11 0 LOAD_FAST       0 (x) 
    2 LOAD_CONST      1 (10)
    4 BINARY_MULTIPLY
    6 LOAD_CONST      2 (42)
    8 BINARY_ADD
   10 RETURN_VALUE
```
Описание шагов:
LOAD_FAST 0 (x): Загрузить значение переменной x из локальной области видимости в стек.
LOAD_CONST 1 (10): Загрузить константу 10 в стек.
BINARY_MULTIPLY: Умножить два верхних элемента стека (x и 10) и поместить результат в стек.
LOAD_CONST 2 (42): Загрузить константу 42 в стек.
BINARY_ADD: Сложить два верхних элемента стека (результат умножения и 42) и поместить результат в стек.
RETURN_VALUE: Вернуть верхний элемент стека (результат сложения) как результат функции.

Эквивалентное выражение на Python:
```python
return x * 10 + 42
```
# Задача 2
Байткод:
```
  5           0 LOAD_CONST               1 (1) 
              2 STORE_FAST               1 (r) 

  6     >>    4 LOAD_FAST                0 (n) 
              6 LOAD_CONST               1 (1) 
              8 COMPARE_OP               4 (>) 
             10 POP_JUMP_IF_FALSE       30 

  7          12 LOAD_FAST                1 (r) 
             14 LOAD_FAST                0 (n) 
             16 INPLACE_MULTIPLY 
             18 STORE_FAST               1 (r) 

  8          20 LOAD_FAST                0 (n) 
             22 LOAD_CONST               1 (1) 
             24 INPLACE_SUBTRACT 
             26 STORE_FAST               0 (n) 
             28 JUMP_ABSOLUTE            4 

  9     >>   30 LOAD_FAST                1 (r) 
             32 RETURN_VALUE 

```
Описание шагов:
LOAD_CONST 1 (1): Загрузить константу 1 в стек.
STORE_FAST 1 (r): Сохранить верхний элемент стека (1) в локальную переменную r.
LOAD_FAST 0 (n): Загрузить значение переменной n из локальной области видимости в стек.
LOAD_CONST 1 (1): Загрузить константу 1 в стек.
COMPARE_OP 4 (>): Сравнить два верхних элемента стека (n и 1) на большее. Результат (True/False) помещается в стек.
POPJUMPIF_FALSE 30: Если верхний элемент стека равен False, перейти к инструкции с меткой 30.
LOAD_FAST 1 (r): Загрузить значение переменной r в стек.
LOAD_FAST 0 (n): Загрузить значение переменной n в стек.
INPLACE_MULTIPLY: Умножить два верхних элемента стека (r и n) и сохранить результат в r.
STORE_FAST 1 (r): Сохранить результат умножения в локальную переменную r.
LOAD_FAST 0 (n): Загрузить значение переменной n в стек.
LOAD_CONST 1 (1): Загрузить константу 1 в стек.
INPLACE_SUBTRACT: Вычесть два верхних элемента стека (n и 1) и сохранить результат в n.
STORE_FAST 0 (n): Сохранить результат вычитания в локальную переменную n.
JUMP_ABSOLUTE 4: Перейти к инструкции с меткой 4.
LOAD_FAST 1 (r): Загрузить значение переменной r в стек.
RETURN_VALUE: Вернуть верхний элемент стека (значение r) как результат функции.

Это функция факториала на Python:
```python
def factorial(n):
    r = 1
    while n > 1:
        r *= n
        n -= 1
    return r

```

# Задача 3
### JVM (Java):
Компилированный байткод::
```
// 0: iconst_1
// 1: istore_1
// 2: iload_0
// 3: iconst_1
// 4: if_icmplt 15
// 7: iload_1
// 8: iload_0
// 9: imul
// 10: istore_1
// 11: iload_0
// 12: iconst_1
// 13: isub
// 14: istore_0
// 15: goto 2
// 18: iload_1
// 19: ireturn
```

# Задача 3
### JVM (Java):
Компилированный байткод::
```
// 0: iconst_1
// 1: istore_1
// 2: iload_0
// 3: iconst_1
// 4: if_icmplt 15
// 7: iload_1
// 8: iload_0
// 9: imul
// 10: istore_1
// 11: iload_0
// 12: iconst_1
// 13: isub
// 14: istore_0
// 15: goto 2
// 18: iload_1
// 19: ireturn
```

# Задача 4
