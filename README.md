# Лабараторная работа №3

---
Шикунов Максим Евгеньевич P3233
`forth | stack | neum | mc | tick | struct | stream | port | pstr | prob2`
Выполнен базовый вариант

## Язык программирования

---

### Синтаксис

__Форма Бэкуса-Наура:__

``` форма Бэкуса-Наура
<program> ::= <term> | <term> "\n" <program>
<term> ::= <variables> | <words> | <call_words>
<variables> ::= <make_variable> | <set_variable> | <variable_on_top_stack>
<make_variable> ::= "VARIABLE" <string_name>
<string_name> ::= [A-Za-z][A-Za-z0-9]*
<set_variable> ::= <number> <string_name> "!"
<number> ::= -?[1-9][0-9]*
<variable_on_top_stack> ::= <string_name> "@"
<words> ::= ":" <string_name> <description> "\n" <commands> ";"
<description> ::= "(" <type> "--" <string_name> ")"
<type> ::= <string_name>
<commands> ::= <command> | <command> "\n" <commands>
<command> ::= "+" | "-" | "*" | "/" | "mod" | "dup" | "drop" | "swap"
           | "=" | ">" | "<" | "." | "exit" | <variables> | <if> | <if_else | <loop>
<if> ::= "if" <term> "then"
<if_else> ::= "if" <term> "else" <term> "then"
<loop> ::= "begin" <term> "until"
```

### Особенности языка

- Используется обратная польская запись для вычислений
- Все переменные хранятся в стеке
- Forth не имеет объявления типов данных
- Есть целочисленные и строковые литералы

### Операции

| __Операции__ | __Стек__                     | __Описание__                                                                       |
|-------------|------------------------------|------------------------------------------------------------------------------------|
| +           | (... a b) --> (... a + b)    | Складываем два верхних числа со стека и кладем на вершину сумму                    |
| -           | (... a b) --> (... a - b)    | Вычитаем из a число b и кладем разность на вершину                                 |
| *           | (... a b) --> (... a * b)    | Умножаем два верхних числа со стека и кладем на вершину результат                  |
| /           | (... a b) --> (... a / b)    | Делим a на число b и кладем результат на вершину стека                             |
| mod         | (... a b) --> (... a mod b)  | Кладем остаток от деления a на b на вершину стека                                  |
| dup         | (... a) --> (... a a)        | Дублирует число с вершины стека и кладет дубликат на вершину                       |
| drop        | (... a) --> (...)            | Удаляет число с вершины стека                                                      |
| swap        | (... a b) --> (... b a)      | Меняет местами два числа, которые лежат на вершине стека                           |
| =           | (... a b) --> (... a = b)    | Если a равно b, то кладем 1 на вершину стека, иначе 0                              |
| \>          | (... a b) --> (... a > b)    | Если b больше a, то кладем 1 на вершину стека, иначе 0                             |
| \<          | (... a b) --> (... a < b)    | Если b меньше a, то кладем 1 на вершину стека, иначе 0                             |
| .           | (... a) --> output(a)        | Печатаем вершину стека в output как число                                          |
| exit        | -                            | Завершаем программу                                                                |
| (a addr) !  | (...)\[addr\] = a            | Сохраняет a по адресу (addr)                                                       |
| (addr) @ | (...)\[addr\] --> (... a)    | Кладет на вершину стека число, которое лежит по адресу                             |
| # | input --> ...a               | Считывает значение из input и кладет на вершину стека                              |
| if | a == True ip++, jmp n        | Если на вершине стека True, то перейдем далее, иначе перейдем на else или endif    |
| else | -                            | Если при команде if на стеке лежало False, то программа перейдет сюда              |
| endif | -                            | Если при команде if на стеке лежало False и нету else, то программа перейдет сюда  |
| begin | -                            | Начало цикла (куда программа будет каждый раз возвращаться                         |
| until | -                            | Если на вершине стека лежит True, то завершит цикл, иначе перейдет на начало цикла |
| emit | (... a) --> output(ascii(a)) | Печатаем вершину стека как символ ASCII |

- : <слово> <команды> ; - Объявление процедуры
- if <true-команды> \[else <false-команды>\] endif - Если вершина стека != 0, то выполняется <true-команды>, иначе выполняется <false-команды>, если они есть
- begin <команды> until - Цикл, который работает пока перед командой until на вершине стека не будет 1
- ." <строка>" - Вывод <строка> в stdout

### Организация памяти

---

Память команд и данных общая. Существует также DataStack, который может быть использован программистом  

Память соответствует фон Неймановской архитектуре. Память программы состоит из: 1 элемент хранит в себе адрес начала хранения переменных, дальше хранятся машинные слова (32-x битные) от первого элемента до переменных, после хранятся сами переменные. Обращение к памяти производится через регистр adress_register

### Система команд

---

- Машинное слово -- 32 бита
- Доступ к памяти осуществляется по адресу, хранящемуся в регистре PC. Изменить данный регистр можно следующими способами:
  - Инкрементировать данный регистр
  - Записи аргумента из машинного слова (при таких контрукциях как jmp, jzs)
- Поток управления:
  - Инкремент PC после каждой инструкции
  - условный и бузусловный переход

#### Набор инструкций

---

Команды языка однозначно транслируются в инструкции

| __Инструкции__ | __Количество тактов__ |
|----------------|-----------------------|
| Fetch | 6 |
| ADD | 7 |
| SUB | 7 |
| MUL | 7 |
| DIV | 7 |
| MOD | 7 |
| DUP | 5 |
 | DROP | 5 |
| SWAP | 8 |
| EQ | 7 |
| NOT_EQ | 7 |
| MORE | 7 |
| LESS | 7 |
| PUSH | 6 |
| ADR_ON_TOP | 6 |
| SAVE_VAR | 12 |
| VAR_ON_TOP | 9 |
| JZS | 11 |
| JMP | 10 |
| PRINT | 8 |
| READ | 6 |
| EMIT | 8 |  
| HALT | 2 |

Такты каждой интрукции высчитываются по тому, сколько в ней есть сигналов, который посылаются машине. Инструкция fetch нужна для выборки следующей команды

### Транслятор

---

Интерфейс командной строки: `translator.py <source.file> <target.file>`  
Реализован в [translator.py](translator.py)

#### Этапы транслирования

1. Первый этап - перевод текста в terms. Класс с контруктором(номер_линии, номер_слова, слово). Также записывание всех имен переменных, процедур и строк на вывод (функция `text2terms`)
2. Второй этап - перевод терм в машинные слова (функция `translate`)
3. Третий этап - выделение памяти для каждой переменной
4. Четвертый этап - запись строк в память

### Модель процессора

Интерфейс командной строки: `machine.py <machine_code_file> <input_file> <log_file>`

#### DataPath

![datapath](images/DataPath.jpg)
Реализован в классе [DataPath](data_path.py)  
`IR` - регистр для хранения машинного слова  
`PC` - указатель на место в памяти, от куда брать следующее машинное слово  
`AR` - регистр для хранения адреса, по которому программа обращается к памяти  
`TOS` - регистр для хранения вершины стека  
`BR` - регистр для для промежуточного хранения из DataStack  
`DataStack` - стек данных  
`Memory` - общая память программы  
На схеме также изображены сигналы, которые приходят из `ControlUnit`, по которым выполняется определенное действие  

#### ControlUnit

![control_unit](images/ControlUnit.png)
Реализован в классе [ControlUnit](control_unit.py)  
`mc_adr` - регистр для хранения адреса микрокоманды, которую надо выполнить  
`MicrocodeMemory` - память микрокоманд, где прописана каждая интрукция  
Считывает по адресу массив сигналов, выполняет каждый из них и отсылает в нужное место  
Тики считают, сколько сигналов было отправлено

#### Сигналы

- DSLatch (Push, Pop) - сигнал для DataStack
- ARLatch (PC, TOS) - прием на `address_register`
- IRLatch (MEM) - прием данных на `instraction_register`
- PCLatch (IR, INC) - прием данных на `pc`
- TosLatch (MEM, IR, BR, ALU, IR_VAR) - прием данных на `top_of_stack`
- ALUValues (VAR) - запись двух чисел в `alu`
- AluLatch (SUM, SUB, DIV, MOD, NOT_EQ, EQ, MORE, LESS) - выбор арифметического действия
- MEMSignal (READ, WRITE, TOS) - сигнал для `memory`
- MCAdrLatch (IR, INC, ZERO) - прием данных на `mc_adr`
- BRLatch (DS) - запрос данных на `buffer_register` от `DataStack`
- CheckFlag (Z, N, V) - проверка флага
- Jumps (JMP, JZS) - выбор перехода
- IOLatch (PRINT, READ, EMIT) - работа с вводом/выводом
- PROG (HALT) - завершение программы
- Instraction (INC) - увелечение счетчика интрукций на один

#### Особенности работы модели

- Цикл симуляции осуществляется в функции `run_machine`
- Шаг моделирования соответсвует одному тику программы с выводом состояния в журнал
- Для журнала состояний процессора используется стандратный модуль logging
- Количество интрукций для моделирования лимиировано
- Остановка моделирования прекращается при:
  - превышения лимита количества выполняемых интрукций
  - исключение EOFError - если нет данных для чтения из портов
  - исключение StopIteration - если выполнена интрукция halt

### Тестирование

---

Тестирование выполняется при помощи golden-тестов  
Запуск golden-тестов: [golden_test](golden_test.py)  
Тесты:

- [golden/cat.yml](golden/cat.yml) - Выводит символы в stdout из stdin, пока не закончаться в буфере
- [golden/hello_name.yml](golden/hello_name.yml) - Запрашивает у пользователя имя и здоровается с ним
- [golden/hello_world.yml](golden/hello_world.yml) - Выводит в stdou "Hello, World!"
- [golden/prob2.yml](golden/prob2.yml) - Выводит сумму всех четно стоящих чисел последовательности Фибоначчи

Запустить тесты: `poetry run pytest . -v`  
CI при помощи GitHub Actions:

```yaml
name: Python CI

on:
  push:
    branches:
      - master

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check commit
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.12

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Run tests and collect coverage
        run: |
          poetry run coverage run -m pytest .
          poetry run coverage report -m
        env:
          CI: true

  lint:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.12

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Check code formatting with Ruff
        run: poetry run ruff format --check .

      - name: Run Ruff linters
        run: poetry run ruff check --ignore=C901 .
```

где:

- poetry - инструмент для управления зависимостьями в Python
- coverage - формирование отчета об уровне покрытия исходного кода тестами
- pytest - утилита для запуска тестов
- rugg - утилита для формирования и проверки стиля кода

Пример использования и журнал работы прроцессора на примере `cat`:

```code
(.venv) PS C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage> cat ./programs/cat
: cat                                                                          
    begin                                                                      
        # dup dup                                                              
        0 !=                                                                   
        if                                                                     
            emit                                                               
        endif                                                                  
        0 =                                                                    
;
exit
(.venv) PS C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage> ./translator.py ./programs/cat ./programs/cat_machine_code
(.venv) PS C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage> cat ./programs/cat_machine_code
[{"index": 0, "opcode": "read", "term": [3, 1, "#"]},
{"index": 1, "opcode": "dup", "term": [3, 2, "dup"]},
{"index": 2, "opcode": "dup", "term": [3, 3, "dup"]},
{"index": 3, "opcode": "push", "arg": "0", "term": [4, 1, "0"]},
{"index": 4, "opcode": "not_eq", "term": [4, 2, "!="]},
{"index": 5, "opcode": "jzs", "arg": 7},
{"index": 6, "opcode": "emit", "term": [6, 1, "emit"]},
{"index": 7, "opcode": "push", "arg": "0", "term": [8, 1, "0"]},
{"index": 9, "opcode": "jzs", "arg": 0},
{"index": 10, "opcode": "halt", "term": [12, 1, "exit"]}]
(.venv) PS C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage> cat ./programs/cat_input
a
(.venv) PS C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage> ./machine.py ./programs/cat_machine_code ./programs/cat_input ./programs/cat.log
(.venv) PS C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage> cat ./programs/cat.log
[DEBUG]  TICK: 0    PC: 1   ADDR: 1   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 1    PC: 1   ADDR: 1   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 2    PC: 1   ADDR: 1   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 3    PC: 1   ADDR: 1   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 4    PC: 1   ADDR: 1   mcADDR: 1  SIGNAL: Instraction.INC TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 5    PC: 1   ADDR: 1   mcADDR: 44 SIGNAL: MCAdrLatch.IR   TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 6    PC: 1   ADDR: 1   mcADDR: 44 SIGNAL: DSLatch.Push    TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 7    PC: 1   ADDR: 1   mcADDR: 45 SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  input: a
[DEBUG]  TICK: 8    PC: 1   ADDR: 1   mcADDR: 45 SIGNAL: IOLatch.READ    TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 9    PC: 1   ADDR: 1   mcADDR: 45 SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 10   PC: 2   ADDR: 1   mcADDR: 45 SIGNAL: PCLatch.INC     TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 11   PC: 2   ADDR: 1   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 12   PC: 2   ADDR: 2   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 13   PC: 2   ADDR: 2   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 14   PC: 2   ADDR: 2   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 15   PC: 2   ADDR: 2   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 16   PC: 2   ADDR: 2   mcADDR: 1  SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 17   PC: 2   ADDR: 2   mcADDR: 12 SIGNAL: MCAdrLatch.IR   TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 18   PC: 2   ADDR: 2   mcADDR: 12 SIGNAL: DSLatch.Push    TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 19   PC: 2   ADDR: 2   mcADDR: 13 SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 20   PC: 3   ADDR: 2   mcADDR: 13 SIGNAL: PCLatch.INC     TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 21   PC: 3   ADDR: 2   mcADDR: 13 SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 22   PC: 3   ADDR: 2   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 23   PC: 3   ADDR: 3   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 24   PC: 3   ADDR: 3   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 25   PC: 3   ADDR: 3   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 26   PC: 3   ADDR: 3   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 27   PC: 3   ADDR: 3   mcADDR: 1  SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 28   PC: 3   ADDR: 3   mcADDR: 12 SIGNAL: MCAdrLatch.IR   TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 29   PC: 3   ADDR: 3   mcADDR: 12 SIGNAL: DSLatch.Push    TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 30   PC: 3   ADDR: 3   mcADDR: 13 SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 31   PC: 4   ADDR: 3   mcADDR: 13 SIGNAL: PCLatch.INC     TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 32   PC: 4   ADDR: 3   mcADDR: 13 SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 33   PC: 4   ADDR: 3   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 34   PC: 4   ADDR: 4   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 35   PC: 4   ADDR: 4   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 36   PC: 4   ADDR: 4   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 37   PC: 4   ADDR: 4   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 38   PC: 4   ADDR: 4   mcADDR: 1  SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 39   PC: 4   ADDR: 4   mcADDR: 25 SIGNAL: MCAdrLatch.IR   TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 40   PC: 4   ADDR: 4   mcADDR: 25 SIGNAL: DSLatch.Push    TOS: 97     Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 41   PC: 4   ADDR: 4   mcADDR: 25 SIGNAL: TosLatch.IR     TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 42   PC: 4   ADDR: 4   mcADDR: 26 SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 43   PC: 5   ADDR: 4   mcADDR: 26 SIGNAL: PCLatch.INC     TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 44   PC: 5   ADDR: 4   mcADDR: 26 SIGNAL: Instraction.INC TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 45   PC: 5   ADDR: 4   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 46   PC: 5   ADDR: 5   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 47   PC: 5   ADDR: 5   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 48   PC: 5   ADDR: 5   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 49   PC: 5   ADDR: 5   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 50   PC: 5   ADDR: 5   mcADDR: 1  SIGNAL: Instraction.INC TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 51   PC: 5   ADDR: 5   mcADDR: 50 SIGNAL: MCAdrLatch.IR   TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97, 97]
[DEBUG]  TICK: 52   PC: 5   ADDR: 5   mcADDR: 50 SIGNAL: ALUValues.VAR   TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 53   PC: 5   ADDR: 5   mcADDR: 50 SIGNAL: AluLatch.NOT_EQ TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 54   PC: 5   ADDR: 5   mcADDR: 51 SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 55   PC: 5   ADDR: 5   mcADDR: 51 SIGNAL: TosLatch.ALU    TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 56   PC: 6   ADDR: 5   mcADDR: 51 SIGNAL: PCLatch.INC     TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 57   PC: 6   ADDR: 5   mcADDR: 51 SIGNAL: Instraction.INC TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 58   PC: 6   ADDR: 5   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 59   PC: 6   ADDR: 6   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 60   PC: 6   ADDR: 6   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 61   PC: 6   ADDR: 6   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 62   PC: 6   ADDR: 6   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 63   PC: 6   ADDR: 6   mcADDR: 1  SIGNAL: Instraction.INC TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 64   PC: 6   ADDR: 6   mcADDR: 35 SIGNAL: MCAdrLatch.IR   TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 65   PC: 6   ADDR: 6   mcADDR: 35 SIGNAL: DSLatch.Push    TOS: 1      Z: 0 N: 0 V: 0
DS: [97, 97, 1]
[DEBUG]  TICK: 66   PC: 6   ADDR: 6   mcADDR: 35 SIGNAL: TosLatch.IR     TOS: 7      Z: 0 N: 0 V: 0
DS: [97, 97, 1]
[DEBUG]  TICK: 67   PC: 6   ADDR: 6   mcADDR: 35 SIGNAL: JUMPS.JZS       TOS: 7      Z: 0 N: 0 V: 0
DS: [97, 97, 1]
[DEBUG]  TICK: 68   PC: 6   ADDR: 6   mcADDR: 36 SIGNAL: MCAdrLatch.INC  TOS: 7      Z: 0 N: 0 V: 0
DS: [97, 97, 1]
[DEBUG]  TICK: 69   PC: 6   ADDR: 6   mcADDR: 36 SIGNAL: DSLatch.Pop     TOS: 7      Z: 0 N: 0 V: 0
DS: [97, 97]
[DEBUG]  TICK: 70   PC: 6   ADDR: 6   mcADDR: 36 SIGNAL: BRLatch.DS      TOS: 7      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 71   PC: 6   ADDR: 6   mcADDR: 36 SIGNAL: TosLatch.BR     TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 72   PC: 6   ADDR: 6   mcADDR: 37 SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 73   PC: 7   ADDR: 6   mcADDR: 37 SIGNAL: PCLatch.INC     TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 74   PC: 7   ADDR: 6   mcADDR: 37 SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 75   PC: 7   ADDR: 6   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 76   PC: 7   ADDR: 7   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 77   PC: 7   ADDR: 7   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 78   PC: 7   ADDR: 7   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 79   PC: 7   ADDR: 7   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 80   PC: 7   ADDR: 7   mcADDR: 1  SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 81   PC: 7   ADDR: 7   mcADDR: 46 SIGNAL: MCAdrLatch.IR   TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  output: a<<a
[DEBUG]  TICK: 82   PC: 7   ADDR: 7   mcADDR: 46 SIGNAL: IOLatch.EMIT    TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 83   PC: 7   ADDR: 7   mcADDR: 47 SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 84   PC: 7   ADDR: 7   mcADDR: 47 SIGNAL: BRLatch.DS      TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 85   PC: 7   ADDR: 7   mcADDR: 47 SIGNAL: TosLatch.BR     TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 86   PC: 7   ADDR: 7   mcADDR: 48 SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 87   PC: 8   ADDR: 7   mcADDR: 48 SIGNAL: PCLatch.INC     TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 88   PC: 8   ADDR: 7   mcADDR: 48 SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 89   PC: 8   ADDR: 7   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 90   PC: 8   ADDR: 8   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 91   PC: 8   ADDR: 8   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 92   PC: 8   ADDR: 8   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 93   PC: 8   ADDR: 8   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 94   PC: 8   ADDR: 8   mcADDR: 1  SIGNAL: Instraction.INC TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 95   PC: 8   ADDR: 8   mcADDR: 25 SIGNAL: MCAdrLatch.IR   TOS: 97     Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 96   PC: 8   ADDR: 8   mcADDR: 25 SIGNAL: DSLatch.Push    TOS: 97     Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 97   PC: 8   ADDR: 8   mcADDR: 25 SIGNAL: TosLatch.IR     TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 98   PC: 8   ADDR: 8   mcADDR: 26 SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 99   PC: 9   ADDR: 8   mcADDR: 26 SIGNAL: PCLatch.INC     TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 100  PC: 9   ADDR: 8   mcADDR: 26 SIGNAL: Instraction.INC TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 101  PC: 9   ADDR: 8   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 102  PC: 9   ADDR: 9   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 103  PC: 9   ADDR: 9   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 104  PC: 9   ADDR: 9   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 105  PC: 9   ADDR: 9   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 106  PC: 9   ADDR: 9   mcADDR: 1  SIGNAL: Instraction.INC TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 107  PC: 9   ADDR: 9   mcADDR: 19 SIGNAL: MCAdrLatch.IR   TOS: 0      Z: 0 N: 0 V: 0
DS: [97]
[DEBUG]  TICK: 108  PC: 9   ADDR: 9   mcADDR: 19 SIGNAL: ALUValues.VAR   TOS: 0      Z: 0 N: 0 V: 0
DS: []
[DEBUG]  TICK: 109  PC: 9   ADDR: 9   mcADDR: 19 SIGNAL: AluLatch.EQ     TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 110  PC: 9   ADDR: 9   mcADDR: 20 SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 111  PC: 9   ADDR: 9   mcADDR: 20 SIGNAL: TosLatch.ALU    TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 112  PC: 10  ADDR: 9   mcADDR: 20 SIGNAL: PCLatch.INC     TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 113  PC: 10  ADDR: 9   mcADDR: 20 SIGNAL: Instraction.INC TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 114  PC: 10  ADDR: 9   mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 115  PC: 10  ADDR: 10  mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 116  PC: 10  ADDR: 10  mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 117  PC: 10  ADDR: 10  mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 118  PC: 10  ADDR: 10  mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 119  PC: 10  ADDR: 10  mcADDR: 1  SIGNAL: Instraction.INC TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 120  PC: 10  ADDR: 10  mcADDR: 35 SIGNAL: MCAdrLatch.IR   TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 121  PC: 10  ADDR: 10  mcADDR: 35 SIGNAL: DSLatch.Push    TOS: 0      Z: 1 N: 0 V: 0
DS: [0]
[DEBUG]  TICK: 122  PC: 10  ADDR: 10  mcADDR: 35 SIGNAL: TosLatch.IR     TOS: 0      Z: 1 N: 0 V: 0
DS: [0]
[DEBUG]  TICK: 123  PC: 0   ADDR: 10  mcADDR: 35 SIGNAL: JUMPS.JZS       TOS: 0      Z: 1 N: 0 V: 0
DS: [0]
[DEBUG]  TICK: 124  PC: 0   ADDR: 10  mcADDR: 36 SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 1 N: 0 V: 0
DS: [0]
[DEBUG]  TICK: 125  PC: 0   ADDR: 10  mcADDR: 36 SIGNAL: DSLatch.Pop     TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 126  PC: 0   ADDR: 10  mcADDR: 36 SIGNAL: BRLatch.DS      TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 127  PC: 0   ADDR: 10  mcADDR: 36 SIGNAL: TosLatch.BR     TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 128  PC: 0   ADDR: 10  mcADDR: 37 SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 129  PC: 1   ADDR: 10  mcADDR: 37 SIGNAL: PCLatch.INC     TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 130  PC: 1   ADDR: 10  mcADDR: 37 SIGNAL: Instraction.INC TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 131  PC: 1   ADDR: 10  mcADDR: 0  SIGNAL: MCAdrLatch.ZERO TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 132  PC: 1   ADDR: 1   mcADDR: 0  SIGNAL: ARLatch.PC      TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 133  PC: 1   ADDR: 1   mcADDR: 0  SIGNAL: MEMSignal.READ  TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 134  PC: 1   ADDR: 1   mcADDR: 1  SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 135  PC: 1   ADDR: 1   mcADDR: 1  SIGNAL: IRLatch.MEM     TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 136  PC: 1   ADDR: 1   mcADDR: 1  SIGNAL: Instraction.INC TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 137  PC: 1   ADDR: 1   mcADDR: 44 SIGNAL: MCAdrLatch.IR   TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 138  PC: 1   ADDR: 1   mcADDR: 44 SIGNAL: DSLatch.Push    TOS: 0      Z: 1 N: 0 V: 0
DS: []
[DEBUG]  TICK: 139  PC: 1   ADDR: 1   mcADDR: 45 SIGNAL: MCAdrLatch.INC  TOS: 0      Z: 1 N: 0 V: 0
DS: []
[WARNING]  No input from user!
[DEBUG]  output_buffer:
                                a

a

instraction_count: 21
tick: 140
```

Пример проверки исходного кода:

```test
(.venv) PS C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage> poetry run pytest . -v
=============================================================================== test session starts ===============================================================================
platform win32 -- Python 3.12.0, pytest-7.4.4, pluggy-1.5.0 -- C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Max\Dropbox\ComputerArchitecture\lab3\ProgrammingLanguage
configfile: pyproject.toml
plugins: golden-0.2.2
collected 4 items

golden_test.py::test_program[golden/cat.yml] PASSED                                                                                                                          [ 25%]
golden_test.py::test_program[golden/hello_name.yml] PASSED                                                                                                                   [ 50%]
golden_test.py::test_program[golden/hello_world.yml] PASSED                                                                                                                  [ 75%]
golden_test.py::test_program[golden/prob2.yml] PASSED                                                                                                                        [100%]
```

```table
| ФИО                       | алг            | LoC | code инстр. | инстр. | такт. |
| Шикунов Максим Евгеньевич | cat            | 12  | 11          | 141    | 932   |
| Шикунов Максим Евгеньевич | hello_name     | 15  | 55          | 495    | 3258  |
| Шикунов Максим Евгеньевич | hello_world    | 2   | 32          | 396    | 2591  |
| Шикунов Максим Евгеньевич | prob2          | 34  | 50          | 982    | 6722  | 
```
