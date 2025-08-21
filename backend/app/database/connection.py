"""
資料庫連接設定
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 創建資料庫引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 創建 SessionLocal 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 創建 Base 類別
Base = declarative_base()

def get_db():
    """獲取資料庫會話"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
