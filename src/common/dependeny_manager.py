from src.database.database import DBHandler


class DependencyManager:
    def __init__(self):
        self.db_connection = DBHandler()
