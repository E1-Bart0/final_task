# Финальное задание
## Вариант 3 Набор софта для библиотекаря

Набор софта включает в себя

* Базу данных
* Набор CLI утилит для работы с базой

python version: 3.9.0

## DataBase
### Поднимем БД через Docker-compose

```angular2html
cd <PATH_TO_PROJECT>
# Установите переменные окпужения в .env и config.ini
# Создайте виртуальное окружение

# Установим библиотеки для питона
make install_requirements
make migrate

# Проинициализируем БД и накатим миграции
make init_db

# Для тестов поднимем другую БД
make init_test_db
```

## CLI утилиты для работы с базой

### digger.py
#### Применение: digger.py [-h] (-s DIR_PATH | -a BOOK_PATH) [-u]

DIR_PATH - путь до папки с каталогом книг в формате fb2, или fb2.zip, или fb2.gz

BOOK_PATH - путь до одной книги (форматы те же)


```angular2html
cd <PATH_TO_PROJECT>/src
python digger.py -s ../books/dir_with_books
```

Утилита должна пройтись по всем предложенным книгам и заполнить в БД информацию
об имеющимся в наличии книгам.
В случае, если информация о какой-то добавляемой в библиотеке книге уже есть,
то если флаг -u задан, то мы обновляем информацию о книге в библиотеке
если флага -u нет, то информация не обновляется.

### seeker.py
#### Применение: seeker.py [-h] -n BOOK_NAME [BOOK_NAME ...] [-a AUTHOR AUTHOR] [-y YEAR] [-s]

AUTHOR - имя автора

BOOK_NAME - название книги

YEAR - год издания

```angular2html
cd <PATH_TO_PROJECT>/src
python seeker.py -n Будем знакомы! -a Эльвира Зимогляд -y 2021
```

Ищет книгу по автору, названию и году.
Если указан флаг -s, то выдает только уникальный идентификатор книги, если не указан, то:
{'name' 'Book name', 'year': 2021, 'author': {'first_name': 'John', 'last_name': 'Doe'}}


### wiper.py
#### Применение: wiper.py [-h] (-n NUMBER | -a)

NUMBER - уникальный идентификатор книги (её номер)

```angular2html
cd <PATH_TO_PROJECT>/src
python wiper.py -n 1
```

Удаляет книгу из библиотеки по номеру. Если задан флаг -a , то удаляет все книги,
очищая библиотеку.
