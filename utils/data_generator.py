import random
import string

import faker
from faker import Faker
fake = Faker()


class DataGenerator:
    @staticmethod
    def generate_random_film():
        random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
        return f"Фильм {random_string}"

    @staticmethod
    def generate_reviews():
        random_string = ''.join(random.choices(string.ascii_lowercase, k=40))
        return random_string

    @staticmethod
    def generate_random_image_url():
        return fake.uri()

    @staticmethod
    def generate_random_price():
        return random.randint(100, 1000)

    @staticmethod
    def generate_random_description():
        random_string = ''.join(random.choices(string.ascii_lowercase, k=30))
        return f"Описание {random_string}"

    @staticmethod
    def generate_random_location():
        locations = ["SPB", "MSK"]
        return random.choice(locations)

    @staticmethod
    def generate_random_published():
        published = [True, False]
        return random.choice(published)

    @staticmethod
    def generate_random_genre_id():
        return random.randint(1, 10)

    @staticmethod
    def generate_random_email():
        unique_part = ''.join(random.choices(string.ascii_lowercase, k=12))
        return f"test-{unique_part}-user@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{fake.first_name()} {fake.last_name()}"

    @staticmethod
    def generate_random_password():
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)