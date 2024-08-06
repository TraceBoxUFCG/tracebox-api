from app.common.database.database import SessionLocal
from sqlalchemy.sql import text


def init() -> None:
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
    except Exception as e:
        raise e


def main() -> None:
    print("Initializing service")
    init()
    print("Service finished initializing")


if __name__ == "__main__":
    main()
