# gem_crud_best

This package implements a modern FastAPI application structure using Async SQLAlchemy 2.0.

## Architecture

The project is structured to ensure separation of concerns and scalability:

- **core**: Contains database configuration (`db_helper`) and the base model class (`Base`). It uses `asyncpg` and `AsyncSession`.
- **models**: SQLAlchemy 2.0 models using `Mapped` and `mapped_column` for strict typing.
- **schemas**: Pydantic models for data validation and serialization (DTOs).
- **crud**: Functions for database interactions, keeping logic separate from views.
- **api**: FastAPI routers handling HTTP requests and responses.

## Database Relationships

### User and Post

We have a **One-to-Many** relationship between `User` and `Post`.

- A **User** can have multiple **Posts**.
- A **Post** belongs to one **User**.

This is implemented using `relationship()` in SQLAlchemy:
- `User.posts`: A list of `Post` objects.
- `Post.author`: A single `User` object.
- `Post.user_id`: The foreign key linking to the user's ID.

When a user is deleted, their posts are automatically deleted (`cascade="all, delete-orphan"`).

## Usage

The API provides endpoints for managing Users and Posts.

- `GET /users/`: List users.
- `POST /users/`: Create a user.
- `GET /users/{id}`: Get a user.
- `GET /posts/`: List posts.
- `POST /posts/?user_id={id}`: Create a post for a specific user.
