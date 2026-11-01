#!/bin/bash
# =============================================================================
# setup_vllm.sh — Install vLLM with ROCm support on AMD Developer Cloud
# Run once after provisioning your AMD GPU instance
# =============================================================================

set -e  # Exit on any error

echo "============================================="
echo "  AMD Developer Cloud — vLLM Setup Script   "
echo "============================================="

# ── 1. System packages ────────────────────────────────────────────────────────
echo "[1/5] Updating system packages..."
sudo apt-get update -qq
sudo apt-get install -y python3-pip python3-venv git wget curl htop

# ── 2. Verify ROCm ───────────────────────────────────────────────────────────
echo "[2/5] Verifying ROCm installation..."
if ! command -v rocm-smi &> /dev/null; then
    echo "ROCm not found. Installing ROCm..."
    wget -q https://repo.radeon.com/amdgpu-install/6.1/ubuntu/jammy/amdgpu-install_6.1.60101-1_all.deb
    sudo dpkg -i amdgpu-install_6.1.60101-1_all.deb
    sudo amdgpu-install -y --usecase=rocm
else
    echo "ROCm already installed:"
    rocm-smi --showdriverversion 2>/dev/null || true
fi

# ── 3. Python virtual environment ────────────────────────────────────────────
echo "[3/5] Creating Python virtual environment..."
python3 -m venv ~/vllm-env
source ~/vllm-env/bin/activate

pip install --upgrade pip wheel setuptools

# ── 4. PyTorch for ROCm 6.1 ─────────────────────────────────────────────────
echo "[4/5] Installing PyTorch (ROCm 6.1 build)..."
pip install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/rocm6.1

# Verify GPU is visible
python3 -c "
import torch
if torch.cuda.is_available():
    print(f'✅ GPU detected: {torch.cuda.get_device_name(0)}')
    print(f'   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
else:
    print('⚠️  GPU not detected — check ROCm installation')
"

# ── 5. Install vLLM ──────────────────────────────────────────────────────────
echo "[5/5] Installing vLLM..."
pip install vllm huggingface_hub

# Install HuggingFace CLI for model downloads
pip install "huggingface_hub[cli]"

echo ""
echo "============================================="
echo "  ✅ Setup complete!"
echo ""
echo "  Next steps:"
echo "  1. source ~/vllm-env/bin/activate"
echo "  2. bash amd_setup/start_server.sh"
echo "============================================="
