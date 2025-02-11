import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s\n-> %(message)s\n",
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
