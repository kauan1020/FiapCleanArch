from typing import List, Optional
from domain.entities import Vehicle, VehicleStatus
from interfaces.repositories import VehicleRepositoryInterface


class CreateVehicleUseCase:
    """
    Use case for creating a new vehicle in the system.
    Validates business rules before creating the vehicle.
    """

    def __init__(self, vehicle_repository: VehicleRepositoryInterface):
        self.vehicle_repository = vehicle_repository

    async def execute(self, vehicle: Vehicle) -> Vehicle:
        """
        Execute the create vehicle use case.

        Args:
            vehicle: Vehicle entity to be created

        Returns:
            Vehicle: Created vehicle entity

        Raises:
            ValueError: If vehicle data is invalid
        """
        if vehicle.price <= 0:
            raise ValueError("Vehicle price must be greater than 0")

        if vehicle.year < 1900 or vehicle.year > 2030:
            raise ValueError("Invalid vehicle year")

        return await self.vehicle_repository.create(vehicle)


class GetVehicleByIdUseCase:
    """
    Use case for retrieving a vehicle by ID.
    """

    def __init__(self, vehicle_repository: VehicleRepositoryInterface):
        self.vehicle_repository = vehicle_repository

    async def execute(self, vehicle_id: int) -> Optional[Vehicle]:
        """
        Execute the get vehicle by ID use case.

        Args:
            vehicle_id: ID of the vehicle to retrieve

        Returns:
            Optional[Vehicle]: Vehicle entity if found, None otherwise
        """
        return await self.vehicle_repository.get_by_id(vehicle_id)


class ListAvailableVehiclesUseCase:
    """
    Use case for listing all available vehicles ordered by price.
    """

    def __init__(self, vehicle_repository: VehicleRepositoryInterface):
        self.vehicle_repository = vehicle_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Execute the list available vehicles use case.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of available vehicle entities ordered by price
        """
        return await self.vehicle_repository.get_all_available(skip, limit)


class ListAllVehiclesUseCase:
    """
    Use case for listing all vehicles (available + sold) ordered by price.
    """

    def __init__(self, vehicle_repository: VehicleRepositoryInterface):
        self.vehicle_repository = vehicle_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Execute the list all vehicles use case.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of all vehicle entities ordered by price
        """
        return await self.vehicle_repository.get_all(skip, limit)


class ListSoldVehiclesUseCase:
    """
    Use case for listing all sold vehicles ordered by price.
    """

    def __init__(self, vehicle_repository: VehicleRepositoryInterface):
        self.vehicle_repository = vehicle_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Execute the list sold vehicles use case.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of sold vehicle entities ordered by price
        """
        return await self.vehicle_repository.get_all_sold(skip, limit)


class UpdateVehicleUseCase:
    """
    Use case for updating an existing vehicle.
    Validates business rules before updating.
    """

    def __init__(self, vehicle_repository: VehicleRepositoryInterface):
        self.vehicle_repository = vehicle_repository

    async def execute(self, vehicle_id: int, vehicle: Vehicle) -> Optional[Vehicle]:
        """
        Execute the update vehicle use case.

        Args:
            vehicle_id: ID of the vehicle to update
            vehicle: Vehicle entity with updated information

        Returns:
            Optional[Vehicle]: Updated vehicle entity if found, None otherwise

        Raises:
            ValueError: If vehicle data is invalid or vehicle is already sold
        """
        existing_vehicle = await self.vehicle_repository.get_by_id(vehicle_id)
        if not existing_vehicle:
            return None

        if existing_vehicle.status == VehicleStatus.SOLD:
            raise ValueError("Cannot update a sold vehicle")

        if vehicle.price <= 0:
            raise ValueError("Vehicle price must be greater than 0")

        if vehicle.year < 1900 or vehicle.year > 2030:
            raise ValueError("Invalid vehicle year")

        return await self.vehicle_repository.update(vehicle_id, vehicle)