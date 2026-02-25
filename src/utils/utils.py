import logging


def get_logger(filename):
    logger = logging.getLogger(f"myfastapp.{filename}")
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


# # Database setup
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = sqlalchemy.orm.declarative_base()