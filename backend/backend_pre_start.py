import logging
from dotenv import load_dotenv, find_dotenv
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from sqlalchemy import text
from session import SessionLocal
from loguru import logger

# Define the maximum number of tries and the wait time between tries
MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1

load_dotenv(find_dotenv())  # take environment variables from .env.

@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    """
    Initialize the database connection.

    This function attempts to establish a connection to the database 
    by creating a session and executing a simple query. If the 
    connection attempt fails, it raises an exception, which 
    causes the retry decorator to retry the connection attempt.

    Raises:
        Exception: An error occurred while trying to connect to the database.
    """
    try:
        # Create a new session
        db = SessionLocal()
        # Try to execute a simple query to check if the database is awake
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    """
    Main function.

    This function logs the start of the service initialization, 
    calls the init function to establish a database connection,
    and then logs the successful completion of the service initialization.
    """
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
