from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class VehicleStatus(Enum):
    """
    Enumeration representing the status of a vehicle in the system.
    Available values:
    - AVAILABLE: Vehicle is available for sale
    - SOLD: Vehicle has been sold
    - RESERVED: Vehicle is reserved for a potential buyer
    """
    AVAILABLE = "available"
    SOLD = "sold"
    RESERVED = "reserved"


class PaymentStatus(Enum):
    """
    Enumeration representing the status of a payment transaction.
    Available values:
    - PENDING: Payment is pending processing
    - COMPLETED: Payment has been successfully processed
    - CANCELLED: Payment has been cancelled
    """
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class User:
    """
    Entity representing a user in the system.

    Attributes:
        id: Unique identifier for the user
        name: Full name of the user
        email: Email address of the user (must be unique)
        cpf: Brazilian CPF document number (must be unique)
        phone: Phone number of the user
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
    """
    id: Optional[int]
    name: str
    email: str
    cpf: str
    phone: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Vehicle:
    """
    Entity representing a vehicle in the dealership system.

    Attributes:
        id: Unique identifier for the vehicle
        brand: Brand/manufacturer of the vehicle
        model: Model name of the vehicle
        year: Manufacturing year of the vehicle
        color: Color of the vehicle
        price: Sale price of the vehicle in the system currency
        status: Current status of the vehicle (available, sold, reserved)
        created_at: Timestamp when the vehicle was created
        updated_at: Timestamp when the vehicle was last updated
    """
    id: Optional[int]
    brand: str
    model: str
    year: int
    color: str
    price: float
    status: VehicleStatus = VehicleStatus.AVAILABLE
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Sale:
    """
    Entity representing a vehicle sale transaction.

    Attributes:
        id: Unique identifier for the sale
        vehicle_id: ID of the vehicle being sold
        user_id: ID of the user purchasing the vehicle
        sale_date: Date when the sale occurred
        payment_code: Unique code for payment processing
        payment_status: Current status of the payment
        created_at: Timestamp when the sale was created
        updated_at: Timestamp when the sale was last updated
    """
    id: Optional[int]
    vehicle_id: int
    user_id: int
    sale_date: datetime
    payment_code: str
    payment_status: PaymentStatus = PaymentStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None