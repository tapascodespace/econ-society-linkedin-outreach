"""Prospect research module using Claude and Brave Search APIs."""

import argparse
import json

import pandas as pd
import requests
from anthropic import Anthropic

from config import ANTHROPIC_API_KEY, BRAVE_SEARCH_API_KEY, CLAUDE_MODEL

client = Anthropic(api_key=ANTHROPIC_API_KEY)

RESEARCH_SYSTEM_PROMPT = """You are a research assistant for a university Economics Society.
Given information about a LinkedIn prospect, identify:

1. **Recent Activity Hooks**
   - Posts they've written (topics, opinions expressed)
   - Comments on others' posts (what caught their attention)
   - Articles shared (what they find valuable)

2. **Professional Context**
   - Current role and responsibilities
   - Recent news (publications, promotions, company updates)
   - Areas of expertise relevant to economics

3. **Connection Points**
   - Shared interests in economics topics
   - University affiliations
   - Mutual connections or events

4. **Communication Style**
   - Formal vs casual tone
   - Academic vs industry-focused language
   - Topics they engage with most

Return a JSON object with these categories.
Only include REAL information—never fabricate details.
If you can't find something, say "Not found" rather than guessing."""


def search_prospect(name: str, company: str) -> str:
    """Search for public information about a prospect using Brave Search."""
    query = f"{name} {company} LinkedIn economics"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_SEARCH_API_KEY,
    }
    params = {"q": query, "count": 5}

    try:
        resp = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json().get("web", {}).get("results", [])
        return "\n".join(
            f"- {r.get('title', '')}: {r.get('description', '')}" for r in results
        )
    except requests.RequestException as e:
        print(f"Search error for {name}: {e}")
        return "No search results available."


def research_prospect(name: str, company: str, title: str, segment: str) -> dict:
    """Research a single prospect using Claude."""
    search_context = search_prospect(name, company)

    user_prompt = f"""Research this prospect for our Economics Society outreach:

Name: {name}
Company/Organization: {company}
Title: {title}
Segment: {segment}

Public search results:
{search_context}

Provide structured research for crafting a personalized LinkedIn message.
Focus on finding genuine connection points related to economics, 
academia, or professional interests that align with our society's mission."""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=RESEARCH_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    try:
        research_text = response.content[0].text
        return json.loads(research_text)
    except (json.JSONDecodeError, IndexError):
        return {"raw_research": response.content[0].text if response.content else ""}


def research_all_prospects(input_csv: str, output_json: str) -> None:
    """Research all prospects from a CSV file and save results."""
    df = pd.read_csv(input_csv)
    results = []

    for _, row in df.iterrows():
        print(f"Researching {row['name']} at {row['company']}...")
        research = research_prospect(
            name=row["name"],
            company=row["company"],
            title=row["title"],
            segment=row["segment"],
        )
        results.append(
            {
                "name": row["name"],
                "company": row["company"],
                "title": row["title"],
                "linkedin_url": row.get("linkedin_url", ""),
                "segment": row["segment"],
                "research": research,
            }
        )

    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Research complete. {len(results)} prospects saved to {output_json}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Research LinkedIn prospects")
    parser.add_argument("--input", required=True, help="Input CSV file path")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    research_all_prospects(args.input, args.output)
