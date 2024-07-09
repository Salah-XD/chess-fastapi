# Chess API

This is a FastAPI application that provides an API endpoint to determine the valid moves for a given chess piece on a chessboard.

## Setup


1. Activate the virtual environment:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On Linux:
     ```sh
     source venv/bin/activate
     ```

2. Install the necessary packages:

   ```sh
    pip install -r requirements.txt   
    ```


3. Build the Docker image:
   ```sh
   docker build -t chess-api .
   ```

4. Run the Docker container:
   ```sh
   docker run -d --name chess-api -p 8000:8000 chess-api
   ```

## Usage

Use tools like Postman or curl to test the API endpoints. For example:



```sh
curl -X POST "http://localhost:8000/chess/queen" -H "Content-Type: application/json" -d '{
    "positions": {
        "Queen": "E7",
        "Bishop": "B7",
        "Rook": "G5",
        "Knight": "C3"
    }
}'

```
```sh
curl -X POST "http://localhost:8000/chess/queen" -H "Content-Type: application/json" -d '{
    "positions": {
        "Queen": "H1",
        "Bishop": "B7",
        "Rook": "H8",
        "Knight": "F3"
    }
}'

```

```sh
curl -X POST "http://localhost:8000/chess/rook" -H "Content-Type: application/json" -d '{
    "positions": {
        "Queen": "A5",
        "Bishop": "G8",
        "Rook": "H5",
        "Knight": "G4"
    }
}'

```
