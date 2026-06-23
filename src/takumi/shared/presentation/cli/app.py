import json

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from takumi import __version__
from takumi.contexts.orchestration.workflow import run_workflow
from takumi.contexts.product_owner.agent import run_po_agent
from takumi.shared.config.settings import get_settings
from takumi.shared.llm.factory import get_llm

app = typer.Typer(
    name="takumi",
    help="AI-powered multi-agent software engineering system.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def version() -> None:
    """Show the Takumi version."""
    console.print(f"takumi {__version__}")


@app.command()
def config() -> None:
    """Show resolved configuration (API keys masked)."""
    settings = get_settings()
    table = Table(title="Takumi Configuration", show_header=True)
    table.add_column("Setting", style="cyan")
    table.add_column("Value")

    for key, value in settings.masked_config().items():
        table.add_row(key, value)

    console.print(table)


@app.command()
def run(
    task: str = typer.Argument(..., help="Development task for the agent team."),
) -> None:
    """Run the multi-agent workflow for a development task."""
    settings = get_settings()
    llm = get_llm(settings)

    console.print(Panel(f"[bold]Task:[/bold] {task}", title="Takumi", border_style="blue"))

    with console.status("[bold green]Running agent workflow..."):
        result = run_workflow(llm, task)

    for agent_name, output in result["artifacts"].items():
        console.print(
            Panel(
                output,
                title=f"[bold]{agent_name.title()}[/bold]",
                border_style="green",
            )
        )

    console.print("[bold green]Workflow completed.[/bold green]")


@app.command()
def po(
    feature: str = typer.Argument(..., help="Raw feature description for the Product Owner agent."),
) -> None:
    """Generate epics and user stories from a feature description."""
    settings = get_settings()
    llm = get_llm(settings)

    console.print(
        Panel(f"[bold]Feature:[/bold] {feature}", title="Product Owner", border_style="blue")
    )

    with console.status("[bold green]Generating backlog..."):
        artifact = run_po_agent(llm, feature)

    output = json.dumps(artifact.model_dump(), indent=2)
    console.print(
        Panel(
            Syntax(output, "json", theme="monokai"),
            title="[bold]Backlog Artifact[/bold]",
            border_style="green",
        )
    )
    console.print("[bold green]Done.[/bold green]")
