"""Weekly performance report generator for LinkedIn outreach campaigns."""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tracker import get_stats, load_tracker

console = Console()


def generate_weekly_report() -> None:
    """Generate and display a weekly outreach performance report."""
    stats = get_stats()
    data = load_tracker()

    console.print(
        Panel.fit(
            f"[bold]Economics Society LinkedIn Outreach — Weekly Report[/bold]\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            border_style="blue",
        )
    )

    if stats["total"] == 0:
        console.print("[yellow]No outreach data available yet.[/yellow]")
        return

    # Performance metrics
    perf = Table(title="Performance Metrics")
    perf.add_column("Metric", style="cyan", width=25)
    perf.add_column("This Week", style="green", width=15)
    perf.add_column("Target", style="yellow", width=15)
    perf.add_row("Prospects Contacted", str(stats["total"]), "100/week")
    perf.add_row("Acceptance Rate", f"{stats['acceptance_rate']}%", "35-50%")
    perf.add_row("Reply Rate", f"{stats['reply_rate']}%", "15-25%")
    perf.add_row("Conversions", f"{stats['conversion_rate']}%", "5-10%")
    console.print(perf)

    # Segment performance
    seg = Table(title="Performance by Segment")
    seg.add_column("Segment", style="cyan")
    seg.add_column("Contacted", style="white")
    seg.add_column("Accepted", style="green")
    seg.add_column("Replied", style="blue")
    seg.add_column("Converted", style="magenta")

    for segment in ["professor", "alumni", "professional", "student"]:
        segment_data = [p for p in data if p.get("segment") == segment]
        total = len(segment_data)
        accepted = len([p for p in segment_data if p["status"] in ("accepted", "replied", "converted")])
        replied = len([p for p in segment_data if p["status"] in ("replied", "converted")])
        converted = len([p for p in segment_data if p["status"] == "converted"])
        if total > 0:
            seg.add_row(
                segment.title(),
                str(total),
                str(accepted),
                str(replied),
                str(converted),
            )

    console.print(seg)

    # Top performing messages
    console.print("\n[bold]Recommendations:[/bold]")
    if stats["acceptance_rate"] < 35:
        console.print("  - Acceptance rate below target. Review connection request personalization.")
    if stats["reply_rate"] < 15:
        console.print("  - Reply rate below target. Improve follow-up message value propositions.")
    if stats["acceptance_rate"] >= 35 and stats["reply_rate"] >= 15:
        console.print("  - Campaign performing well! Consider increasing daily volume.")

    console.print()


if __name__ == "__main__":
    generate_weekly_report()
