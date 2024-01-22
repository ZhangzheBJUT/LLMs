import os
from singleton import Singleton
class Config(metaclass=Singleton):
    """Configuration class to store the state of bools for different scripts access"""

    def __init__(self) -> None:
        """Initialize the Config class"""

        self.access_key_id = os.getenv('ACCESS_KEY_ID')
        self.access_key_secret = os.getenv('ACCESS_KEY_SECRET')
        self.agent_key = os.getenv('AGENT_KEY')
        self.app_id = os.getenv('APP_ID')
        self.WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", 8000))

        current_path = os.path.abspath(os.path.dirname(__file__))
        self.doc_file_path = os.path.join(current_path, '../' + os.getenv('DOC_FILE_PATH'))
        self.vector_persist_path = os.path.join(current_path, '../' + os.getenv('VECTOR_PERSIST_PATH'))
        self.model_name = os.path.join(current_path, '../' + os.getenv('MODEL_NAME'))

        self.vector_store_name = os.getenv('VECTOR_STORE_NAME')