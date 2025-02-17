"""The mathematical calculate exercise."""

import os

from dotenv import load_dotenv

load_dotenv('.env_vars/.env.wse')

POINTS_FOR_THE_TASK = int(os.getenv('POINTS_FOR_THE_TASK', 0))
"""The number of points awarded for a correctly completed task,
by default (`int`).
"""
MAX_POINTS_BALANCE = int(os.getenv('MAX_POINTS_BALANCE', 0))
"""The maximum allowed accumulation of points on the user's balance.
(`int`)
"""
