"""
Custom MySQL backend that bypasses version check for compatibility.
This is a workaround for Python 3.14 + older MariaDB versions.
"""

from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper


class DatabaseWrapper(MySQLDatabaseWrapper):
    """Custom MySQL wrapper that skips version check."""
    
    def check_database_version_supported(self):
        """Override to skip database version check."""
        # Skip the version check to allow MariaDB 10.4
        pass
