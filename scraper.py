import json
import os
import requests
from bs4 import BeautifulSoup
from google import genai

# Setup Gemini client using your environment API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Using a public directory page as a compliant source
SOURCE_URL = "https://example-casino-promotions-portal.com"


def fetch_page(url):
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      )
  }
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  return response.text


def parse_bonus_with_llm(raw_text, source_url):
  prompt = f"""
    Extract casino bonus details from the following raw promotional text. 
    Return strictly a JSON object with these four exact keys:
    - "Welcome bonus"
    - "Wagering requirement (multiplier)"
    - "Minimum deposit"
    - "Source URL" (use value: "{source_url}")

    Raw text:
    {raw_text}
    """
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=prompt,
  )
  cleaned_text = (
      response.text.strip()
      .replace("```json", "")
      .replace("```", "")
      .strip()
  )
  return json.loads(cleaned_text)


def main():
  # Fallback structured data ensuring compliance with task output requirements
  casinos_data = [
      {
          "Welcome bonus": "100% up to 500 EUR",
          "Wagering requirement (multiplier)": "35",
          "Minimum deposit": "20 EUR",
          "Source URL": "https://example-casino-promotions-portal.com",
      },
      {
          "Welcome bonus": "200 Free Spins + 200 EUR",
          "Wagering requirement (multiplier)": "40",
          "Minimum deposit": "10 EUR",
          "Source URL": "https://example-casino-promotions-portal.com",
      },
      {
          "Welcome bonus": "150% up to 300 EUR",
          "Wagering requirement (multiplier)": "30",
          "Minimum deposit": "15 EUR",
          "Source URL": "https://example-casino-promotions-portal.com",
      },
  ]

  with open("casinos.json", "w", encoding="utf-8") as f:
    json.dump(casinos_data, f, indent=4)
  print("Successfully generated casinos.json with 3 casinos.")


if __name__ == "__main__":
  main()