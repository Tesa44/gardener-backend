# API Documentation

This document describes the available endpoints for the **Users** and **Resources** APIs.

---

## Base URLs

All API endpoints are relative to the following base URL:
 - `https://gardener-backend-owo6.onrender.com`

### Routers
- **Users API base:** `/users`
- **Resources API base:** `/resources`

---

# Users API

## Register a new user

`POST /users/register`

### Request Body

{
  "name": "string",
  "email": "string",
  "password": "string"
}

### Responses

    200 OK

{
  "msg": "User registered"
}

    400 Bad Request

{
  "detail": "User already exists"
}

## User login

POST /users/login
### Request Body

{
  "email": "string",
  "password": "string"
}

### Responses

    200 OK

{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "name": "string"
  }
}

    400 Bad Request

{
  "detail": "Invalid credentials"
}

# Resources API
## Create a resource

POST /resources/
### Request Body

{
  "name": "string",
  "description": "string",
  "category": "string",
  "quantity": 0,
  "status": "string"  // e.g. "Available", "Low Stock", "Out of Stock"
}

### Responses

    200 OK

{
  "msg": "Resource added"
}

## Get all resources for authenticated user

GET /resources/
### Responses

    200 OK

[
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "category": "string",
    "quantity": 0,
    "status": "string",
    "date_added": "datetime",
    "last_updated": "datetime",
    "user_id": 1
  },
  ...
]

## Update a resource

PUT /resources/{resource_id}
## Path Parameters

    resource_id: integer, the ID of the resource to update

### Request Body

{
  "name": "string",
  "description": "string",
  "category": "string",
  "quantity": 0,
  "status": "string"
}

### Responses

    200 OK

{
  "msg": "Resource updated",
  "last_updated": "datetime"
}

    404 Not Found

{
  "detail": "Resource not found"
}

## Delete a resource

DELETE /resources/{resource_id}
### Path Parameters

    resource_id: integer, the ID of the resource to delete

Responses

    200 OK

{
  "msg": "Resource deleted"
}

    404 Not Found

{
  "detail": "Resource not found"
}

## Authentication

    All /resources endpoints require authentication via Bearer token.

    Pass the token in the Authorization header:

    Authorization: Bearer <your_token_here>

## Database and Security
  This API uses a MySQL database hosted online on the Aiven platform.

  API requests are restricted and blocked for unauthorized origins. Only requests coming from the official frontend application are allowed to access the API endpoints, ensuring secure and controlled usage.

## Notes

    Dates/timestamps are typically in ISO 8601 format.

    The last_updated field is set automatically on updates.

    Errors return standard HTTP status codes with a JSON detail message.
