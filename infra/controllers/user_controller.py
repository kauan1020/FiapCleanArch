from typing import Dict, Any, List
from domain.entities import User
from use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    ListUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase
)
from interfaces.presenters import UserPresenterInterface


class UserController:
    """
    Controller for handling user-related HTTP requests.
    Coordinates between use cases and presenters following Clean Architecture principles.
    """

    def __init__(
            self,
            create_user_use_case: CreateUserUseCase,
            get_user_by_id_use_case: GetUserByIdUseCase,
            list_users_use_case: ListUsersUseCase,
            update_user_use_case: UpdateUserUseCase,
            delete_user_use_case: DeleteUserUseCase,
            user_presenter: UserPresenterInterface
    ):
        self.create_user_use_case = create_user_use_case
        self.get_user_by_id_use_case = get_user_by_id_use_case
        self.list_users_use_case = list_users_use_case
        self.update_user_use_case = update_user_use_case
        self.delete_user_use_case = delete_user_use_case
        self.user_presenter = user_presenter

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle user creation request.

        Args:
            user_data: Dictionary containing user information

        Returns:
            Dict[str, Any]: Response with created user data

        Raises:
            ValueError: If user data is invalid or constraints are violated
        """
        user = User(
            id=None,
            name=user_data["name"],
            email=user_data["email"],
            cpf=user_data["cpf"],
            phone=user_data["phone"]
        )

        created_user = await self.create_user_use_case.execute(user)
        return self.user_presenter.present_created_user(created_user)

    async def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Handle get user by ID request.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            Dict[str, Any]: Response with user data or None if not found
        """
        user = await self.get_user_by_id_use_case.execute(user_id)
        if not user:
            return {"error": "User not found", "status_code": 404}

        return self.user_presenter.present_user(user)

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Handle list users request with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Dict[str, Any]]: Response with list of users
        """
        users = await self.list_users_use_case.execute(skip, limit)
        return self.user_presenter.present_users(users)

    async def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle user update request.

        Args:
            user_id: ID of the user to update
            user_data: Dictionary containing updated user information

        Returns:
            Dict[str, Any]: Response with updated user data

        Raises:
            ValueError: If user data is invalid or constraints are violated
        """
        user = User(
            id=user_id,
            name=user_data["name"],
            email=user_data["email"],
            cpf=user_data["cpf"],
            phone=user_data["phone"]
        )

        updated_user = await self.update_user_use_case.execute(user_id, user)
        if not updated_user:
            return {"error": "User not found", "status_code": 404}

        return self.user_presenter.present_user(updated_user)

    async def delete_user(self, user_id: int) -> Dict[str, Any]:
        """
        Handle user deletion request.

        Args:
            user_id: ID of the user to delete

        Returns:
            Dict[str, Any]: Response with deletion status
        """
        deleted = await self.delete_user_use_case.execute(user_id)
        if not deleted:
            return {"error": "User not found", "status_code": 404}

        return {"message": "User deleted successfully", "status_code": 200}