"""Defines abstract base reward model."""

from typing import TypeVar

from django.db import models

from .task import BaseTask

BaseTaskT = TypeVar('BaseTaskT', bound=BaseTask)
BaseRewardT = TypeVar('BaseRewardT', bound='BaseReward')


class BaseReward(models.Model):
    """Abstract base model for rewards with Generic ForeignKey."""

    reward = models.PositiveSmallIntegerField()
    task = BaseTaskT

    class Meta:
        """Class configuration."""

        abstract = True
