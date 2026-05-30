"""
余额相关的Pydantic模型
"""
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, validator


class BalanceInfo(BaseModel):
    """单个资产余额信息"""
    asset: str = Field(..., description="资产名称")
    free: str = Field(..., description="可用余额")
    locked: str = Field(..., description="锁定余额")
    total: str = Field(..., description="总余额")
    usdt_value: Optional[str] = Field(None, description="USDT价值")
    percentage: Optional[float] = Field(None, description="占总资产百分比")
    
    @validator('asset')
    def asset_must_be_uppercase(cls, v):
        return v.upper()
    
    class Config:
        schema_extra = {
            "example": {
                "asset": "BTC",
                "free": "0.12345678",
                "locked": "0.00000000",
                "total": "0.12345678",
                "usdt_value": "4567.89",
                "percentage": 45.67
            }
        }


class BalanceRequest(BaseModel):
    """余额查询请求"""
    asset: Optional[str] = Field(None, description="特定资产名称")
    threshold: Optional[float] = Field(1.0, description="USDT价值阈值", ge=0)
    sort_by: Optional[str] = Field("value", description="排序方式: value, amount, asset")
    sort_order: Optional[str] = Field("desc", description="排序顺序: asc, desc")
    
    @validator('asset')
    def asset_to_uppercase(cls, v):
        return v.upper() if v else v
    
    @validator('sort_by')
    def validate_sort_by(cls, v):
        allowed = ['value', 'amount', 'asset']
        if v not in allowed:
            raise ValueError(f'sort_by must be one of {allowed}')
        return v
    
    @validator('sort_order')
    def validate_sort_order(cls, v):
        allowed = ['asc', 'desc']
        if v not in allowed:
            raise ValueError(f'sort_order must be one of {allowed}')
        return v


class BalanceResponse(BaseModel):
    """余额查询响应"""
    balances: List[BalanceInfo] = Field(..., description="余额列表")
    total_count: int = Field(..., description="总资产数量")
    filtered_count: int = Field(..., description="过滤后数量")
    total_usdt_value: str = Field(..., description="总USDT价值")
    threshold: float = Field(..., description="使用的阈值")
    timestamp: int = Field(..., description="查询时间戳")
    
    class Config:
        schema_extra = {
            "example": {
                "balances": [
                    {
                        "asset": "BTC",
                        "free": "0.12345678",
                        "locked": "0.00000000",
                        "total": "0.12345678",
                        "usdt_value": "4567.89",
                        "percentage": 45.67
                    }
                ],
                "total_count": 50,
                "filtered_count": 5,
                "total_usdt_value": "10000.00",
                "threshold": 1.0,
                "timestamp": 1703000000000
            }
        }


class AccountInfo(BaseModel):
    """账户信息"""
    account_type: str = Field(..., description="账户类型")
    can_trade: bool = Field(..., description="是否可交易")
    can_withdraw: bool = Field(..., description="是否可提现")
    can_deposit: bool = Field(..., description="是否可充值")
    total_assets: int = Field(..., description="总资产数量")
    update_time: int = Field(..., description="更新时间")
    
    class Config:
        schema_extra = {
            "example": {
                "account_type": "SPOT",
                "can_trade": True,
                "can_withdraw": True,
                "can_deposit": True,
                "total_assets": 50,
                "update_time": 1703000000000
            }
        } 