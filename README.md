# Takumi

AI-powered multi-agent software engineering system that simulates a complete development team to design, build, test, and iterate on software automatically.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Quick start

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env and set your API key (OPENAI_API_KEY or ANTHROPIC_API_KEY)
# Or use Ollama locally — see "Local with Ollama" below

# Verify installation
uv run takumi version
uv run takumi config

# Run the multi-agent workflow
uv run takumi run "Add user authentication with JWT"
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | `openai`, `anthropic`, or `ollama` | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | — |
| `ANTHROPIC_API_KEY` | Anthropic API key | — |
| `OPENAI_MODEL` | OpenAI model name | `gpt-4o` |
| `ANTHROPIC_MODEL` | Anthropic model name | `claude-sonnet-4-20250514` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2` |
| `LOG_LEVEL` | Log level | `INFO` |

## Local with Ollama

Run models locally without cloud API keys:

```bash
# 1. Install and start Ollama (https://ollama.com)
ollama serve

# 2. Pull a model
ollama pull llama3.2

# 3. Configure Takumi
cat >> .env <<'EOF'
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
EOF

# 4. Run
uv run takumi run "Add user authentication with JWT"
```

Other models that work well for coding: `qwen2.5-coder`, `codellama`, `deepseek-r1`.

## Project structure

```
src/takumi/
├── contexts/           # Bounded contexts (domain boundaries)
│   ├── orchestration/  # LangGraph workflow, state, routing
│   └── team/           # Agent roles and configuration
├── shared/             # Cross-cutting kernel and infrastructure
│   ├── config/         # Settings and environment
│   ├── llm/            # LLM provider factory
│   ├── presentation/   # CLI, future API
│   └── tools/          # Development tools (future)
└── main.py             # CLI entrypoint
```

## Development

```bash
uv sync --dev
uv run pytest
uv run ruff check .
```

## Roadmap

- [ ] Real development tools (filesystem, git, shell, test runner)
- [ ] Agent-specific prompts and reasoning
- [ ] Persistent memory and LangGraph checkpoints
- [ ] Integration with sisques-labs agent/prompt services
- [ ] REST API

## License

Private — sisques-labs
