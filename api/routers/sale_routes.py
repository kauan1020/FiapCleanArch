from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.schemas import SaleCreateSchema, PaymentWebhookSchema, PaymentWebhookByIdSchema
from infra.database import get_db
from infra.repositories.sale_repository import SQLAlchemySaleRepository
from infra.repositories.vehicle_repository import SQLAlchemyVehicleRepository
from infra.repositories.user_repository import SQLAlchemyUserRepository
from infra.gateways.external_gateways import MockPaymentGateway, MockNotificationGateway
from infra.presenters.api_presenters import SalePresenter
from infra.controllers.sale_controller import SaleController
from use_cases.sale_use_cases import (
    CreateSaleUseCase,
    UpdatePaymentStatusUseCase,
    GetSaleByIdUseCase,
    ListSalesUseCase,
    DeleteSaleUseCase
)

router = APIRouter(prefix="/sales", tags=["sales"])


def get_sale_controller(db: Session = Depends(get_db)) -> SaleController:
    """
    Dependency injection for SaleController.
    Creates and configures all necessary dependencies for sale operations.

    Args:
        db: Database session dependency

    Returns:
        SaleController: Configured sale controller instance
    """
    sale_repository = SQLAlchemySaleRepository(db)
    vehicle_repository = SQLAlchemyVehicleRepository(db)
    user_repository = SQLAlchemyUserRepository(db)
    payment_gateway = MockPaymentGateway()
    notification_gateway = MockNotificationGateway()
    sale_presenter = SalePresenter()

    create_sale_use_case = CreateSaleUseCase(
        sale_repository,
        vehicle_repository,
        user_repository,
        payment_gateway,
        notification_gateway
    )

    get_sale_by_id_use_case = GetSaleByIdUseCase(sale_repository)
    list_sales_use_case = ListSalesUseCase(sale_repository)
    delete_sale_use_case = DeleteSaleUseCase(sale_repository)

    update_payment_status_use_case = UpdatePaymentStatusUseCase(
        sale_repository,
        vehicle_repository,
        user_repository,
        notification_gateway
    )

    return SaleController(
        create_sale_use_case,
        get_sale_by_id_use_case,
        list_sales_use_case,
        update_payment_status_use_case,
        delete_sale_use_case,
        sale_presenter
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_sale(
        sale_data: SaleCreateSchema,
        controller: SaleController = Depends(get_sale_controller)
):
    """
    Create a new vehicle sale.

    Args:
        sale_data: Sale creation data containing vehicle_id and user_id
        controller: Sale controller dependency

    Returns:
        Dict: Created sale data with payment information

    Raises:
        HTTPException: If sale creation fails due to validation or business rule violations
    """
    try:
        result = await controller.create_sale(sale_data.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{sale_id}")
async def get_sale(
        sale_id: int,
        controller: SaleController = Depends(get_sale_controller)
):
    """
    Get a sale by ID.

    Args:
        sale_id: ID of the sale to retrieve
        controller: Sale controller dependency

    Returns:
        Dict: Sale data

    Raises:
        HTTPException: If sale is not found
    """
    result = await controller.get_sale(sale_id)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result


@router.get("/")
async def list_sales(
        skip: int = 0,
        limit: int = 100,
        controller: SaleController = Depends(get_sale_controller)
):
    """
    List all sales with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: Sale controller dependency

    Returns:
        List[Dict]: List of sales
    """
    return await controller.list_sales(skip, limit)


@router.delete("/{sale_id}")
async def delete_sale(
        sale_id: int,
        controller: SaleController = Depends(get_sale_controller)
):
    """
    Delete a sale.
    Only allows deletion of sales with pending payment status.

    Args:
        sale_id: ID of the sale to delete
        controller: Sale controller dependency

    Returns:
        Dict: Deletion confirmation

    Raises:
        HTTPException: If sale is not found or cannot be deleted
    """
    result = await controller.delete_sale(sale_id)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result


@router.post("/webhook/payment", status_code=status.HTTP_200_OK)
async def payment_webhook_by_code(
        payment_data: PaymentWebhookSchema,
        controller: SaleController = Depends(get_sale_controller)
):
    """
    Webhook endpoint for payment status updates using payment code.
    External payment service calls this endpoint to update payment status.

    Args:
        payment_data: Payment webhook data containing payment_code and status
        controller: Sale controller dependency

    Returns:
        Dict: Updated payment status information

    Raises:
        HTTPException: If payment code is not found
    """
    try:
        result = await controller.update_payment_status_by_code(payment_data.model_dump())
        if "error" in result:
            raise HTTPException(status_code=result["status_code"], detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

