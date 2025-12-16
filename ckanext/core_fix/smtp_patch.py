"""
SMTP wrapper to handle host:port in server configuration.

This patches smtplib.SMTP to automatically split host:port strings,
fixing TLS handshake issues with AWS SES and other SMTP providers.
"""
from __future__ import annotations

import smtplib
import socket
from urllib.parse import urlparse


class SMTPHostPortWrapper(smtplib.SMTP):
    """
    Wrapper for smtplib.SMTP that handles host:port in the host parameter.

    Some configurations may have the port embedded in the hostname string
    (e.g., "smtp.example.com:587"). This causes TLS handshake failures
    because the SNI (Server Name Indication) includes the port, which is invalid.

    This wrapper automatically splits the host:port and passes them separately.
    """

    # socket._GLOBAL_DEFAULT_TIMEOUT is used as the default timeout value
    def __init__(
        self,
        host="",
        port=0,
        local_hostname=None,
        timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
        source_address=None,
    ):
        """Initialize SMTP connection, automatically parsing host:port if needed."""
        if host and ':' in host and port == 0:
            host, port = self._parse_smtp_server(host)

        super().__init__(host, port, local_hostname, timeout, source_address)

    @staticmethod
    def _parse_smtp_server(smtp_server: str) -> tuple[str, int]:
        """Parse SMTP server that may include port.

        Examples:
            'smtp.example.com' -> ('smtp.example.com', 25)
            'smtp.example.com:587' -> ('smtp.example.com', 587)
            '[::1]:587' -> ('::1', 587)
        """
        default_port = 0

        if '://' not in smtp_server:
            smtp_server = 'smtp://' + smtp_server

        parsed = urlparse(smtp_server)
        host = parsed.hostname
        port = parsed.port or default_port

        if not host:
            raise ValueError(f"Invalid SMTP server: {smtp_server}")

        return host, port
