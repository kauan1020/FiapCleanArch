# Vehicle Store API

A REST API for vehicle dealership management system built with FastAPI following Clean Architecture principles and SOLID design patterns.

## Architecture

This project follows Clean Architecture with clear separation of concerns:

```
├── domain/              # Business entities and rules
├── api/                # API routes and schemas
├── use_cases/          # Application business logic
├── interfaces/         # Contracts and abstractions
├── infra/             # Infrastructure implementations
│   ├── controllers/    # HTTP request handlers
│   ├── repositories/   # Data persistence
│   ├── gateways/      # External services
│   └── presenters/    # Response formatting
```

## Features

### User Management
- Create, read, update, delete users
- Email and CPF uniqueness validation
- User profile management

### Vehicle Management
- Create and update vehicle listings
- List available vehicles (ordered by price)
- List sold vehicles (ordered by price)
- Vehicle status management (available/sold/reserved)

### Sales Management
- Process vehicle sales
- Payment integration via webhook
- Automatic vehicle status updates
- Sale confirmation notifications

### Payment Integration
- Payment processing through external gateway
- Webhook endpoint for payment status updates
- Automatic vehicle status management based on payment

## API Endpoints

### Users
- `POST /users` - Create user
- `GET /users/{id}` - Get user by ID
- `GET /users` - List users (paginated)
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Vehicles
- `POST /vehicles` - Create vehicle
- `GET /vehicles/{id}` - Get vehicle by ID
- `GET /vehicles` - List available vehicles (ordered by price)
- `GET /vehicles/sold` - List sold vehicles (ordered by price)
- `PUT /vehicles/{id}` - Update vehicle

### Sales
- `POST /sales` - Create sale
- `POST /sales/webhook/payment` - Payment webhook

## Quick Start

### Using Docker Compose

1. Clone the repository
2. Run the application:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database

3. Run migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn main:app --reload
```

## Database Schema

The system uses PostgreSQL with the following main entities:

- **Users**: Customer information with unique email and CPF
- **Vehicles**: Vehicle inventory with pricing and status
- **Sales**: Transaction records linking users and vehicles

## Design Patterns

### Clean Architecture
- **Domain Layer**: Pure business logic and entities
- **Use Cases Layer**: Application-specific business rules
- **Interface Adapters**: Controllers, presenters, and gateways
- **Infrastructure Layer**: Database, external services, and frameworks

### SOLID Principles
- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Derived classes are substitutable for base classes
- **I**nterface Segregation: Many specific interfaces over one general interface
- **D**ependency Inversion: Depend on abstractions, not concretions

## Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

The application includes comprehensive unit tests for all layers:

```bash
pytest
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- Default: `postgresql://admin:password@localhost:5432/vehicle_store`

## Contributing

1. Follow the established architecture patterns
2. Maintain clear separation between layers
3. Write comprehensive tests
4. Use dependency injection for all external dependencies
5. Keep business logic pure and framework-independent