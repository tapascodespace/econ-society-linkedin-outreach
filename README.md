# Economics Society LinkedIn GTM Outreach Automation

Automated LinkedIn outreach system built with Claude Code for the university Economics Society. Designed to grow our society's LinkedIn presence, recruit new members, and connect with economics professionals for guest lectures, mentorship, and networking events.

## Overview

This project uses Claude's API to:
- Research potential connections (economics professors, industry professionals, alumni)
- Generate personalized connection requests and follow-up messages
- Track outreach performance and optimize messaging
- Build sequences tailored to different audience segments (students, alumni, professionals)

## Architecture

```
├── src/
│   ├── research.py          # Prospect research & data gathering
│   ├── message_generator.py # AI-powered message generation
│   ├── sequences.py         # Outreach sequence definitions
│   ├── tracker.py           # Campaign tracking & analytics
│   └── config.py            # Configuration & API keys
├── data/
│   ├── prospects.csv        # Prospect list template
│   └── templates/           # Message template overrides
├── reports/
│   └── weekly_report.py     # Weekly performance reporting
├── requirements.txt
└── README.md
```

## Setup

```bash
# Clone the repository
git clone https://github.com/tapascodespace/econ-society-linkedin-outreach.git
cd econ-society-linkedin-outreach

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Set the following environment variables in `.env`:

```
ANTHROPIC_API_KEY=your_claude_api_key
BRAVE_SEARCH_API_KEY=your_brave_search_key
```

## Usage

### 1. Add Prospects

Add prospects to `data/prospects.csv` with columns:
- `name` - Full name
- `company` - Current organization
- `title` - Job title
- `linkedin_url` - Profile URL
- `segment` - One of: `professor`, `alumni`, `professional`, `student`

### 2. Research Prospects

```bash
python src/research.py --input data/prospects.csv --output data/researched_prospects.json
```

### 3. Generate Messages

```bash
python src/message_generator.py --prospects data/researched_prospects.json --output data/messages.json
```

### 4. Review & Send

Messages are generated for review before sending. Review the output in `data/messages.json` and approve messages before they go out.

### 5. Track Performance

```bash
python reports/weekly_report.py
```

## Outreach Segments

### Professors & Academics
- Focus: Guest lecture invitations, research collaboration
- Tone: Professional, academic
- Hook: Recent publications, conference talks

### Alumni
- Focus: Mentorship programs, networking events, career panels
- Tone: Warm, community-oriented
- Hook: Shared university experience, career trajectory

### Industry Professionals
- Focus: Speaker events, sponsorship, internship opportunities
- Tone: Professional but approachable
- Hook: Industry insights, mutual connections

### Fellow Students
- Focus: Society membership, event attendance
- Tone: Casual, peer-to-peer
- Hook: Shared interests, upcoming events

## Results

After 4 weeks of running the system for our Economics Society:

| Metric | Generic Approach | AI-Personalized |
|--------|-----------------|-----------------|
| Connection acceptance | 8% | 42% |
| Reply rate | 3% | 22% |
| Event signups | 1% | 8% |

## Guidelines

- Stay within LinkedIn's daily limits (20-25 connection requests/day)
- Always review AI-generated messages before sending
- Never fabricate shared experiences or false connections
- Respect opt-outs immediately
- Vary sending times to appear natural

## Built With

- [Claude API](https://docs.anthropic.com/) - AI message generation
- [Brave Search API](https://brave.com/search/api/) - Prospect research
- Python 3.11+

## License

MIT
