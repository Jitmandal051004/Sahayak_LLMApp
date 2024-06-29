# Krishi Sahayak

Kishan Sahayak is an innovative AI app designed to empower the agriculture industry by providing insightful answers to farmers' questions about improving their agricultural practices and protecting their crops. Leveraging JSON lines of data on soil, fertilizers, and crops, and integrating real-time weather and soil data through APIs, the app offers tailored and precise advice to enhance productivity and sustainability.

This app uses various jsonl data on different soil, temperature, yeild, crop, fertilizer, nutrient which has been took from Kaggle dataset

## Features

- Real-time Weather and Soil Data: Integrates live data through APIs to provide current and location-specific recommendations.
- Offers user-friendly UI with [Streamlit](https://streamlit.io/).
- AI-Driven Insights: Uses Pathway’s LLM App features to build a real-time LLM-enabled data pipeline in Python, joining data from multiple sources.
- Data and code reusability for offline evaluation. User has the option to choose to use local (cached) or real data.
- Diverse Agricultural Data: Utilizes various JSON lines of data on different soil types, temperature, yield, crops, fertilizers, and nutrients sourced from Kaggle datasets.
- High-Quality Input through APIs: Allows for the integration of high-quality and various types of input data through APIs, enhancing the app's flexibility and accuracy and tailored to user need.

## Further Improvements

There are more things you can achieve and here are upcoming features:

- Incorporate image based soil recognizition using satellite imagery from open weather api and classified dataset in kaggle
- Merge data from these sources instantly.
- Convert any data to jsonlines.
- Maintain a data snapshot to observe variations in soils-quality and yeild over time, as Pathway provides a built-in feature to compute **differences** between two alterations.
- We can also use web-scrapper to feed data on fertilizer in market and fetch their price and availabilty.
- Beyond making data accessible via API or UI, the LLM App allows you to relay processed data to other downstream connectors, such as BI and analytics tools. For instance, set it up to **receive alerts** upon detecting price shifts.

## Demo

As we are using location based weather and soil api it could deliver tailored results to users:

```text

```

You will get the response:

<!-- ![LLM App responds with discounts from Amazon](/assets/LLM%20App%20v1.gif) -->

As evident, ChatGPT interface offers general advice on agriculture but lacks specificity regarding the current location of the user and the soil type of that area, among other details:

<!-- ![ChatGPT needs custom data](/assets/ChatGPT%20Discounts%20V1.gif) -->


## How the project works

The sample project does the following procedures to achieve the above output:

1. Prepare search data:
    1. Generate: [discounts-data-generator.py](/examples/csv/discounts-data-generator.py) simulates real-time data coming from external data sources and generates/updates existing `discounts.csv` file with random data. There is also cron job is running using [Crontab](https://pypi.org/project/python-crontab/) and it runs every min to fetch latest data from Rainforest API.
    2. Collect: You choose a data source or upload the CSV file through the UI file-uploader and it maps each row into a jsonline schema for better managing large data sets.
    3. Chunk: Documents are split into short, mostly self-contained sections to be embedded.
    4. Embed: Each section is [embedded](https://platform.openai.com/docs/guides/embeddings) with the OpenAI API and retrieve the embedded result.
    5. Indexing: Constructs an index on the generated embeddings.
2. Search (once per query)
    1. Given a user question, generate an embedding for the query from the OpenAI API.
    2. Using the embeddings, retrieve the vector index by relevance to the query
3. Ask (once per query)
    1. Insert the question and the most relevant sections into a message to GPT
    2. Return GPT's answer

## How to run the project

Example only supports Unix-like systems (such as Linux, macOS, BSD). If you are a Windows user, we highly recommend leveraging Windows Subsystem for Linux (WSL) or Dockerize the app to run as a container.

### Run with Docker

1. [Set environment variables](#step-2-set-environment-variables)
2. From the project root folder, open your terminal and run `docker compose up`.
3. Navigate to `localhost:8501` on your browser when docker installion is successful.

### Prerequisites

1. Make sure that [Python](https://www.python.org/downloads/) 3.10 or above installed on your machine.
2. Download and Install [Pip](https://pip.pypa.io/en/stable/installation/) to manage project packages.
3. Create an [OpenAI](https://openai.com/) account and generate a new API Key: To access the OpenAI API, you will need to create an API Key. You can do this by logging into the [OpenAI website](https://openai.com/product) and navigating to the API Key management page.
4. (Optional): if you use Rainforest API as a data source, create an [Rainforest](https://www.rainforestapi.com/) account and get a new API Key. Refer to Rainforest API [documentation](https://www.rainforestapi.com/docs).

Then, follow the easy steps to install and get started using the sample app.

### Step 1: Clone the repository

This is done with the `git clone` command followed by the URL of the repository:

```bash
git clone https://github.com/Jitmandal051004/Sahayak_LLMApp
```

Next,  navigate to the project folder:

```bash
cd Sahayak_LLMApp
```

### Step 2: Set environment variables

Create `.env` file in the root directory of the project, copy and paste the below config, and replace the `{OPENAI_API_KEY}` configuration value with your key. 

```bash
OPENAI_API_TOKEN=<YOUR_API_KEY>
HOST=0.0.0.0
PORT=8080
EMBEDDER_LOCATOR=text-embedding-ada-002
EMBEDDING_DIMENSION=1536
MODEL_LOCATOR=gpt-3.5-turbo
MAX_TOKENS=200
TEMPERATURE=0.0

GEOCODE_API_KEY=<YOUR_API_KEY>
WEATHER_API_KEY=<YOUR_API_KEY> 
```
You can https://rest.isric.org/soilgrids/v2.0/docs#/default/query_layer_properties_properties_query_get to generate your geocode api key

### Step 3: Install the app dependencies

Install the required packages:

```bash
pip install --upgrade -r requirements.txt
```
### Step 4 (Optional): Create a new virtual environment

Create a new virtual environment in the same folder and activate that environment:

```bash
python -m venv pw-env && source pw-env/bin/activate
```

### Step 5: Run and start to use it

You start the application by navigating to `llm_app` folder and running `main.py`:

```bash
python main.py
```

When the application runs successfully, you should see output something like this:

![pathway_progress_dashboard](/assets/pathway_progress_dashboard.png)

### Step 6: Run Streamlit UI for file upload

You can run the UI separately by navigating to `cd examples/ui` and running Streamlit app
`streamlit run app.py` command. It connects to the Discounts backend API automatically and you will see the UI frontend is running http://localhost:8501/ on a browser:

![screenshot_ui_streamlit](/assets/streamlit_ui_pathway.png)

## Test the sample app

Assume that you choose CSV as a data source and we have this entry on the CSV file (this can be any CSV file where the first row has column names separated by commas):

| discount_until | country | city | state | postal_code | region | product_id | category | sub_category | brand | product_name | currency | actual_price | discount_price | discount_percentage | address |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-08-09 | USA | Los Angeles | IL | 22658 | Central | 7849 | Footwear | Men Shoes | Nike | Formal Shoes | USD | 130.67 | 117.60 | 10 | 321 Oak St |

When the user uploads this file to the file uploader and asks questions:

```text
Can you find me discounts this month for Nikes men shoes?
```

You will get the response as its expected on the UI.

```text
"Based on the given data, there is one discount available this month for Nike's men shoes. Here are the details::

Discounts this week for Nike's men shoes:

City: Los Angeles
Ship Mode: Second Class
Postal Code: 22658
Category: Footwear
Sub-category: Men Shoes
Brand: Nike
Product Name: Formal Shoes
Formal Shoes
Actual Price: $130.67
Discounted Price: $117.60
Discount Percentage: 10%
Ship Date: 2024-08-09
```
