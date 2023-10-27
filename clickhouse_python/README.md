# ClickHouse Python

This example will focus on everything that relates with ClickHouse in order to create a backend in Python for the OpenBB Terminal Pro. For more information, read our main [README.md](/README.md).

## 1. Get started with ClickHouse

Check website: https://clickhouse.com/.

Create an account at https://clickhouse.cloud.

## 2. ClickHouse and Python

Read the [official ClickHouse connector for python](https://clickhouse.com/docs/en/integrations/python).

TL;DR: Install ClickHouse with `pip install clickhouse-connect`

## 3. Extract ClickHouse information

You will need to identify the following from your ClickHouse account

```python
client =  v.get_client(
    host="XYZ",
    port=8443,
    username="default",
    password="XYZ",
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
