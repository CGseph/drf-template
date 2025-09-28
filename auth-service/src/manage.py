#!/usr/bin/env python
import os
import sys
from pathlib import Path


def main() -> None:
    src_dir = Path(__file__).resolve().parent
    if str(src_dir) not in sys.path:
        sys.path.append(str(src_dir))
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.development"),
    )
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
