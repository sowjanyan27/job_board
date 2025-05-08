# User Management API

## Description

This project provides a FAST  APIs for managing user data. The API allows for fetching a list of users, streaming user data in batches, and retrieving individual users by their ID. The core functionality is implemented using **FastAPI**, and the data is stored and retrieved using **SQLAlchemy** ORM.

## File: `user.py`

### Description

The `user.py` file contains the **User model**, **Pydantic schema** for user data validation, and any related logic for managing users in the database. This file plays a central role in defining the structure of the user data and ensuring proper validation of the data through Pydantic models.

### Features

- **User Model**: The `User` class defines the database model for the user, including the user attributes (e.g., `id`, `name`, `email`, etc.).
- **Pydantic Schema**: The `UserOut` Pydantic model is used for serializing the user data when it is returned in API responses.
- **CRUD Operations**: The file may also contain methods that interact with the database to create, retrieve, update, and delete users.
