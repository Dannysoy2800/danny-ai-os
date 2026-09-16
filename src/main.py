"""Main entry point for Danny AI OS"""

import sys
from typing import Optional
from src.core.logger import setup_logger
from src.core.config import settings
from src.agents.manager import ManagerAgent
from src.core.exceptions import DannyAIOSError

logger = setup_logger(__name__)


def main(message: Optional[str] = None) -> int:
    """Main application entry point

    Args:
        message: Optional message to process

    Returns:
        Exit code
    """
    try:
        logger.info(f"Starting {settings.app_name} v{settings.app_version}")
        logger.info(f"Environment: {settings.environment}")
        logger.info(f"Debug mode: {settings.debug}")

        # Initialize agent
        agent = ManagerAgent()

        # Execute with provided message or default
        test_message = message or "Hello Danny AI OS!"
        logger.info(f"Executing with message: {test_message}")

        result = agent.execute(test_message)

        logger.info(f"Execution completed successfully")
        logger.info(f"Result: {result}")

        print(f"\n✅ Success!\nResult: {result}")
        return 0

    except DannyAIOSError as e:
        logger.error(f"Application error: {str(e)}")
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n❌ Unexpected error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
