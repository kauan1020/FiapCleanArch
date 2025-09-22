from datetime import datetime
from typing import Optional, List
import uuid
from domain.entities import Sale, VehicleStatus, PaymentStatus
from interfaces.repositories import SaleRepositoryInterface, VehicleRepositoryInterface, UserRepositoryInterface
from interfaces.gateways import PaymentGatewayInterface, NotificationGatewayInterface


class CreateSaleUseCase:
    """
    Use case for creating a new vehicle sale.
    Handles payment processing and vehicle status update.
    """

    def __init__(
            self,
            sale_repository: SaleRepositoryInterface,
            vehicle_repository: VehicleRepositoryInterface,
            user_repository: UserRepositoryInterface,
            payment_gateway: PaymentGatewayInterface,
            notification_gateway: NotificationGatewayInterface
    ):
        self.sale_repository = sale_repository
        self.vehicle_repository = vehicle_repository
        self.user_repository = user_repository
        self.payment_gateway = payment_gateway
        self.notification_gateway = notification_gateway

    async def execute(self, vehicle_id: int, buyer_cpf: str) -> Sale:
        """
        Execute the create sale use case.

        Args:
            vehicle_id: ID of the vehicle being sold
            buyer_cpf: CPF of the person purchasing the vehicle

        Returns:
            Sale: Created sale entity

        Raises:
            ValueError: If vehicle or user not found, or vehicle not available
        """
        vehicle = await self.vehicle_repository.get_by_id(vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        if vehicle.status != VehicleStatus.AVAILABLE:
            raise ValueError("Vehicle is not available for sale")

        user = await self.user_repository.get_by_cpf(buyer_cpf)
        if not user:
            raise ValueError("User with this CPF not found")

        payment_code = str(uuid.uuid4())

        payment_data = {
            "amount": vehicle.price,
            "customer_email": user.email,
            "customer_cpf": user.cpf,
            "description": f"Vehicle purchase: {vehicle.brand} {vehicle.model} {vehicle.year}"
        }

        payment_response = await self.payment_gateway.process_payment(payment_data)

        sale = Sale(
            id=None,
            vehicle_id=vehicle_id,
            user_id=user.id,  # Usa o user.id encontrado pelo CPF
            sale_date=datetime.now(),
            payment_code=payment_response.get("payment_code", payment_code),
            payment_status=PaymentStatus.PENDING
        )

        created_sale = await self.sale_repository.create(sale)

        await self.vehicle_repository.update_status(vehicle_id, VehicleStatus.RESERVED)

        await self.notification_gateway.send_sale_confirmation(
            user.email,
            {
                "sale_id": created_sale.id,
                "vehicle": f"{vehicle.brand} {vehicle.model} {vehicle.year}",
                "price": vehicle.price,
                "payment_code": created_sale.payment_code
            }
        )

        return created_sale


class GetSaleByIdUseCase:
    """
    Use case for retrieving a sale by ID.
    """

    def __init__(self, sale_repository: SaleRepositoryInterface):
        self.sale_repository = sale_repository

    async def execute(self, sale_id: int) -> Optional[Sale]:
        """
        Execute the get sale by ID use case.

        Args:
            sale_id: ID of the sale to retrieve

        Returns:
            Optional[Sale]: Sale entity if found, None otherwise
        """
        return await self.sale_repository.get_by_id(sale_id)


class ListSalesUseCase:
    """
    Use case for listing all sales with pagination.
    """

    def __init__(self, sale_repository: SaleRepositoryInterface):
        self.sale_repository = sale_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        """
        Execute the list sales use case.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Sale]: List of sale entities
        """
        return await self.sale_repository.get_all(skip, limit)


class DeleteSaleUseCase:
    """
    Use case for deleting a sale from the system.
    Only allows deletion of sales with pending payment status.
    """

    def __init__(self, sale_repository: SaleRepositoryInterface):
        self.sale_repository = sale_repository

    async def execute(self, sale_id: int) -> bool:
        """
        Execute the delete sale use case.

        Args:
            sale_id: ID of the sale to delete

        Returns:
            bool: True if deleted successfully, False otherwise

        Raises:
            ValueError: If sale cannot be deleted (payment completed)
        """
        sale = await self.sale_repository.get_by_id(sale_id)
        if not sale:
            return False

        if sale.payment_status.value == "completed":
            raise ValueError("Cannot delete a completed sale")

        return await self.sale_repository.delete(sale_id)


class UpdatePaymentStatusUseCase:
    """
    Use case for updating payment status via webhook.
    Updates vehicle status based on payment result.
    """

    def __init__(
            self,
            sale_repository: SaleRepositoryInterface,
            vehicle_repository: VehicleRepositoryInterface,
            user_repository: UserRepositoryInterface,
            notification_gateway: NotificationGatewayInterface
    ):
        self.sale_repository = sale_repository
        self.vehicle_repository = vehicle_repository
        self.user_repository = user_repository
        self.notification_gateway = notification_gateway

    async def execute_by_payment_code(self, payment_code: str, payment_status: PaymentStatus) -> Optional[Sale]:
        """
        Execute the update payment status use case by payment code.

        Args:
            payment_code: Unique payment code
            payment_status: New payment status

        Returns:
            Optional[Sale]: Updated sale entity if found, None otherwise
        """
        sale = await self.sale_repository.update_payment_status(payment_code, payment_status)
        if not sale:
            return None

        return await self._update_vehicle_and_notify(sale, payment_status)

    async def execute_by_sale_id(self, sale_id: int, payment_status: PaymentStatus) -> Optional[Sale]:
        """
        Execute the update payment status use case by sale ID.

        Args:
            sale_id: Unique sale identifier
            payment_status: New payment status

        Returns:
            Optional[Sale]: Updated sale entity if found, None otherwise
        """
        sale = await self.sale_repository.update_payment_status_by_id(sale_id, payment_status)
        if not sale:
            return None

        return await self._update_vehicle_and_notify(sale, payment_status)

    async def _update_vehicle_and_notify(self, sale: Sale, payment_status: PaymentStatus) -> Sale:
        """
        Update vehicle status and send notifications.

        Args:
            sale: Sale entity
            payment_status: Payment status

        Returns:
            Sale: Updated sale entity
        """
        if payment_status == PaymentStatus.COMPLETED:
            await self.vehicle_repository.update_status(sale.vehicle_id, VehicleStatus.SOLD)
        elif payment_status == PaymentStatus.CANCELLED:
            await self.vehicle_repository.update_status(sale.vehicle_id, VehicleStatus.AVAILABLE)

        user = await self.user_repository.get_by_id(sale.user_id)
        vehicle = await self.vehicle_repository.get_by_id(sale.vehicle_id)

        if user and vehicle:
            await self.notification_gateway.send_payment_notification(
                user.email,
                {
                    "sale_id": sale.id,
                    "vehicle": f"{vehicle.brand} {vehicle.model} {vehicle.year}",
                    "payment_status": payment_status.value,
                    "payment_code": sale.payment_code
                }
            )

        return sale