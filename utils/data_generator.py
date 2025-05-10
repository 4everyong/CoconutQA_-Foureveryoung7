import random
import string
from faker import Faker
fake = Faker("ru_RU")


class DataGenerator:
    @staticmethod
    def generate_random_film():
        random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
        return f"Фильм {random_string}"

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