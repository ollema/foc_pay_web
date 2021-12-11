#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":

    certs = [
        ("SWISH_PROD_CERT", ".certs/prod/cert.pem"),
        ("SWISH_PROD_KEY", ".certs/prod/swish.key"),
        ("SWISH_TEST_CERT", ".certs/test/cert.pem"),
        ("SWISH_TEST_KEY", ".certs/test/swish.key"),
    ]

    for cert_env_name, cert_file_path in certs:
        if not os.path.exists(cert_file_path):
            if cert_env_name not in os.environ:
                raise RuntimeError(f"{cert_env_name} not set and {cert_file_path} not present")
            else:
                with open(cert_file_path, "w") as f:
                    f.write(os.environ[cert_env_name])

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment "
                "variable? Did you forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # foc_pay_web directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "foc_pay_web"))

    execute_from_command_line(sys.argv)
