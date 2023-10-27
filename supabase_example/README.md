# Supabase example

## Step 1 - Install Dependencies

Start by running: `pip install supabase-py`

This will install the [official Supabase connector for python](https://supabase.com/docs/reference/python/introduction).


## Step 2 - Add Supabase Account info

You will need to identify the following from your Supabase account

```python
supabase: Client = create_client(
    url="XYZ",
    key="XYZ"
)
```

All the information can be found on your project, in Project Settings.

The URL is in the **Project URL** box.

The API key is under **Project API keys**. There are 2 keys available:

- The first is safe to use in a browser if you have enabled Row Level Security for your tables and configured policies.

- The second has the ability to bypass Row Level Security, and should be more secure.


## Step 3 - Configure the widgets.json and endpoints

Following our [Readme.md](/README.md) you can now configure the widgets.json and endpoints for your backend.

## Step 4 Run the backend

Run the backend with :

```python
Run `uvicorn main:app --port 5050`
```

## Step 5 - Add to Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.dev/app/data-connectors) with the base url of your API. In this case it is `http://localhost:5050`
