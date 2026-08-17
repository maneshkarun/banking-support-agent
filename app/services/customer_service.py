"""Customer business operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.services.exceptions import ConflictError, NotFoundError


class CustomerService:
    """Provide customer registration and retrieval operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the service with a database session."""

        self.session = session

    def create(self, payload: CustomerCreate) -> Customer:
        """Register a customer after enforcing email uniqueness."""

        if self.session.scalar(select(Customer).where(Customer.email == payload.email)):
            raise ConflictError("A customer with this email already exists")
        customer = Customer(**payload.model_dump())
        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def get(self, customer_id: int) -> Customer:
        """Return a customer by identifier or raise a not-found error."""

        customer = self.session.get(Customer, customer_id)
        if customer is None:
            raise NotFoundError("Customer not found")
        return customer

