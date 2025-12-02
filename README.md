# Online Drive - Driver Order Assignment System

A scalable backend system for managing online drivers and order assignments, built with Django, Django REST Framework, and Django Channels for real-time updates.

## Features

- **Driver Management**: Drivers can go online/offline and update their location
- **Order Management**: Clients can create orders that are automatically assigned to available drivers
- **Real-time Updates**: WebSocket support for live driver availability updates
- **Automatic Assignment**: Orders are automatically assigned to online and available drivers
- **RESTful API**: Clean and well-documented REST API endpoints
- **Type Hints**: Full Python type hinting for better code quality
- **Dockerized**: Easy deployment with Docker and Docker Compose
- **CI/CD**: Automated testing and linting with GitHub Actions

## Tech Stack

- **Python 3.11**
- **Django 5.0.1**
- **Django REST Framework 3.14.0**
- **Django Channels 4.0.0** (WebSocket support)
- **PostgreSQL 15** (Database)
- **Redis 7** (Cache and Channel Layer)
- **drf-spectacular 0.27.1** (OpenAPI 3.0 Documentation)
- **Docker & Docker Compose**
- **GitHub Actions** (CI/CD)

## API Documentation

The API is fully documented using **OpenAPI 3.0** (Swagger) specification with **drf-spectacular**.

### Interactive API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: [http://localhost:8088/api/docs/](http://localhost:8088/api/docs/)

  - Interactive API documentation with "Try it out" functionality
  - Test all endpoints directly from the browser
  - View request/response schemas, parameters, and authentication

- **ReDoc**: [http://localhost:8088/api/redoc/](http://localhost:8088/api/redoc/)

  - Clean, three-panel documentation layout
  - Better for reading and understanding the API structure

- **OpenAPI Schema**: [http://localhost:8088/api/schema/](http://localhost:8088/api/schema/)
  - Raw OpenAPI 3.0 schema in YAML format
  - Can be imported into Postman, Insomnia, or other API clients

### Features of the API Documentation

- ✅ **Complete Request/Response Schemas**: Every endpoint shows exact request body and response format
- ✅ **Authentication Support**: Test authenticated endpoints directly from Swagger UI
- ✅ **Parameter Documentation**: All path parameters, query parameters, and headers documented
- ✅ **Error Responses**: All possible error codes (400, 401, 403, 404) documented with descriptions
- ✅ **Try It Out**: Execute API calls directly from the documentation interface
- ✅ **Code Examples**: See example requests and responses for each endpoint
- ✅ **Organized by Tags**: Endpoints grouped by Drivers, Orders, and Authentication

## Project Structure

```
online-drive-test/
├── apps/
│   ├── users/          # User authentication and management
│   ├── drivers/        # Driver models, services, and APIs
│   └── orders/         # Order models, services, and APIs
├── config/             # Django project settings
├── .github/workflows/  # CI/CD configuration
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Docker image configuration
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Prerequisites

- Docker and Docker Compose
- Git

## Installation and Setup

### 1. Clone the Repository

```bash
git https://github.com/murtazox04/online-drive-test.git
cd online-drive-test
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=online_drive_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6333

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Build and Run with Docker

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8088`

### 4. Create a Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access Admin Panel

Navigate to `http://localhost:8088/admin` and login with your superuser credentials.

## API Endpoints

### Driver Endpoints

#### Set Driver Online

```
POST /api/drivers/online/
```

Sets the authenticated driver as online.

**Authentication**: Required (Driver only)

**Response**:

```json
{
  "id": 1,
  "user": {...},
  "latitude": null,
  "longitude": null,
  "is_online": true,
  "is_busy": false,
  "is_available": true,
  "vehicle_number": "ABC123",
  "vehicle_model": "Toyota Camry",
  "last_online_at": "2024-01-15T10:30:00Z"
}
```

#### Set Driver Offline

```
POST /api/drivers/offline/
```

Sets the authenticated driver as offline.

**Authentication**: Required (Driver only)

#### Update Driver Location

```
PATCH /api/drivers/location/
```

Updates the driver's current location.

**Authentication**: Required (Driver only)

**Request Body**:

```json
{
  "latitude": 40.712776,
  "longitude": -74.005974
}
```

#### Get Driver Status

```
GET /api/drivers/status/
```

Returns the current status of the authenticated driver.

**Authentication**: Required (Driver only)

#### Get Available Drivers

```
GET /api/drivers/available/
```

Returns a list of all online and available drivers.

**Authentication**: Required

**Response**:

```json
[
  {
    "id": 1,
    "username": "driver1",
    "phone_number": "+1234567890",
    "latitude": 40.712776,
    "longitude": -74.005974,
    "vehicle_number": "ABC123",
    "vehicle_model": "Toyota Camry"
  }
]
```

### Order Endpoints

#### Create Order

```
POST /api/orders/create/
```

Creates a new order. The order is automatically assigned to an available driver if one exists.

**Authentication**: Required (Client only)

**Request Body**:

```json
{
  "pickup_latitude": 40.712776,
  "pickup_longitude": -74.005974,
  "pickup_address": "123 Main St, New York, NY",
  "dropoff_latitude": 40.758896,
  "dropoff_longitude": -73.98513,
  "dropoff_address": "456 Broadway, New York, NY",
  "notes": "Please call when you arrive"
}
```

**Response**:

```json
{
  "id": 1,
  "client": {...},
  "driver": 1,
  "driver_detail": {...},
  "status": "ASSIGNED",
  "pickup_latitude": 40.712776,
  "pickup_longitude": -74.005974,
  "pickup_address": "123 Main St, New York, NY",
  "dropoff_latitude": 40.758896,
  "dropoff_longitude": -73.985130,
  "dropoff_address": "456 Broadway, New York, NY",
  "notes": "Please call when you arrive",
  "created_at": "2024-01-15T10:30:00Z",
  "assigned_at": "2024-01-15T10:30:05Z",
  "completed_at": null
}
```

#### Get My Orders

```
GET /api/orders/my-orders/
```

Returns all orders for the authenticated user (client orders or driver assignments).

**Authentication**: Required

#### Get Order Details

```
GET /api/orders/<order_id>/
```

Returns detailed information about a specific order.

**Authentication**: Required

#### Complete Order

```
PATCH /api/orders/<order_id>/complete/
```

Marks an order as completed. Only the assigned driver can complete their orders.

**Authentication**: Required (Driver only)

## WebSocket Endpoints

### Available Drivers Stream

```
ws://localhost:8088/ws/drivers/
```

Real-time stream of available drivers.

**Connection**: Establish WebSocket connection

**Message Types**:

**Receive**: Driver list on connection

```json
{
  "type": "driver_list",
  "drivers": [...]
}
```

**Send**: Request driver list update

```json
{
  "type": "get_drivers"
}
```

**Receive**: Driver update notification

```json
{
  "type": "driver_update",
  "drivers": [...]
}
```

## Order Status Flow

```
CREATED → ASSIGNED → COMPLETED
```

1. **CREATED**: Order is created by client, waiting for driver assignment
2. **ASSIGNED**: Order is assigned to an available driver
3. **COMPLETED**: Driver completes the order

## Running Tests

```bash
# Run all tests
docker-compose exec web pytest

# Run with coverage
docker-compose exec web pytest --cov=apps --cov-report=html

# Run specific test file
docker-compose exec web pytest apps/drivers/tests.py
```

## Code Quality

### Run Linting

```bash
# Flake8
docker-compose exec web flake8 apps config

# Black (code formatting)
docker-compose exec web black --check apps config

# MyPy (type checking)
docker-compose exec web mypy apps config
```

### Auto-format Code

```bash
docker-compose exec web black apps config
```

## Database Migrations

```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate
```

## Development

### Without Docker

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Setup PostgreSQL and Redis locally

4. Run migrations:

```bash
python manage.py migrate
```

5. Run development server:

```bash
python manage.py runserver 8088
# For WebSocket support
daphne -b 0.0.0.0 -p 8088 config.asgi:application
```

## Architecture Highlights

### Service Layer Pattern

Business logic is separated into service classes (`services.py`) for better testability and reusability.

### Caching

Available drivers list is cached in Redis for 60 seconds to reduce database load.

### Database Optimization

- Proper indexing on frequently queried fields
- `select_related` and `prefetch_related` for query optimization
- Database transactions for atomic operations

### Real-time Updates

Django Channels with Redis backend for scalable WebSocket connections.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please create an issue in the GitHub repository.
