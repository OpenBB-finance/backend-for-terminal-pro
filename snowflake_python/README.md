# Snowflake Python

This example will focus on everything that relates with Snowflake in order to create a backend in Python for the OpenBB Terminal Pro. For more information, read our main [README.md](/README.md).

## 1. Get started with Snowflake

Check website: https://www.snowflake.com/en/.

Create an account at https://app.snowflake.com/.

## 2. Snowflake and Python

Read the [official Snowflake connector for python](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector).

TL;DR: Install Supabase with `pip install snowflake-connector-python`

## 3. Extract Supabase information

You will need to identify the following from your snowflake account

```python
conn = snowflake.connector.connect(
    user="",
    password="",
    account="",
    warehouse="COMPUTE_WH",
    database="Cybersyn_Weather__Environmental_Essentials",
    schema="CYBERSIN",
)
```

Account can be found in **Accounts** under the **Admin section**. It will look like: https://xxxxxx-xxxxxx.snowflakecomputing.com

The other information is found under the relevant Database you want to query.

In our example, the data used is from the **Cybersyn_Weather__Environmental_Essentials** database. You can read more information about it [here](https://app.snowflake.com/marketplace/listing/GZTSZAS2KIM/cybersyn-inc-cybersyn-weather-environmental-essentials?search=cybersin&sortBy=relevant&pricing=free).
