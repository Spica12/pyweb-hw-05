<h1 align="center">Homework-05</h1>

Публічне АПІ ПриватБанка дозволяє отримати інформацію про готівку курсах валют ПриватБанку та НБУ на обрану дату. Архів зберігає дані за останні 4 роки

Напишіть консольну утиліту, яка повертає курс EUR та USD ПриватБанку протягом останніх кількох днів. Встановіть обмеження, що в утиліті можна дізнатися курс валют не більше, ніж за останні 10 днів. Для запиту до АПІ використовуйте Aiohttp client. Дотримуйтесь принципів SOLID під час написання завдання. Обробляйте коректно помилки при мережевих запитах.

Приклад роботи:

py .\main.py 2

Результат програми:

[\n
  {\n
    '03.11.2022': {\n
      'EUR': {\n
        'sale': 39.4,\n
        'purchase': 38.4\n
      },\n
      'USD': {\n
        'sale': 39.9,\n
        'purchase': 39.4\n
      }
    }
  },
  {
    '02.11.2022': {
      'EUR': {
        'sale': 39.4,
        'purchase': 38.4
      },
      'USD': {
        'sale': 39.9,
        'purchase': 39.4
      }
    }
  }
]

Додаткова частина

1) додайте можливість вибору, через передані параметри консольної утиліти, додаткових валют у відповіді програми
2) візьміть чат на веб-сокетах з лекційного матеріалу та додайте до нього можливість введення команди exchange. Вона показує користувачам поточний 3)   курс валют у текстовому форматі. Формат представлення виберіть на власний розсуд
3) розширте додану команду exchange, щоб була можливість переглянути курс валют в чаті за останні кілька днів. 
    Приклад exchange 2
4) за допомогою пакетів aiofile та aiopath додайте логування до файлу, коли була виконана команда exchange у чаті