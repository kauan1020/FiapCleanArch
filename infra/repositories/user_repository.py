from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities import User
from interfaces.repositories import UserRepositoryInterface
from infra.models import UserModel


class SQLAlchemyUserRepository(UserRepositoryInterface):
    """
    SQLAlchemy implementation of UserRepositoryInterface.
    Handles database operations for user entities using SQLAlchemy ORM.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create(self, user: User) -> User:
        """
        Create a new user in the database.

        Args:
            user: User entity to be created

        Returns:
            User: Created user with assigned ID
        """
        db_user = UserModel(
            name=user.name,
            email=user.email,
            cpf=user.cpf,
            phone=user.phone
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return self._model_to_entity(db_user)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by its ID from the database.

        Args:
            user_id: Unique identifier of the user

        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._model_to_entity(db_user) if db_user else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email address from the database.

        Args:
            email: Email address of the user

        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._model_to_entity(db_user) if db_user else None

    async def get_by_cpf(self, cpf: str) -> Optional[User]:
        """
        Retrieve a user by CPF document number from the database.

        Args:
            cpf: CPF document number of the user

        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        db_user = self.db.query(UserModel).filter(UserModel.cpf == cpf).first()
        return self._model_to_entity(db_user) if db_user else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Retrieve all users with pagination from the database.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[User]: List of user entities
        """
        db_users = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(db_user) for db_user in db_users]

    async def update(self, user_id: int, user: User) -> Optional[User]:
        """
        Update an existing user in the database.

        Args:
            user_id: ID of the user to update
            user: User entity with updated information

        Returns:
            Optional[User]: Updated user entity if found, None otherwise
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None

        db_user.name = user.name
        db_user.email = user.email
        db_user.cpf = user.cpf
        db_user.phone = user.phone

        self.db.commit()
        self.db.refresh(db_user)

        return self._model_to_entity(db_user)

    async def delete(self, user_id: int) -> bool:
        """
        Delete a user from the database.

        Args:
            user_id: ID of the user to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True

    def _model_to_entity(self, model: UserModel) -> User:
        """
        Convert SQLAlchemy model to domain entity.

        Args:
            model: SQLAlchemy user model

        Returns:
            User: Domain user entity
        """
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            cpf=model.cpf,
            phone=model.phone,
            created_at=model.created_at,
            updated_at=model.updated_at
        )