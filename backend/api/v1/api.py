"""
API v1 路由配置
"""
from fastapi import APIRouter

from api.v1.endpoints import balance, distribution, kline, groups

api_router = APIRouter()

# 包含各个模块的路由
api_router.include_router(
    balance.router, 
    prefix="/balance", 
    tags=["余额管理"]
)

api_router.include_router(
    distribution.router, 
    prefix="/distribution", 
    tags=["资产分布"]
)

api_router.include_router(
    kline.router, 
    prefix="/kline", 
    tags=["K线数据"]
)

api_router.include_router(
    groups.router, 
    prefix="/groups", 
    tags=["分组管理"]
) 