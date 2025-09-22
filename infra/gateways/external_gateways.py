import uuid
from typing import Dict, Any
from interfaces.gateways import PaymentGatewayInterface, NotificationGatewayInterface


class MockPaymentGateway(PaymentGatewayInterface):
    """
    Mock implementation of PaymentGatewayInterface for testing and development.
    Simulates external payment service behavior.
    """

    async def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a payment through mock external payment service.

        Args:
            payment_data: Dictionary containing payment information including
                         amount, customer data, and payment method

        Returns:
            Dict[str, Any]: Response from mock payment service containing
                           payment code and initial status
        """
        payment_code = str(uuid.uuid4())

        return {
            "payment_code": payment_code,
            "status": "pending",
            "amount": payment_data.get("amount"),
            "message": "Payment processing initiated"
        }

    async def get_payment_status(self, payment_code: str) -> str:
        """
        Retrieve the current status of a payment from mock external service.

        Args:
            payment_code: Unique payment code from payment processor

        Returns:
            str: Current payment status (pending, completed, cancelled)
        """
        return "pending"


class MockNotificationGateway(NotificationGatewayInterface):
    """
    Mock implementation of NotificationGatewayInterface for testing and development.
    Simulates external notification service behavior.
    """

    async def send_sale_confirmation(self, user_email: str, sale_data: Dict[str, Any]) -> bool:
        """
        Send sale confirmation notification to user via mock service.

        Args:
            user_email: Email address of the user
            sale_data: Dictionary containing sale information

        Returns:
            bool: True if notification sent successfully, False otherwise
        """
        print(f"Mock: Sending sale confirmation to {user_email}")
        print(f"Sale data: {sale_data}")
        return True

    async def send_payment_notification(self, user_email: str, payment_data: Dict[str, Any]) -> bool:
        """
        Send payment status notification to user via mock service.

        Args:
            user_email: Email address of the user
            payment_data: Dictionary containing payment information

        Returns:
            bool: True if notification sent successfully, False otherwise
        """
        print(f"Mock: Sending payment notification to {user_email}")
        print(f"Payment data: {payment_data}")
        return True