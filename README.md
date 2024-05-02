# Backend examples for the OpenBB Terminal Pro

## Introduction

Spinning up an OpenBB API is a versatile way to host your data and integrate it into widgets. Whether hosted internally or externally, this method provides a standardized API structure that Pro widgets can effortlessly connect to.

Note: Most of the examples provided use Python FastAPI due to our familiarity with the library, but the same could be done utilizing different languages.

The Main tenants are:

1. Data returned should be in JSON non-nested format.

Example :

```json
[
 {
  "color": "red",
  "value": "#f00"
 },
 {
  "color": "green",
  "value": "#0f0"
 }
]
```

2. Ensure that you have a well-structured ```widgets.json``` file. This file defines widget properties such as name, description, category, type, endpoint, and other information needed. Each widget needs to be defined in this file – You can find the format in any of the templates folder with a detailed definition below.

3. API - If hosting locally you must enable CORS and have an endpoint available that will return the ```widgets.json``` file.

## Supported Integrations and Templates

Each Integration below has its folder which contains an example of a different implementation.

| Integration | Description |
| ----------- | ----------- |
| [Snowflake](/snowflake_python/README.md) | Snowflake is a cloud-based data warehousing platform. (Deprecated : Use Native Integration) |
| [ClickHouse](/clickhouse_python/README.md) | ClickHouse is an open-source column-oriented DBMS. |
| [Supabase](/supabase_python/README.md) | Supabase is an open source Firebase alternative. |
| [MindsDB](/mindsdb_python/README.md) | MindsDB is an open-source AI layer for existing databases. |
| [ElasticSearch](/elasticsearch_python/README.md) | Elasticsearch is a search engine based on the Lucene library. |
| [Readfile](/readfile_example/README.md) | This integration allows reading data directly from a file. |
| [Public](/public_endpoint/README.md) | This integration allows fetching data from public APIs. |
| [Plotly](/plotly_example/README.md) | Plotly is a Python graphing library for interactive graphs. |

## Getting Started

1. Go into the folder you want to test

2. Read the README.md file with instructions

3. Run `uvicorn main:app --port 5050`

(add an image of what it looks like in the console)

3. Add steps for Data Connectors in the Terminal Pro

(add steps according to Terminal Pro)

## Code explained

### main.py

This is responsible for running the FastAPI with endpoints that will be consumed by the Terminal Pro.

This file:

* Enables cross-origin resource sharing (CORS) and configures it according to the domain where FastAPI is running and the Terminal Pro link.

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

This file is a dictionary, and each dictionary within represents a widget with different configurations that can be passed.

You must ensure that in your `widget.json` you pass the three required fields - everything else is optional but allows for more configuration.

Also note that the key must be unique.

```jsonc
{
  "financial_data_from_supabase": { // must be unique in your widgets.json
    "name": "Financial data supabase", // required
    "description": "Financial data from supabase", // required
    "endpoint": "financial_data_from_supabase", // required
    "category": "economy", // optional
    "searchCategory": "economy", // optional
    "gridData": { // optional
      "w": 20,
      "h": 5
    }
  }
}
```

### Passing Params (Table Only)

To pass params in the widget you can check out he example below :

You can see we set our endpoint to take the symbol param and then handle it to pass to the API (In our example we hit
a unique endpoint but the url request ultimately looks like this against our api `/get_options?symbol=AMZN` )

In our main.py :

```python
@app.get("/get_options")
def get_options(symbol: str):
    """Get options data"""

    response = requests.get(f'https://test.com/options/flow/{symbol}')

    if response.status_code == 200:
        data = response.json()
        return data
```

And in our widgets.json :

```jsonc
{
  "get_options": {
    "name": "Options Data",
    "description": "Options Data from Source",
    "category": "options",
    "searchCategory": "options",
    "widgetType": "options",
    "params": { "symbol": "", "optional": { "interval": [1, 2, 3, 4, 5] } }, //interval isn't needed here just showing other ways to pass more params
    // another example is "params": { "symbol": "", "date": "string" }, - which gives you a date picker to send
    // note - symbol and date are passed outside of optional
    "endpoint": "get_options",
    "gridData": {
      "w": 20,
      "h": 5
    },
    "data": {
      "table": {
        "showAll": true, // show all data from the resp in a table
        "index": "symbol" // name of the field for the index
      }
    }
  }
}

This then allows us to use the pass the ticker to the endpoint along with any other optional params you need.

```

Each widget will have the following properties:

```jsonc
{
  // required properties
  "name": "string", // Name of the widget in the list the user sees. Displayed on top left of widget.
  "description": "string", // Description to show to the user on the info button and on the search/add widget menu.
  "endpoint": "string", // Endpoint for the widget data.
  // optional properties
  "category": "string", // Category to show the widget under the widget search. If you pass a category we don't have it will make one. Default : My Widgets
  "sub_category": "string", // Sub category to show in the widget search. Default : None
  "source": ["source"], // sources for the advanced widget - you can pass multiple here
  "gridData": {
    // Grid data configuration for the widget. How large you want the widget to be on initial render
    "x": 0, // Horizontal grid position.
    "y": 0, // Vertical grid position.
    "w": 0, // Width for the widget in the grid.
    "h": 0, // Height for the widget in the grid.
    "minH": 0, // Minimum height.
    "minW": 0, // Minimum width.
    "maxH": 0, // Maximum height.
    "maxW": 0, // Maximum width.
    "static": false, // Indicates if the widget is static and cannot be moved. Default : false
    "isDraggable": true // Specifies if the widget can be dragged. Default : true
  },
  "storage": {
    // Storage for the widget that doesn't fit in the other fields.
    "key": "value"
  },
  "defaultViz" : "table", // Default visualization for the widget. Can be one of table or chart (default : table)
  "type": "string", // Main widget type (chart, table, note, custom).
  "widgetId": "string", // Identifier for the specific widget instance. Used to map with openbb ui widgets.
  "data": {
    "dataKey": "string", // Key for the data.
    "table": {
      // Configurations for the Table
      "enableCharts": true, // Allow charting to work from the widget table (default: true)
      "showAll": true, // Indicates if all data should be shown.
      "transpose": true, // Indicates if the table should be transposed.
      "columnsDefs": [
        {
          // Configuration for table columns.
          "field": "string", // Field name from the JSON data.
          "headerName": "string", // Header name for the column.
          "chartDataType": "string", // Chart data type (category, series, time, excluded).
          "cellDataType": "string", // Cell data type (text, number, boolean, date, dateString, object).
          "formatterFn": "string", // Formatter function (int, bigInt, etc.).
          "renderFn": "string", // Render function (green, red, titleCase, etc.).
          "width": 0, // Width of the column.
          "hide": true, // Indicates if the column should be hidden.
        }
      ],
      "mode": "string", // Display mode for the table (light, dark).
      "density": "string", // Density mode for the table (compact, default).
    },
    "chart": {
      // Chart instance that hits a callback for the JSON data.
      "callback": "string" // Callback function for the chart.
    }
  },
  "endpointMethod": "GET", // Endpoint method (GET, POST).
  "endpointHeaders": [
    {
      // Endpoint headers.
      "key": "string",
      "value": "string"
    }
  ],
  "params": {
    // URL params to send to the endpoint (e.g., callback endpoint in "analyst_upgrades_downgrades").
    "key": "value"
  }
}
```
