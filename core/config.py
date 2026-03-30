import os
# import yaml
from dotenv import load_dotenv

load_dotenv()  # loads .env once


class Config:
    def __init__(self):
        self.login_url = os.getenv("LOGIN_URL")
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASS")
        self.referer_url = os.getenv("REFERER_URL")
        self.origin_url = os.getenv("ORIGIN_URL")


    def auth(self):
        return {
            "login_url": self.login_url,
            "email": self.email,
            "password": self.password,
            "referer_url": self.referer_url,
            "origin_url": self.origin_url,
        }
