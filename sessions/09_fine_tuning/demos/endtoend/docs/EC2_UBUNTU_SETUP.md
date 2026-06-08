# EC2 Ubuntu Setup

Use this checklist before running the fine-tuning script on EC2.

## Target Instance

Recommended instance:

```text
g6.xlarge
```

Recommended storage:

```text
100 GB EBS root volume
```

Why this works:

- `g6.xlarge` has 1 NVIDIA L4 GPU with 24 GB VRAM.
- The 0.5B model plus LoRA adapters fit comfortably.
- 100 GB is enough for the repo, Python environment, Hugging Face cache, dataset, checkpoints, adapter, metrics, and prompt-check files.

## Recommended AMI

Best option for fewer setup problems:

```text
AWS Deep Learning Base GPU AMI or Deep Learning OSS NVIDIA Driver GPU AMI on Ubuntu
```

These AMIs usually already include NVIDIA drivers. If you use a plain Ubuntu AMI,
install and verify the NVIDIA driver before installing PyTorch.

## 1. Connect To EC2

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

## 2. Verify Disk Space

```bash
df -h
lsblk
```

You want the filesystem where the repo lives to have enough free space. For this
demo, use a 100 GB EBS volume.

## 3. Install System Packages

```bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip git git-lfs build-essential tmux nvtop
git lfs install
```

## 4. Verify Or Install NVIDIA Driver

First check whether the GPU driver already works:

```bash
nvidia-smi
```

If this prints the NVIDIA L4 GPU, continue to the Python setup.

If `nvidia-smi` is not found or cannot talk to the driver, use Ubuntu's driver
utility:

```bash
sudo apt-get update
sudo apt-get install -y ubuntu-drivers-common
ubuntu-drivers devices
sudo ubuntu-drivers install
sudo reboot
```

After reconnecting:

```bash
nvidia-smi
```

Expected result: one NVIDIA L4 GPU should appear.

## 5. Create Python Environment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 6. Install PyTorch With CUDA

The command below uses the CUDA 12.6 wheel channel:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

If this fails because your AMI has a different driver stack, use the official
PyTorch selector and choose Linux, pip, Python, CUDA:

```text
https://pytorch.org/get-started/locally/
```

## 7. Install Fine-Tuning Libraries

```bash
pip install transformers datasets accelerate peft trl bitsandbytes pandas scikit-learn hf_xet
```

What these packages do:

- `transformers`: loads the Qwen base model and tokenizer
- `datasets`: creates train/validation/test datasets
- `accelerate`: helps Transformers place work on the GPU
- `peft`: creates and trains LoRA adapters
- `bitsandbytes`: supports low-memory quantized training modes
- `pandas`: reads the generated CSV
- `scikit-learn`: available for simple metrics and utilities
- `hf_xet`: speeds up Hugging Face downloads for repositories using Xet storage

## 8. Verify Python Can See The GPU

```bash
python - <<'PY'
import torch
print("torch:", torch.__version__)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu:", torch.cuda.get_device_name(0))
    print("memory GB:", round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 2))
PY
```

Expected:

```text
cuda available: True
gpu: NVIDIA L4
memory GB: about 24
```

## 9. Use tmux For The 1-2 Hour Run

```bash
tmux new -s finetune
source .venv/bin/activate
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

Detach safely:

```text
Ctrl-b then d
```

Reconnect:

```bash
tmux attach -t finetune
```

## 10. Output Location

The script keeps demo-generated artifacts under:

```text
sessions/09_fine_tuning/demos/endtoend/output/
```

The script keeps Markdown docs and prompt handouts under:

```text
sessions/09_fine_tuning/demos/endtoend/docs/
```
