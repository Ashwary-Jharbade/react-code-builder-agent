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