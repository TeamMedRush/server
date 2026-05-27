# Architecture

## Overview
MedRush Server is split into four main layers:

1. `mrs/framework`
2. `mrs/routes`
3. `mrs/services`
4. `mrs/database`

The framework owns request parsing, response generation, routing, and middleware execution.
Routes translate HTTP requests into service calls.
Services implement application rules and talk to the database.
The database layer is an in-memory repository with typed tables and simple query support.

## Request Flow
1. `mrs/framework/server.py` accepts the socket request and builds a `Request`.
2. `mrs/framework/router.py` matches the path and executes `pre` middleware.
3. The route handler validates request shape and calls the service layer.
4. The service layer performs business logic and uses the repository.
5. `post` middleware runs after the handler returns.
6. `mrs/framework/models/response.py` serializes the response bytes back to the socket.

## Layer Responsibilities

### Framework
- `Request` and `Response` models
- path matching and endpoint dispatch
- middleware execution
- HTTP response serialization

### Routes
- request parsing
- minimal validation
- credential extraction for protected endpoints
- translating service errors into HTTP status codes

Routes should stay thin. They should not contain business logic or persistence logic.

### Services
- account creation and update
- auth sign up/sign in
- order booking and acceptance
- inventory management
- domain validation that does not belong in the HTTP layer

Services should be the primary place to extend the product behavior.

### Database
- in-memory tables
- typed column schema
- simple query operations
- shared repository singleton

The current database is intentionally lightweight. It is structured so it can later be swapped for a persistent backend without rewriting routes.

## Current Domain Model

### Auth
There is one shared auth table for all personas.
Each auth record stores:
- persona
- profile table
- profile id
- email
- phone
- password
- token

### User
Users store:
- name
- email
- phone
- age
- home location lat/long
- address fields

Users can:
- create an account
- update an account
- book orders

### Agent
Agents store:
- name
- email
- phone
- age

Agents can:
- create an account
- update an account
- list pending orders
- accept an order

### Partner
Partners store:
- name
- email
- phone
- lat/long location
- address fields

Partners can:
- create an account
- update an account
- read inventory
- bulk update inventory

## Middleware
Middleware is attached at route registration time using:

```python
Router.endpoint(path, pre=[...], post=[...])
```

The middleware callables are simple `request -> request` functions.

- `pre` runs before the route handler
- `post` runs after the route handler finishes

Use middleware for cross-cutting request mutation, especially auth token extraction.

## How To Update Things

### Add a new endpoint
1. Add a route in `mrs/routes/...`.
2. Call the service layer from the route handler.
3. Add or reuse middleware via `pre` or `post`.
4. Add a test under `tests/` with `langex` expectations.

### Add a new service
1. Put the implementation in `mrs/services/`.
2. Keep request parsing out of the service.
3. Use the repository tables through `mrs.database.repository`.
4. Add tests that exercise the service through a route or a direct service call.

### Add a new table or field
1. Update `mrs/database/__init__.py` schema.
2. Update service validation and update logic.
3. Add or adjust tests.

### Add middleware
1. Put the callable in `mrs/middleware/`.
2. Attach it in the route decorator using `pre=[...]` or `post=[...]`.
3. Keep the callable simple and request-focused.

## Test Strategy
The suite uses `langex` expectations through `python -m tests`.
Tests should stay small and direct:

- use helper modules for common payloads and request helpers
- keep expectations on zero-arg functions
- reset repository state between scenarios
- prefer route-level checks for HTTP behavior and direct service calls for domain behavior

## Dev Ecosystem
Development commands are routed through `dev.sh`.
That script sources the local environment, loads `config.sh`, and exposes the shell commands in `scripts/` as `dev <command>`.

The command layout is:

- `scripts/help.sh` lists commands and loads the matching docs file from `scripts/docs/`
- `scripts/setup.sh` installs the venv and dependencies
- `scripts/run.sh` runs the application module
- `scripts/test.sh` runs `python -m tests`
- `scripts/fmt.sh` runs the formatter
- `scripts/install.sh` installs packages and refreshes `requirements.txt`
- `scripts/build.sh` is present but intentionally not implemented in this version

When you add a new developer command, add both:

1. a `scripts/<command>.sh` executable
2. a matching `scripts/docs/<command>.txt` file

## Notes
The database is still in-memory and the auth store is intentionally low-effort.
That is acceptable for the current version, but the architecture keeps the boundaries clear so persistence and safer auth can be added later without changing the overall shape of the app.
