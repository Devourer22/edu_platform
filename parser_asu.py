# Подключаем библиотеки: selenium, webdriver
# Используем импорт команды "Ву", чтобы отфильтровать данные по классу на странице
from selenium.webdriver.common.by import By
from selenium import webdriver



def parsing(url):
    browser = webdriver.Chrome()
    browser.get(url)

    # Ищем в коде страницы определённый класс
    blocks = browser.find_elements(By.CLASS_NAME, 'schedule_table-body-rows_group')

    # Создаем пустой список дней недели
    timetable_by_day = {
        "пн": [],
        "вт": [],
        "ср": [],
        "чт": [],
        "пт": [],
        "сб": [],
    }

    day_schedule = []

    # Разбиваем полученную информацию на строки и заполняем список
    if blocks:
        for elements in blocks:
            text = elements.text
            lines = text.split('\n')
            day_of_week = lines[0]
            date = lines[1]
            schedule_info = lines[2:]
            timetable_by_day[day_of_week].append(schedule_info)
    else:
        # Если пусто:
        return 0

    return timetable_by_day


def search_schedule(parsed_schedule, desired_day):
    new_schedule = []
    for day, schedule in parsed_schedule.items():
        if day.lower() == desired_day.lower() or desired_day.lower() == 'все':
            day_schedule = []
            day_schedule.append(f'{day}:')
            for item in schedule:
                if not item[0].isdigit():
                    continue  # Пропускаем итерацию, если нет числового обозначения пары
                for i in range(0, len(item), 5):
                    # Проверяем, что элементы доступны в списке
                    if i + 4 >= len(item):
                        break  # Если элементы не доступны, выходим из цикла
                    pair_number = item[i]
                    times = item[i + 1]
                    subject = item[i + 2]
                    teacher = item[i + 3]
                    room = item[i + 4]
                    day_schedule.append(f' {pair_number} - {times}, {subject}, {teacher}, {room}')
            new_schedule.append('\n'.join(day_schedule))
    return new_schedule

