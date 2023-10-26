# Read File Example


## Step 1 - Review your JSON or CSV data for consistency.

Check the mock data we have provided for example formats in both CSV and JSON. You can adapt them more but the examples work for these formats.

## Step 2 - Configure your widgets.json and endpoints.

You will notice in the [widgets.json](/readfile_example/widgets.json) we have identified many of the values for the "chartDataType" - this is essential in having it work correctly for charting - you can modify this but generally you want text to be `category` or your index and the actual data to be `series`.

There are many other configurations you can do which are laid out in the main [readme.md file](/README.md)

## Step 3 - Run the backend

One you have your data in the folder you can run the backend with :

```python
Run `uvicorn main:app --port 5050`
```

## Step 4 - Add to Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.dev/app/data-connectors) with the base url of your API. In this case it is `http://localhost:5050`
