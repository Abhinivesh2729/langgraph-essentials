import os
from dotenv import load_dotenv

def load_env_vars(env_path=".env"):
    load_dotenv(env_path, override=True)

# Usage
load_env_vars()