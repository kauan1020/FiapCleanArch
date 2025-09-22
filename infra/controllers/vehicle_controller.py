from typing import Dict, Any, List
from domain.entities import Vehicle
from use_cases.vehicle_use_cases import (
    CreateVehicleUseCase,
    GetVehicleByIdUseCase,
    ListAllVehiclesUseCase,
    ListAvailableVehiclesUseCase,
    ListSoldVehiclesUseCase,
    UpdateVehicleUseCase
)
from interfaces.presenters import VehiclePresenterInterface


class VehicleController:
    """
    Controller for handling vehicle-related HTTP requests.
    Coordinates between use cases and presenters following Clean Architecture principles.
    """

    def __init__(
            self,
            create_vehicle_use_case: CreateVehicleUseCase,
            get_vehicle_by_id_use_case: GetVehicleByIdUseCase,
            list_all_vehicles_use_case: ListAllVehiclesUseCase,
            list_available_vehicles_use_case: ListAvailableVehiclesUseCase,
            list_sold_vehicles_use_case: ListSoldVehiclesUseCase,
            update_vehicle_use_case: UpdateVehicleUseCase,
            vehicle_presenter: VehiclePresenterInterface
    ):
        self.create_vehicle_use_case = create_vehicle_use_case
        self.get_vehicle_by_id_use_case = get_vehicle_by_id_use_case
        self.list_all_vehicles_use_case = list_all_vehicles_use_case
        self.list_available_vehicles_use_case = list_available_vehicles_use_case
        self.list_sold_vehicles_use_case = list_sold_vehicles_use_case
        self.update_vehicle_use_case = update_vehicle_use_case
        self.vehicle_presenter = vehicle_presenter

    async def create_vehicle(self, vehicle_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle vehicle creation request.

        Args:
            vehicle_data: Dictionary containing vehicle information

        Returns:
            Dict[str, Any]: Response with created vehicle data

        Raises:
            ValueError: If vehicle data is invalid
        """
        vehicle = Vehicle(
            id=None,
            brand=vehicle_data["brand"],
            model=vehicle_data["model"],
            year=vehicle_data["year"],
            color=vehicle_data["color"],
            price=vehicle_data["price"]
        )

        created_vehicle = await self.create_vehicle_use_case.execute(vehicle)
        return self.vehicle_presenter.present_created_vehicle(created_vehicle)

    async def get_vehicle(self, vehicle_id: int) -> Dict[str, Any]:
        """
        Handle get vehicle by ID request.

        Args:
            vehicle_id: ID of the vehicle to retrieve

        Returns:
            Dict[str, Any]: Response with vehicle data or error if not found
        """
        vehicle = await self.get_vehicle_by_id_use_case.execute(vehicle_id)
        if not vehicle:
            return {"error": "Vehicle not found", "status_code": 404}

        return self.vehicle_presenter.present_vehicle(vehicle)

    async def list_all_vehicles(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Handle list all vehicles request with pagination.
        Returns all vehicles (available + sold) ordered by price (ascending).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Dict[str, Any]]: Response with list of all vehicles
        """
        vehicles = await self.list_all_vehicles_use_case.execute(skip, limit)
        return self.vehicle_presenter.present_all_vehicles(vehicles)

    async def list_available_vehicles(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Handle list available vehicles request with pagination.
        Returns vehicles ordered by price (ascending).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Dict[str, Any]]: Response with list of available vehicles
        """
        vehicles = await self.list_available_vehicles_use_case.execute(skip, limit)
        return self.vehicle_presenter.present_vehicles(vehicles)

    async def list_sold_vehicles(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Handle list sold vehicles request with pagination.
        Returns vehicles ordered by price (ascending).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Dict[str, Any]]: Response with list of sold vehicles
        """
        vehicles = await self.list_sold_vehicles_use_case.execute(skip, limit)
        return self.vehicle_presenter.present_vehicles(vehicles)

    async def update_vehicle(self, vehicle_id: int, vehicle_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle vehicle update request.

        Args:
            vehicle_id: ID of the vehicle to update
            vehicle_data: Dictionary containing updated vehicle information

        Returns:
            Dict[str, Any]: Response with updated vehicle data

        Raises:
            ValueError: If vehicle data is invalid or vehicle is sold
        """
        vehicle = Vehicle(
            id=vehicle_id,
            brand=vehicle_data["brand"],
            model=vehicle_data["model"],
            year=vehicle_data["year"],
            color=vehicle_data["color"],
            price=vehicle_data["price"]
        )

        updated_vehicle = await self.update_vehicle_use_case.execute(vehicle_id, vehicle)
        if not updated_vehicle:
            return {"error": "Vehicle not found", "status_code": 404}

        return self.vehicle_presenter.present_vehicle(updated_vehicle)