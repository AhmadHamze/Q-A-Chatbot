# Q&A Chatbot

This is a dummy project to learn how to create a chatbot using Python, LLMs, and related technologies.

## Usage

First, create a Python virtual environment:

```bash
python3.12 -m venv env
```
> You can use another Python version, but make sure to change the command accordingly.

Ensure the environment is activated:

```bash
source env/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

After the installation is complete, create a file named `.env`, inside it you have to store your API key like this:

```python
GPT_4o_API_KEY="YOUR_API_KEY"
```

> It is important that you check the naming of the API key with what is in the code. The code won't work if the name is different. 

## Embedding file Chatbot

This is the chatbot that uses the embeddings file to answer questions.

### Obtaining the embeddings file

In order to run the chatbot, you need to have the file `question_embeddings_gpu.npy` in the `data` directory. This file contains the embeddings of the questions in the dataset.

Check `notebooks/chatbot_generate_embeddings.ipynb` to generate this file.

### Running the Chatbot

To run the medical chatbot, run `./run.sh`, this will start a gradio server.

> If you're using Windows, run `python -m src.chatbot.medical_chatbot` instead of `./run.sh`.

Once the gradio server is ready, you can access the chatbot interface by opening the following link in your browser:

```
localhost:7860
```

## Running the Chatbot in Docker

The docker chatbot is different than the local one, it uses Hugging Face api instead of sentence_transformers to generate the embeddings.
The reason behind this is to keep the container size to a minimum.

You can run the container with `docker compose up`, you should see `uvicorn` starting on port 8000.

Once the uvicorn server is ready, you can use curl commands to interact with the API.

```curl
curl -X POST "http://localhost:8000/chat/" -H "Content-Type: application/json" -d "{\"query\":\"During the night, I sometimes wake up on a sever pain in my right calve, it looks like muscle spasm. It sometimes last for minutes causing a lot of pain, what can I do for prevention?\"}"
```
### AWS Secrets Manager

The code is using AWS Secrets Manager to fetch secrets needed to run the application, you should create your own secret on AWS Secret manager and update the code accordingly if needed.

If you want to run the container locally, you have to put the AWS credentials in the `.env` file, like this:

```python
AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY"
AWS_REGION="AWS_REGION"
```

You should also have configured your AWS credentials in your local machine, you can do this by running:

```bash
aws configure
```

These will be used by the `docker-compose.yaml` file to run the container locally.

> As of April 2025, AWS does not recommend using the `aws configure` command to set up your credentials, check AWS for best practices.
