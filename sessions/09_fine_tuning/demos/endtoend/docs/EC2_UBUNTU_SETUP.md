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
Deep Learning Base OSS Nvidia Driver GPU AMI (Ubuntu 24.04)
```

This AMI is published by AWS Deep Learning AMIs and includes the NVIDIA driver
stack, CUDA directories, Docker, NVIDIA container tooling, and AWS CLI. AWS
documents this AMI family as supporting G6 instances, including the `g6.xlarge`
target used in this demo.

For North Virginia, use this region:

```text
us-east-1
```

Do not hardcode an AMI ID from an old note. AMI IDs change by region and release
date. Get the current AMI ID from AWS at launch time.

### Option A: Find It In The AWS Console

1. Open the EC2 console.
2. Switch the region to **US East (N. Virginia) us-east-1**.
3. Choose **Launch instance**.
4. In **Application and OS Images**, search:

```text
Deep Learning Base OSS Nvidia Driver GPU AMI (Ubuntu 24.04)
```

5. Choose the x86_64 AWS-owned image, then select `g6.xlarge`.

### Option B: Get The Latest AMI ID From AWS CLI

Run this in AWS CloudShell or any terminal where AWS CLI credentials are
configured:

```bash
aws ssm get-parameter \
  --region us-east-1 \
  --name /aws/service/deeplearning/ami/x86_64/base-oss-nvidia-driver-gpu-ubuntu-24.04/latest/ami-id \
  --query "Parameter.Value" \
  --output text
```

Alternative lookup by AMI name:

```bash
aws ec2 describe-images \
  --region us-east-1 \
  --owners amazon \
  --filters \
    "Name=name,Values=Deep Learning Base OSS Nvidia Driver GPU AMI (Ubuntu 24.04) ????????" \
    "Name=state,Values=available" \
  --query "reverse(sort_by(Images, &CreationDate))[:1].ImageId" \
  --output text
```

If you use a plain Ubuntu AMI instead, install and verify the NVIDIA driver
before installing PyTorch.

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

## 6. Install Fine-Tuning Requirements

The end-to-end demo maintains its own requirements file:

```bash
sessions/09_fine_tuning/demos/endtoend/requirements.txt
```

Install all GPU fine-tuning libraries from that file:

```bash
python -m pip install -r sessions/09_fine_tuning/demos/endtoend/requirements.txt
```

The requirements file includes:

- PyTorch, torchvision, and torchaudio from the CUDA 12.6 PyTorch wheel index
- Transformers, Datasets, Accelerate, PEFT, TRL, bitsandbytes, and Hugging Face download helpers
- pandas, scikit-learn, numpy, and a compatible `httpx`

If you already installed these packages earlier, upgrade them before a full run:

```bash
python -m pip install --upgrade -r sessions/09_fine_tuning/demos/endtoend/requirements.txt
```

What these packages do:

- `torch`, `torchvision`, `torchaudio`: CUDA-enabled PyTorch training stack
- `transformers`: loads the Qwen base model and tokenizer
- `datasets`: creates train/validation/test datasets
- `httpx`: HTTP client dependency used by Hugging Face datasets and hub tools
- `accelerate`: helps Transformers place work on the GPU
- `peft`: creates and trains LoRA adapters
- `bitsandbytes`: supports low-memory quantized training modes
- `pandas`: reads the generated CSV
- `scikit-learn`: available for simple metrics and utilities
- `hf_xet`: speeds up Hugging Face downloads for repositories using Xet storage

If PyTorch installation fails because your AMI has a different driver stack,
use the official PyTorch selector and choose Linux, pip, Python, CUDA:

```text
https://pytorch.org/get-started/locally/
```

## 7. Verify Python Can See The GPU

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

## 8. Use tmux For The 1-2 Hour Run

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

## 9. Output Location

The script keeps demo-generated artifacts under:

```text
sessions/09_fine_tuning/demos/endtoend/output/
```

The script keeps Markdown docs and prompt handouts under:

```text
sessions/09_fine_tuning/demos/endtoend/docs/
```

## Troubleshooting: TrainingArguments Keyword Error

If the run stops with an error like this:

```text
TypeError: TrainingArguments.__init__() got an unexpected keyword argument 'group_by_length'
```

Your installed `transformers` package does not support every option used by the
training script. Use the latest version of this script, which skips unsupported
`TrainingArguments` options automatically. You can also upgrade the fine-tuning
libraries:

```bash
source .venv/bin/activate
python -m pip install --upgrade -r sessions/09_fine_tuning/demos/endtoend/requirements.txt
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

After the script fix, seeing a message like this is okay:

```text
TrainingArguments compatibility: skipping unsupported options for this Transformers version: group_by_length
```

That means the script detected the older package behavior and continued with
the supported training settings.

## Troubleshooting: httpx RequestError Import Error

If the run stops before Step 01 with an error like this:

```text
AttributeError: module 'httpx' has no attribute 'RequestError'
```

Your virtual environment has an incompatible or broken `httpx` package. Repair
the venv, verify the import, then rerun:

```bash
cd ~/LearningGenAI
source .venv/bin/activate

python -m pip install --upgrade --force-reinstall "httpx>=0.27,<1" datasets huggingface_hub

python - <<'PY'
import httpx, datasets
print("httpx:", httpx.__version__, "RequestError:", hasattr(httpx, "RequestError"))
print("datasets:", datasets.__version__)
PY

python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

Expected verification:

```text
RequestError: True
```

## Troubleshooting: huggingface-hub Version Error

If the run stops before Step 01 with an error like this:

```text
huggingface-hub>=0.34.0,<1.0 is required ... but found huggingface-hub==1.18.0
```

Your virtual environment has a `huggingface-hub` 1.x package, but the installed
Transformers stack for this demo expects `huggingface-hub` below 1.0. Repair the
venv, then reinstall from the demo requirements file:

```bash
cd ~/LearningGenAI
source .venv/bin/activate

python -m pip install --upgrade --force-reinstall "huggingface_hub>=0.34,<1"
python -m pip install --upgrade -r sessions/09_fine_tuning/demos/endtoend/requirements.txt

python - <<'PY'
import huggingface_hub, transformers
print("huggingface_hub:", huggingface_hub.__version__)
print("transformers:", transformers.__version__)
PY

python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

Expected verification:

```text
huggingface_hub: 0.x
```
