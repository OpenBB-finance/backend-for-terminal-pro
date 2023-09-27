# Backend template for the OpenBB Terminal Pro

Backend template to bring your own data into the OpenBB Terminal Pro using FastAPI.

## Templates available

Each folder contains an example of a different implementation, the goal is to increase the amount of different use cases so that each customer can start from the one that is most relevant.

#### public_endpoint

This utilizes data from https://api.llama.fi/v2/chain without any modification. This could have been added to the Terminal Pro directly using the "Add Single Widget" functionality - but using the widgets.json file we have more control over the widget.

TBD: Add image of widget to be added.

#### endpoint with API key

tbd

#### process csv file

tbd

#### process json file

tbd

#### python code

tbd


## How to run

1. Go into the folder you want to test
2. Run `uvicorn main:app --port 5050`

(add image of what it looks in console)

3. Add steps for Data Connectors in the Terminal Pro

(add steps according to Terminal Pro)

## Code explained

### main.py

This is responsible by running the FastAPI with endpoints that will be consumed by the Terminal Pro.

This file:

* Enables cross-origin resource sharing (CORS) and configures it according to the domain where FastAPI is running and Terminal Pro link.

* Initializes FastAPI with `app = FastAPI()`

* Ensures that there's a `/widgets.json` file that the OpenBB Terminal Pro can use to configure the widgets configured

```python
@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    file_path = "widgets.json"
    with open(file_path, "r") as file:
        data = json.load(file)
    return JSONResponse(content=data)
```

* Creates remaining endpoints that retrieve data that will be consumed by the Terminal Pro

### widgets.json

This contains the settings for all the widgets that the backend contains.

This file is a dictionary, and each dictionary within represents a widget.

Each widget will have the following properties:

* **name**: The name of the widget

* **description**: The description of the widget for the search

* **category**: The category associated with the widget

* **searchCategory**: Is this necessary? How does it differ from previous?

* **widgetType**: Unsure what this means - Andrew

* **widgetId**: We should not allow user to control this to avoid clashes internally. We should take their name and add a uuid after or so.

* **endpoint**: This is what is the endpoint from the base url provided to FastAPI where the widget data can be found

* **gridData**: This contains 2 settings therein:

    - **w**: Width of widget

    - **h**: Height of widget

* **data**: Is there another option than table? Do we want to allow charts by default or so?

    - **table**: Contains the following settings

        - **index**: Column name to be the table index

        - **showAll**: `true` if all columns are displayed

        - **columnDefs**: Allows to control each widget column. This contains a list of dictionaries for each column that we are intered in displaying. Examples of properties that can be selected:

            -  **headerName**: Name of the column to be displayed

            - **field**: Actual name of the field according to data

            - **chartDataType** (optional): If we set `category` that allows users to chart from raw data and use those labels.
