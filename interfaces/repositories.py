from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import User, Vehicle, Sale, VehicleStatus, PaymentStatus

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import User, Vehicle, Sale, VehicleStatus, PaymentStatus


class UserRepositoryInterface(ABC):
    """
    Abstract interface for user repository operations.
    Defines the contract for data persistence operations related to users.
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Create a new user in the repository.

        Args:
            user: User entity to be created

        Returns:
            User: Created user with assigned ID
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by its ID.

        Args:
            user_id: Unique identifier of the user

        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email address.

        Args:
            email: Email address of the user

        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_cpf(self, cpf: str) -> Optional[User]:
        """
        Retrieve a user by CPF document number.

        Args:
            cpf: CPF document number of the user

        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Retrieve all users with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[User]: List of user entities
        """
        pass

    @abstractmethod
    async def update(self, user_id: int, user: User) -> Optional[User]:
        """
        Update an existing user in the repository.

        Args:
            user_id: ID of the user to update
            user: User entity with updated information

        Returns:
            Optional[User]: Updated user entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """
        Delete a user from the repository.

        Args:
            user_id: ID of the user to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        pass


class VehicleRepositoryInterface(ABC):
    """
    Abstract interface for vehicle repository operations.
    Defines the contract for data persistence operations related to vehicles.
    """

    @abstractmethod
    async def create(self, vehicle: Vehicle) -> Vehicle:
        """
        Create a new vehicle in the repository.

        Args:
            vehicle: Vehicle entity to be created

        Returns:
            Vehicle: Created vehicle with assigned ID
        """
        pass

    @abstractmethod
    async def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """
        Retrieve a vehicle by its ID.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            Optional[Vehicle]: Vehicle entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all_available(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Retrieve all available vehicles ordered by price (ascending).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of available vehicle entities ordered by price
        """
        pass

    @abstractmethod
    async def get_all_sold(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Retrieve all sold vehicles ordered by price (ascending).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of sold vehicle entities ordered by price
        """
        pass

    @abstractmethod
    async def update(self, vehicle_id: int, vehicle: Vehicle) -> Optional[Vehicle]:
        """
        Update an existing vehicle in the repository.

        Args:
            vehicle_id: ID of the vehicle to update
            vehicle: Vehicle entity with updated information

        Returns:
            Optional[Vehicle]: Updated vehicle entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def update_status(self, vehicle_id: int, status: VehicleStatus) -> Optional[Vehicle]:
        """
        Update the status of a vehicle.

        Args:
            vehicle_id: ID of the vehicle to update
            status: New status for the vehicle

        Returns:
            Optional[Vehicle]: Updated vehicle entity if found, None otherwise
        """
        pass


class SaleRepositoryInterface(ABC):
    """
    Abstract interface for sale repository operations.
    Defines the contract for data persistence operations related to sales.
    """

    @abstractmethod
    async def create(self, sale: Sale) -> Sale:
        """
        Create a new sale in the repository.

        Args:
            sale: Sale entity to be created

        Returns:
            Sale: Created sale with assigned ID
        """
        pass

    @abstractmethod
    async def get_by_id(self, sale_id: int) -> Optional[Sale]:
        """
        Retrieve a sale by its ID.

        Args:
            sale_id: Unique identifier of the sale

        Returns:
            Optional[Sale]: Sale entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        """
        Retrieve all sales with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Sale]: List of sale entities
        """
        pass

    @abstractmethod
    async def get_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        """
        Retrieve a sale by payment code.

        Args:
            payment_code: Unique payment code for the sale

        Returns:
            Optional[Sale]: Sale entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def update_payment_status(self, payment_code: str, status: PaymentStatus) -> Optional[Sale]:
        """
        Update the payment status of a sale.

        Args:
            payment_code: Payment code of the sale to update
            status: New payment status

        Returns:
            Optional[Sale]: Updated sale entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def update_payment_status_by_id(self, sale_id: int, status: PaymentStatus) -> Optional[Sale]:
        """
        Update the payment status of a sale by sale ID.

        Args:
            sale_id: ID of the sale to update
            status: New payment status

        Returns:
            Optional[Sale]: Updated sale entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def delete(self, sale_id: int) -> bool:
        """
        Delete a sale from the repository.

        Args:
            sale_id: ID of the sale to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        pass


class VehicleRepositoryInterface(ABC):
    """
    Abstract interface for vehicle repository operations.
    Defines the contract for data persistence operations related to vehicles.
    """

    @abstractmethod
    async def create(self, vehicle: Vehicle) -> Vehicle:
        """
        Create a new vehicle in the repository.

        Args:
            vehicle: Vehicle entity to be created

        Returns:
            Vehicle: Created vehicle with assigned ID
        """
        pass

    @abstractmethod
    async def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """
        Retrieve a vehicle by its ID.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            Optional[Vehicle]: Vehicle entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all_available(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Retrieve all available vehicles ordered by price (ascending).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of available vehicle entities ordered by price
        """
        pass

    @abstractmethod
    async def get_all_sold(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Retrieve all sold vehicles ordered by price (ascending).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of sold vehicle entities ordered by price
        """
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Retrieve all vehicles ordered by price (ascending).

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Vehicle]: List of all vehicle entities ordered by price
        """
        pass

    @abstractmethod
    async def update(self, vehicle_id: int, vehicle: Vehicle) -> Optional[Vehicle]:
        """
        Update an existing vehicle in the repository.

        Args:
            vehicle_id: ID of the vehicle to update
            vehicle: Vehicle entity with updated information

        Returns:
            Optional[Vehicle]: Updated vehicle entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def update_status(self, vehicle_id: int, status: VehicleStatus) -> Optional[Vehicle]:
        """
        Update the status of a vehicle.

        Args:
            vehicle_id: ID of the vehicle to update
            status: New status for the vehicle

        Returns:
            Optional[Vehicle]: Updated vehicle entity if found, None otherwise
        """
        pass


class SaleRepositoryInterface(ABC):
    """
    Abstract interface for sale repository operations.
    Defines the contract for data persistence operations related to sales.
    """

    @abstractmethod
    async def create(self, sale: Sale) -> Sale:
        """
        Create a new sale in the repository.

        Args:
            sale: Sale entity to be created

        Returns:
            Sale: Created sale with assigned ID
        """
        pass

    @abstractmethod
    async def get_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        """
        Retrieve a sale by payment code.

        Args:
            payment_code: Unique payment code for the sale

        Returns:
            Optional[Sale]: Sale entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def update_payment_status(self, payment_code: str, status: PaymentStatus) -> Optional[Sale]:
        """
        Update the payment status of a sale.

        Args:
            payment_code: Payment code of the sale to update
            status: New payment status

        Returns:
            Optional[Sale]: Updated sale entity if found, None otherwise
        """
        pass