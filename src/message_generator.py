"""AI-powered message generation for LinkedIn outreach."""

import argparse
import json

from anthropic import Anthropic

from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    SEGMENTS,
    SOCIETY_DESCRIPTION,
    SOCIETY_NAME,
)

client = Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_connection_request(prospect: dict) -> dict:
    """Generate a personalized connection request (max 300 chars)."""
    segment = prospect["segment"]
    segment_config = SEGMENTS.get(segment, SEGMENTS["professional"])

    prompt = f"""Write a LinkedIn connection request for this prospect.
You are reaching out on behalf of {SOCIETY_NAME}: {SOCIETY_DESCRIPTION}

Prospect:
- Name: {prospect['name']}
- Title: {prospect['title']}
- Company: {prospect['company']}
- Segment: {segment}

Research:
{json.dumps(prospect.get('research', {}), indent=2)}

CONSTRAINTS:
- Maximum 300 characters (including spaces) — this is a hard limit
- Tone: {segment_config['tone']}
- Focus: {segment_config['focus']}
- Reference ONE specific thing from their activity or background
- End with a reason to connect, not a pitch
- No salesy language, no generic flattery
- Sound like a real student, not a bot

Write 3 options ranked by quality. Return as JSON:
{{"messages": [{{"text": "...", "hook": "what personalization angle was used", "char_count": N}}]}}"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        return json.loads(response.content[0].text)
    except (json.JSONDecodeError, IndexError):
        return {"raw": response.content[0].text if response.content else ""}


def generate_followup(prospect: dict, original_message: str, day: int) -> dict:
    """Generate a follow-up message based on sequence stage."""
    segment = prospect["segment"]
    segment_config = SEGMENTS.get(segment, SEGMENTS["professional"])

    if day <= 3:
        stage = "first_followup"
        instruction = (
            "Thank them for connecting (briefly). Expand on the topic "
            "from the connection request. Offer specific value. "
            "End with a soft question, not a meeting request."
        )
    elif day <= 7:
        stage = "value_message"
        instruction = (
            "Share something genuinely useful—an article, insight, or "
            "resource relevant to their interests. Brief explanation of "
            "why it's relevant to them specifically."
        )
    elif day <= 14:
        stage = "soft_ask"
        instruction = (
            "If they've engaged, suggest a specific next step (attend our "
            "event, join a panel, grab coffee). If no engagement, share "
            "one more piece of value."
        )
    else:
        stage = "graceful_close"
        instruction = (
            "Acknowledge they're busy. Leave the door open. Mention one "
            "upcoming event they might find interesting. No pressure."
        )

    prompt = f"""Write a LinkedIn follow-up message.
You are reaching out on behalf of {SOCIETY_NAME}.

Prospect: {prospect['name']} ({prospect['title']} at {prospect['company']})
Segment: {segment} | Tone: {segment_config['tone']}
Original connection request: "{original_message}"
Sequence stage: {stage} (Day {day})

Research:
{json.dumps(prospect.get('research', {}), indent=2)}

Instructions: {instruction}

Keep under 500 characters. Sound like a real student.
Return as JSON: {{"text": "...", "stage": "{stage}", "char_count": N}}"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        return json.loads(response.content[0].text)
    except (json.JSONDecodeError, IndexError):
        return {"raw": response.content[0].text if response.content else ""}


def generate_all_messages(prospects_json: str, output_json: str) -> None:
    """Generate messages for all researched prospects."""
    with open(prospects_json) as f:
        prospects = json.load(f)

    results = []
    for prospect in prospects:
        print(f"Generating messages for {prospect['name']}...")
        connection_request = generate_connection_request(prospect)

        best_message = ""
        if "messages" in connection_request and connection_request["messages"]:
            best_message = connection_request["messages"][0].get("text", "")

        segment = prospect["segment"]
        sequence_days = SEGMENTS.get(segment, SEGMENTS["professional"])["sequence_days"]

        followups = []
        for day in sequence_days[1:]:
            followup = generate_followup(prospect, best_message, day)
            followups.append({"day": day, "message": followup})

        results.append(
            {
                "prospect": {
                    "name": prospect["name"],
                    "company": prospect["company"],
                    "segment": prospect["segment"],
                },
                "connection_request": connection_request,
                "followups": followups,
            }
        )

    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Messages generated for {len(results)} prospects. Saved to {output_json}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LinkedIn outreach messages")
    parser.add_argument("--prospects", required=True, help="Researched prospects JSON")
    parser.add_argument("--output", required=True, help="Output messages JSON")
    args = parser.parse_args()

    generate_all_messages(args.prospects, args.output)
