import os
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import httpx
import json
from typing import Optional
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Assistant Server")

# 从环境变量获取配置
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
SYSTEM_API_KEY = os.getenv("SYSTEM_API_KEY")

api_key_header = APIKeyHeader(name="X-API-Key")

class CommandRequest(BaseModel):
    command: str
    voice_input: Optional[bool] = False
    target_devices: Optional[list[str]] = []

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != SYSTEM_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.post("/execute")
async def execute_command(request: CommandRequest, api_key: str = Security(verify_api_key)):
    try:
        # 记录命令
        logger.info(f"Received command: {request.command} at {datetime.now()}")
        
        # 调用智谱AI API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                headers={
                    "Authorization": f"Bearer {ZHIPU_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "glm-4",
                    "messages": [{"role": "user", "content": request.command}]
                }
            )
            
            ai_response = response.json()
            
            # 处理AI响应
            # TODO: 实现命令执行逻辑
            
            # 发送推送通知
            if request.target_devices:
                await send_push_notification(request.target_devices, ai_response)
                
            return {"status": "success", "response": ai_response}
            
    except Exception as e:
        logger.error(f"Error executing command: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def send_push_notification(devices: list[str], message: str):
    # TODO: 实现设备推送逻辑
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem") 