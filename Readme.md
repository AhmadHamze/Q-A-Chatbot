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

## Running the backend

To run the backend, run `./run_api.sh`, this will start a uvicorn server.

> If you're using Windows, run `python -m src.api` instead of `./run_api.sh`.

Once the uvicorn server is ready, you can use curl commands to interact with the API.

```curl
curl -X POST "http://localhost:8000/chat/" -H "Content-Type: application/json" -d "{\"query\":\"During the night, I sometimes wake up on a sever pain in my right calve, it looks like muscle spasm. It sometimes last for minutes causing a lot of pain, what can I do for prevention?\"}"
```