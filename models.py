from langchain.chat_models import init_chat_model

model = init_chat_model("ollama:qwen2.5:7b")

# model = init_chat_model("ollama:qwen3-30b-16k-context")