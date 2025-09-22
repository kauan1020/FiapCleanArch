from abc import ABC, abstractmethod
from typing import Dict, Any


class PaymentGatewayInterface(ABC):
    """
    Abstract interface for payment gateway operations.
    Defines the contract for external payment processing services.
    """

    @abstractmethod
    async def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a payment through external payment service.

        Args:
            payment_data: Dictionary containing payment information including
                         amount, customer data, and payment method

        Returns:
            Dict[str, Any]: Response from payment service containing
                           payment code and initial status
        """
        pass

    @abstractmethod
    async def get_payment_status(self, payment_code: str) -> str:
        """
        Retrieve the current status of a payment from external service.

        Args:
            payment_code: Unique payment code from payment processor

        Returns:
            str: Current payment status (pending, completed, cancelled)
        """
        pass


class NotificationGatewayInterface(ABC):
    """
    Abstract interface for notification gateway operations.
    Defines the contract for external notification services.
    """

    @abstractmethod
    async def send_sale_confirmation(self, user_email: str, sale_data: Dict[str, Any]) -> bool:
        """
        Send sale confirmation notification to user.

        Args:
            user_email: Email address of the user
            sale_data: Dictionary containing sale information

        Returns:
            bool: True if notification sent successfully, False otherwise
        """
        pass

    @abstractmethod
    async def send_payment_notification(self, user_email: str, payment_data: Dict[str, Any]) -> bool:
        """
        Send payment status notification to user.

        Args:
            user_email: Email address of the user
            payment_data: Dictionary containing payment information

        Returns:
            bool: True if notification sent successfully, False otherwise
        """
        pass