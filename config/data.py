import os
from dotenv import load_dotenv

load_dotenv()


class Data:

    def __init__(self):
        self.LOGIN = os.getenv("LOGIN")
        self.PASSWORD = os.getenv("PASSWORD")
        if not self.LOGIN or not self.PASSWORD:
            raise ValueError("LOGIN и PASSWORD должны быть заданы в .env или переменных окружения")