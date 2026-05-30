"""
应用配置管理
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用设置"""
    
    # 应用基础配置
    app_name: str = "币安资产管理系统"
    debug: bool = Field(default=False, env="DEBUG")
    
    # 币安API配置
    binance_api_key: str = Field(..., env="BINANCE_API_KEY")
    binance_api_secret: str = Field(..., env="BINANCE_API_SECRET")
    binance_testnet: bool = Field(default=False, env="BINANCE_TESTNET")
    
    # 数据库配置
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    sqlite_url: str = Field(default="sqlite:///./binance_assets.db", env="SQLITE_URL")
    
    # Redis配置
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # 缓存配置
    cache_ttl: int = Field(default=300, env="CACHE_TTL")  # 5分钟
    balance_cache_ttl: int = Field(default=60, env="BALANCE_CACHE_TTL")  # 1分钟
    price_cache_ttl: int = Field(default=10, env="PRICE_CACHE_TTL")  # 10秒
    
    # WebSocket配置
    ws_heartbeat_interval: int = Field(default=30, env="WS_HEARTBEAT_INTERVAL")
    
    # 任务调度配置
    enable_scheduler: bool = Field(default=True, env="ENABLE_SCHEDULER")
    price_update_interval: int = Field(default=30, env="PRICE_UPDATE_INTERVAL")  # 30秒
    
    # USDT过滤默认值
    default_usdt_threshold: float = Field(default=1.0, env="DEFAULT_USDT_THRESHOLD")
    
    class Config:
        env_file = "../env.env"
        case_sensitive = False


# 全局设置实例
settings = Settings() 