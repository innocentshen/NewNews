"""
数据库连接管理
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import Generator, AsyncGenerator

from .config import settings

# 同步数据库引擎
engine = create_engine(
    settings.sqlite_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False}  # SQLite特定配置
)

# 异步数据库引擎 (如果使用PostgreSQL)
async_engine = None
if settings.database_url:
    async_engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
    )

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = None
if async_engine:
    AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

# 基类
Base = declarative_base()
metadata = MetaData()

def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """获取异步数据库会话"""
    if AsyncSessionLocal is None:
        raise RuntimeError("异步数据库未配置")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)

async def create_async_tables():
    """异步创建数据库表"""
    if async_engine:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all) 