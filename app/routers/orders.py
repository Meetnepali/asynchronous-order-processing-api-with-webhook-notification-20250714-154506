from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from app.schemas import OrderCreate, OrderInDB, OrderResponse, ErrorResponse
from app.db import get_session
from app.models import Order
from app.webhook import notify_webhook
import os

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=201, responses={
    400: {"model": ErrorResponse, "description": "Validation Error"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}, summary="Place a new order", response_description="Order created successfully")
async def place_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """
    Place a new order. Validates input, persists to database, and asynchronously notifies external webhook.
    """
    try:
        db_order = Order(**order.dict())
        session.add(db_order)
        await session.commit()
        await session.refresh(db_order)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred while saving order.")
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        background_tasks.add_task(notify_webhook, webhook_url, OrderInDB.from_orm(db_order))
    return OrderResponse(order=OrderInDB.from_orm(db_order))


@router.get("/{order_id}", response_model=OrderResponse, responses={
    404: {"model": ErrorResponse, "description": "Order Not Found"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}, summary="Get order by ID", response_description="Order details")
async def get_order(order_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve an order by its unique ID.
    """
    try:
        result = await session.get(Order, order_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Order ID {order_id} not found.")
        return OrderResponse(order=OrderInDB.from_orm(result))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while retrieving order.")
