import importlib
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

if __name__ == "__main__":
    #Run backend
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    app_api = importlib.import_module("examples.api.app")
    app_api.run(host=host, port=port)
