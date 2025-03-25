# Q&A Chatbot

This is a dummy project to learn how to create a chatbot using Python, LLMs, and related technologies.

## Usage

First, create a Python virtual environment:

```bash
python3.12 -m venv env
```
Make sure it it activated:

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

## Chatbot

## Obtaining the embeddings file

In order to run the chatbot, you need to have the file `question_embeddings_gpu.npy` in the `data` directory. This file contains the embeddings of the questions in the dataset.

Check `notebooks/chatbot_generate_embeddings.ipynb` to generate this file.

## Running the Chatbot

To run the code, you can use the following command from root directory:

```bash
python3.12 -m src.chatbot.medical_chatbot
```

Once the gradio server is ready, you can access the chatbot interface by opening the following link in your browser:

```
localhost:7860
```