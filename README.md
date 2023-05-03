# openai-multi-client

[![pypi](https://img.shields.io/pypi/v/openai_multi_client)](https://pypi.org/project/openai_multi_client/)

`openai-multi-client` is a Python library that allows you to easily make multiple concurrent requests to the OpenAI API,
either in order or unordered, with built-in retries for failed requests. It keeps your application code synchronous and
easy to understand, without you having to reason about concurrency and deadlocks. This library is particularly useful
when working with the OpenAI API for tasks that require a large number of requests.

### Table of Contents

1. [Motivation](#Motivation)
2. [Features](#Features)
3. [Installation](#Installation)
4. [Usage Example](#Usage-Example)
5. [API Reference](#API-Reference)
6. [Extended Example Adapted from Real-World Use](#Extended-Example-Adapted-from-Real-World-Use)
7. [Contributing](#Contributing)
8. [License](#License)
9. [Authorship Disclosure](#Authorship-Disclosure)

## Motivation

Imagine you're sitting at your desk, eager to run a state-of-the-art language model analysis on your extensive database
of collected articles. You're excited about discovering all the hidden gems and insights your data has to offer.
However, there's one tiny problem – if you send requests to the API in a serial manner, it would take a lifetime to
complete.

This is where the OpenAI Multi-Client comes in. This library was created to help you fully utilize OpenAI's API without
having to wait too long for results. It's designed to manage concurrent API requests so you can focus on analyzing the
insights provided by the language model.

No longer do you have to wait for one request to finish before starting the next. With OpenAI Multi-Client, you can now
send multiple requests simultaneously, while also ensuring that any failed requests will be retried automatically.
Furthermore, the library can be configured to maintain the order of requests and responses.

So, the next time you find yourself with a collection of articles waiting to be analyzed, remember that OpenAI
Multi-Client is here to help. Happy analyzing!

## Features

- Concurrently send multiple requests to the OpenAI API
- Support for ordered and unordered request handling
- Built-in retries for failed requests with customizable retry settings
- Customizable API client for easy testing and mocking
- Simple, easy-to-use interface

## Installation

To install `openai-multi-client`, run:

```bash
pip install openai-multi-client
```

## Usage Example

Here is an example of how to use the `openai-multi-client` library.

```python
from openai_multi_client import OpenAIMultiClient

# Remember to set the OPENAI_API_KEY environment variable to your API key
api = OpenAIMultiClient(endpoint="chats", data_template={"model": "gpt-3.5-turbo"})


def make_requests():
    for num in range(1, 10):
        api.request(data={
            "messages": [{
                "role": "user",
                "content": f"Can you tell me what is {num} * {num}?"
            }]
        }, metadata={'num': num})


api.run_request_function(make_requests)

for result in api:
    num = result.metadata['num']
    response = result.response['choices'][0]['message']['content']
    print(f"{num} * {num}:", response)
```

If you want the answers to be in the same order as the requests are sent, import and use `OpenAIMultiOrderedClient`
instead of `OpenAIMultiClient`.

If you prefer, you can use callback style programming instead of the iterating over the results:

```python
from openai_multi_client import OpenAIMultiClient, Payload

# Remember to set the OPENAI_API_KEY environment variable to your API key
api = OpenAIMultiClient(endpoint="chats", data_template={"model": "gpt-3.5-turbo"})


def on_result(result: Payload):
    num = result.metadata['num']
    response = result.response['choices'][0]['message']['content']
    print(f"{num} * {num}:", response)


def make_requests():
    for num in range(1, 10):
        api.request(data={
            "messages": [{
                "role": "user",
                "content": f"Can you tell me what is {num} * {num}?"
            }]
        }, metadata={'num': num}, callback=on_result)


api.run_request_function(make_requests)
api.pull_all()
```

You can find more complete examples [here](./real_test.py) and [here](./mock_test.py).

## API Reference

In the `OpenAIMultiClient` and `OpenAIMultiOrderedClient` classes, the `endpoint` and `data` parameters correspond to
the endpoints and parameters expected by the official OpenAI API clients.

## Configuring API Keys and Endpoints

Setting up OpenAI Multi-Client is straightforward. Since it utilizes the official OpenAI client under the hood, all you
need to do is import the `openai` library and configure it as you usually would.

To set up your API key, simply import the `openai` module and configure the API key using the following code:

```python
import openai

openai.api_key = "your_api_key_here"
```

Setting the environmental variable `OPENAI_API_KEY` also works as expected.

You can also configure the API endpoint if needed:

```python
openai.api_base = "azure_openai_api_base_here"
```

Once you've configured the `openai` library with your API key and endpoint, OpenAI Multi-Client will automatically use
these settings when sending requests to the API. This makes it easy to integrate OpenAI Multi-Client into your existing
projects without having to worry about separate configurations.

### Endpoints

The `endpoint` parameter in the `request()` method or during the initialization of the classes specifies which OpenAI
API endpoint to use for the requests. The available endpoints are:

- `"completions"`: For text completion requests using the `Completion` endpoint.
- `"chats"` or `"chat.completions"`: For chat completion requests using the `ChatCompletion` endpoint.
- `"embeddings"`: For embedding requests using the `Embedding` endpoint.
- `"edits"`: For edit requests using the `Edit` endpoint.
- `"images"`: For image requests using the `Image` endpoint.
- `"fine-tunes"`: For fine-tuning requests using the `FineTune` endpoint.

### Data

The `data` parameter in the `request()` method specifies the request data sent to the OpenAI API. The data should be a
dictionary containing the required and optional parameters for the specified endpoint. For example:

- For the `"completions"` endpoint, the `data` dictionary may include
  the `model`, `prompt`, `temperature`, `max_tokens`, and other parameters expected by the `Completion` endpoint.
- For the `"chats"` endpoint, the `data` dictionary may include the `model`, `messages`, `temperature`, `max_tokens`,
  and other parameters expected by the `ChatCompletion` endpoint.

When using the `OpenAIMultiClient` or `OpenAIMultiOrderedClient`, make sure to provide the appropriate `endpoint` and
the corresponding `data` as required by the official OpenAI API clients.

For more details, see the [official documentation](https://github.com/openai/openai-python).

### OpenAIMultiClient

`OpenAIMultiClient` is the primary class for making unordered concurrent requests to the OpenAI API.

#### Initialization

You initialize multiple instances of the clients and each will behave independently, with their own queue of requests
and responses. The `OpenAIMultiClient` class can be initialized with the following parameters:

```python
OpenAIMultiClient(
    concurrency=10,
    max_retries=10,
    wait_interval=0,
    retry_multiplier=1,
    retry_max=60,
    endpoint=None,
    data_template=None,
    metadata_template=None,
    custom_api=None)
```

- `concurrency`: (Optional) The number of concurrent requests. Default is 10.
- `max_retries`: (Optional) The maximum number of retries for failed requests. Default is 10.
- `wait_interval`: (Optional) The waiting time between retries. Default is 0.
- `retry_multiplier`: (Optional) The multiplier for the waiting time between retries. Default is 1.
- `retry_max`: (Optional) The maximum waiting time between retries. Default is 60.
- `endpoint`: (Optional) The OpenAI API endpoint to be used, e.g., `"chats"` or `"completions"`.
- `data_template`: (Optional) A template for the data sent with each request. The request data will be merged with this
  template.
- `metadata_template`: (Optional) A template for the metadata associated with each request. The request metadata will be
  merged with this template.
- `custom_api`: (Optional) A custom API function that can be used for testing or mocking the OpenAI API. You can also
  use this to connect to models other than LLMs.

You should set `concurrency` to a sensible value based on your API rate limit. For paid customers using `gpt-3.5-turbo`,
you have 3,500 requests per minute. Let's be generous and assume a request completes in one second. To avoid hitting the
rate limit while maintaining a high throughput, you could set `concurrency` to a value like 50 or 100. Since you are not
charged for failed requests and since exponential backoff is in effect, your requests will eventually complete even if
you set `concurrency` to a high value, but as failed requests take up your rate limit, throughput will be lower.

It is recommended to test your code with a mock API first when you are developing, because using the real API, high
concurrency burns money fast. [This example](./mock_test.py) might be helpful.

You can check your limits [here](https://platform.openai.com/account/rate-limits).

#### Methods

**Important Note**: Calling `request` may block the thread if the input queue is full. It is recommended to put the
requesting logic into a function and call that function using `run_request_function` as done in the example, as it
ensures that the requesting logic runs concurrently without blocking the main thread. The blocking of the input queue is
a **key feature** of this library to ensure that your memory will not be flooded with a petabyte of pending requests
streaming from your database.

- `request(data, endpoint=None, metadata=None, max_retries=None, retry_multiplier=None, retry_max=None)`: Adds a request
  to the queue.
    - `data`: The data (as a dict) to be sent with the request.
    - `endpoint`: (Optional) The API endpoint to be used for this specific request.
    - `metadata`: (Optional) Metadata associated with the request.
    - `callback`: (Optional) A callback function that will be called with the payload object.
    - `max_retries`: (Optional) The maximum number of retries for failed requests. Default is the value set during
      initialization.
    - `retry_multiplier`: (Optional) The multiplier for the waiting time between retries. Default is the value set
      during initialization.
    - `retry_max`: (Optional) The maximum waiting time between retries. Default is the value set during initialization.

- `run_request_function(input_function, *args, stop_at_end=True, **kwargs)`: Executes the input function in a separate
  thread, allowing it to add requests to the queue without blocking.
    - `input_function`: A function that adds requests to the queue using the `request()` method.
    - `*args`: (Optional) Additional arguments passed to the input function.
    - `stop_at_end`: (Optional) Whether to stop the event loop after executing the input function. Default is True.
    - `**kwargs`: (Optional) Additional keyword arguments passed to the input function.

To retrieve results, use the client as an iterator. The following is also available:

- `pull_all()`: Pulls all responses from the queue and discard them. Useful to get the queue started if you are using
  callbacks.

### OpenAIMultiOrderedClient

`OpenAIMultiOrderedClient` is a subclass of `OpenAIMultiClient` for making ordered concurrent requests to the OpenAI
API. The usage is the same as `OpenAIMultiClient`, but the responses will be returned in the order they were added to
the queue.

### Logging

The library uses the standard Python logging module. You can set the logging level
using `logging.basicConfig(level=logging.INFO)` or `logging.basicConfig(level=logging.DEBUG)`.

## Extended Example Adapted from Real-World Use

The scenario in the Motivation section is genuinely real. Although the OpenAI cookbook provides a [recipe](https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py) for making parallel requests, it relies on files for data persistence and can be quite challenging to adapt and use. We were surprised that a library like this didn't exist already, so we decided to create one ourselves.

Here's a brief overview of the system. External and internal articles are continuously streamed from scrapers and other sources into a database. For each article, we let ChatGPT answer a few questions about it, and then we store the text and embeddings of the answers back into the database. The embeddings are indexed for nearest-neighbor search. At peak hours, we expect a high volume of articles, making the use of `OpenAIMultiClient` essential.

We'll be using [CozoDB](https://github.com/cozodb/cozo) to store everything. CozoDB is a transactional hybrid relational-graph-vector database that uses Datalog for queries, which we developed for our work. In the real scenario that this example is based on, article deduplication, full-text search, and recursive, agentic behavior are also integrated using the functionalities provided by the database. However, these details have been omitted in the example for simplicity.

The setup of the database and schema can be found in the code snippet below, where we create tables for articles and embeddings and index the embeddings for nearest-neighbor search:

```python
from pycozo.client import Client

# We use a global variable for the db for simplicity
db = Client('rocksdb', 'analysis.db')  # Using the RocksDB backend for persistence

# Create the schema

# The articles
db.run('''
:create article {
    id: Uuid default rand_uuid_v4() # The key
    =>
    title: String,                  # Title of the article
    text: String,                   # Text of the article
    analysis: Json default {}       # Analyses will be stored in the JSON object
}
''')

# The embeddings are stored separately from the articles
# Not strictly necessary, but cleaner
db.run('''
:create embedding {
    id: Uuid,                 # The key consists of the article ID and the analysis key
    analysis_key: String      # The analysis key
    =>
    embedding: <F32; 1536>    # The embedding of the article
}
''')

# Put the embeddings into an index for nearest-neighbor search
db.run('''
::hnsw create embedding:idx {
    dim: 1536,
    fields: [embedding],
    ef_construction: 200,
    m: 50,
}
''')
```

The streaming service calls a function to insert articles into the database, and the database's ID is auto-generated:

```python
def insert(title, text):
    db.run('''
       ?[title, text] <- [[$title, $text]]

       :put article {=> title, text}
    ''', {'title': title, 'text': text})
```

In another file, we set up the OpenAI multi-client and define the questions we want to ask.

```python
from openai_client import OpenAIMultiClient

# We could use separate clients for embedding and analysis to achieve more concurrency
# But we'll just use a single client for simplicity
client = OpenAIMultiClient()

QUESTIONS = {
    'economic': '''
You are the economics advisor to company X.
Read the article from the user and summarize the potential economic impact for company X implied by the article from your perspective.
Write clearly and concisely, in one paragraph. If there is no economic impact, write "No economic impact."
    ''',

    'political': '''
You are the political advisor to company X.
Read the article from the user and summarize the potential political impact for company X implied by the article from your perspective.
Write clearly and concisely, in one paragraph. If there is no political impact, write "No political impact."
    ''',

    'technological': '''
You are the technology advisor to company X.
Read the article from the user and summarize the potential technological impact for company X implied by the article from your perspective.
Write clearly and concisely, in one paragraph. If there is no technological impact, write "No technological impact."
'''
}
```

The core of the system involves using the client to ask questions and store the results back into the database. When the answers are inserted into the database, we use the client again to get the embeddings and store them in the database as well. We use database callbacks to achieve this:


```python
# Callback function to be called when the database is updated
def insert_callback(op_name, new_rows, old_rows):
    # We only handle puts. Logic for handling deletes omitted for simplicity
    if op_name == 'Put':
        # Make a dict from the old rows replaced by the update
        existing = {
            id: analysis
            for [id, _title, _text, analysis] in old_rows
        }
        # Iterate over the inserted or updated rows
        for id, title, text, analysis in new_rows:
            # If the article already exists, we request embeddings for any newly added analyses
            if id in existing:
                old_analyses = existing[id]
                for key, value in analysis.items():
                    if key not in old_analyses:
                        # Make a request for the embedding
                        # The metadata are used for inserting the results back into the DB
                        client.request(
                            endpoint="embeddings",
                            data={
                                'model': "text-embedding-ada-002",
                                'input': f'{key} impact:\n{value}'
                            },
                            metadata={
                                'type': 'embedding',
                                'id': id,
                                'key': key
                            },
                            callback=on_embedding_result
                        )
            else:
                # Otherwise, we ask for analyses for all questions
                context_text = f'{title}\n\n{text}'

                for key, question in QUESTIONS.items():
                    # Make a request for the analysis
                    client.request(
                        endpoint="chats",
                        data={
                            # You can use GPT-4 if you are rich!
                            "model": "gpt-3.5-turbo",
                            "messages": [{
                                "role": "system", "content": question
                            }, {
                                "role": "user", "content": context_text
                            }]

                        },
                        metadata={
                            'type': 'analysis',
                            'id': id,
                            'key': key
                        },
                        callback=on_analysis_result
                    )


# Register the callback, this will be called whenever an article is inserted or deleted
# As the database already runs callbacks on a separate thread, 
# we don't need to use run_request_function
callback_handle = db.register_callback('article', insert_callback)
```

Callback functions handle the results from the OpenAI client and start the system:

```python
def on_embedding_result(result):
    if result.failed:
        print(f'Failed to get embedding for article {result.metadata["id"]}')
        return

    embedding = result.response['data'][0]['embedding']
    db.run('''
        ?[id, analysis_key, embedding] <- [[$id, $analysis_key, $embedding]]
        :put embedding {id, analysis_key => embedding}
    ''', {
        'id': result.metadata['id'],
        'analysis_key': result.metadata['key'],
        'embedding': embedding
    })


def on_analysis_result(result):
    if result.failed:
        print(f'Failed to get embedding for article {result.metadata["id"]}')
        return

    analysis = {
        result.metadata['key']: result.response['choices'][0]['message']['content']
    }
    
    db.run('''
        ?[id, analysis] := *analysis{id, analysis: old}, analysis = old ++ $analysis
        :update article {id => analysis}
    ''', {
        'id': result.metadata['id'],
        'analysis': analysis
    })
```

Finally, we start the system:

```python
client.pull_all()
```

With this system in place, we can easily access the top news we're interested in by running nearest-neighbor vector searches:


```python
for question in ['Red-alert level innovation from competitors',
                 'Disruption to our supply chain',
                 'Dangers to our overseas personnel in the Middle East']:
    # the `embed` function also uses the OpenAI multi-client, but its definition is omitted.
    embedding = embed(question)
    res = db.run('''
        ?[id, title, text] := ~article:idx{id, title, text | query: $q, k: 3}
    ''', {'q': embedding})
    print(res)
```

As you can see from the example questions, it would be challenging to find relevant news articles in the database without the analysis. But with the analysis, we can get the relevant articles very quickly. This is the power of vector indexing. We can also set up more agents to monitor the analysis and notify the CEO when something important comes up, or even have a community of agents using the database to collaborate. Thanks to the OpenAI multi-client, these agents can move at the speed of thought!

## Contributing

Contributions to `openai-multi-client` are welcome! Feel free to submit a pull request or open an issue on GitHub.

## License

`openai-multi-client` is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authorship Disclosure

GPT-4 wrote most of this README by analyzing code, incorporating the techniques outlined before.