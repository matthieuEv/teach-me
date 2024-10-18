<p align="center">
    <img src="src/assets/logo.png" alt="Logo" width="80" height="80">
</p>

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/matthieuEv/teach-me/python_tests.yml?style=for-the-badge)

# Teach Me

Ask your AI teacher to teach you anything, he will provide you with a video lecture on the topic and a quiz to test your knowledge!

## Example


## Installation

> The project was made and tested on `python@3.12.7`
>
> If you encounter any problems, try switching to this version.

Creating a virtual environment is recommended.
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Install the required packages
```bash
pip install -r requirements.txt
```

You need to copy the `.env.template` file to `.env` and fill in the `NVIDIA_API_KEY` fields, you can get the `Nvidia` token from [here](https://build.nvidia.com/explore/discover).

Also, don't forget to install the `ffmpeg` package on your system.

```bash
# test if ffmpeg is installed
ffmpeg -version

# if not installed

# Linux
sudo apt install ffmpeg

# Mac
brew install ffmpeg

# Windows
choco install ffmpeg
```

## Run "Teach Me"

```bash
python src/main.py
```
