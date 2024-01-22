from dotenv import load_dotenv, find_dotenv

# Load the users .env file into environment variables
#load_dotenv(verbose=True, override=True)
#ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#load_dotenv(os.path.join(ROOT_PATH, ".env"))
#print(ROOT_PATH)

_ = load_dotenv(find_dotenv())
del load_dotenv
