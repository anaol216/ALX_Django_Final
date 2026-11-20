
# API Testing Guide

## Base URL

http://127.0.0.1:8000

## Product Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/ | List products |
| POST | /api/ | Create a product |
| GET | /api/{id}/ | Retrieve a product |
| PUT | /api/{id}/ | Update a product |
| PATCH | /api/{id}/ | Partially update a product |
| DELETE | /api/{id}/ | Delete a product |

## Category Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/categories/ | List categories |
| POST | /api/categories/ | Create a category |
| GET | /api/categories/{id}/ | Retrieve a category |
| PUT | /api/categories/{id}/ | Update a category |
| PATCH | /api/categories/{id}/ | Partially update a category |
| DELETE | /api/categories/{id}/ | Delete a category |

## Testing with Postman

1. Start the Django development server.
2. Open Postman.
3. Select the required HTTP method.
4. Enter the endpoint URL.
5. For POST, PUT, and PATCH, select Body → raw → JSON.
6. Send the request and inspect the response status and body.

## Expected HTTP Status Codes

- 200 OK: Successful retrieval or update.
- 201 Created: Resource successfully created.
- 204 No Content: Resource successfully deleted.
- 400 Bad Request: Invalid request data.
- 404 Not Found: Resource does not exist.
