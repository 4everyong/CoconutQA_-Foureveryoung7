#Modul_4\Cinescope\db_requester\sql_alchemy_client_simple_example.py
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Подключение к базе данных
host = "92.255.111.76"
port = 31200
database_name = "db_movies"
username = "postgres"
password = "AmwFrtnR2"

#формируем урл для подключения к базе
connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
#обьект для подключения к базе данных
engine = create_engine(connection_string)


# Modul_4\Cinescope\db_requester\sql_alchemy_client_simple_example.py
def sdl_alchemy_SQL():
    query = """
    SELECT id, email, full_name, "password", created_at, updated_at, verified, banned, roles
    FROM public.users
    WHERE id = :user_id;
    """

    # Параметры запроса для подстановки в наш SQL запрос
    user_id = "d3f7f169-9771-4c76-bd97-7619dc97af40"

    # Выполняем запрос
    with engine.connect() as connection:  # выполняем соединенеи с базой данных и автоматически закрываем его по завершени выполнения
        result = connection.execute(text(query), {"user_id": user_id})
        for row in result:
            print(row)


if __name__ == "__main__":
    sdl_alchemy_SQL()