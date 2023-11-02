# Plotly example

This utilizes data from https://api.llama.fi/v2/chain and renders the data as a barchart directly instead of a table.


## Step 1 - Configure your widgets.json and endpoints.

In [main.py](/plotly_example/widgets.json) configure your Plotly object and export it as `figure.to_json()` like shown in the example. In our case we are creating a bar chart.

## Step 2 - Configure your widgets.json and endpoints.

You will notice in the [widgets.json](/plotly_example/widgets.json) we have identified the data as chart instead of table as we did in other examples and set our chart type as bar to match the plotly export - You can set the type to whatever you are exporting - we will render the plotly object based on what is exported.

There are many other configurations you can do which are laid out in the main [readme.md file](/README.md)

## Step 3 - Run the backend

One you have your data in the folder you can run the backend with :

```python
Run `uvicorn main:app --port 5050`
```

## Step 3 - Add to Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.dev/app/data-connectors) with the base url of your API. In this case it is `http://localhost:5050`
