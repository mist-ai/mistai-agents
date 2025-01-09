import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create handlers
file_handler = logging.FileHandler("logs.log", mode="a")

# Create formatters and add them to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
