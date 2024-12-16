# Backend examples for OpenBB Pro

## Introduction

An OpenBB Pro Custom Backend is a versatile way to connect your data to widgets inside OpenBB Pro. Whether hosted internally or externally, this method provides a standardized structure that OpenBB Pro widgets can read and then display any data.

Note: Most of the examples provided use Python FastAPI due to our familiarity with the library, but the same could be done utilizing different languages.

The Main tenants are:

1. **Data returned should be in JSON format** (Note : you can utilize the "dataKey" variable in the widgets.json if you have nested JSON.)

<details>
    <summary>Example JSON</summary>

    ```json
    [
      {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "price": 150.5,
        "marketCap": 2500000000,
        "change": 1.25
      },
      {
        "ticker": "GOOGL",
        "name": "Alphabet Inc.",
        "price": 2800.75,
        "marketCap": 1900000000,
        "change": -0.75
      },
      {
        "ticker": "MSFT",
        "name": "Microsoft Corporation",
        "price": 300.25,
        "marketCap": 220000000,
        "change": 0.98
      },
    ]
    ```

</details>

2. **An endpoint returning a ```widgets.json``` file** : This file defines widget properties such as name, description, category, type, endpoint, and other information. Each widget will be defined in this file – You can find the format in any of the templates folder with a detailed definition below.

3. **CORS Enabled** : If hosting locally you must enable [CORS](https://fastapi.tiangolo.com/tutorial/cors/).

4. **Adding Authentication (optional)** : If your backend requires authentication we offer the ability to set a query param or header when you connect to it through OpenBB Pro. These values are sent on every request when configured. If you require another method - please reach out to us.

## Supported Integrations and Templates

Each Integration below has a folder which contains an example of different implementations - We recommend starting with the Table Widget Example.

| Integration | Description |
| ----------- | ----------- |
| [Table Widget](/widget_examples/table_widget) | A good example of widgets with a table returned and tables with parameters |
| [Chart Widget](/widget_examples/chart_widget) | A good example of widgets with a graph returned and tables with parameters |
| [Markdown Widget](/widget_examples/markdown_widget) | A good example of widgets with a markdown returned and tables with parameters |
| [Metric Widget](/widget_examples/metric_widget) | A good example of widgets with a metric returned and tables with parameters |

| Advanced Examples | Description |
| [Parameters Widget](/advanced_examples/parameters_example) | A good example of widgets with parameters |
| [Grouping Widgets](/advanced_examples/grouping_widgets) | A good example of widgets with grouped widgets |
| [Column and Cell Rendering](/advanced_examples/column_and_cell_rendering) | A good example of widgets with custom column and cell rendering |

| Database Connection Examples | Description |
| [ClickHouse](/database_examples/clickhouse_python/README.md) | ClickHouse is an open-source column-oriented DBMS. |
| [Supabase](/database_examples/supabase_python/README.md) | Supabase is an open source Firebase alternative. |
| [MindsDB](/database_examples/mindsdb_python/README.md) | MindsDB is an open-source AI layer for existing databases. |
| [ElasticSearch](/database_examples/elasticsearch_python/README.md) | Elasticsearch is a search engine based on the Lucene library. |
| [ArticDB](/database_examples/articdb_python/README.md) | Using ArticDB to add data to a widget. |
| [Snowflake](/database_examples/snowflake_connector_python/README.md) | Snowflake is a cloud-based data warehousing platform. |


## Getting Started

1. Go into the folder you want to run (we recommend the "Full Example") and read the `README.md` file with instructions.

2. Run `pip install -r requirements.txt`

3. Run `uvicorn main:app --port 5050` to start your backend.

4. Create a Custom Backend on OpenBB Pro with the link to your API URL (e.g., <http://localhost:5050>).

## Code explained

### main.py

This file is responsible for running the FastAPI with endpoints that will be consumed by OpenBB Pro.

* Enables cross-origin resource sharing (CORS) and configures it according to the domain where FastAPI is running and the Pro link.

* Initializes FastAPI with `app = FastAPI()`

* Ensures that there's a `/widgets.json` file that OpenBB Pro can use to configure the widgets configured

  <details>
      <summary>Endpoint to fetch widgets.json file</summary>

  ```python
  @app.get("/widgets.json")
  def get_widgets():
      """Widgets configuration file for OpenBB Pro"""
      file_path = "widgets.json"
      with open(file_path, "r") as file:
          data = json.load(file)
      return JSONResponse(content=data)
  ```

  </details>

* Creates remaining endpoints that retrieve data that will be consumed by OpenBB Pro

### widgets.json

This file contains the settings for all the widgets that the backend contains. Each dictionary within represents a widget with different configurations.

You must ensure that in your `widgets.json` you pass the three required fields - everything else is optional but allows for more configuration.

Also note that the key must be unique.

  <details>
      <summary>Example widgets.json file</summary>

```jsonc
{
  "financial_data": { // must be unique in your widgets.json
    "name": "Financial data", // required - Name of the Widget
    "description": "Financial data from the backend", // required - Description of the Widget
    "endpoint": "financial_data", // required - What endpoint to hit from the main.py file
  }
}
```

For more examples on what you can pass and setting up your own backend - you can head to our documentation at <https://docs.openbb.co/pro>.

## Additional Configurations / Troubleshooting

### HTTPS

Some browsers (Safari) or applications (Excel on Mac) require HTTPS to be enabled to fetch data from an API.

To enable HTTPS in your local environment, follow these steps:

1. Install [mkcert](https://github.com/FiloSottile/mkcert).
2. cd into the backend you will be using, e.g. `cd snowflake_python`.
3. Run `mkcert localhost 127.0.0.1 ::1`. This will create `localhost+2.pem` and `localhost+2-key.pem` files in the current directory.
4. Run `uvicorn main:app --port 5050 --ssl-keyfile=localhost+2-key.pem --ssl-certfile=localhost+2.pem --reload` to start the server with HTTPS enabled.
