# PRJCT_HLPR

<p align=center>
<img src="https://ru.picmix.com/pic/download?picId=10073143&key=e3959" alt="Матриця" width="200"/>
</p>

## 📝 Опис

**PRJCT_HLPR** - це консольний помічник з елементами стилю фільму "Матриця", який допомагає керувати контактами та нотатками. Програма має два режими роботи: простий та "матричний" з візуальними ефектами.

## ✨ Особливості

- 📋 Управління контактами (додавання, редагування, видалення)
- 📅 Збереження днів народження контактів
- 📧 Збереження електронних адрес
- 📝 Створення та керування нотатками
- 🔍 Пошук по контактах та нотатках
- 🎬 Спеціальний режим "Матриця" з візуальними ефектами

## 🚀 Встановлення

### Використання Poetry

```bash
# Встановлення залежностей
poetry install
poetry shell
```

### Використання pip

```bash
# Для розробки
pip install -e .

# Для готового додатку
pip install .
```

## 🎮 Запуск програми

### Звичайний режим

```bash
assistant
```

### Режим "Матриця"

```bash
matrix
```

або

```bash
assistant --matrix
```

## 🛠️ Доступні команди

| Команда                                    | Опис                             |
| ------------------------------------------ | -------------------------------- |
| `help`                                     | Вивести довідку по командах      |
| `hello`                                    | Вивести вітальне повідомлення    |
| `save`                                     | Зберегти адресну книгу           |
| `add [ім'я] [телефон]`                     | Додати новий контакт або телефон |
| `set email [ім'я] [email]`                 | Додати email для контакту        |
| `set birthday [ім'я] [дата]`               | Встановити день народження       |
| `days to birthday [ім'я]`                  | Показати кількість днів до ДН    |
| `show birthday list [дата]`                | Показати ДН до певної дати       |
| `change phone [ім'я] [старий] [новий]`     | Змінити телефон                  |
| `change email/birthday [ім'я] [нові дані]` | Редагувати дані                  |
| `remove [ім'я] [телефон/birthday/email]`   | Видалити інформацію              |
| `info [ім'я]`                              | Інформація про контакт           |
| `delete [ім'я]`                            | Видалити контакт                 |
| `show all`                                 | Показати всі контакти            |
| `search [запит]`                           | Пошук за символами               |
| `create note [автор] [назва]`              | Створити нотатку                 |
| `append note tags [назва] [теги]`          | Додати теги                      |
| `show notes`                               | Показати нотатки                 |
| `deletion note [назва]`                    | Видалити нотатку                 |
| `clear notes`                              | Видалити всі нотатки             |
| `searching note by tags [теги]`            | Пошук за тегами                  |
| `exit`, `close`                            | Вихід з програми                 |

### Режим "Матриця"

```
MATRIX: SECURITY SYSTEM
........................
Scanning in progress...
Biometric authentication: ▓▒░▓▒░▓▒░▓▒░▓▒░ [SUCCESS]
Access decryption: 100%

========================================
ACCESS GRANTED
Welcome to project PRJCT_HLPR
========================================
```

## 📁 Структура даних

- Контакти зберігаються в `new_book.csv`
- Нотатки зберігаються в `notes_save.csv`

## 🔧 Вимоги

- Python 3.12+
- Модулі: prompt-toolkit, colorama

## 🤝 Розробники

- blavikensbutcher

---

> _"Знати шлях і пройти його – не одне й теж"_ — Морфеус
