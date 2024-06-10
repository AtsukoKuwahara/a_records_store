# A's Records Store

A simple web application for managing a record store, built with Flask and MongoDB.

## Table of Contents

- [A's Records Store](#as-records-store)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Routes](#routes)
  - [Models](#models)
    - [User](#user)
    - [Product](#product)
    - [RecordOfTheWeek](#recordoftheweek)
    - [Order](#order)
  - [Forms](#forms)
    - [LoginForm](#loginform)
    - [RegisterForm](#registerform)
  - [Static Files](#static-files)
    - [CSS](#css)
    - [Images](#images)
    - [JavaScript](#javascript)
  - [Templates](#templates)
    - [Includes](#includes)
    - [Pages](#pages)
  - [License](#license)

## Features

- User registration and login
- User roles (admin and regular user)
- Admin page to set the record of the week
- Display of the record of the week with a custom message
- Product listing with the ability to buy products
- Shopping cart functionality
- Flash messages for feedback
- Responsive design with a clean UI

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/username/a_records_store.git
    cd a_records_store
    ```

2. **Set up a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set environment variables**:
    Create a `.flaskenv` file in the root directory with the following content:
    ```
    FLASK_ENV=development
    FLASK_APP=main.py
    SECRET_KEY='a_secure_and_long_random_string'
    ```

5. **Run the application**:
    ```sh
    flask run
    ```

## Usage

1. **Register a new user**: Navigate to `/register` to create a new account.
2. **Login**: Use the `/login` route to log in to the application.
3. **Admin Actions**:
    - Only the user with `user_id` 1 is an admin by default.
    - Navigate to `/admin` to set the record of the week and add a message.
4. **Browse Products**: View available products on the `/product` page.
5. **Shopping Cart**: Add products to the shopping cart and manage orders on the `/order` page.

## Project Structure

```
a_records_store/
│
├── .flaskenv
├── requirements.txt
├── config.py
├── main.py
├── application/
│   ├── __init__.py
│   ├── model.py
│   ├── routes.py
│   ├── forms.py
│   ├── shoppingcart.py
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── image/
│       │   ├── abbey_road.jpg
│       │   ├── logo1.png
│       │   ├── logo2.png
│       │   ├── placeholder.png
│       │   └── IMG_1194_land.jpg
│       └── js/
│           └── script.js
│   └── templates/
│       ├── includes/
│       │   ├── nav.html
│       │   └── footer.html
│       ├── admin.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── product.html
│       ├── order.html
│       └── layout.html
└── data/
    ├── products.json
    ├── coming_soon_products.json
    └── README.md
```

## Routes

- **GET /index**: Displays the homepage with the record of the week and coming soon products.
- **GET /register**: Registration page for new users.
- **POST /register**: Handles user registration.
- **GET /login**: Login page for existing users.
- **POST /login**: Handles user login.
- **GET /product**: Displays the product listing.
- **POST /order**: Manages the shopping cart and order process.
- **GET /admin**: Admin page to set the record of the week.
- **POST /admin**: Handles the update of the record of the week.

## Models

### User

Represents a user in the application.

- `user_id`: Unique identifier for the user.
- `first_name`: User's first name.
- `last_name`: User's last name.
- `email`: User's email address (unique).
- `password`: Hashed password.
- `role`: Role of the user (default is 'user').

### Product

Represents a product in the store.

- `product_id`: Unique identifier for the product.
- `title`: Title of the product.
- `artist`: Artist of the product.
- `label`: Label of the product.
- `price`: Price of the product.

### RecordOfTheWeek

Represents the record of the week.

- `product_id`: Identifier of the product selected as the record of the week.
- `message`: Message from the admin about why this record was selected.
- `created_at`: Timestamp when the record was created (defaults to the current time).

### Order

Represents an order placed by a user.

- `user_id`: Identifier of the user who placed the order.
- `product_id`: Identifier of the ordered product.
- `quantity`: Quantity of the product ordered.
- `is_order`: Boolean indicating whether the order is placed or not.

## Forms

### LoginForm

Used for user login.

- `email`: Email field with validation.
- `password`: Password field with validation.
- `submit`: Submit button.

### RegisterForm

Used for user registration.

- `email`: Email field with validation.
- `password`: Password field with validation.
- `password_confirm`: Password confirmation field with validation.
- `first_name`: First name field with validation.
- `last_name`: Last name field with validation.
- `submit`: Submit button.

## Static Files

### CSS

- `style.css`: Contains all the styles for the application.

### Images

- `abbey_road.jpg`: Image for the record of the week.
- `logo1.png`: Logo image with text.
- `logo2.png`: Logo image without text.
- `placeholder.png`: Placeholder image for products.
- `IMG_1194_land.jpg`: Background image.

### JavaScript

- `script.js`: Contains JavaScript functions for the application.

## Templates

### Includes

- `nav.html`: Contains the navigation bar.
- `footer.html`: Contains the footer.

### Pages

- `admin.html`: Admin page to set the record of the week.
- `index.html`: Homepage displaying the record of the week and coming soon products.
- `login.html`: Login page.
- `register.html`: Registration page.
- `product.html`: Product listing page.
- `order.html`: Shopping cart and order page.
- `layout.html`: Base layout for the application.

## License

This project is licensed under the MIT License.