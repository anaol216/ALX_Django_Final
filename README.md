# E-commerce Product API

## Project Overview
This project is a comprehensive E-commerce Product API built with **Django** and **Django REST Framework (DRF)**. It serves as the backend for an e-commerce platform, enabling product management, user authentication, and advanced search functionalities. The API mimics real-world backend responsibilities, focusing on scalability, security, and performance.

## Features

### Product Management (CRUD)
- **Create, Read, Update, Delete**: Full CRUD operations for managing products.
- **Product Attributes**: Each product includes Name, Description, Price, Category, Stock Quantity, Image URL, and Created Date.
- **Validation**: Enforces strict validation for essential fields like Price, Name, and Stock Quantity.
- **Stock Management**: (Optional/Planned) Automatic stock reduction upon order placement.

### User Management
- **Authentication**: Secure user management with unique Username, Email, and Password.
- **Permissions**: Restricted access ensures only authenticated users can manage (create, update, delete) products.

### Product Search
- **Search Capabilities**: Search products by Name or Category.
- **Flexible Matching**: Supports partial matches for product names.
- **Pagination**: Optimized search results with pagination handling.

### Product View
- **Listing & Details**: Retrieve product lists or view specific product details via ID.
- **Filtering**: Filter products by Category, Price Range, and Stock Availability.
- **Detailed Info**: Responses include all relevant product data (Name, Description, Price, Category, Stock, Image URL).

## Technical Architecture

### Database
- **ORM**: Utilizes Django ORM for seamless database interaction.
- **Models**: Defines robust models for `Products` and `Users`.
- **Categorization**: Products are organized by categories (e.g., Electronics, Clothing).

### Authentication
- **System**: Built on Django’s authentication system.
- **Security**: CRUD operations are secured behind authentication barriers.
- **Token Auth**: (Optional) Implementation of JWT (Token-based authentication) for enhanced security.

### API Design
- **Framework**: Developed using Django REST Framework (DRF).
- **RESTful Principles**: Adopts standard HTTP methods (GET, POST, PUT, DELETE).
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes (e.g., 404 Not Found, 400 Bad Request).

### Deployment
- **Platform**: Information on deployment (e.g., Heroku, PythonAnywhere).
- **Standards**: Configured for stability, security, and accessibility.

## Future Enhancements & Stretch Goals
- **Product Reviews**: User ratings and reviews system.
- **Advanced Categories**: Dynamic category management (CRUD for categories).
- **Multiple Images**: Support for uploading and storing multiple images per product.
- **Wishlist**: Functionality for users to save products for later.
- **Stock Automation**: Real-time stock reduction on purchase.
- **Discounts**: Promotional discount system for specific products.

## Getting Started

### Prerequisites
- Python 3.x
- Django
- Django REST Framework

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd ALX_Django_Final
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
