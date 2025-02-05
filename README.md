# Little Lemon API Project using Django REST Framework

This project is part of the **Meta Back-End Developer Professional Certificate**. It implements RESTful APIs for the **Little Lemon** restaurant system, covering features such as user management, menu items, carts, orders, and role-based access control. The project utilizes **Django** and **Django Rest Framework (DRF)** to handle user authentication, role management, and CRUD operations.


## Project Highlights

- **Full-Stack API**: Developed using Django and DRF to provide robust backend functionality.
- **Token-Based Authentication**: Secure access with **Djoser** for authentication.
- **Role-Based Access Control**: Role-based API access for different users, such as Customer, Manager and DeliveryCrew.
- **Advanced Querying**: Implements searching, sorting, filtering and pagination for efficient data retrieval.
- **Rate Limiting**: Applies role-based throttling to prevent abuse of the API.
- **Comprehensive Endpoints**: Covers user registration, role group management, menu management, cart handling, and order processing.


## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [API Testing](#api-testing)
- [License](#license)


## Project Overview

This project serves as a comprehensive role-based access control API for a restaurant application, where superusers, managers, customers, and delivery crew each have distinct permissions.

- **SuperUser** has full administrative access, with the ability to assign or revoke roles for both **Manager** and **DeliveryCrew**. The superuser has access to all features and permissions in the system.
- **Manager** can assign or revoke roles for both **Manager** and **DeliveryCrew**, manage menu items, handle orders, and assign **DeliveryCrew** to specific orders.
- **Customer** refers to users who are not assigned to any group. Customers can search for menu items, add them to the cart, and place orders.
- **DeliveryCrew** is assigned to orders by the **Manager** and can update the delivery status of the orders assigned to them.

The system follows role-based access control (RBAC) to manage user permissions and streamline restaurant operations.


## Features

- **Searching**: Allows users to search results based on query parameters.
- **Sorting**: Enables sorting of results by various attributes.
- **Filtering**: Enables filtering of orders based on status.
- **Pagination**: Returns paginated results to enhance performance.
- **Throttling**: Role-based rate limiting prevents excessive requests.
- **Role-Based Access Control**: Users with specific roles (e.g., Manager, DeliveryCrew) can perform different actions.
- **Authentication**: Token-based authentication ensures secure access to endpoints.


## Technologies Used

- **Backend**: Django, Django REST Framework (DRF)
- **Authentication**: Djoser (Token-based authentication)
- **Database**: SQLite3


## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/TANMOY-TRC/Meta-Back-End-Developer-LittleLemonAPI.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Meta-Back-End-Developer-LittleLemonAPI
   ```

3. Install dependencies and activate the virtual environment:
   ```bash
   pipenv install
   pipenv shell
   ```

4. Apply the migrations:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. Create superuser:
   ```bash
   python3 manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python3 manage.py runserver
   ```

7. Navigate to Django Admin Panel and login as superuser:
   ```bash
   http://127.0.0.1:8000/admin/
   ```

8. Create two user groups: `Manager` and `DeliveryCrew`.


## API Endpoints

#### `/auth/users/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `POST` | Anyone | Creates new user credential | Not Required | 201 |

**Payload**:
```js
{
   "email": "string",
   "username": "string",
   "password": "string"
}
```

#### `/auth/users/me/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Authenticated User | Returns user details | Required | 200 |

#### `/auth/token/login/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `POST` | Valid User | Returns auth token | Not Required | 200 |

**Payload**:
```js
{
   "username": "string",
   "password": "string"
}
```

#### `/auth/token/logout/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `POST` | Authenticated User | Destroys the auth token | Required | 204 |

#### `/api/categories/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Anyone | Retrives all categories | Not Required | 200 |
| `POST` | Manager | Adds new category | Required | 201 |

**Payload**:
```js
{
   "title": "string"
}
```

#### `/api/categories/{id}/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Anyone | Retrives specific category | Not Required | 200 |
| `PUT` | Manager | Modifies specific category | Required | 200 |
| `PATCH` | Manager | Modifies specific field | Required | 200 |
| `DELETE` | Manager | Deletes the category | Required | 204 |

**Payload**:
```js
{
   "title": "string"
}
```

#### `/api/menu-items/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Anyone | Retrives all menu items | Not Required | 200 |
| `POST` | Manager | Adds new menu item | Required | 201 |

**Payload**:
```js
{
   "title": "string",
   "price": "decimal",
   "category_id": number,
   "featured": boolean
}
```

#### `/api/menu-items/{id}/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Anyone | Retrives specific menu item | Not Required | 200 |
| `PUT` | Manager | Modifies specific menu item | Required | 200 |
| `PATCH` | Manager | Modifies specific fields | Required | 200 |
| `DELETE` | Manager | Deletes the menu item | Required | 204 |

**Payload**:
```js
{
   "title": "string",
   "price": "decimal",
   "category_id": number,
   "featured": boolean
}
```

#### `/api/cart/menu-items/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Customer | Retrives all items from cart | Required | 200 |
| `POST` | Customer | Adds new item in cart | Required | 201 |
| `DELETE` | Customer | Deletes all items from cart | Required | 200 |

**Payload**:
```js
{
   "menuitem_id": number,
   "quantity": number
}
```

#### `/api/cart/menu-items/{id}/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Customer | Retrives specific item from cart | Required | 200 |
| `PUT` | Customer | Modifies specific item from cart | Required | 200 |
| `PATCH` | Customer | Modifies specific fields | Required | 200 |
| `DELETE` | Customer | Deletes the item from cart | Required | 204 |

**Payload**:
```js
{
   "menuitem_id": number,
   "quantity": number
}
```

#### `/api/orders/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Customer | Retrives all orders created by the customer | Required | 200 |
| `GET` | Manager | Retrives all orders by all users | Required | 200 |
| `GET` |  DeliveryCrew | Retrives all orders assigned to the delivery crew | Required | 200 |
| `POST` | Customer | Creates a order by using the cart | Required | 201 |

#### `/api/orders/{id}/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Authenticated User | Retrives specific order | Required | 200 |
| `PUT` | Manager | Modifies specific order | Required | 200 |
| `PATCH` | Manager | Assigns delivery crew | Required | 200 |
| `PATCH` | DeliveryCrew | Updates status | Required | 200 |
| `DELETE` | Manager | Deletes the order | Required | 204 |

**Payload**:
```js
{
   "delivery_crew_id": number,
   "status": boolean
}
```

#### `/api/groups/manager/users/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Manager | Retrives all users from the Manager group | Required | 200 |
| `POST` | Manager | Adds user to Manager group | Required | 201 |

**Payload**:
```js
{
   "username": "string"
}
```

#### `/api/groups/manager/users/{userId}/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `DELETE` | Manager | Deletes user from Manager group | Required | 200 |

#### `/api/groups/delivery-crew/users/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `GET` | Manager | Retrives all users from the DeliveryCrew group | Required | 200 |
| `POST` | Manager | Adds user to DeliveryCrew group | Required | 201 |

**Payload**:
```js
{
   "username": "string"
}
```

#### `/api/groups/delivery-crew/users/{userId}/`
| Method | Role | Action | AUTH TOKEN | STATUS CODE |
| ------ | ---- | ------ | ---------- | ----------- |
| `DELETE` | Manager | Deletes user from DeliveryCrew group | Required | 200 |


## API Testing

The API can be tested by sending HTTP requests to the appropriate endpoints using tools such as [Insomnia](https://insomnia.rest/download).


## License

This project is licensed under the [MIT License](./LICENSE).
