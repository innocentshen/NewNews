"""
Binance API 服务层
集成现有的binance_api模块
"""
import sys
import os
from typing import List, Dict, Any, Optional
from decimal import Decimal

# 添加binance_api模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
binance_api_path = os.path.join(current_dir, '..', '..', 'binance', 'binance_api')
sys.path.insert(0, binance_api_path)

from binance_account import BinanceAccount
from exceptions import BinanceAPIError

from core.config import settings


class BinanceService:
    """Binance API服务类"""
    
    def __init__(self):
        self._account = None
    
    def get_account(self) -> BinanceAccount:
        """获取账户实例"""
        if self._account is None:
            self._account = BinanceAccount()
        return self._account
    
    async def get_account_info(self) -> Dict[str, Any]:
        """获取账户信息"""
        try:
            with self.get_account() as account:
                return account.get_account_info()
        except BinanceAPIError as e:
            raise ValueError(f"获取账户信息失败: {str(e)}")
    
    async def get_balances(
        self, 
        threshold: Optional[float] = None,
        asset: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取余额信息
        
        Args:
            threshold: USDT价值阈值，默认使用配置中的值
            asset: 特定资产名称，如果指定则只返回该资产
        
        Returns:
            余额列表
        """
        try:
            with self.get_account() as account:
                if threshold is None:
                    threshold = settings.default_usdt_threshold
                
                if asset:
                    balance = account.get_balance(asset=asset)
                    return [balance] if balance else []
                else:
                    return account.get_balance(threshold=threshold)
        except BinanceAPIError as e:
            raise ValueError(f"获取余额信息失败: {str(e)}")
    
    async def get_balance_by_asset(self, asset: str) -> Optional[Dict[str, Any]]:
        """获取特定资产余额"""
        try:
            with self.get_account() as account:
                return account.get_balance(asset=asset.upper())
        except BinanceAPIError as e:
            raise ValueError(f"获取{asset}余额失败: {str(e)}")
    
    async def get_price(self, symbol: str) -> Dict[str, Any]:
        """获取价格信息"""
        try:
            with self.get_account() as account:
                return account.get_price(symbol)
        except BinanceAPIError as e:
            raise ValueError(f"获取{symbol}价格失败: {str(e)}")
    
    async def get_24hr_ticker(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """获取24小时价格统计"""
        try:
            with self.get_account() as account:
                return account.get_24hr_ticker(symbol)
        except BinanceAPIError as e:
            raise ValueError(f"获取24小时统计失败: {str(e)}")
    
    async def calculate_total_value_usdt(self, balances: List[Dict[str, Any]]) -> Decimal:
        """计算总USDT价值"""
        total_value = Decimal('0')
        
        for balance in balances:
            if balance['asset'] == 'USDT':
                total_value += Decimal(str(balance['total']))
            else:
                try:
                    # 获取对USDT的价格
                    symbol = f"{balance['asset']}USDT"
                    price_data = await self.get_price(symbol)
                    price = Decimal(str(price_data.get('price', 0)))
                    amount = Decimal(str(balance['total']))
                    total_value += price * amount
                except:
                    # 如果获取价格失败，跳过该资产
                    continue
        
        return total_value
    
    def close(self):
        """关闭连接"""
        if self._account:
            self._account.close()
            self._account = None


# 全局服务实例
binance_service = BinanceService() 