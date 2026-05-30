"""
余额管理API端点
"""
import time
from typing import Optional
from decimal import Decimal
from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import JSONResponse

from schemas.balance import BalanceRequest, BalanceResponse, BalanceInfo, AccountInfo
from services.binance_service import binance_service
from core.config import settings

router = APIRouter()


@router.get("/info", response_model=AccountInfo, summary="获取账户信息")
async def get_account_info():
    """获取币安账户基本信息"""
    try:
        info = await binance_service.get_account_info()
        return AccountInfo(**info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@router.get("/", response_model=BalanceResponse, summary="获取余额列表")
async def get_balances(
    threshold: Optional[float] = Query(
        default=None, 
        description="USDT价值阈值，默认1.0",
        ge=0
    ),
    sort_by: str = Query(
        default="value", 
        description="排序方式: value(价值), amount(数量), asset(资产名)"
    ),
    sort_order: str = Query(
        default="desc", 
        description="排序顺序: asc(升序), desc(降序)"
    )
):
    """
    获取账户余额列表
    
    - **threshold**: USDT价值阈值，只显示大于该值的资产
    - **sort_by**: 排序方式
    - **sort_order**: 排序顺序
    """
    try:
        # 使用默认阈值如果未指定
        if threshold is None:
            threshold = settings.default_usdt_threshold
        
        # 获取余额数据
        balances_data = await binance_service.get_balances(threshold=threshold)
        
        # 转换为响应格式
        balance_items = []
        total_usdt_value = Decimal('0')
        
        for balance in balances_data:
            balance_info = BalanceInfo(
                asset=balance['asset'],
                free=balance['free'],
                locked=balance['locked'],
                total=balance['total'],
                usdt_value=balance.get('usdt_value', '0'),
                percentage=balance.get('percentage', 0)
            )
            balance_items.append(balance_info)
            
            if balance.get('usdt_value'):
                total_usdt_value += Decimal(str(balance['usdt_value']))
        
        # 应用排序
        if sort_by == "value":
            balance_items.sort(
                key=lambda x: float(x.usdt_value or 0), 
                reverse=(sort_order == "desc")
            )
        elif sort_by == "amount":
            balance_items.sort(
                key=lambda x: float(x.total), 
                reverse=(sort_order == "desc")
            )
        elif sort_by == "asset":
            balance_items.sort(
                key=lambda x: x.asset, 
                reverse=(sort_order == "desc")
            )
        
        return BalanceResponse(
            balances=balance_items,
            total_count=len(balances_data),
            filtered_count=len(balance_items),
            total_usdt_value=str(total_usdt_value),
            threshold=threshold,
            timestamp=int(time.time() * 1000)
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@router.get("/{asset}", response_model=BalanceInfo, summary="获取特定资产余额")
async def get_balance_by_asset(
    asset: str = Path(..., description="资产名称，如BTC, ETH等")
):
    """获取特定资产的余额信息"""
    try:
        balance_data = await binance_service.get_balance_by_asset(asset)
        
        if not balance_data:
            raise HTTPException(
                status_code=404, 
                detail=f"未找到资产 {asset.upper()} 的余额信息"
            )
        
        return BalanceInfo(
            asset=balance_data['asset'],
            free=balance_data['free'],
            locked=balance_data['locked'],
            total=balance_data['total'],
            usdt_value=balance_data.get('usdt_value', '0'),
            percentage=balance_data.get('percentage', 0)
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@router.post("/", response_model=BalanceResponse, summary="查询余额（POST方式）")
async def query_balances(request: BalanceRequest):
    """
    使用POST方式查询余额，支持更复杂的查询参数
    """
    try:
        # 获取余额数据
        if request.asset:
            # 查询特定资产
            balance_data = await binance_service.get_balance_by_asset(request.asset)
            balances_data = [balance_data] if balance_data else []
        else:
            # 查询所有资产
            balances_data = await binance_service.get_balances(threshold=request.threshold)
        
        # 转换格式并计算总价值
        balance_items = []
        total_usdt_value = Decimal('0')
        
        for balance in balances_data:
            balance_info = BalanceInfo(
                asset=balance['asset'],
                free=balance['free'],
                locked=balance['locked'],
                total=balance['total'],
                usdt_value=balance.get('usdt_value', '0'),
                percentage=balance.get('percentage', 0)
            )
            balance_items.append(balance_info)
            
            if balance.get('usdt_value'):
                total_usdt_value += Decimal(str(balance['usdt_value']))
        
        # 应用排序
        if request.sort_by == "value":
            balance_items.sort(
                key=lambda x: float(x.usdt_value or 0), 
                reverse=(request.sort_order == "desc")
            )
        elif request.sort_by == "amount":
            balance_items.sort(
                key=lambda x: float(x.total), 
                reverse=(request.sort_order == "desc")
            )
        elif request.sort_by == "asset":
            balance_items.sort(
                key=lambda x: x.asset, 
                reverse=(request.sort_order == "desc")
            )
        
        return BalanceResponse(
            balances=balance_items,
            total_count=len(balances_data),
            filtered_count=len(balance_items),
            total_usdt_value=str(total_usdt_value),
            threshold=request.threshold or settings.default_usdt_threshold,
            timestamp=int(time.time() * 1000)
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}") 