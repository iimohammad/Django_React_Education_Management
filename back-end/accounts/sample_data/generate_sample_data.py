import csv
import random


class Command:
    @staticmethod
    def generate_random_username():
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=6))

    @staticmethod
    def generate_random_name():
        return ''.join(random.choices(
            'abcdefghijklmnopqrstuvwxyz', k=5)).capitalize()

    @staticmethod
    def generate_random_email():
        domain = random.choice(['example.com', 'test.org', 'sample.net'])
        return f'{Command.generate_random_username()}@{domain}'

    @staticmethod
    def generate_random_semester():
        season = random.choice(['Spring', 'Summer', 'Fall', 'Winter'])
        year = random.randint(2010, 2023)
        return f'{season} {year}'

    @staticmethod
    def generate_random_gpa():
        return round(random.uniform(2.0, 4.0), 2)

    @staticmethod
    def generate_random_year():
        return random.randint(2015, 2025)

    @staticmethod
    def handle(*args, **options):
        # Generate sample data for each model
        user_data = [{'username': Command.generate_random_username(),
                      'first_name': Command.generate_random_name(),
                      'last_name': Command.generate_random_name(),
                      'email': Command.generate_random_email()} for _ in range(100)]

        student_data = [
            {'entry_semester': Command.generate_random_semester(), 'gpa': Command.generate_random_gpa(),
             'entry_year': Command.generate_random_year(), 'year_of_study': random.randint(1, 4)}
            for _ in range(100)
        ]

        teacher_data = [
            {'expertise': random.choice(['Computer Science', 'Mathematics', 'Physics']),
             'rank': random.choice(['Assistant Professor', 'Associate Professor', 'Professor']),
             'department__department_name': random.choice(['Department A', 'Department B', 'Department C'])}
            for _ in range(100)
        ]

        assistant_data = [
            {'field__major_name': random.choice(
                ['Chemistry', 'Biology', 'Geology', 'Mathematics', 'Physics'])}
            for _ in range(100)
        ]

        # Write data to CSV files
        with open('user_data.csv', 'w', newline='') as user_file:
            user_writer = csv.DictWriter(
                user_file, fieldnames=user_data[0].keys())
            user_writer.writeheader()
            user_writer.writerows(user_data)

        with open('student_data.csv', 'w', newline='') as student_file:
            student_writer = csv.DictWriter(
                student_file, fieldnames=student_data[0].keys())
            student_writer.writeheader()
            student_writer.writerows(student_data)

        with open('steacher_data.csv', 'w', newline='') as teacher_file:
            teacher_writer = csv.DictWriter(
                teacher_file, fieldnames=teacher_data[0].keys())
            teacher_writer.writeheader()
            teacher_writer.writerows(teacher_data)

        with open('assistant_data.csv', 'w', newline='') as assistant_file:
            assistant_writer = csv.DictWriter(
                assistant_file, fieldnames=assistant_data[0].keys())
            assistant_writer.writeheader()
            assistant_writer.writerows(assistant_data)

        print('Sample data exported successfully')


# Execute the command
Command.handle()
