"""
币安资产管理系统 - FastAPI后端
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

from core.config import settings
from api.v1.api import api_router

app = FastAPI(
    title="币安资产管理系统",
    description="基于FastAPI的币安资产管理和分析系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加GZIP压缩中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 包含API路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return {"message": "币安资产管理系统API", "version": "1.0.0", "status": "运行中"}

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "binance-asset-manager"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["./"],
    ) 