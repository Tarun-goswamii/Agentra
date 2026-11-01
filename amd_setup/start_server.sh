#!/bin/bash
# =============================================================================
# start_server.sh — Launch vLLM OpenAI-compatible API server on AMD GPU
# =============================================================================

set -e

# ── Config (edit as needed) ───────────────────────────────────────────────────
MODEL="${AMD_MODEL:-mistralai/Mistral-7B-Instruct-v0.3}"
HOST="0.0.0.0"
PORT="${AMD_PORT:-8000}"
MAX_LEN="${MAX_MODEL_LEN:-4096}"
DTYPE="float16"       # Use float16 for MI200 series; bfloat16 for MI300
PARALLEL="${TENSOR_PARALLEL:-1}"  # Increase if you have multiple GPUs

echo "============================================="
echo "  AMD vLLM API Server"
echo "  Model   : $MODEL"
echo "  Host    : $HOST:$PORT"
echo "  Max len : $MAX_LEN tokens"
echo "============================================="

# Activate venv if it exists
if [ -d "$HOME/vllm-env" ]; then
    source "$HOME/vllm-env/bin/activate"
fi

# Show GPU status
echo ""
echo "GPU Status:"
rocm-smi --showmeminfo vram 2>/dev/null || true
echo ""

# ── Launch vLLM server ────────────────────────────────────────────────────────
echo "Starting vLLM server... (first run downloads model ~14GB)"
echo "API will be available at: http://$HOST:$PORT/v1"
echo ""

python -m vllm.entrypoints.openai.api_server \
    --model "$MODEL" \
    --dtype "$DTYPE" \
    --tensor-parallel-size "$PARALLEL" \
    --host "$HOST" \
    --port "$PORT" \
    --max-model-len "$MAX_LEN" \
    --trust-remote-code \
    --disable-log-requests

# ── Alternative models (uncomment to use instead) ─────────────────────────────
# Llama 3.1 8B (better quality):
# python -m vllm.entrypoints.openai.api_server \
#     --model meta-llama/Meta-Llama-3.1-8B-Instruct \
#     --dtype float16 --host 0.0.0.0 --port 8000 --max-model-len 4096

# Qwen 2.5 7B (multilingual, strong reasoning):
# python -m vllm.entrypoints.openai.api_server \
#     --model Qwen/Qwen2.5-7B-Instruct \
#     --dtype float16 --host 0.0.0.0 --port 8000 --max-model-len 4096

# DeepSeek-R1 7B (reasoning-focused):
# python -m vllm.entrypoints.openai.api_server \
#     --model deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
#     --dtype float16 --host 0.0.0.0 --port 8000 --max-model-len 4096
