from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities import Sale, PaymentStatus
from interfaces.repositories import SaleRepositoryInterface
from infra.models import SaleModel


class SQLAlchemySaleRepository(SaleRepositoryInterface):
    """
    SQLAlchemy implementation of SaleRepositoryInterface.
    Handles database operations for sale entities using SQLAlchemy ORM.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create(self, sale: Sale) -> Sale:
        """
        Create a new sale in the database.

        Args:
            sale: Sale entity to be created

        Returns:
            Sale: Created sale with assigned ID
        """
        db_sale = SaleModel(
            vehicle_id=sale.vehicle_id,
            user_id=sale.user_id,
            sale_date=sale.sale_date,
            payment_code=sale.payment_code,
            payment_status=sale.payment_status
        )
        self.db.add(db_sale)
        self.db.commit()
        self.db.refresh(db_sale)

        return self._model_to_entity(db_sale)

    async def get_by_id(self, sale_id: int) -> Optional[Sale]:
        """
        Retrieve a sale by its ID from the database.

        Args:
            sale_id: Unique identifier of the sale

        Returns:
            Optional[Sale]: Sale entity if found, None otherwise
        """
        db_sale = self.db.query(SaleModel).filter(SaleModel.id == sale_id).first()
        return self._model_to_entity(db_sale) if db_sale else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        """
        Retrieve all sales with pagination from the database.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Sale]: List of sale entities
        """
        db_sales = self.db.query(SaleModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(db_sale) for db_sale in db_sales]

    async def get_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        """
        Retrieve a sale by payment code from the database.

        Args:
            payment_code: Unique payment code for the sale

        Returns:
            Optional[Sale]: Sale entity if found, None otherwise
        """
        db_sale = self.db.query(SaleModel).filter(SaleModel.payment_code == payment_code).first()
        return self._model_to_entity(db_sale) if db_sale else None

    async def update_payment_status(self, payment_code: str, status: PaymentStatus) -> Optional[Sale]:
        """
        Update the payment status of a sale in the database.

        Args:
            payment_code: Unique payment code for the sale
            status: New payment status

        Returns:
            Optional[Sale]: Updated sale entity if found, None otherwise
        """
        db_sale = self.db.query(SaleModel).filter(SaleModel.payment_code == payment_code).first()
        if not db_sale:
            return None

        db_sale.payment_status = status
        self.db.commit()
        self.db.refresh(db_sale)

        return self._model_to_entity(db_sale)

    async def update_payment_status_by_id(self, sale_id: int, status: PaymentStatus) -> Optional[Sale]:
        """
        Update the payment status of a sale in the database using sale ID.

        Args:
            sale_id: Unique sale identifier
            status: New payment status

        Returns:
            Optional[Sale]: Updated sale entity if found, None otherwise
        """
        db_sale = self.db.query(SaleModel).filter(SaleModel.id == sale_id).first()
        if not db_sale:
            return None

        db_sale.payment_status = status
        self.db.commit()
        self.db.refresh(db_sale)

        return self._model_to_entity(db_sale)

    async def delete(self, sale_id: int) -> bool:
        """
        Delete a sale from the database.

        Args:
            sale_id: ID of the sale to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        db_sale = self.db.query(SaleModel).filter(SaleModel.id == sale_id).first()
        if not db_sale:
            return False

        self.db.delete(db_sale)
        self.db.commit()
        return True

    def _model_to_entity(self, model: SaleModel) -> Sale:
        """
        Convert SQLAlchemy model to domain entity.

        Args:
            model: SQLAlchemy sale model

        Returns:
            Sale: Domain sale entity
        """
        return Sale(
            id=model.id,
            vehicle_id=model.vehicle_id,
            user_id=model.user_id,
            sale_date=model.sale_date,
            payment_code=model.payment_code,
            payment_status=model.payment_status
        )