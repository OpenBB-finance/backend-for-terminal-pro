# Backend template for the OpenBB Terminal Pro

Spinning up an OpenBB API is a versatile way to host your data and integrate it into widgets. Whether hosted internally or externally, this method provides a standardized API structure that Pro widgets can effortlessly connect to. While this repository is an example using Python FastAPI - this same structure can be used to achieve any language-agnostic approach.

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
	}...
]
```

2. Ensure that you have a well-structured ```widgets.json``` file. This file defines widget properties such as name, description, category, type, endpoint, and other information needed. Each widget needs to be defined in this file – You can find the format in any of the templates folder with a detailed definition below.

3. API - If hosting locally you must enable CORS and have an endpoint available that will return the ```widgets.json``` file.


## Supported Integrations

| Integration | Description | Supported |
| ----------- | ----------- | --------- |
| Elastic | Elasticsearch is a search engine based on the Lucene library. | ✅ |
| Clickhouse | ClickHouse is an open-source column-oriented DBMS. | ✅ |
| MindsDB | MindsDB is an open-source AI layer for existing databases. | ✅ |
| Snowflake | Snowflake is a cloud-based data warehousing platform. | ✅ |
| Readfile | This integration allows reading data directly from a file. | ✅ |
| Public | This integration allows fetching data from public APIs. | ✅ |
| Plotly | Plotly is a Python graphing library for interactive graphs. | ✅ |

## Templates available

Each folder contains an example of a different implementation, the goal is to increase the amount of different use cases so that each customer can start from the one that is most relevant.


* [Public endpoint](/public_endpoint/README.md)
* [Plotly from public endpoint](/plotly_example/README.md)
* [Read file example](/readfile_example/README.md)
* [Snowflake example](/snowflake_example/README.md)


## How to run

1. Go into the folder you want to test
2. Run `uvicorn main:app --port 5050`

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

This file is a dictionary, and each dictionary within represents a widget.

Each widget will have the following properties:

# Widget Type Definition

widgets.json definitions

All of the values available are here

```jsonc
{
  // Basic props
  "id": "string", // Unique identifier for the widget.
  "innerTab": "string", // If it's from a template, it may have a tab assigned, e.g., equity template.
  "gridData": {
    // Grid data configuration for the widget.
    "x": 0, // Horizontal grid position.
    "y": 0, // Vertical grid position.
    "w": 0, // Width for the widget in the grid.
    "h": 0, // Height for the widget in the grid.
    "minH": 0, // Minimum height.
    "minW": 0, // Minimum width.
    "maxH": 0, // Maximum height.
    "maxW": 0, // Maximum width.
    "moved": true, // Indicates if the widget has been moved.
    "static": false, // Indicates if the widget is static and cannot be moved.
    "isDraggable": true // Specifies if the widget can be dragged.
  },
  "storage": {
    // Storage for the widget that doesn't fit in the other fields.
    "key": "value"
  },
  "aiHistory": [
    {
      // AI history for the widget.
      "question": "string", // Question for the AI.
      "answer": "string", // Answer from the AI.
      "ticker": "string" // Ticker at the time of the question.
    }
  ],
  "schema": {
    // Schema for the widget.
    "properties": {
      // Properties for the schema.
      "key": {
        "type": "string", // Type of property (object, array, string, number, boolean).
        "title": "string", // Title for the property.
        "description": "string", // Description for the property.
        "default": "value", // Default value for the property.
        "choices": ["option1", "option2"], // Choices for the property.
        "format": "string", // Format for the property (url, email, date, date-time, time, color).
        "mandatory": true, // Indicates if the property is mandatory.
        "specifics": {
          "min": 0, // Minimum value for the property.
          "max": 100 // Maximum value for the property.
        }
      }
    }
  },
  "external": false, // Indicates if the widget is external, i.e., if data is loaded from outside OpenBB API.
  "name": "string", // Name of the widget in the list the user sees. Displayed on top left of widget.
  "type": "string", // Main widget type (chart, table, note, custom).
  "description": "string", // Description to show to the user on the info button and on the search/add widget menu.
  "widgetId": "string", // Identifier for the specific widget instance. Used to map with openbb ui widgets.
  "data": {
    // Data configuration for the widget.
    "schemaData": {
      // Schema data for the widget.
      "key": "value"
    },
    "gridChart": {
      // Configuration for having a chart detached from aggrid table.
      "chartModel": "string", // The model of the aggrid chart.
      "fromTableId": "string" // Identifier for the source table of the chart data.
    },
    "values": [
      {
        // Array of x and y coordinate values.
        "x": 0,
        "y": 0
      }
    ],
    "mainTicker": {
      // Main ticker information. Displayed on top left after the widget name. Normally can be changed on this dropdown.
      "tickerProperty": "value"
    },
    "securities": ["security1", "security2"], // Array of security types.
    "secondaryTickers": ["ticker1", "ticker2"], // Array of secondary tickers.
    "hideControls": true, // Indicates if controls should be hidden.
    "color": "color", // Color configuration for the widget (used in Notes to store the color of the note).
    "html": "string", // HTML content to be displayed (used in Notes to save the note content).
    "dataKey": "string", // Key for the data.
    "table": {
      // Configuration for table columns.
      "columnState": {
        "key": "value"
      },
      "mode": "string", // Display mode for the table (light, dark).
      "density": "string", // Density mode for the table (compact, default).
      "transpose": true, // Indicates if the table should be transposed.
      "period": ["period1", "period2"], // Period information for the table.
      "showAll": true, // Indicates if all data should be shown.
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
          "maxWidth": 0, // Maximum width of the column.
          "minWidth": 0, // Minimum width of the column.
          "hide": true, // Indicates if the column should be hidden.
          "rowGroup": true // Indicates if the column is a row group column.
        }
      ]
    },
    "chart": {
      // Chart instance that hits a callback for the JSON data.
      "callback": "string" // Callback function for the chart.
    }
  },
  "endpoint": "string", // Endpoint or endpoints for the widget data.
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
  },
  "options": {
    // Widget options.
    "size": "string", // Size configuration for the widget (normal, maximize).
    "chartType": "string", // Type of chart to display (line, candlestick, bar).
    "allowTickerChange": true, // Indicates if ticker change is allowed.
    "allowSecondaryTickersChange": true, // Indicates if secondary ticker change is allowed.
    "allowChartTypeChange": true, // Indicates if chart type change is allowed.
    "allowTimeframeChange": true, // Indicates if timeframe change is allowed.
    "allowRaw": true, // Indicates if raw data is allowed.
    "allowSettingsChange": true // Indicates if settings change is allowed.
  },
  "groupId": "string" // Identifier for a widget group.
}
```


## Have an existing API and want to turn it into an OpenBB backend?

Highlight here what they need to do - it is really the same - just think we should have this be an item

just add a widgets.json - and point it toward your endpoints

add the endpoint to hit widgets.json
