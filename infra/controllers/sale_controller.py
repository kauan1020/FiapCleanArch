from typing import Dict, Any, List
from domain.entities import PaymentStatus
from use_cases.sale_use_cases import CreateSaleUseCase, UpdatePaymentStatusUseCase, GetSaleByIdUseCase, ListSalesUseCase, DeleteSaleUseCase
from interfaces.presenters import SalePresenterInterface


class SaleController:
    """
    Controller for handling sale-related HTTP requests.
    Coordinates between use cases and presenters following Clean Architecture principles.
    """

    def __init__(
            self,
            create_sale_use_case: CreateSaleUseCase,
            get_sale_by_id_use_case: GetSaleByIdUseCase,
            list_sales_use_case: ListSalesUseCase,
            update_payment_status_use_case: UpdatePaymentStatusUseCase,
            delete_sale_use_case: DeleteSaleUseCase,
            sale_presenter: SalePresenterInterface
    ):
        self.create_sale_use_case = create_sale_use_case
        self.get_sale_by_id_use_case = get_sale_by_id_use_case
        self.list_sales_use_case = list_sales_use_case
        self.update_payment_status_use_case = update_payment_status_use_case
        self.delete_sale_use_case = delete_sale_use_case
        self.sale_presenter = sale_presenter

    async def create_sale(self, sale_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle vehicle sale creation request.

        Args:
            sale_data: Dictionary containing sale information with vehicle_id and buyer_cpf

        Returns:
            Dict[str, Any]: Response with created sale data

        Raises:
            ValueError: If sale data is invalid or constraints are violated
        """
        vehicle_id = sale_data["vehicle_id"]
        buyer_cpf = sale_data["buyer_cpf"]

        created_sale = await self.create_sale_use_case.execute(vehicle_id, buyer_cpf)
        return self.sale_presenter.present_created_sale(created_sale)

    async def get_sale(self, sale_id: int) -> Dict[str, Any]:
        """
        Handle get sale by ID request.

        Args:
            sale_id: ID of the sale to retrieve

        Returns:
            Dict[str, Any]: Response with sale data or error if not found
        """
        sale = await self.get_sale_by_id_use_case.execute(sale_id)
        if not sale:
            return {"error": "Sale not found", "status_code": 404}

        return self.sale_presenter.present_sale(sale)

    async def list_sales(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Handle list sales request with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Dict[str, Any]]: Response with list of sales
        """
        sales = await self.list_sales_use_case.execute(skip, limit)
        return [self.sale_presenter.present_sale(sale) for sale in sales]

    async def update_payment_status_by_code(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle payment status update webhook request by payment code.

        Args:
            payment_data: Dictionary containing payment_code and status

        Returns:
            Dict[str, Any]: Response with updated payment status
        """
        payment_code = payment_data["payment_code"]
        payment_status = self._parse_payment_status(payment_data["status"])

        updated_sale = await self.update_payment_status_use_case.execute_by_payment_code(
            payment_code, payment_status
        )

        if not updated_sale:
            return {"error": "Sale not found", "status_code": 404}

        return self.sale_presenter.present_payment_update(updated_sale)

    async def update_payment_status_by_id(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle payment status update webhook request by sale ID.

        Args:
            payment_data: Dictionary containing sale_id and status

        Returns:
            Dict[str, Any]: Response with updated payment status
        """
        sale_id = payment_data["sale_id"]
        payment_status = self._parse_payment_status(payment_data["status"])

        updated_sale = await self.update_payment_status_use_case.execute_by_sale_id(
            sale_id, payment_status
        )

        if not updated_sale:
            return {"error": "Sale not found", "status_code": 404}

        return self.sale_presenter.present_payment_update(updated_sale)

    async def delete_sale(self, sale_id: int) -> Dict[str, Any]:
        """
        Handle sale deletion request.

        Args:
            sale_id: ID of the sale to delete

        Returns:
            Dict[str, Any]: Response with deletion status
        """
        try:
            deleted = await self.delete_sale_use_case.execute(sale_id)
            if not deleted:
                return {"error": "Sale not found", "status_code": 404}

            return {"message": "Sale deleted successfully", "status_code": 200}
        except ValueError as e:
            return {"error": str(e), "status_code": 400}

    def _parse_payment_status(self, status_str: str) -> PaymentStatus:
        """
        Parse payment status string to enum.

        Args:
            status_str: Status string to parse

        Returns:
            PaymentStatus: Parsed payment status enum
        """
        status_lower = status_str.lower()
        if status_lower == "completed":
            return PaymentStatus.COMPLETED
        elif status_lower == "cancelled":
            return PaymentStatus.CANCELLED
        else:
            return PaymentStatus.PENDING