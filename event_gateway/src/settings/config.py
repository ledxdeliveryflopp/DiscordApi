import configparser
from dataclasses import dataclass

from src.settings.settings import settings


@dataclass
class AlembicIni:
    """Настройка alembic ini"""
    config = configparser.ConfigParser()

    def set_database_url(self) -> None:
        """Установка database url в alembic ini"""
        self.config.read('alembic.ini')
        self.config.set("alembic", "sqlalchemy.url", settings.database_settings.get_full_db_path)
        with open('alembic.ini', 'w') as config_file:
            self.config.write(config_file)


def init_alembic_ini() -> AlembicIni:
    return AlembicIni()


alembic_ini_settings = init_alembic_ini()
