# MindsDB example

## Step 1 - Install Dependencies

Start by running: `pip install mindsdb_sdk` - This will install the [official snowflake connector for python](https://mindsdb.com/blog/introduction-to-python-sdk-interact-with-mindsdb-directly-from-python).


## Step 2 - Add MindsDB Account info

You will need to identify the following from your MindsDB account

```python
server = mindsdb_sdk.connect(
    login='xxx',
    password='xxxx'
)
```

If you are using MindsDB Cloud account, this is simply your login and password to access your account.

NOTE: If you installed MindsDB locally via pip or Docker, use the connect method with one argument being your IP address and port.

```python
mindsdb_sdk.connect('http://127.0.0.1:47334')
```

## Step 3 - Configure the widgets.json and endpoints

Following our [Readme.md](/README.md) you can now configure the widgets.json and endpoints for your backend.

## Step 4 Run the backend

Run the backend with :

```python
Run `uvicorn main:app --port 5050`
```

## Step 5 - Add to Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.dev/app/data-connectors) with the base url of your API. In this case it is `http://localhost:5050`
