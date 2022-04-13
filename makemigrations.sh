#!/usr/bin/env sh

# First argument will be the message
alembic revision --autogenerate -m $1