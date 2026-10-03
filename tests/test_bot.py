import os
import unittest
from unittest.mock import patch

with patch.dict(
    os.environ,
    {"TELEGRAM_BOT_TOKEN": "test-token", "OPENAI_API_KEY": "test-key"},
):
    import bot


class BotClientTests(unittest.TestCase):
    def test_default_endpoint_is_not_overridden(self):
        with patch.object(bot, "AsyncOpenAI") as client_factory:
            bot.create_openai_client("openai-key")

        client_factory.assert_called_once_with(api_key="openai-key")

    def test_explicit_openai_compatible_endpoint_is_used(self):
        with patch.object(bot, "AsyncOpenAI") as client_factory:
            bot.create_openai_client("proxy-key", "http://localhost:3001/v1")

        client_factory.assert_called_once_with(
            api_key="proxy-key", base_url="http://localhost:3001/v1"
        )


if __name__ == "__main__":
    unittest.main()
