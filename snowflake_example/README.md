# Snowflake example


## Step 1 - Install Dependencies

Start by running: `pip install snowflake-connector-python` - This will install the [official snowflake connector for python](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector).


## Step 2 - Add Snowflake Account info

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

Account can be found in Accounts under the Admin section- ex. https://xxxxxx-xxxxxx.snowflakecomputing.com

The other information is found under the relevant Database you want to query.

In our example, the data used is from the Cybersyn_Weather__Environmental_Essentials database.

## Step 3 - Configure the widgets.json and endpoints

Following our [Readme.md](/README.md) you can now configure the widgets.json and endpoints for your backend.

## Step 4 Run the backend

Run the backend with :

```python
Run `uvicorn main:app --port 5050`
```

## Step 5 - Add to Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.dev/app/data-connectors) with the base url of your API. In this case it is `http://localhost:5050`
