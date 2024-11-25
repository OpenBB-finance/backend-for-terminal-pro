# Full example

This utilizes data from <https://api.llama.fi/v2/chain> and other sources to render the data as a chart or table widget inside an OpenBB dashboard.

For more examples on what you can pass and setting up your own backend - you can head to our documentation at <https://docs.openbb.co/pro>.

This example also includes a widget that calls an endpoint to fetch a list of values and then renders it as a dropdown.

## Step 1 - Configure your main.py

In [main.py](/full_example/main.py) configure your FastAPI instance to have an endpoint returning json for each widget you want to render.

## Step 2 - Configure your widgets.json and endpoints

You will notice in the [widgets.json](/full_example/widgets.json) we have identified the data for one endpoint as chart for the plotly render - we will render the plotly object based on what is exported.

In addition to the chart type, you can also add the other widgets that are available in the widgets.json file.

There are many other configurations you can do which are laid out in the main [readme.md file](/README.md)

## Step 3 - Run the backend

One you have your data in the folder you can run the backend with :

```python
pip install -r requirements.txt
```

```python
Run `uvicorn main:app --port 5050`
```

## Step 3 - Add to Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.co/app/data-connectors) with the base url of your API. In this case it is `http://localhost:5050`
