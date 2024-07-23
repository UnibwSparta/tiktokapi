# SPARTA TikTok API

![Linting Status](https://github.com/UnibwSparta/tiktokapi/actions/workflows/linting.yaml/badge.svg)
![Test Status](https://github.com/UnibwSparta/tiktokapi/actions/workflows/test.yaml/badge.svg)
![Build Status](https://github.com/UnibwSparta/tiktokapi/actions/workflows/build.yaml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Welcome to the official GitHub repository for the [SPARTA](https://dtecbw.de/sparta) TikTok API, a powerful Python implementation to interact with TikTok's Research API in a robust and efficient manner.

## 🚀 Features

- Methods for gathering video metadata, users and more.
- Asynchronous API calls support.
- Efficient error handling.
- Comprehensive documentation with usage examples.

## 📦 Installation

We recommend using [Poetry](https://python-poetry.org/docs/) for managing the project dependencies. If you don't have Poetry installed, check their [official documentation](https://python-poetry.org/docs/#installation) for guidance.

To install the SPARTA TikTok API via Poetry:

```bash
poetry add sparta-tiktokapi
```

or to install it via pip:

```bash
pip3 install sparta-tiktokapi
```

## 📝 Quick Start

Here's a simple example to get you started:

```python
from datetime import date
from sparta.tiktokapi.access import create_bearer_token
from sparta.tiktokapi.videos.videos import query_videos

client_key = "xxxxxxxxxxx"
client_secret = "xxxxxxxxxxx"

bearer_token = create_bearer_token(client_key, client_secret)
query = {"or": [{"operation": "IN", "field_name": "username", "field_values": ["@tiktok"]}]}
start = date(2023, 1, 1)
end = date(2023, 1, 31)

async for video in query_videos(bearer_token, query, start, end, max_count=100):
    print(video)
```

For in-depth methods and examples, consult our [official documentation](https://unibwsparta.github.io/tiktokapi/index.html).

## 🛠 Development & Contribution
Clone the Repo:

```bash
git clone https://github.com/UnibwSparta/tiktokapi.git
cd tiktokapi
```

Install Dependencies:
```bash
poetry install
```

Submit Your Changes: Make your improvements and propose a Pull Request!

## 🧪 Testing
Tests are powered by pytest. Execute tests with:

```bash
poetry run pytest tests/
```

## ❓ Support & Feedback
Issues? Feedback? Use the [GitHub issue tracker](https://github.com/UnibwSparta/tiktokapi/issues).

## 📜 License
MIT License. View [LICENSE](https://github.com/UnibwSparta/tiktokapi/blob/main/LICENSE) for details.

## Project SPARTA
SPARTA is an interdisciplinary research project at the UniBw M. The Chair of Political Science is responsible for managing the project. The project is funded by dtec.bw (Digitalization and Technology Research Center of the Bundeswehr). dtec.bw is funded by the European Union - NextGenerationEU.
