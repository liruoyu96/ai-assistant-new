import asyncio
from typing import List
import httpx
import logging
import os

logger = logging.getLogger(__name__)

class PushService:
    def __init__(self):
        # 配置不同设备的推送接口
        self.push_configs = {
            "xiaomi_phone": {
                "api_url": "https://api.xiaomi.com/push",
                "api_key": os.getenv("XIAOMI_PUSH_KEY")
            },
            "xiaomi_tv": {
                "api_url": "https://api.xiaomi.com/tv/push",
                "api_key": os.getenv("XIAOMI_TV_KEY")
            },
            "huawei_tablet": {
                "api_url": "https://api.huawei.com/push",
                "api_key": os.getenv("HUAWEI_PUSH_KEY")
            }
        }
        
    async def push_to_devices(self, devices: List[str], message: str):
        tasks = []
        for device in devices:
            if device in self.push_configs:
                tasks.append(self.push_to_device(device, message))
        
        await asyncio.gather(*tasks)
    
    async def push_to_device(self, device: str, message: str):
        config = self.push_configs.get(device)
        if not config:
            logger.error(f"No push configuration found for device: {device}")
            return
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    config["api_url"],
                    headers={"Authorization": f"Bearer {config['api_key']}"},
                    json={"message": message}
                )
                response.raise_for_status()
                logger.info(f"Successfully pushed message to {device}")
        except Exception as e:
            logger.error(f"Failed to push to {device}: {str(e)}") 