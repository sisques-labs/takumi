from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from takumi import __version__
from takumi.config.settings import LLMProvider, Settings
from takumi.llm.factory import get_llm
from takumi.main import app

runner = CliRunner()


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.llm_provider == LLMProvider.OPENAI
    assert settings.openai_model == "gpt-4o"
    assert settings.anthropic_model == "claude-sonnet-4-20250514"


def test_settings_validate_openai_key() -> None:
    settings = Settings(llm_provider=LLMProvider.OPENAI, openai_api_key="")
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        settings.validate_api_key()


def test_settings_validate_anthropic_key() -> None:
    settings = Settings(llm_provider=LLMProvider.ANTHROPIC, anthropic_api_key="")
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        settings.validate_api_key()


def test_settings_masked_config() -> None:
    settings = Settings(openai_api_key="sk-test-key-1234")
    masked = settings.masked_config()
    assert masked["openai_api_key"] == "sk-t...1234"
    assert "(not set)" in masked["anthropic_api_key"]


@patch("langchain_openai.ChatOpenAI")
def test_get_llm_openai(mock_chat_openai: MagicMock) -> None:
    settings = Settings(llm_provider=LLMProvider.OPENAI, openai_api_key="sk-test")
    get_llm(settings)
    mock_chat_openai.assert_called_once_with(
        api_key="sk-test",
        model="gpt-4o",
    )


@patch("langchain_anthropic.ChatAnthropic")
def test_get_llm_anthropic(mock_chat_anthropic: MagicMock) -> None:
    settings = Settings(llm_provider=LLMProvider.ANTHROPIC, anthropic_api_key="sk-ant-test")
    get_llm(settings)
    mock_chat_anthropic.assert_called_once_with(
        api_key="sk-ant-test",
        model_name="claude-sonnet-4-20250514",
    )


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_cli_config() -> None:
    result = runner.invoke(app, ["config"])
    assert result.exit_code == 0
    assert "llm_provider" in result.stdout


@patch("takumi.cli.app.run_workflow")
@patch("takumi.cli.app.get_llm")
def test_cli_run(mock_get_llm: MagicMock, mock_run_workflow: MagicMock) -> None:
    mock_run_workflow.return_value = {
        "task": "test task",
        "messages": [],
        "current_agent": "reviewer",
        "artifacts": {
            "architect": "Design proposal",
            "developer": "Implementation plan",
            "tester": "Test plan",
            "reviewer": "Review notes",
        },
    }

    result = runner.invoke(app, ["run", "test task"])
    assert result.exit_code == 0
    assert "Workflow completed" in result.stdout
    mock_get_llm.assert_called_once()
    mock_run_workflow.assert_called_once()
