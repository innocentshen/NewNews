"""
K线数据API端点
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="获取K线数据")
async def get_kline():
    """获取K线数据 - 待实现"""
    return {"message": "K线数据功能正在开发中"} 