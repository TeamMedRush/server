<div align="center">

# Medrush Server

Backend server for Medrush, a platform for managing a hyperlocal quick commerce for medicines and healthcare products.

</div>

## Installation

```sh
# Clone the repository
git clone https://github.com/TeamMedRush/server.git
cd server

# Source the development environment
source dev.sh

# Setup and run
dev setup
dev run
```

## About

Medrush Server is the backend component of the Medrush platform, designed to handle core functionalities such as user management, order processing, inventory management, and more. It provides a robust API for the frontend applications to interact with, ensuring a seamless experience for users.

## Project Structure

```tree
mrs
├── __init__.py
├── __main__.py
├── core
│   ├── __init__.py
│   └── server.py
├── framework
│   ├── __init__.py
│   ├── analyser.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── request.py
│   │   └── response.py
│   ├── router.py
│   └── server.py
└── routes
    ├── __init__.py
    ├── api
    │   ├── __init__.py
    │   └── v1
    │       ├── __init__.py
    │       ├── agent.py
    │       ├── partner.py
    │       └── user.py
    ├── home.py
    └── static.py
```

## Links

- [GitHub](https://github.com/TeamMedRush/server)
- [License](https://github.com/TeamMedRush/server/tree/main/LICENSE)

## Contributors

<a href="https://github.com/TeamMedRush/server/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=TeamMedRush/server" />
</a>

