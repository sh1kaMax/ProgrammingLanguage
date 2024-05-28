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

### Организация памяти

---
