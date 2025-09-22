from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.schemas import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from infra.database import get_db
from infra.repositories.user_repository import SQLAlchemyUserRepository
from infra.presenters.api_presenters import UserPresenter
from infra.controllers.user_controller import UserController
from use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    ListUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase
)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    """
    Dependency injection for UserController.
    Creates and configures all necessary dependencies for user operations.

    Args:
        db: Database session dependency

    Returns:
        UserController: Configured user controller instance
    """
    user_repository = SQLAlchemyUserRepository(db)
    user_presenter = UserPresenter()

    create_user_use_case = CreateUserUseCase(user_repository)
    get_user_by_id_use_case = GetUserByIdUseCase(user_repository)
    list_users_use_case = ListUsersUseCase(user_repository)
    update_user_use_case = UpdateUserUseCase(user_repository)
    delete_user_use_case = DeleteUserUseCase(user_repository)

    return UserController(
        create_user_use_case,
        get_user_by_id_use_case,
        list_users_use_case,
        update_user_use_case,
        delete_user_use_case,
        user_presenter
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreateSchema,
        controller: UserController = Depends(get_user_controller)
):
    """
    Create a new user.

    Args:
        user_data: User creation data
        controller: User controller dependency

    Returns:
        Dict: Created user data

    Raises:
        HTTPException: If user creation fails due to validation or constraint errors
    """
    try:
        result = await controller.create_user(user_data.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}")
async def get_user(
        user_id: int,
        controller: UserController = Depends(get_user_controller)
):
    """
    Get a user by ID.

    Args:
        user_id: ID of the user to retrieve
        controller: User controller dependency

    Returns:
        Dict: User data

    Raises:
        HTTPException: If user is not found
    """
    result = await controller.get_user(user_id)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result


@router.get("/")
async def list_users(
        skip: int = 0,
        limit: int = 100,
        controller: UserController = Depends(get_user_controller)
):
    """
    List all users with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: User controller dependency

    Returns:
        List[Dict]: List of users
    """
    return await controller.list_users(skip, limit)


@router.put("/{user_id}")
async def update_user(
        user_id: int,
        user_data: UserUpdateSchema,
        controller: UserController = Depends(get_user_controller)
):
    """
    Update an existing user.

    Args:
        user_id: ID of the user to update
        user_data: Updated user data
        controller: User controller dependency

    Returns:
        Dict: Updated user data

    Raises:
        HTTPException: If user is not found or validation fails
    """
    try:
        result = await controller.update_user(user_id, user_data.model_dump())
        if "error" in result:
            raise HTTPException(status_code=result["status_code"], detail=result["error"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}")
async def delete_user(
        user_id: int,
        controller: UserController = Depends(get_user_controller)
):
    """
    Delete a user.

    Args:
        user_id: ID of the user to delete
        controller: User controller dependency

    Returns:
        Dict: Deletion confirmation

    Raises:
        HTTPException: If user is not found
    """
    result = await controller.delete_user(user_id)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result