from typing import Dict, Any, List
from domain.entities import User, Vehicle, Sale
from interfaces.presenters import UserPresenterInterface, VehiclePresenterInterface, SalePresenterInterface


class UserPresenter(UserPresenterInterface):
    """
    Implementation of UserPresenterInterface for API responses.
    Formats user data for REST API consumption.
    """

    def present_user(self, user: User) -> Dict[str, Any]:
        """
        Present a single user entity for API response.

        Args:
            user: User entity to be presented

        Returns:
            Dict[str, Any]: Formatted user data for API response
        """
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "cpf": user.cpf,
            "phone": user.phone,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }

    def present_users(self, users: List[User]) -> List[Dict[str, Any]]:
        """
        Present a list of user entities for API response.

        Args:
            users: List of user entities to be presented

        Returns:
            List[Dict[str, Any]]: List of formatted user data for API response
        """
        return [self.present_user(user) for user in users]

    def present_created_user(self, user: User) -> Dict[str, Any]:
        """
        Present a newly created user entity for API response.

        Args:
            user: Created user entity

        Returns:
            Dict[str, Any]: Formatted created user data for API response
        """
        response = self.present_user(user)
        response["message"] = "User created successfully"
        return response


class VehiclePresenter(VehiclePresenterInterface):
    """
    Implementation of VehiclePresenterInterface for API responses.
    Formats vehicle data for REST API consumption.
    """

    def present_vehicle(self, vehicle: Vehicle) -> Dict[str, Any]:
        """
        Present a single vehicle entity for API response.

        Args:
            vehicle: Vehicle entity to be presented

        Returns:
            Dict[str, Any]: Formatted vehicle data for API response
        """
        return {
            "id": vehicle.id,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "color": vehicle.color,
            "price": vehicle.price,
            "status": vehicle.status.value,
            "created_at": vehicle.created_at.isoformat() if vehicle.created_at else None,
            "updated_at": vehicle.updated_at.isoformat() if vehicle.updated_at else None
        }

    def present_vehicles(self, vehicles: List[Vehicle]) -> List[Dict[str, Any]]:
        """
        Present a list of vehicle entities for API response.

        Args:
            vehicles: List of vehicle entities to be presented

        Returns:
            List[Dict[str, Any]]: List of formatted vehicle data for API response
        """
        return [self.present_vehicle(vehicle) for vehicle in vehicles]

    def present_all_vehicles(self, vehicles: List[Vehicle]) -> List[Dict[str, Any]]:
        """
        Present a list of all vehicle entities (any status) for API response.

        Args:
            vehicles: List of all vehicle entities to be presented

        Returns:
            List[Dict[str, Any]]: List of formatted vehicle data for API response
        """
        return [self.present_vehicle(vehicle) for vehicle in vehicles]

    def present_created_vehicle(self, vehicle: Vehicle) -> Dict[str, Any]:
        """
        Present a newly created vehicle entity for API response.

        Args:
            vehicle: Created vehicle entity

        Returns:
            Dict[str, Any]: Formatted created vehicle data for API response
        """
        response = self.present_vehicle(vehicle)
        response["message"] = "Vehicle created successfully"
        return response


class SalePresenter(SalePresenterInterface):
    """
    Implementation of SalePresenterInterface for API responses.
    Formats sale data for REST API consumption.
    """

    def present_sale(self, sale: Sale) -> Dict[str, Any]:
        """
        Present a single sale entity for API response.

        Args:
            sale: Sale entity to be presented

        Returns:
            Dict[str, Any]: Formatted sale data for API response
        """
        return {
            "id": sale.id,
            "vehicle_id": sale.vehicle_id,
            "user_id": sale.user_id,
            "sale_date": sale.sale_date.isoformat(),
            "payment_code": sale.payment_code,
            "payment_status": sale.payment_status.value,
            "created_at": sale.created_at.isoformat() if sale.created_at else None,
            "updated_at": sale.updated_at.isoformat() if sale.updated_at else None
        }

    def present_created_sale(self, sale: Sale) -> Dict[str, Any]:
        """
        Present a newly created sale entity for API response.

        Args:
            sale: Created sale entity

        Returns:
            Dict[str, Any]: Formatted created sale data for API response
        """
        response = self.present_sale(sale)
        response["message"] = "Sale created successfully"
        return response

    def present_payment_update(self, sale: Sale) -> Dict[str, Any]:
        """
        Present a sale with updated payment status for API response.

        Args:
            sale: Sale entity with updated payment status

        Returns:
            Dict[str, Any]: Formatted payment update data for API response
        """
        response = self.present_sale(sale)
        response["message"] = "Payment status updated successfully"
        return response