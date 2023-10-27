# ClickHouse example

## Step 1 - Install Dependencies

Start by running: `pip install clickhouse-connect`

This will install the [official ClickHouse connector for python](https://clickhouse.com/docs/en/integrations/python).


## Step 2 - Add ClickHouse Account info

You will need to identify the following from your ClickHouse account

```python
client =  v.get_client(
    host="",
    port=8443,
    username="default",
    password="",
)
```

By default, the port and username should be `8443` and `"default"`.

The password is the one associated with your ClickHouse account.

The host can be found by going into ClickHouse Services, thhen clicking on the "Connect" dropdown and selecting "View connection string".

There you'll see a "Native" tab with the following

```console
./clickhouse client --host abc123de45.us-east-1.aws.clickhouse.cloud --secure --password
```

where your host will be `abc123de45.us-east-1.aws.clickhouse.cloud`.


## Step 3 - Configure the widgets.json and endpoints

Following our [Readme.md](/README.md) you can now configure the widgets.json and endpoints for your backend.


## Step 4 Run the backend

Run the backend with :

```python
Run `uvicorn main:app --port 5050`
```

## Step 5 - Add to the Terminal Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.dev/app/data-connectors) with the base url of your API.

In this case it is `http://localhost:5050`
