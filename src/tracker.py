"""Campaign tracking and analytics for LinkedIn outreach."""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

DATA_DIR = Path(__file__).parent.parent / "data"
TRACKER_FILE = DATA_DIR / "tracker.json"


def load_tracker() -> list[dict]:
    """Load the outreach tracker data."""
    if TRACKER_FILE.exists():
        with open(TRACKER_FILE) as f:
            return json.load(f)
    return []


def save_tracker(data: list[dict]) -> None:
    """Save the outreach tracker data."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def add_prospect(
    name: str,
    company: str,
    title: str,
    segment: str,
    linkedin_url: str = "",
) -> None:
    """Add a new prospect to the tracker."""
    data = load_tracker()
    prospect = {
        "name": name,
        "company": company,
        "title": title,
        "segment": segment,
        "linkedin_url": linkedin_url,
        "status": "queued",
        "messages_sent": [],
        "created_at": datetime.now().isoformat(),
        "notes": "",
    }
    data.append(prospect)
    save_tracker(data)
    console.print(f"[green]Added {name} to tracker[/green]")


def update_status(name: str, status: str, note: str = "") -> None:
    """Update prospect status. Valid statuses: queued, sent, accepted, replied, converted."""
    valid_statuses = {"queued", "sent", "accepted", "replied", "converted", "declined"}
    if status not in valid_statuses:
        console.print(f"[red]Invalid status. Choose from: {valid_statuses}[/red]")
        return

    data = load_tracker()
    for prospect in data:
        if prospect["name"] == name:
            prospect["status"] = status
            if note:
                prospect["notes"] = note
            save_tracker(data)
            console.print(f"[green]Updated {name} to {status}[/green]")
            return

    console.print(f"[red]Prospect {name} not found[/red]")


def log_message(name: str, message_type: str, content: str) -> None:
    """Log a sent message for a prospect."""
    data = load_tracker()
    for prospect in data:
        if prospect["name"] == name:
            prospect["messages_sent"].append(
                {
                    "type": message_type,
                    "content": content,
                    "sent_at": datetime.now().isoformat(),
                }
            )
            if prospect["status"] == "queued":
                prospect["status"] = "sent"
            save_tracker(data)
            console.print(f"[green]Logged {message_type} for {name}[/green]")
            return

    console.print(f"[red]Prospect {name} not found[/red]")


def get_stats() -> dict:
    """Calculate outreach statistics."""
    data = load_tracker()
    if not data:
        return {"total": 0}

    df = pd.DataFrame(data)
    status_counts = df["status"].value_counts().to_dict()
    segment_counts = df["segment"].value_counts().to_dict()

    total = len(data)
    accepted = status_counts.get("accepted", 0) + status_counts.get("replied", 0) + status_counts.get("converted", 0)
    replied = status_counts.get("replied", 0) + status_counts.get("converted", 0)
    converted = status_counts.get("converted", 0)

    return {
        "total": total,
        "by_status": status_counts,
        "by_segment": segment_counts,
        "acceptance_rate": round(accepted / total * 100, 1) if total else 0,
        "reply_rate": round(replied / total * 100, 1) if total else 0,
        "conversion_rate": round(converted / total * 100, 1) if total else 0,
    }


def display_dashboard() -> None:
    """Display a rich console dashboard of outreach stats."""
    stats = get_stats()

    if stats["total"] == 0:
        console.print("[yellow]No prospects tracked yet.[/yellow]")
        return

    console.print("\n[bold]Economics Society LinkedIn Outreach Dashboard[/bold]\n")

    # Summary table
    summary = Table(title="Campaign Summary")
    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", style="green")
    summary.add_row("Total Prospects", str(stats["total"]))
    summary.add_row("Acceptance Rate", f"{stats['acceptance_rate']}%")
    summary.add_row("Reply Rate", f"{stats['reply_rate']}%")
    summary.add_row("Conversion Rate", f"{stats['conversion_rate']}%")
    console.print(summary)

    # Status breakdown
    status_table = Table(title="Status Breakdown")
    status_table.add_column("Status", style="cyan")
    status_table.add_column("Count", style="green")
    for status, count in stats.get("by_status", {}).items():
        status_table.add_row(status, str(count))
    console.print(status_table)

    # Segment breakdown
    segment_table = Table(title="By Segment")
    segment_table.add_column("Segment", style="cyan")
    segment_table.add_column("Count", style="green")
    for segment, count in stats.get("by_segment", {}).items():
        segment_table.add_row(segment, str(count))
    console.print(segment_table)


if __name__ == "__main__":
    display_dashboard()
