# Cat Babysitter CRUD

This project implements client-server CRUD system for cat babysitter bookings.

## Project Structure

- `cat_client.py`: Sends CRUD requests to the server.
- `cat_server.py`: Receives requests, executes CRUD operations, and sends responses.
- `cat_db.py`: Database layer using SQLite (`cats.db`).

## CRUD Components

### `BD` class (`cat_db.py`)

The `BD` class is responsible for persistence and database operations:

- `insert(owner, cat, days, price, city) -> int`: Creates a booking and returns the generated `id`.
- `get(id) -> tuple | None`: Reads one booking by `id`.
- `update(id, owner, cat, days, price, city)`: Updates an existing booking.
- `delete(id)`: Deletes a booking by `id`.
- `list() -> list[tuple]`: Returns all bookings.

The table created is:

- `bookings(id INTEGER PRIMARY KEY, owner_name TEXT, cat_name TEXT, days INTEGER, price_per_day REAL, city TEXT)`

### Server flow (`cat_server.py`)

The server listens on `127.0.0.1:65535`, accepts one client connection, and handles opcodes:

- `c`: create
- `r`: read
- `u`: update
- `d`: delete
- `l`: list

### Client flow (`cat_client.py`)

The client provides an interactive menu and validates user input before sending data.

## Data Model

Booking fields:

- `id` (int): primary key.
- `owner_name` (string): cat owner's name.
- `cat_name` (string): cat name.
- `days` (int): number of babysitting days.
- `price_per_day` (float): daily price.
- `city` (string): service city.

## Limits and Validation

Because the protocol encodes some values in 1 byte and 2 bytes, practical limits are:

- `id`: `0..65535` (2-byte unsigned integer in protocol).
- `owner_name`: up to `255 bytes` (UTF-8 encoded length stored in 1 byte).
- `cat_name`: up to `255 bytes` (UTF-8 encoded length stored in 1 byte).
- `days`: `0..255` (1-byte unsigned integer).
- `price_per_day`: must be `>= 0.0` (encoded as 8-byte float, `double`).
- `city`: up to `255 bytes` (UTF-8 encoded length stored in 1 byte).

## How to Run with `uv`

From the repository root, open two terminals.

### 1) Start the server

```bash
uv run ./project-1-cat-babysitter/cat_server.py
```


### 2) Start the client

```bash
uv run ./project-1-cat-babysitter/cat_client.py
```


## Notes

- Start the server before the client.
- The SQLite file (`cats.db`) should be created automatically.