# Scrapy-MTK

This project was done as an extension to the Django for Everybody course (https://www.dj4e.com).
Scrape the site https://www.cambridge-mt.com/ms/mtk/ with educational purposes.

## Clone

```bash
git clone https://github.com/ignacio-nava/Scrapy-MTK.git
```

## Usage

```bash
cd Scrapy-MTK/
python3 -m venv "your_venv"
source "your_venv"/bin/activate
pip install -r requirements.txt
cd dj4eProject/
mkdir models_files
scrapy crawl multitracks
```

After that, you should have three CSV files in *models_files/*
