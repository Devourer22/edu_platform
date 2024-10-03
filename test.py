from datetime import datetime, timedelta


class Schedule:
    def __init__(self, week_type):
        self.week_type = week_type
        self.schedule = {}

    def add_task(self, day, task, total_lessons):
        if day in self.schedule:
            self.schedule[day].append(
                (task, total_lessons, 0))  # Добавляем кортеж (предмет, общее количество занятий, прогресс)
        else:
            self.schedule[day] = [(task, total_lessons, 0)]

    def complete_task(self, day, task):
        for idx, (t, total, progress) in enumerate(self.schedule[day]):
            if t == task:
                if progress < total:
                    self.schedule[day][idx] = (t, total, progress + 1)
                else:
                    print(f"All lessons for {task} completed.")

    def print_schedule(self):
        for day, tasks in self.schedule.items():
            print(f"{day}:", end=" ")
            tasks_str = []
            for task, total, progress in tasks:
                tasks_str.append(f"{task} ({progress}/{total})")
            print(", ".join(tasks_str))


class BlueWeek(Schedule):
    def __init__(self):
        super().__init__("Blue")


class RedWeek(Schedule):
    def __init__(self):
        super().__init__("Red")


class SemesterSchedule:
    def __init__(self, start_date, end_date, blue_week_schedule, red_week_schedule):
        self.start_date = start_date
        self.end_date = end_date
        self.current_date = start_date
        self.blue_week_schedule = blue_week_schedule
        self.red_week_schedule = red_week_schedule
        self.current_week = None

    def create_schedule(self):
        while self.current_date < self.end_date:
            week_start = self.current_date.strftime('%d.%m')
            self.current_date += timedelta(days=6)
            week_end = self.current_date.strftime('%d.%m')
            if self.current_week is None or self.current_week.week_type == "Red":
                self.current_week = self.blue_week_schedule
                print(f"{week_start} - {week_end} - Blue Week")
            else:
                self.current_week = self.red_week_schedule
                print(f"{week_start} - {week_end} - Red Week")

            for day, tasks in self.current_week.schedule.items():
                print(f"{day}:", end=" ")
                for task, total, progress in tasks:
                    print(f"{task} ({progress}/{total}),", end=" ")
                print()
            print()
            self.current_date += timedelta(days=1)


def transform_data(data):
    blue_week_schedule = BlueWeek()
    red_week_schedule = RedWeek()
    for day, tasks in data.items():
        for task in tasks:
            subject = task[2].split('.')[2].strip()  # Extracting subject from the third element of the task
            total_tasks = int(task[0])  # Converting total tasks to integer
            if data[day] == data['пн']:
                blue_week_schedule.add_task(day.capitalize(), subject, total_tasks)
            else:
                red_week_schedule.add_task(day.capitalize(), subject, total_tasks)
    return blue_week_schedule, red_week_schedule


# Исходные данные
data = {'пн': [], 'вт': [], 'ср': [['3', '11:20 - 12:50', 'конс. Технологии разработки программного обеспечения', 'доц. Грязнов А.С.', '203 К']], 'чт': [['3', '11:20 - 12:50', 'экз. Технологии разработки программного обеспечения', 'доц. Грязнов А.С.', '203 К']], 'пт': [], 'сб': []}

# Преобразование данных
blue_week_schedule, red_week_schedule = transform_data(data)

# Создаем объект SemesterSchedule и выводим расписание
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 1, 12)
semester_schedule = SemesterSchedule(start_date, end_date, blue_week_schedule, red_week_schedule)
print(f"Semester Schedule from {start_date.strftime('%d.%m')} to {end_date.strftime('%d.%m')}:")
semester_schedule.create_schedule()
