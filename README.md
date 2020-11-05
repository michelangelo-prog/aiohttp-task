# aiohttp-task

## Start

```bash
docker-compose up --build
```

Access the application at the address [http://0.0.0.0:8000/](http://0.0.0.0:8000/)

## Description


- [POST] `/api/v1/items/` - create new item

    Example request body:
    ```
    {
        "key": "example_key",
        "value": 1
    }
    ```

    Example response:
    
    ```
    {
        "status": "Request created."
    }
    ```
  
- [GET] `/api/v1/items/{key}` - get item

    Example response:
    
    ```
    {
        "key": "example_key",
        "value": 1
    }
    ```