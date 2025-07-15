from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, conint, constr, ValidationError
import uuid
import random
import logging
import time
from typing import Optional

router = APIRouter()

# In-memory storage for orders
orders_db = {}

ROUTES = ["North-East", "Central", "West Loop", "Downtown Express"]
ASSIGNMENT_DELAY = 2  # seconds

# Pydantic Model for order input
class OrderCreate(BaseModel):
    customer_name: constr(min_length=1, max_length=100)
    address: constr(min_length=5, max_length=200)
    item_count: conint(gt=0, le=100)

# Model for out-of-API responses
class OrderResponse(BaseModel):
    order_id: str
    status: str
    route: Optional[str]
    customer_name: Optional[str]
    address: Optional[str]
    item_count: Optional[int]

# Background function to assign route
def assign_route_background(order_id: str):
    # Simulated heavy computation delay
    logging.info(f"Assigning route for order {order_id}...")
    time.sleep(ASSIGNMENT_DELAY)
    route = random.choice(ROUTES)
    if order_id in orders_db:
        orders_db[order_id]["status"] = "assigned"
        orders_db[order_id]["route"] = route
        logging.info(f"Route '{route}' assigned for order {order_id}")
    else:
        logging.error(f"Order ID {order_id} not found during background processing.")

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    try:
        # Input already validated by Pydantic
        order_id = str(uuid.uuid4())
        orders_db[order_id] = {
            "customer_name": order.customer_name,
            "address": order.address,
            "item_count": order.item_count,
            "status": "pending",
            "route": None
        }
        background_tasks.add_task(assign_route_background, order_id)
        logging.info(f"Created order {order_id} for '{order.customer_name}', status set to 'pending'")
        return OrderResponse(
            order_id=order_id,
            status="pending",
            route=None
        )
    except ValidationError as e:
        logging.error(f"Invalid order input: {e.json()}")
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as ex:
        logging.error(f"Error creating order: {str(ex)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_status(order_id: str):
    order = orders_db.get(order_id)
    if not order:
        logging.warning(f"Order {order_id} not found on GET.")
        raise HTTPException(status_code=404, detail="Order not found.")
    return OrderResponse(
        order_id=order_id,
        status=order["status"],
        route=order["route"],
        customer_name=order["customer_name"],
        address=order["address"],
        item_count=order["item_count"]
    )
