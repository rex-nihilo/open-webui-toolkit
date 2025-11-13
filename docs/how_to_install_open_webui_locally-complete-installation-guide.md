# How to Install Open WebUI Locally — Complete Installation Guide

[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Docs-blue.svg?style=flat-square&logo=github)](https://github.com/open-webui/open-webui) [![License: License CC-BY-SA](https://img.shields.io/badge/License-CC--BY--SA--4.0%20-blue.svg?style=flat-square)](http://creativecommons.org/licenses/by-sa/4.0/)

A comprehensive guide for Windows, macOS, and Linux for beginners.

---

## Table of Contents

- [What is Open WebUI?](#what-is-open-webui)
- [Hardware Requirements](#hardware-requirements)
- [Prerequisites](#prerequisites)
- [Part 1: Installing Ollama](#part-1-installing-ollama)
  - [Installing Ollama on Windows](#installing-ollama-on-windows)
  - [Installing Ollama on macOS](#installing-ollama-on-macos)
  - [Installing Ollama on Linux](#installing-ollama-on-linux)
  - [After Ollama Installation](#after-ollama-installation)
- [Part 2: Installing Open WebUI](#part-2-installing-open-webui)
  - [Method 1: Docker Installation (Recommended)](#method-1-docker-installation-recommended)
  - [Method 2: Python Installation (Advanced)](#method-2-python-installation-advanced)
- [First Access and Account Creation](#first-access-and-account-creation)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Additional Resources](#additional-resources)

---

This guide provides step-by-step instructions for installing Open WebUI and Ollama on your local machine. Whether you're using Windows, macOS, or Linux, this guide will help you set up a complete local AI environment.

**Important:** This guide focuses exclusively on **installation**. Configuration and usage instructions are covered in separate documentation.

---

<a id="what-is-open-webui"></a>

## What is Open WebUI?

Open WebUI is a self-hosted, open-source web interface that allows you to interact with large language models (LLMs) through a ChatGPT-like interface. It runs entirely on your local machine, ensuring privacy and offline functionality.

**Key Features:**
- ChatGPT-like user interface
- Completely private and offline
- Support for multiple LLM backends (Ollama, OpenAI API, etc.)
- Model management and customization
- No external API costs or data sharing

🔗 For more details: [**Introduction to Open WebUI**](https://github.com/rex-nihilo/open-webui-toolkit/blob/main/docs/introduction_to_open_webui.md)

---

<a id="hardware-requirements"></a>

## Hardware Requirements

### Minimum Requirements

| Component | Specification | Notes |
|-----------|---------------|-------|
| **CPU** | 4 cores (x86_64 or ARM64) | Intel, AMD, or Apple Silicon |
| **RAM** | 8 GB | For small models (3B-7B parameters) |
| **Storage** | 20 GB free space | SSD strongly recommended |
| **OS** | Windows 10/11, macOS 11+, Linux | 64-bit systems only |

### Recommended Requirements

| Component | Specification | Notes |
|-----------|---------------|-------|
| **CPU** | 8+ cores | Faster inference |
| **RAM** | 16 GB or more | For larger models (13B+ parameters) |
| **Storage** | 50 GB+ free space (SSD) | Models can be 4-30 GB each |
| **GPU** | NVIDIA GPU with 8+ GB VRAM | Optional but significantly faster |

**Note for Beginners:** Start with small models like `phi3:mini` (2 GB) or `llama3.2:3b` (2 GB) to test on minimal hardware before downloading larger models.

---

<a id="prerequisites"></a>

## Prerequisites

### Required for All Users

- **Administrative/Root Access:** You'll need permission to install software
- **Internet Connection:** Required for initial downloads (20 GB+ for full setup)
- **Web Browser:** Chrome, Firefox, Safari, or Edge

### Platform-Specific Tools

| Platform | Required Tools |
|----------|----------------|
| **Windows** | PowerShell or Command Prompt (built-in) |
| **macOS** | Terminal (built-in) |
| **Linux** | Terminal (built-in) |

**Note:** All required software will be downloaded during the installation process. No prior technical knowledge is required.

---

<a id="part-1-installing-ollama"></a>

## Part 1: Installing Ollama

Ollama is the backend engine that runs large language models on your computer. Think of it as the "brain" that processes your prompts, while Open WebUI is the "interface" you interact with.

**Open WebUI requires Ollama to function.** You cannot use Open WebUI without Ollama or another compatible backend.

**What Ollama Does:**
- **Downloads and manages AI models**: Ollama simplifies the process of acquiring models. With a single command like `ollama pull llama3.2`, it downloads the model from its library, handles verification, and stores it locally. It easily lets you switch between different models (e.g., CodeLlama for programming, Llama 3 for general chat).
- **Runs models locally on your hardware**: This is the core feature. Ollama executes the AI model entirely on your own machine—be it a laptop, desktop, or home server. Your data never needs to leave your computer.
- **Provides an API for applications like Open WebUI**: Ollama runs a local server with a REST API that other applications can communicate with. Open WebUI uses this API to send your prompts to Ollama and receive the generated text back, presenting it to you in a beautiful chat interface. Other apps, like code editors or custom scripts, can also use this API.
- **Handles GPU acceleration automatically**: Ollama is optimized for performance. It automatically detects and utilizes your computer's GPU (if available and supported, e.g., NVIDIA, AMD, or Apple Silicon) to dramatically speed up model inference. If a GPU isn't available, it falls back to the CPU seamlessly.

**Why Do You Need It? The Key Benefits:**

Using Ollama, especially when paired with Open WebUI, offers significant advantages over cloud-based AI services:
- 🔒 **Complete Privacy and Security**: Since everything runs locally, your conversations, documents, and data are never sent to a third-party server. This is essential for sensitive information, proprietary code, or confidential documents.
-  🎛️ **Full Control and Customization**: You are not limited by a company's rules or model availability. You can choose from a vast ecosystem of open-source models, fine-tune them for specific tasks, and run them exactly how you want, without usage restrictions or filters.
- 💰 **Cost-Effective**: After the initial hardware investment, using Ollama is free. There are no per-prompt fees, subscription costs, or API rate limits. You can experiment and use it as much as you like.
- 📡 **Offline Functionality**: Once the models are downloaded, you can use Ollama and Open WebUI completely offline. This is perfect for travel, areas with poor connectivity, or simply ensuring your workflow is never interrupted.
- 🎯 **A Unified Platform**: Ollama acts as a central hub for all your local models. Instead of managing multiple, disparate AI tools, you can manage and interact with dozens of different models all through one system (Ollama) and one interface (Open WebUI).

---

<a id="installing-ollama-on-windows"></a>

### Installing Ollama on Windows

#### Step 1: Download Ollama

1. Open your web browser
2. Visit the official Ollama website: [https://ollama.com](https://ollama.com)
3. Click the **"Download"** button
4. Click **"Download for Windows"**
5. Save the `OllamaSetup.exe` file to your Downloads folder

#### Step 2: Run the Installer

1. Locate `OllamaSetup.exe` in your Downloads folder
2. Double-click the file to run it
3. If Windows SmartScreen appears:
   - Click **"More info"**
   - Click **"Run anyway"**
4. Follow the installation wizard:
   - Click **"Next"**
   - Accept the license agreement
   - Choose installation location (default is recommended)
   - Click **"Install"**
5. Wait for installation to complete (1-2 minutes)
6. Click **"Finish"**

#### Step 3: Verify Installation

1. Open **PowerShell**:
   - Press `Windows Key + X`
   - Select **"Windows PowerShell"** or **"Terminal"**
2. Type the following command and press Enter:

```bash
ollama --version
```

3. You should see output like:

```
ollama version is 0.x.x
```

**Troubleshooting:** If you see "command not found":
- Restart your computer
- Open a new PowerShell window
- If still not working, add Ollama to PATH manually (see Troubleshooting section)

#### Step 4: Start Ollama Service

Ollama should start automatically. To verify:

```bash
ollama serve
```

If it says "Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address", Ollama is already running. This is normal.

**Important:** Keep this PowerShell window open, or minimize it. Ollama needs to run in the background for Open WebUI to work.

---

<a id="installing-ollama-on-macos"></a>

### Installing Ollama on macOS

#### Step 1: Download Ollama

1. Visit [https://ollama.com](https://ollama.com)
2. Click **"Download for Mac"**
3. Save the `.zip` file to your Downloads folder

#### Step 2: Install Ollama

1. Open **Finder**
2. Navigate to **Downloads**
3. Double-click **"Ollama-darwin.zip"**
4. Drag **"Ollama.app"** to your **Applications** folder
5. Open **Applications** folder
6. Right-click **"Ollama"** and select **"Open"**
7. If you see a security warning:
   - Click **"Open"** to confirm

#### Step 3: Verify Installation

1. Open **Terminal**:
   - Press `Command + Space`
   - Type "Terminal" and press Enter
2. Type:

```bash
ollama --version
```

3. Expected output:

```
ollama version is 0.x.x
```

#### Step 4: Start Ollama

Ollama should start automatically in the menu bar. Look for the Ollama icon (llama head) in the top-right corner.

To test from Terminal:

```bash
ollama serve
```

---

<a id="installing-ollama-on-linux"></a>

### Installing Ollama on Linux

#### Step 1: Download and Install

Open your terminal and run the following command:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

This script will:
- Download Ollama
- Install it to `/usr/local/bin/`
- Create a systemd service
- Start Ollama automatically

**Expected output:**

```
>>> Installing ollama to /usr/local
>>> Downloading Linux amd64 bundle
>>> Creating ollama user...
>>> Adding ollama user to render group...
>>> Adding ollama user to video group...
>>> Creating ollama systemd service...
>>> Enabling and starting ollama service...
```

#### Step 2: Verify Installation

```bash
ollama --version
```

Expected output:

```
ollama version is 0.x.x
```

#### Step 3: Check Service Status

```bash
sudo systemctl status ollama
```

You should see:

```
● ollama.service - Ollama Service
   Loaded: loaded (/etc/systemd/system/ollama.service; enabled)
   Active: active (running)
```

#### Step 4: Enable Auto-Start (Optional)

To ensure Ollama starts automatically when your computer boots:

```bash
sudo systemctl enable ollama
```

**Troubleshooting GPU Support:**

For NVIDIA GPUs:

```bash
# Check if CUDA is detected
nvidia-smi

# If not installed, install NVIDIA drivers and CUDA toolkit
# Instructions vary by distribution - see your distro's documentation
```

For AMD GPUs:

```bash
curl -L https://ollama.com/download/ollama-linux-amd64-rocm.tgz -o ollama-linux-amd64-rocm.tgz
sudo tar -C /usr/ -xzf ollama-linux-amd64-rocm.tgz
```

---

<a id="after-ollama-installation"></a>

### After Ollama Installation

To confirm Ollama is working correctly on any platform:

1. Open your web browser
2. Navigate to: [http://localhost:11434](http://localhost:11434) to check that Ollama is available online, this shoud display `Ollama is running`
3. Navigate to: [http://localhost:11434/api/version](http://localhost:11434/api/version) to get Ollama version
4. On terminal/PowerShell:

```bash
ollama list
```

This shows your installed models. If this is your first install, the list will be empty. That's normal!

---

#### Recommended Starter Models

Before installing Open WebUI, let's download a model to test with.

| Model | Size | RAM Needed | Best For |
|-------|------|------------|----------|
| `phi3:mini` | 2.3 GB | 4 GB | Testing, coding |
| `llama3.2:3b` | 2 GB | 4 GB | General use, fast |
| `llama3.2:1b` | 1.3 GB | 2 GB | Very lightweight |
| `gemma2:2b` | 1.6 GB | 4 GB | Google's model |

#### Download a Model

Choose one model from above and run:

```bash
ollama pull phi3:mini
```

**What happens:**
- Ollama connects to its model library
- Downloads the model (2-4 GB, takes 2-10 minutes depending on internet speed)
- Stores it locally in:
  - Windows: `C:\Users\YourName\.ollama\models`
  - macOS: `~/.ollama/models`
  - Linux: `/usr/share/ollama/.ollama/models`

**Example output:**

```
pulling manifest
pulling 8934d96d3f08... 100% ▕████████████████▏ 2.3 GB
pulling 8c17c2ebb0ea... 100% ▕████████████████▏ 7.0 KB
pulling 590d74a5569b... 100% ▕████████████████▏ 6.0 KB
verifying sha256 digest
writing manifest
success
```

#### Test the Model

```bash
ollama run phi3:mini
```

You'll enter an interactive chat. Type a message:

```
>>> Hello! Who are you?
```

The model will respond. Type `/bye` to exit.

**Congratulations!** Ollama is now fully installed and working. Now we can install Open WebUI.

---

<a id="part-2-installing-open-webui"></a>

## Part 2: Installing Open WebUI

You have two options: Docker (recommended for beginners) or Python (for advanced users).

---

<a id="method-1-docker-installation-recommended"></a>

### Method 1: Docker Installation (Recommended)

Docker provides an isolated environment and is the easiest installation method.

#### Why Docker?
- ✅ One-command installation
- ✅ No dependency conflicts
- ✅ Easy to update and uninstall
- ✅ Works identically across all platforms
- ✅ Officially supported by Open WebUI team

#### Step 1: Install Docker

**Windows:**

1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Run `Docker Desktop Installer.exe`
3. Follow the installation wizard:
   - Enable WSL 2 if prompted
   - Check "Use WSL 2 instead of Hyper-V" if shown
   - Complete installation
4. Restart your computer if prompted
5. Launch Docker Desktop from the Start menu
6. Sign in or create a free Docker account
7. Wait for Docker to start (green icon in system tray)

**macOS:**

1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Open the `.dmg` file
3. Drag Docker to Applications folder
4. Open Docker from Applications
5. Authorize with system password when prompted
6. Sign in or create a free account
7. Wait for Docker to start (whale icon in menu bar)

**Linux (Ubuntu/Debian):**

Open terminal and run:

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to docker group (avoid needing sudo)
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Enable Docker to start on boot
sudo systemctl enable docker
```

**Log out and back in** for group changes to take effect.

#### Step 2: Verify Docker Installation

Open a new terminal/PowerShell and run:

```bash
docker --version
docker compose version
```

Expected output:

```
Docker version 27.3.1, build ce12230
Docker Compose version v2.29.7
```

**Troubleshooting:**
- If "command not found": Restart your terminal/computer
- If Docker Desktop shows errors: Check system requirements (Windows 10 21H2+ or Windows 11)

#### Step 3: Install Open WebUI with Docker

**Simple Installation (Ollama on same machine):**

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

**What this command does:**
- `docker run -d`: Run container in background (detached mode)
- `-p 3000:8080`: Map port 3000 on your machine to port 8080 in container
- `--add-host=host.docker.internal:host-gateway`: Allow container to access Ollama on your machine
- `-v open-webui:/app/backend/data`: Store database persistently (prevents data loss)
- `--name open-webui`: Name the container "open-webui"
- `--restart always`: Restart container if it stops or after system reboot
- `ghcr.io/open-webui/open-webui:main`: Use the latest official image

**What happens:**
1. Docker downloads Open WebUI image (~1-2 GB, takes 2-5 minutes)
2. Creates a container
3. Starts Open WebUI automatically

**Expected output:**

```
Unable to find image 'ghcr.io/open-webui/open-webui:main' locally
main: Pulling from open-webui/open-webui
[...download progress...]
Status: Downloaded newer image for ghcr.io/open-webui/open-webui:main
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

The long string at the end is your container ID.

#### Step 4: Verify Container is Running

```bash
docker ps
```

You should see:

```
CONTAINER ID   IMAGE                                PORTS                    NAMES
a1b2c3d4e5f6   ghcr.io/open-webui/open-webui:main  0.0.0.0:3000->8080/tcp   open-webui
```

#### Step 5: Access Open WebUI

1. Wait 30 seconds for Open WebUI to initialize
2. Open your web browser
3. Navigate to: [http://localhost:3000](http://localhost:3000)

**Note:** If you see a "connection refused" error, wait another minute and refresh.

**Alternative Installation - Ollama on Different Server:**

If Ollama is running on a different computer or server:

```bash
docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://192.168.1.100:11434 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

Replace `192.168.1.100` with your Ollama server's IP address.

#### Managing Your Docker Installation

**Stop Open WebUI:**

```bash
docker stop open-webui
```

**Start Open WebUI:**

```bash
docker start open-webui
```

**View logs (troubleshooting):**

```bash
docker logs open-webui
```

**Update to latest version:**

```bash
docker stop open-webui
docker rm open-webui
docker pull ghcr.io/open-webui/open-webui:main
# Then run the docker run command again from Step 3
```

**Uninstall completely:**

```bash
docker stop open-webui
docker rm open-webui
docker rmi ghcr.io/open-webui/open-webui:main
docker volume rm open-webui
```

---

<a id="method-2-python-installation-advanced"></a>

### Method 2: Python Installation (Advanced)

This method installs Open WebUI directly without Docker. It requires more steps but uses fewer system resources.

**Prerequisites:**
- Python 3.11 or higher
- Node.js 20 or higher
- Git

#### Step 1: Install System Dependencies

**Windows:**

1. **Python 3.11+:**
   - Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Run installer
   - **Important:** Check "Add Python to PATH"
   - Click "Install Now"

2. **Node.js 20+:**
   - Download LTS version from [https://nodejs.org/](https://nodejs.org/)
   - Run installer with default options

3. **Git:**
   - Download from [https://git-scm.com/downloads](https://git-scm.com/downloads)
   - Run installer with default options

**macOS:**

1. Install Homebrew if not already installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install dependencies:

```bash
brew install python@3.11 node git
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nodejs npm git
```

#### Step 2: Verify Installed Versions

```bash
python --version    # Should show 3.11 or higher
python3 --version   # On macOS/Linux, use python3
node --version      # Should show v20 or higher
npm --version
git --version
```

**Troubleshooting:** If commands not found, restart your terminal.

#### Step 3: Clone Open WebUI Repository

Choose a location for installation. For example:

**Windows:**

```bash
cd C:\Users\YourName\Documents
```

**macOS/Linux:**

```bash
cd ~/Documents
```

Then clone:

```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
```

#### Step 4: Set Up Python Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Your prompt should now show `(venv)` at the beginning.

#### Step 5: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This takes 5-10 minutes. You'll see many packages being installed.

**If you encounter errors:**

```bash
pip install --upgrade wheel setuptools
pip install -r requirements.txt
```

#### Step 6: Set Data Directory (Important)

**Windows:**

```bash
$env:DATA_DIR = "$HOME\open-webui-data"
```

**macOS/Linux:**

```bash
export DATA_DIR="$HOME/open-webui-data"
```

**Why this matters:** Without setting `DATA_DIR`, your data will be stored in a temporary location and lost when you update.

#### Step 7: Start Open WebUI

```bash
open-webui serve
```

**Expected output:**

```
  ___                  __        __   _     _   _ ___
 / _ \ _ __   ___ _ __\ \      / /__| |__ | | | |_ _|
| | | | '_ \ / _ \ '_ \\ \ /\ / / _ \ '_ \| | | || |
| |_| | |_) |  __/ | | |\ V  V /  __/ |_) | |_| || |
 \___/| .__/ \___|_| |_| \_/\_/ \___|_.__/ \___/|___|
      |_|

v0.4.6 - building the best open-source AI user interface.
https://github.com/open-webui/open-webui

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

**Keep this terminal window open.** Open WebUI is now running.

#### Step 8: Access Open WebUI

Open your web browser and go to: [http://localhost:8080](http://localhost:8080)

#### Managing Your Python Installation

**Stop Open WebUI:**
- Press `Ctrl+C` in the terminal where it's running

**Start Open WebUI:**
1. Navigate to the open-webui folder
2. Activate virtual environment (see Step 4)
3. Run `open-webui serve`

**Update Open WebUI:**

```bash
cd open-webui
git pull
pip install -r requirements.txt
```

---

<a id="first-access-and-account-creation"></a>

## First Access and Account Creation

When you first access Open WebUI:

1. You'll see a welcome screen
2. Click **"Sign up"**
3. Fill in the form:
   - **Email:** Your email (stored locally only, not sent anywhere)
   - **Name:** Your display name
   - **Password:** Choose a secure password
4. Click **"Create Account"**

**Important Notes:**
- The **first account created becomes the admin**
- All data is stored locally on your computer
- No data is sent to external servers
- Email is only used for identification within the interface

After creating your account, you'll be logged in automatically.

---

<a id="troubleshooting"></a>

## Troubleshooting

### Ollama Issues

**Problem: "ollama command not found"**

Solution:
- Restart your terminal/computer
- Check if Ollama is in PATH:
  - Windows: Search "Environment Variables" in Start menu, check PATH includes Ollama
  - macOS/Linux: Check `which ollama`

**Problem: "Error: could not connect to ollama"**

Solution:
- Verify Ollama is running: `ollama serve`
- Check if Ollama service is active
- On Windows: Look for Ollama icon in system tray
- On macOS: Look for Ollama icon in menu bar
- On Linux: `sudo systemctl status ollama`

**Problem: Models download very slowly**

Solution:
- Check your internet connection
- Large models (13B+) can be 10-30 GB
- Consider using smaller models initially

**Problem: "Error: GPU not detected"**

Solution:
- Verify GPU drivers are installed and up to date
- NVIDIA: Install CUDA Toolkit 11.8 or 12.x from [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
- AMD: Use ROCm version of Ollama (Linux only)
- Ollama will use CPU if GPU not available (slower but functional)

### Docker Issues

**Problem: "docker: command not found"**

Solution:
- Verify Docker Desktop is running (check system tray/menu bar)
- Restart Docker Desktop
- Reinstall Docker Desktop
- On Linux: Check if Docker service is running: `sudo systemctl status docker`

**Problem: "port 3000 already in use"**

Solution:

Option 1 - Use different port:

```bash
docker run -d -p 3001:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

Then access at [http://localhost:3001](http://localhost:3001)

Option 2 - Find and stop process using port 3000:

Windows:

```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

macOS/Linux:

```bash
lsof -i :3000
kill -9 <PID>
```

**Problem: "Cannot connect to Docker daemon"**

Solution:
- Start Docker Desktop
- Wait for it to fully initialize (green icon)
- On Linux: `sudo systemctl start docker`
- Check Docker Desktop settings for WSL integration (Windows)

**Problem: Container exits immediately**

Solution:

Check logs:

```bash
docker logs open-webui
```

Common causes:
- Port conflict (see above)
- Insufficient disk space (need 20 GB free)
- Corrupted download (delete and re-pull image)

### Open WebUI Access Issues

**Problem: "502 Bad Gateway" or connection refused**

Solution:
- Wait 1-2 minutes after starting (initialization time)
- Verify Ollama is running: `ollama list` should work
- Check firewall isn't blocking ports 3000 or 8080
- Verify Docker container is running: `docker ps`

**Problem: "Cannot connect to Ollama" in Open WebUI**

Solution:

Docker installation:
- Verify `--add-host=host.docker.internal:host-gateway` was in docker run command
- Check Ollama is accessible: `curl http://localhost:11434/api/tags`

Python installation:
- Set OLLAMA_BASE_URL: `export OLLAMA_BASE_URL=http://localhost:11434`
- Restart Open WebUI

**Problem: Models not appearing in dropdown**

Solution:
- Pull at least one model: `ollama pull phi3:mini`
- Restart Open WebUI
- Check Ollama connection in Open WebUI settings

### Python Installation Issues

**Problem: `pip install` fails with compilation errors**

Solution:

Windows:
- Install Microsoft C++ Build Tools: [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

macOS:
- Install Xcode Command Line Tools: `xcode-select --install`

Linux:
- Install build essentials: `sudo apt install build-essential python3-dev`

**Problem: "No module named 'open-webui'" after installation**

Solution:
- Ensure virtual environment is activated (see `(venv)` in prompt)
- Reinstall: `pip install --upgrade --force-reinstall open-webui`

---

<a id="faq"></a>

## FAQ

### General Questions

**Q: Do I need an internet connection to use Open WebUI after installation?**

A: No. After downloading models, everything runs offline. You only need internet for:
- Initial installation
- Downloading new models
- Updating software

**Q: Is my data private?**

A: Yes, completely. Everything runs locally on your machine. No data is sent to external servers unless you explicitly configure external APIs.

**Q: How much disk space do I need?**

A: Minimum 20 GB free space. Each model requires:
- Small models (1B-3B): 1-2 GB
- Medium models (7B): 4-5 GB
- Large models (13B): 8-10 GB
- Very large models (70B+): 30-50 GB

**Q: Can I use Open WebUI without Ollama?**

A: Open WebUI requires a backend. Options are:
- Ollama (recommended, local)
- OpenAI API (requires API key and internet)
- Other OpenAI-compatible APIs

For local, offline use, Ollama is required.

**Q: Which installation method should I choose?**

A: For most users: **Docker**
- Easier to install
- Easier to update
- No dependency conflicts
- Officially supported

Use Python installation only if:
- You have limited disk space (Docker requires ~2 GB extra)
- You need to customize the installation
- You're experienced with Python development

### Model Questions

**Q: Which model should I download first?**

A: Start small:
- `phi3:mini` (2.3 GB) - Good for testing, coding assistance
- `llama3.2:3b` (2 GB) - Fast, general-purpose
- `gemma2:2b` (1.6 GB) - Very fast, lightweight

Once comfortable, try larger models:
- `llama3.2:11b` (7 GB) - Better quality
- `mixtral:8x7b` (26 GB) - High quality, requires 32 GB RAM

**Q: How do I download additional models?**

A: Use Ollama:

```bash
ollama pull <model-name>
```

Browse available models at [https://ollama.com/library](https://ollama.com/library)

**Q: Can I delete models I don't use?**

A: Yes:

```bash
ollama rm <model-name>
```

**Q: Where are models stored?**

A:
- Windows: `C:\Users\YourName\.ollama\models`
- macOS: `~/.ollama/models`
- Linux: `/usr/share/ollama/.ollama/models` or `~/.ollama/models`

### Performance Questions

**Q: Why is inference slow?**

A: Several factors affect speed:
- **Model size:** Larger models are slower
- **Hardware:** More RAM and CPU cores help
- **GPU:** Using GPU is 5-10x faster than CPU
- **Context length:** Longer conversations slow down inference

Tips to improve:
- Use smaller models
- Close other applications
- Enable GPU acceleration
- Reduce context window size

**Q: Does Open WebUI require a GPU?**

A: No, CPU-only works fine. GPU accelerates inference significantly but is optional.

**Q: My computer gets hot when running models**

A: Normal. LLMs are computationally intensive. Ensure:
- Good ventilation
- Laptop on hard surface (not bed/couch)
- Consider using smaller models
- Limit concurrent operations

### Update and Maintenance

**Q: How do I update Open WebUI?**

A: Docker:

```bash
docker stop open-webui
docker rm open-webui
docker pull ghcr.io/open-webui/open-webui:main
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

Python:

```bash
cd open-webui
source venv/bin/activate  # or venv\Scripts\activate on Windows
git pull
pip install --upgrade -r requirements.txt
```

**Q: How do I update Ollama?**

A:
- **Windows/macOS:** Download and run the latest installer from [https://ollama.com](https://ollama.com)
- **Linux:** Run the install script again: `curl -fsSL https://ollama.com/install.sh | sh`

**Q: Will updating delete my data?**

A: No. Your data is stored separately:
- Docker: In the `open-webui` volume
- Python: In the directory specified by `DATA_DIR`
- Models: In Ollama's model directory

Always remains safe during updates.

**Q: How do I back up my data?**

A: Docker:

```bash
docker run --rm -v open-webui:/data -v $(pwd):/backup alpine tar czf /backup/open-webui-backup.tar.gz -C /data .
```

Python:

```bash
# Back up your DATA_DIR folder
cp -r ~/open-webui-data ~/open-webui-backup
```

Models (copy the entire directory):

```bash
# Windows
xcopy /E /I C:\Users\YourName\.ollama\models C:\Backup\ollama-models

# macOS/Linux
cp -r ~/.ollama/models ~/backup/ollama-models
```

### Troubleshooting Questions

**Q: Can I run multiple instances of Open WebUI?**

A: Yes, but each needs a unique port:

```bash
docker run -d -p 3001:8080 --add-host=host.docker.internal:host-gateway -v open-webui-2:/app/backend/data --name open-webui-2 --restart always ghcr.io/open-webui/open-webui:main
```

**Q: How do I completely uninstall everything?**

A: 

**Docker installation:**

```bash
# Stop and remove Open WebUI
docker stop open-webui
docker rm open-webui
docker rmi ghcr.io/open-webui/open-webui:main
docker volume rm open-webui

# Uninstall Docker Desktop (optional)
# Windows: Use "Add or Remove Programs"
# macOS: Drag Docker.app to Trash
# Linux: sudo apt remove docker-ce docker-ce-cli containerd.io
```

**Python installation:**

```bash
# Delete the cloned repository
rm -rf ~/Documents/open-webui  # Adjust path as needed

# Remove virtual environment
rm -rf ~/Documents/open-webui/venv
```

**Ollama:**

```bash
# Windows: Use "Add or Remove Programs" to uninstall Ollama
# Delete models folder: C:\Users\YourName\.ollama

# macOS: 
rm -rf /Applications/Ollama.app
rm -rf ~/.ollama

# Linux:
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /etc/systemd/system/ollama.service
sudo rm /usr/local/bin/ollama
sudo userdel ollama
rm -rf /usr/share/ollama
rm -rf ~/.ollama
```

**Q: Open WebUI won't start after system reboot**

A: 

Docker:
- Ensure Docker Desktop starts automatically (check settings)
- Container should auto-start with `--restart always` flag
- Manually start: `docker start open-webui`

Python:
- You must manually start Open WebUI after each reboot
- Navigate to folder, activate venv, run `open-webui serve`

Ollama:
- Windows: Should auto-start (check system tray)
- macOS: Should auto-start (check menu bar)
- Linux: Enabled by systemd: `sudo systemctl enable ollama`

**Q: Getting "Out of memory" errors**

A: Your model is too large for available RAM. Solutions:
1. Use a smaller model
2. Close other applications
3. Reduce context window (in model parameters)
4. Add more RAM to your system
5. Use quantized versions (e.g., `llama3.2:7b-q4` instead of `llama3.2:7b`)

**Q: Can I use Open WebUI on a different computer than Ollama?**

A: Yes! Ollama can run on one machine (server) and Open WebUI on another (client).

On Ollama machine:

```bash
# Make Ollama accessible on network
# Windows/macOS: Set environment variable
OLLAMA_HOST=0.0.0.0 ollama serve

# Linux: Edit systemd service
sudo systemctl edit ollama
```

Add:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Then restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

On Open WebUI machine (Docker):

```bash
docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://192.168.1.100:11434 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

Replace `192.168.1.100` with your Ollama machine's IP address.

**Q: Error: "CUDA out of memory"**

A: Your GPU doesn't have enough VRAM. Solutions:
1. Use smaller models
2. Reduce batch size
3. Close GPU-intensive applications
4. Use CPU instead (slower): `CUDA_VISIBLE_DEVICES="" ollama serve`

**Q: How do I enable GPU support?**

A: GPU support is automatic if:
- NVIDIA GPU: CUDA drivers installed
- AMD GPU: ROCm installed (Linux only)
- Apple Silicon: Built-in (Metal)

Verify GPU is detected:

```bash
# NVIDIA
nvidia-smi

# Check Ollama is using GPU (look for GPU utilization while running model)
```

### Platform-Specific Questions

**Q: WSL or native Windows for Ollama?**

A: **Native Windows is recommended**. Ollama for Windows has better performance and easier setup than WSL.

**Q: Can I run this on a Raspberry Pi?**

A: Yes, but:
- Raspberry Pi 4/5 with 8 GB RAM minimum
- Use ARM-compatible models
- Expect slower performance
- Install ARM version of Ollama and Open WebUI

**Q: Does this work on Apple Silicon (M1/M2/M3)?**

A: Yes! Apple Silicon has excellent performance for LLMs:
- Ollama uses Metal for GPU acceleration
- Unified memory architecture is efficient
- 16 GB RAM recommended for larger models

**Q: Can I install this on a server without GUI?**

A: Yes:
- Install Ollama (headless)
- Use Docker or Python method for Open WebUI
- Access via web browser from another machine
- Ensure ports 11434 (Ollama) and 3000/8080 (Open WebUI) are accessible

---

<a id="additional-resources"></a>

## Additional Resources

### Official Documentation

- **Open WebUI GitHub:** [https://github.com/open-webui/open-webui](https://github.com/open-webui/open-webui)
- **Open WebUI Documentation:** [https://docs.openwebui.com](https://docs.openwebui.com)
- **Ollama GitHub:** [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
- **Ollama Documentation:** [https://docs.ollama.com/](https://docs.ollama.com/)

### Model Resources

- **Ollama Model Library:** [https://ollama.com/library](https://ollama.com/library)
- **Hugging Face Models:** [https://huggingface.co/models](https://huggingface.co/models)
- **Model Performance Benchmarks:** Search "LLM benchmark" for comparison charts

### Community and Support

- **Open WebUI Discord:** Join via GitHub repository
- **Reddit:** r/LocalLLaMA, r/OpenWebUI
- **GitHub Issues:** Report bugs or ask questions on respective repositories

### Learning Resources

- **Prompt Engineering Guide:** [https://www.promptingguide.ai](https://www.promptingguide.ai)
- **LLM Basics:** Search for "Large Language Models explained" on YouTube
- **Docker Tutorial:** [https://docs.docker.com/get-started/](https://docs.docker.com/get-started/)

### Tools and Utilities

- **GPU Monitoring:**
  - NVIDIA: `nvidia-smi`
  - AMD: `radeontop`
  - macOS: Activity Monitor > GPU
  
- **System Monitoring:**
  - Windows: Task Manager
  - macOS: Activity Monitor
  - Linux: `htop`, `btop`

---

## Next Steps After Installation

Now that you have Open WebUI and Ollama installed:

1. **Explore different models:** Try various models to find what works best for your hardware and use case
2. **Read the configuration guide:** Learn how to customize Open WebUI settings (separate documentation)
3. **Join the community:** Connect with other users to share tips and get help
4. **Experiment with prompts:** Learn effective prompting techniques for better responses

**Important:** This guide covers installation only. For usage instructions, configuration, and advanced features, refer to the official Open WebUI documentation.

---

## 📄 License

[![License License CCBYSA](https://img.shields.io/badge/License-CC--BY--SA--4.0%20-blue.svg?style=flat-square)](http://creativecommons.org/licenses/by-sa/4.0/)

This file is part of the [**Open WebUI Toolkit**](https://github.com/rex-nihilo/open-webui-toolkit) project.
This textual content is licensed under **CC BY-SA 4.0**.

You are free to:
- **Share**: Copy and redistribute in any medium or format
- **Adapt**: Remix, transform, and build upon the material

Under the following terms:
- **Attribution**: Give appropriate credit
- **ShareAlike**: Distribute under same license
- **No additional restrictions**: Cannot apply legal terms or technological measures that legally restrict others

## 👤 Author

**Rex Nihilo**

- GitHub: [@rex-nihilo](https://github.com/rex-nihilo)
- Project: [Open WebUI Toolkit](https://github.com/rex-nihilo/open-webui-toolkit)
- OpenWebUI: [@rexnihilo](https://openwebui.com/u/rexnihilo)
- Website: [https://rexnihilo.com](https://rexnihilo.com)

## 💖 Support

If you find this work helpful:

- ⭐ **Star the repository** on GitHub
- 📢 **Share** with other Open WebUI users
- 💬 **Contribute** your own variations and tips
- 📝 **Write a blog post** about your Open WebUI use case
- 🎥 **Create a tutorial** video (credit this guide)
- ☕ **Buy me a coffee** (or a beer)

---

**Licence:** [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/) | **Last updated:** November 2025 by **Rex Nihilo**
