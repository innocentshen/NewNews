"""
分组管理API端点
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="获取资产分组")
async def get_groups():
    """获取资产分组 - 待实现"""
    return {"message": "分组管理功能正在开发中"} 