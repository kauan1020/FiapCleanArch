from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities import Vehicle, VehicleStatus
from interfaces.repositories import VehicleRepositoryInterface
from infra.models import VehicleModel


class SQLAlchemyVehicleRepository(VehicleRepositoryInterface):
    """
    SQLAlchemy implementation of VehicleRepositoryInterface.
    Handles database operations for vehicle entities using SQLAlchemy ORM.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create(self, vehicle: Vehicle) -> Vehicle:
        """
        Create a new vehicle in the database.

        Args:
            vehicle: Vehicle entity to be created

        Returns:
            Vehicle: Created vehicle with assigned ID
        """
        db_vehicle = VehicleModel(
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            color=vehicle.color,
            price=vehicle.price,
            status=vehicle.status
        )
        self.db.add(db_vehicle)
        self.db.commit()
        self.db.refresh(db_vehicle)

        return self._model_to_entity(db_vehicle)

    async def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """
        Retrieve a vehicle by its ID from the database.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            Optional[Vehicle]: Vehicle entity if found, None otherwise
        """
        db_vehicle = self.db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        return self._model_to_entity(db_vehicle) if db_vehicle else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Retrieve all vehicles ordered by price (ascending) from the database.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of all vehicle entities ordered by price
        """
        db_vehicles = (
            self.db.query(VehicleModel)
            .order_by(VehicleModel.price.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._model_to_entity(db_vehicle) for db_vehicle in db_vehicles]

    async def get_all_available(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Retrieve all available vehicles ordered by price (ascending) from the database.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of available vehicle entities ordered by price
        """
        db_vehicles = (
            self.db.query(VehicleModel)
            .filter(VehicleModel.status == VehicleStatus.AVAILABLE)
            .order_by(VehicleModel.price.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._model_to_entity(db_vehicle) for db_vehicle in db_vehicles]

    async def get_all_sold(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Retrieve all sold vehicles ordered by price (ascending) from the database.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of sold vehicle entities ordered by price
        """
        db_vehicles = (
            self.db.query(VehicleModel)
            .filter(VehicleModel.status == VehicleStatus.SOLD)
            .order_by(VehicleModel.price.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._model_to_entity(db_vehicle) for db_vehicle in db_vehicles]

    async def update(self, vehicle_id: int, vehicle: Vehicle) -> Optional[Vehicle]:
        """
        Update an existing vehicle in the database.

        Args:
            vehicle_id: ID of the vehicle to update
            vehicle: Vehicle entity with updated information

        Returns:
            Optional[Vehicle]: Updated vehicle entity if found, None otherwise
        """
        db_vehicle = self.db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        if not db_vehicle:
            return None

        db_vehicle.brand = vehicle.brand
        db_vehicle.model = vehicle.model
        db_vehicle.year = vehicle.year
        db_vehicle.color = vehicle.color
        db_vehicle.price = vehicle.price

        self.db.commit()
        self.db.refresh(db_vehicle)

        return self._model_to_entity(db_vehicle)

    async def update_status(self, vehicle_id: int, status: VehicleStatus) -> Optional[Vehicle]:
        """
        Update the status of a vehicle in the database.

        Args:
            vehicle_id: ID of the vehicle to update
            status: New status for the vehicle

        Returns:
            Optional[Vehicle]: Updated vehicle entity if found, None otherwise
        """
        db_vehicle = self.db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        if not db_vehicle:
            return None

        db_vehicle.status = status
        self.db.commit()
        self.db.refresh(db_vehicle)

        return self._model_to_entity(db_vehicle)

    def _model_to_entity(self, model: VehicleModel) -> Vehicle:
        """
        Convert SQLAlchemy model to domain entity.

        Args:
            model: SQLAlchemy vehicle model

        Returns:
            Vehicle: Domain vehicle entity
        """
        return Vehicle(
            id=model.id,
            brand=model.brand,
            model=model.model,
            year=model.year,
            color=model.color,
            price=model.price,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )