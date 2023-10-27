# ElasticSearch example

## Step 1 - Install Dependencies

Start by running: `pip install elasticsearch` - This will install the [official ElasticSearch connector for python](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html).


## Step 2 - Add ElasticSearch Account info

You will need to identify the following from your ElasticSearch account

```python
client = Elasticsearch(
  "",
  api_key=""
)
```

Your Elasticsearch endpoint can be found on the "My deployment" page of your deployment. It will be under Applications, in front of "Elasticsearch" and you can click on "Copy endpoint" directly.

For the API key, you can generate it on the "Management" page under Security.

## Step 3 - Configure the widgets.json and endpoints

Following our [Readme.md](/README.md) you can now configure the widgets.json and endpoints for your backend.

## Step 4 Run the backend

Run the backend with :

```python
Run `uvicorn main:app --port 5050`
```

## Step 5 - Add to Pro

Now you can add the backend to the [data connectors page](https://pro.openbb.dev/app/data-connectors) with the base url of your API. In this case it is `http://localhost:5050`
