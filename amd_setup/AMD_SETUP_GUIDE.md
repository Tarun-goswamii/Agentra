# AMD Developer Cloud — vLLM Setup Guide

## Prerequisites
- AMD Developer Cloud account with $100 credits
- An AMD Instinct GPU instance (MI210, MI250, or MI300)
- ROCm 6.x pre-installed on the instance (AMD Cloud images come with it)

---

## Step 1 — Provision Your Instance

1. Log in to [AMD Developer Cloud](https://developer.amd.com/amd-developer-cloud/)
2. Click **"Launch Instance"**
3. Choose an image with **ROCm pre-installed** (e.g., Ubuntu 22.04 + ROCm 6.1)
4. Select GPU: **MI210 (16 GB)** is recommended for 7B models
5. Download your SSH key, then connect:
   ```bash
   ssh -i your-key.pem ubuntu@<INSTANCE_PUBLIC_IP>
   ```

---

## Step 2 — Verify ROCm

```bash
rocm-smi         # Should show your AMD GPU
rocminfo         # Detailed GPU info
hipcc --version  # HIP compiler
```

---

## Step 3 — Install vLLM (ROCm Build)

Run the setup script from this repo:
```bash
bash amd_setup/setup_vllm.sh
```

Or manually:
```bash
# Install PyTorch for ROCm 6.1
pip install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/rocm6.1

# Install vLLM (ROCm pre-built wheel)
pip install vllm
```

---

## Step 4 — Start the vLLM API Server

```bash
bash amd_setup/start_server.sh
```

Or manually (Mistral 7B):
```bash
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.3 \
    --dtype float16 \
    --tensor-parallel-size 1 \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 4096
```

For Llama 3.1 8B (slightly better quality):
```bash
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Meta-Llama-3.1-8B-Instruct \
    --dtype float16 \
    --tensor-parallel-size 1 \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 4096
```

> **Note**: First run downloads the model (~14 GB). It caches after that.

---

## Step 5 — Verify the API is Running

```bash
curl http://localhost:8000/v1/models
# Should return JSON with the model name
```

---

## Step 6 — Configure .env on Your Local Machine

Copy `.env.example` to `.env` and fill in:
```
AMD_BASE_URL=http://<INSTANCE_PUBLIC_IP>:8000/v1
AMD_MODEL=mistralai/Mistral-7B-Instruct-v0.3
AMD_API_KEY=EMPTY
LLM_BACKEND=amd
```

> **Security tip**: Open port 8000 only in AMD Cloud firewall settings,
> or use SSH tunneling: `ssh -L 8000:localhost:8000 ubuntu@<IP>`
> Then set `AMD_BASE_URL=http://localhost:8000/v1`

---

## Step 7 — Run the App

```bash
# Install Python deps (on local machine or AMD instance)
pip install -r requirements.txt

# Launch Streamlit
streamlit run app.py
```

---

## Cost Estimates (MI210 Instance)

| Model | VRAM Used | Tokens/sec | $/hr (estimate) |
|-------|-----------|------------|-----------------|
| Mistral-7B-Instruct | ~14 GB | ~80 tok/s | ~$0.50–1.00 |
| Llama-3.1-8B-Instruct | ~16 GB | ~70 tok/s | ~$0.50–1.00 |

With $100 credits → **100+ hours of GPU inference**

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `rocm-smi` not found | Re-install ROCm: `sudo apt install rocm` |
| Out of memory | Add `--max-model-len 2048` flag |
| Model download slow | Run `huggingface-cli download <model>` first |
| Port 8000 unreachable | Check AMD Cloud security group / firewall rules |
