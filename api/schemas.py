from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserCreateSchema(BaseModel):
    """
    Schema for user creation request.
    Validates input data for creating a new user.
    """
    name: str
    email: EmailStr
    cpf: str
    phone: str

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v):
        """
        Validate CPF format (basic validation).

        Args:
            v: CPF string to validate

        Returns:
            str: Validated CPF

        Raises:
            ValueError: If CPF format is invalid
        """
        if not v or len(v.replace('.', '').replace('-', '')) != 11:
            raise ValueError('CPF must have 11 digits')
        return v


class UserUpdateSchema(BaseModel):
    """
    Schema for user update request.
    Validates input data for updating an existing user.
    """
    name: str
    email: EmailStr
    cpf: str
    phone: str

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v):
        """
        Validate CPF format (basic validation).

        Args:
            v: CPF string to validate

        Returns:
            str: Validated CPF

        Raises:
            ValueError: If CPF format is invalid
        """
        if not v or len(v.replace('.', '').replace('-', '')) != 11:
            raise ValueError('CPF must have 11 digits')
        return v


class UserResponseSchema(BaseModel):
    """
    Schema for user response.
    Defines the structure of user data returned by the API.
    """
    id: int
    name: str
    email: str
    cpf: str
    phone: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class VehicleCreateSchema(BaseModel):
    """
    Schema for vehicle creation request.
    Validates input data for creating a new vehicle.
    """
    brand: str
    model: str
    year: int
    color: str
    price: float

    @field_validator('year')
    @classmethod
    def validate_year(cls, v):
        """
        Validate vehicle year.

        Args:
            v: Year to validate

        Returns:
            int: Validated year

        Raises:
            ValueError: If year is invalid
        """
        if v < 1900 or v > 2030:
            raise ValueError('Year must be between 1900 and 2030')
        return v

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        """
        Validate vehicle price.

        Args:
            v: Price to validate

        Returns:
            float: Validated price

        Raises:
            ValueError: If price is invalid
        """
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v


class VehicleUpdateSchema(BaseModel):
    """
    Schema for vehicle update request.
    Validates input data for updating an existing vehicle.
    """
    brand: str
    model: str
    year: int
    color: str
    price: float

    @field_validator('year')
    @classmethod
    def validate_year(cls, v):
        """
        Validate vehicle year.

        Args:
            v: Year to validate

        Returns:
            int: Validated year

        Raises:
            ValueError: If year is invalid
        """
        if v < 1900 or v > 2030:
            raise ValueError('Year must be between 1900 and 2030')
        return v

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        """
        Validate vehicle price.

        Args:
            v: Price to validate

        Returns:
            float: Validated price

        Raises:
            ValueError: If price is invalid
        """
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v


class VehicleResponseSchema(BaseModel):
    """
    Schema for vehicle response.
    Defines the structure of vehicle data returned by the API.
    """
    id: int
    brand: str
    model: str
    year: int
    color: str
    price: float
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class SaleCreateSchema(BaseModel):
    """
    Schema for sale creation request.
    Validates input data for creating a new sale.
    """
    vehicle_id: int
    buyer_cpf: str

    @field_validator('buyer_cpf')
    @classmethod
    def validate_cpf(cls, v):
        """
        Validate CPF format (basic validation).

        Args:
            v: CPF string to validate

        Returns:
            str: Validated CPF

        Raises:
            ValueError: If CPF format is invalid
        """
        if not v or len(v.replace('.', '').replace('-', '')) != 11:
            raise ValueError('CPF must have 11 digits')
        return v


class SaleResponseSchema(BaseModel):
    """
    Schema for sale response.
    Defines the structure of sale data returned by the API.
    """
    id: int
    vehicle_id: int
    user_id: int
    sale_date: datetime
    payment_code: str
    payment_status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PaymentWebhookSchema(BaseModel):
    """
    Schema for payment webhook request using payment code.
    Validates payment status update data from external payment service.
    """
    payment_code: str
    status: str

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """
        Validate payment status.

        Args:
            v: Status to validate

        Returns:
            str: Validated status

        Raises:
            ValueError: If status is invalid
        """
        valid_statuses = ['pending', 'completed', 'cancelled']
        if v.lower() not in valid_statuses:
            raise ValueError(f'Status must be one of: {valid_statuses}')
        return v.lower()


class PaymentWebhookByIdSchema(BaseModel):
    """
    Schema for payment webhook request using sale ID.
    Validates payment status update data from external payment service.
    """
    sale_id: int
    status: str

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """
        Validate payment status.

        Args:
            v: Status to validate

        Returns:
            str: Validated status

        Raises:
            ValueError: If status is invalid
        """
        valid_statuses = ['pending', 'completed', 'cancelled']
        if v.lower() not in valid_statuses:
            raise ValueError(f'Status must be one of: {valid_statuses}')
        return v.lower()