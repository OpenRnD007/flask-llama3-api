
# Flask llama3 Rest Backend

This platform offers a sophisticated chat interface that allows you to query and analyze your private documents with utmost discretion.
We are using Meta llama3 for offline LLM and Flask for exposing API  


## Features

- Start a Topic
  - Add Your Docs: Put in docs that are all about the topic you're talking about.
- Have a Chat
  - Ask Anything: You can ask any questions that have to do with the topic.
  - Get Insights: Feel free to ask for a deeper look or some thoughts on the topic.



## Getting Started

### Prerequisites

•  Python 3.6+

•  Good to have GPU machine

•  Libraries required for your LLM


### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/OpenRnD007/flask-llama3-api.git
cd flask-llama3-api
```

Install the required packages:
```bash
chmod +x install_lib
./install_lib
```

### Running the Application
Start the server:

```bash
python run.py
```

The server will start on http://localhost:5000/.

For gitpod

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/OpenRnD007/flask-llama3-api)

## Usage/Examples

To use the API, send a POST request to /api with the required payload:

#### Upload documents (pdf | csv | json)
```bash
curl -X POST http://localhost:5000/api/fileupload -F "file=@FILEPATH" -F "filetype=FILE_TYPE" -F "collection_name=TOPIC_NAME"
```
Make sure to replace `FILEPATH` with `actual filepath`, `FILE_TYPE` with `[pdf | csv | json]` and `TOPIC_NAME` with `name of topic`

#### Ask Question
```bash
curl -X POST http://localhost:5000/api/askquestion -H "Content-Type: application/json" -d '{"question":QUESTION, "collection_name":TOPIC_NAME}'
```
Make sure to replace `QUESTION` with `actual question` and `TOPIC_NAME` with `name of topic`


## License

This project is licensed under the MIT License.


## Authors

- [@openrnd007](https://www.github.com/openrnd007)

