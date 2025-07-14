import httpx
from app.schemas import OrderInDB

async def notify_webhook(webhook_url: str, order: OrderInDB):
    payload = order.dict()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(webhook_url, json=payload, timeout=5.0)
            resp.raise_for_status()
        except Exception as e:
            # In production, log errors - here just pass silently
            pass
