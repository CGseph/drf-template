# Django REST Framework Service Template
A microservice template built for Django REST Framework

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Poetry (for local development)
- Python 3.10+

### 1. Clone and Setup

```bash
git clone <repository-url>
cd drf-template
```

### 2. Build and Run with Docker

```bash
# Build all images
make build-images

# Run the complete stack
make run-images

# Or run in background
docker-compose up -d
```

### 3. Run Database Migrations

```bash
# Run migrations
make migrate-auth-service

# Or create new migrations if you've made model changes
make makemigrations-auth-service
```

### 4. Create Admin User (Optional)

```bash
# Create a superuser for admin access
docker-compose exec auth-service poetry run python src/manage.py createsuperuser
```

## 🛠️ Development Setup

### Local Development (without Docker)

```bash
# Install dependencies
cd auth-service
poetry install

# Run migrations
make migrate-auth-service

# Start development server
make run-auth-service
```

### Available Make Commands

```bash
make help                    # Show all available commands
make build-images           # Build Docker images
make build-images-no-cache  # Build without cache
make run-images            # Run the project
make clean-images          # Stop and remove containers/volumes
make run-auth-service      # Run auth service locally
make migrate-auth-service   # Run database migrations
make makemigrations-auth-service # Create new migrations
make shell-auth-service     # Open Django shell
```

## 📡 API Endpoints

### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | List all users | Yes (Session/Basic) |
| GET | `/api/users/{id}/` | Get user details | Yes (Session/Basic) |
| POST | `/api/users/{id}/change-password/` | Change user password | Admin Only |

## 🔧 Usage Examples

### 1. List Users (Session Authentication)

```bash
# Using session authentication (login first)
curl -X GET http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -b cookies.txt
```

### 2. List Users (Basic Authentication)

```bash
# Using basic authentication
curl -X GET http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -u "username:password"
```

### 3. Change User Password (Admin Only)

```bash
# Using basic authentication for admin
curl -X POST http://localhost:8000/api/users/1/change-password/ \
  -H "Content-Type: application/json" \
  -u "admin:adminpassword" \
  -d '{
    "new_password": "newsecurepassword456",
    "confirm_password": "newsecurepassword456"
  }'
```

## 🗄️ Database Configuration

The service uses PostgreSQL with the following default settings:

- **Host**: `localhost` (or `auth-db` in Docker)
- **Port**: `5432`
- **Database**: `postgres`
- **Username**: `postgres`
- **Password**: `postgres`

### Redis Configuration

Redis is configured with:

- **Host**: `localhost` (or `auth-redis` in Docker)
- **Port**: `6379`
- **Password**: `mypassword` (from `infra/redis/redis.conf`)

## 🔒 Security Features

- **Password Validation**: Django's built-in password validators
- **Session Authentication**: Secure session-based auth for development
- **Basic Authentication**: HTTP Basic Auth for API testing
- **Admin-Only Operations**: Password changes restricted to admins
- **Input Validation**: Comprehensive serializer validation
- **Caching**: Redis-based caching with automatic invalidation


## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps auth-db

   # Check logs
   docker-compose logs auth-db
   ```

2. **Migration Issues**
   ```bash
   # Reset migrations (development only)
   docker-compose exec auth-service poetry run python src/manage.py migrate --fake-initial
   ```

3. **Redis Connection Issues**
   ```bash
   # Check Redis status
   docker-compose exec auth-redis redis-cli ping
   ```

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs auth-service
docker-compose logs auth-db
docker-compose logs auth-redis
```

## 📝 Development Notes

- **Authentication**: Session and Basic authentication for development
- **Caching**: Redis caching is enabled with 15-minute timeouts
- **Hot Reload**: Source code is mounted for development
- **Debug Mode**: Debugpy is available on port 5678 for debugging
