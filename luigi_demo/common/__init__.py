import os

from dotenv import dotenv_values

DOTENV_CONFIG_FILE = '.env.test' if os.getenv('ENV') == 'test' else '.env.dev'

config = {
    **dotenv_values(DOTENV_CONFIG_FILE),
    **os.environ,
}
