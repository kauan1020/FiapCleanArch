from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.schemas import VehicleCreateSchema, VehicleUpdateSchema
from infra.database import get_db
from infra.repositories.vehicle_repository import SQLAlchemyVehicleRepository
from infra.presenters.api_presenters import VehiclePresenter
from infra.controllers.vehicle_controller import VehicleController
from use_cases.vehicle_use_cases import (
    CreateVehicleUseCase,
    GetVehicleByIdUseCase,
    ListAllVehiclesUseCase,
    ListAvailableVehiclesUseCase,
    ListSoldVehiclesUseCase,
    UpdateVehicleUseCase
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def get_vehicle_controller(db: Session = Depends(get_db)) -> VehicleController:
    """
    Dependency injection for VehicleController.
    Creates and configures all necessary dependencies for vehicle operations.

    Args:
        db: Database session dependency

    Returns:
        VehicleController: Configured vehicle controller instance
    """
    vehicle_repository = SQLAlchemyVehicleRepository(db)
    vehicle_presenter = VehiclePresenter()

    create_vehicle_use_case = CreateVehicleUseCase(vehicle_repository)
    get_vehicle_by_id_use_case = GetVehicleByIdUseCase(vehicle_repository)
    list_all_vehicles_use_case = ListAllVehiclesUseCase(vehicle_repository)
    list_available_vehicles_use_case = ListAvailableVehiclesUseCase(vehicle_repository)
    list_sold_vehicles_use_case = ListSoldVehiclesUseCase(vehicle_repository)
    update_vehicle_use_case = UpdateVehicleUseCase(vehicle_repository)

    return VehicleController(
        create_vehicle_use_case,
        get_vehicle_by_id_use_case,
        list_all_vehicles_use_case,
        list_available_vehicles_use_case,
        list_sold_vehicles_use_case,
        update_vehicle_use_case,
        vehicle_presenter
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vehicle(
        vehicle_data: VehicleCreateSchema,
        controller: VehicleController = Depends(get_vehicle_controller)
):
    """
    Create a new vehicle.

    Args:
        vehicle_data: Vehicle creation data
        controller: Vehicle controller dependency

    Returns:
        Dict: Created vehicle data

    Raises:
        HTTPException: If vehicle creation fails due to validation errors
    """
    try:
        result = await controller.create_vehicle(vehicle_data.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{vehicle_id}")
async def get_vehicle(
        vehicle_id: int,
        controller: VehicleController = Depends(get_vehicle_controller)
):
    """
    Get a vehicle by ID.

    Args:
        vehicle_id: ID of the vehicle to retrieve
        controller: Vehicle controller dependency

    Returns:
        Dict: Vehicle data

    Raises:
        HTTPException: If vehicle is not found
    """
    result = await controller.get_vehicle(vehicle_id)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

@router.get("/available/")
async def list_available_vehicles(
        skip: int = 0,
        limit: int = 100,
        controller: VehicleController = Depends(get_vehicle_controller)
):
    """
    List all available vehicles ordered by price (ascending).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: Vehicle controller dependency

    Returns:
        List[Dict]: List of available vehicles
    """
    return await controller.list_available_vehicles(skip, limit)


@router.get("/sold/")
async def list_sold_vehicles(
        skip: int = 0,
        limit: int = 100,
        controller: VehicleController = Depends(get_vehicle_controller)
):
    """
    List all sold vehicles ordered by price (ascending).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: Vehicle controller dependency

    Returns:
        List[Dict]: List of sold vehicles
    """
    return await controller.list_sold_vehicles(skip, limit)


@router.get("/all/")
async def list_all_vehicles(
        skip: int = 0,
        limit: int = 100,
        controller: VehicleController = Depends(get_vehicle_controller)
):
    """
    List all vehicles (available + sold + reserved) ordered by price (ascending).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: Vehicle controller dependency

    Returns:
        List[Dict]: List of all vehicles
    """
    return await controller.list_all_vehicles(skip, limit)


@router.put("/{vehicle_id}")
async def update_vehicle(
        vehicle_id: int,
        vehicle_data: VehicleUpdateSchema,
        controller: VehicleController = Depends(get_vehicle_controller)
):
    """
    Update an existing vehicle.

    Args:
        vehicle_id: ID of the vehicle to update
        vehicle_data: Updated vehicle data
        controller: Vehicle controller dependency

    Returns:
        Dict: Updated vehicle data

    Raises:
        HTTPException: If vehicle is not found or validation fails
    """
    try:
        result = await controller.update_vehicle(vehicle_id, vehicle_data.model_dump())
        if "error" in result:
            raise HTTPException(status_code=result["status_code"], detail=result["error"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))