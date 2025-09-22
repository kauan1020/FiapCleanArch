from typing import List, Optional
from domain.entities import User
from interfaces.repositories import UserRepositoryInterface


class CreateUserUseCase:
    """
    Use case for creating a new user in the system.
    Validates business rules before creating the user.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, user: User) -> User:
        """
        Execute the create user use case.

        Args:
            user: User entity to be created

        Returns:
            User: Created user entity

        Raises:
            ValueError: If email or CPF already exists
        """
        existing_email = await self.user_repository.get_by_email(user.email)
        if existing_email:
            raise ValueError("Email already exists")

        existing_cpf = await self.user_repository.get_by_cpf(user.cpf)
        if existing_cpf:
            raise ValueError("CPF already exists")

        return await self.user_repository.create(user)


class GetUserByIdUseCase:
    """
    Use case for retrieving a user by ID.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> Optional[User]:
        """
        Execute the get user by ID use case.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        return await self.user_repository.get_by_id(user_id)


class ListUsersUseCase:
    """
    Use case for listing all users with pagination.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Execute the list users use case.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[User]: List of user entities
        """
        return await self.user_repository.get_all(skip, limit)


class UpdateUserUseCase:
    """
    Use case for updating an existing user.
    Validates business rules before updating.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, user_id: int, user: User) -> Optional[User]:
        """
        Execute the update user use case.

        Args:
            user_id: ID of the user to update
            user: User entity with updated information

        Returns:
            Optional[User]: Updated user entity if found, None otherwise

        Raises:
            ValueError: If email or CPF already exists for another user
        """
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            return None

        if user.email != existing_user.email:
            existing_email = await self.user_repository.get_by_email(user.email)
            if existing_email and existing_email.id != user_id:
                raise ValueError("Email already exists")

        if user.cpf != existing_user.cpf:
            existing_cpf = await self.user_repository.get_by_cpf(user.cpf)
            if existing_cpf and existing_cpf.id != user_id:
                raise ValueError("CPF already exists")

        return await self.user_repository.update(user_id, user)


class DeleteUserUseCase:
    """
    Use case for deleting a user from the system.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> bool:
        """
        Execute the delete user use case.

        Args:
            user_id: ID of the user to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        return await self.user_repository.delete(user_id)