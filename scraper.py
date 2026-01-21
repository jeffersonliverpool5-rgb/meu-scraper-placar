name: Atualizar Placares AiScore

on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do código
        uses: actions/checkout@v3

      - name: Instalar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Instalar Selenium e Chrome
        run: |
          python -m pip install --upgrade pip
          pip install selenium webdriver-manager
          sudo apt-get update
          sudo apt-get install google-chrome-stable

      - name: Executar Scraper
        run: python scraper.py

      - name: Salvar alterações no GitHub
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"
          git add placares.txt
          git commit -m "Atualizando placares" || exit 0
          git push
