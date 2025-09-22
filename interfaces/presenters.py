from abc import ABC, abstractmethod
from typing import Dict, Any, List
from domain.entities import User, Vehicle, Sale


class UserPresenterInterface(ABC):
    """
    Abstract interface for user data presentation.
    Defines the contract for formatting user data for API responses.
    """

    @abstractmethod
    def present_user(self, user: User) -> Dict[str, Any]:
        """
        Present a single user entity for API response.

        Args:
            user: User entity to be presented

        Returns:
            Dict[str, Any]: Formatted user data for API response
        """
        pass

    @abstractmethod
    def present_users(self, users: List[User]) -> List[Dict[str, Any]]:
        """
        Present a list of user entities for API response.

        Args:
            users: List of user entities to be presented

        Returns:
            List[Dict[str, Any]]: List of formatted user data for API response
        """
        pass

    @abstractmethod
    def present_created_user(self, user: User) -> Dict[str, Any]:
        """
        Present a newly created user entity for API response.

        Args:
            user: Created user entity

        Returns:
            Dict[str, Any]: Formatted created user data for API response
        """
        pass


class VehiclePresenterInterface(ABC):
    """
    Abstract interface for vehicle data presentation.
    Defines the contract for formatting vehicle data for API responses.
    """

    @abstractmethod
    def present_vehicle(self, vehicle: Vehicle) -> Dict[str, Any]:
        """
        Present a single vehicle entity for API response.

        Args:
            vehicle: Vehicle entity to be presented

        Returns:
            Dict[str, Any]: Formatted vehicle data for API response
        """
        pass

    @abstractmethod
    def present_vehicles(self, vehicles: List[Vehicle]) -> List[Dict[str, Any]]:
        """
        Present a list of vehicle entities for API response.

        Args:
            vehicles: List of vehicle entities to be presented

        Returns:
            List[Dict[str, Any]]: List of formatted vehicle data for API response
        """
        pass

    @abstractmethod
    def present_all_vehicles(self, vehicles: List[Vehicle]) -> List[Dict[str, Any]]:
        """
        Present a list of all vehicle entities (any status) for API response.

        Args:
            vehicles: List of all vehicle entities to be presented

        Returns:
            List[Dict[str, Any]]: List of formatted vehicle data for API response
        """
        pass

    @abstractmethod
    def present_created_vehicle(self, vehicle: Vehicle) -> Dict[str, Any]:
        """
        Present a newly created vehicle entity for API response.

        Args:
            vehicle: Created vehicle entity

        Returns:
            Dict[str, Any]: Formatted created vehicle data for API response
        """
        pass


class SalePresenterInterface(ABC):
    """
    Abstract interface for sale data presentation.
    Defines the contract for formatting sale data for API responses.
    """

    @abstractmethod
    def present_sale(self, sale: Sale) -> Dict[str, Any]:
        """
        Present a single sale entity for API response.

        Args:
            sale: Sale entity to be presented

        Returns:
            Dict[str, Any]: Formatted sale data for API response
        """
        pass

    @abstractmethod
    def present_created_sale(self, sale: Sale) -> Dict[str, Any]:
        """
        Present a newly created sale entity for API response.

        Args:
            sale: Created sale entity

        Returns:
            Dict[str, Any]: Formatted created sale data for API response
        """
        pass

    @abstractmethod
    def present_payment_update(self, sale: Sale) -> Dict[str, Any]:
        """
        Present a sale with updated payment status for API response.

        Args:
            sale: Sale entity with updated payment status

        Returns:
            Dict[str, Any]: Formatted payment update data for API response
        """
        pass