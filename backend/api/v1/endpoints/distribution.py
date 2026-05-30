"""
资产分布API端点
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="获取资产分布数据")
async def get_distribution():
    """获取资产分布数据 - 待实现"""
    return {"message": "资产分布功能正在开发中"} 