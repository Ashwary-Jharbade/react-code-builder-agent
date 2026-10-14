## Guide to create small context model on top of ollama modal
1. nano qwen3-30B-16K-context

2. File contents

FROM qwen3:30b-a3b-thinking-2507-q4_K_M

PARAMETER num_ctx 16384

3. ollama create qwen3-30b-16k-context -f ./ollamaModelConfig/qwen3-30b-16k-context


## To run project
1. uv run langgraph dev

## To build docker image
docker build -t agent .
docker build --no-cache -t agent .

## To run via docker
docker run --rm -p 8123:8123 agent


## Connect openwiki with local modal
export OPENWIKI_PROVIDER=openai-compatible
export OPENWIKI_MODEL_ID="llama3.2"
export OPENAI_COMPATIBLE_BASE_URL="http://localhost:11434/v1"
export OPENAI_COMPATIBLE_API_KEY="ollama"

Local Skill Call
<img width="1280" height="660" alt="Screenshot 2026-10-14 at 11 57 30 PM" src="https://github.com/user-attachments/assets/ddf789c7-c0d7-4c86-bcac-703be3df278d" />
