# Public endpoint Example

This utilizes data from https://api.llama.fi/v2/chain without any modification. This could have been added to the Terminal Pro directly using the "Add Single Widget" functionality - but using the widgets.json file we have more control over the widget.

## Step 1 - Configure your widgets.json and endpoints.

You will notice in the [widgets.json](/public_endpoint/widgets.json) we have identified many of the values for the "chartDataType" - this is essential in having it work correctly for charting - you can modify this but generally you want text to be `category` or your index and the actual data to be `series`.

There are many other configurations you can do which are laid out in the main [readme.md file](/README.md)

## Step 2 - Run the backend

One you have your data in the folder you can run the backend with :

```python
Run `uvicorn main:app --port 5050`
```

## Step 3 - Add to Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.dev/app/data-connectors) with the base url of your API. In this case it is `http://localhost:5050`
