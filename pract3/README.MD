# Задача 1



# Задача 2
Dhall:
```dhall
let Group = λ(n : Natural) → "ИКБО-" ++ Natural/show n ++ "-20"

let Student =
      { age : Natural, group : Text, name : Text }

let students : List Student =
      [ { age = 19, group = Group 4, name = "Иванов И.И." }
      , { age = 18, group = Group 5, name = "Петров П.П." }
      , { age = 18, group = Group 5, name = "Сидоров С.С." }
      , { age = 20, group = Group 6, name = "Михеев Н.В." }
      ]

let groups : List Text =
      [ Group 1, Group 2, Group 3, Group 4, Group 5, Group 6, Group 7
      , Group 8, Group 9, Group 10, Group 11, Group 12, Group 13
      , Group 14, Group 15, Group 16, Group 17, Group 18, Group 19
      , Group 20, Group 21, Group 22, Group 23, Group 24
      ]

let output = 
  { groups = groups
  , students = students
  , subject = "Конфигурационное управление"
  }

in output
```

# Задача 3
```python
import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
S = D | S D
D = 0 | 1
'''
for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'S'))

```

# Задача 4
```python
import random

def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar

def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
S = ( S ) | { S } | 
'''
for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'S'))
```

# Задача 5
```python
import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = T | E | T 
T = F | T & F 
F = ~ F | ( E ) | x | y
'''
for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```
