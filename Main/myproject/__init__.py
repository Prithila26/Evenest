"""
Django project initialization.

This module configures PyMySQL as the default MySQL driver for Django.
This allows Django to use PyMySQL instead of MySQLdb, which is more
compatible with Vercel and doesn't require C extensions to be compiled.
"""

import pymysql

# Install PyMySQL as the MySQLdb implementation for Django
# This must happen before any Django imports that use the database
pymysql.install_as_MySQLdb()
