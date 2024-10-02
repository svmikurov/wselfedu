"""Points manager."""

from mathematics.models import MathematicsAnalytic
from users.models import Points, UserApp


def get_points_balance(user_id: int) -> int:
    """Get user points balance."""
    try:
        balance = (
            Points.objects.filter(
                user=UserApp.objects.get(pk=user_id),
            )
            .last()
            .balance
        )
    except AttributeError:
        balance = 0
    except UserApp.DoesNotExist:
        balance = 0
    return balance


class PointsManager:
    """Points manager class."""

    @staticmethod
    def get_number_points(user_id: int) -> int:
        """Get points to award for specific user.

        The amount of reward points may differ among users.

        :param int user_id: The user ID to whom points are awarded.
        :return: The number of points as a reward for
         success task solution.
        :rtype: int
        """
        # Temporary number_points is fixed number
        number_points = 40
        return number_points

    @classmethod
    def _add_points(
        cls,
        *,
        user_id: int,
        task_id: int,
    ) -> None:
        """Add points to the user's points balance.

        Adds user points to
        :py:class:`~users.models.points.Points` model.
        """
        user = UserApp.objects.get(pk=user_id)
        task = MathematicsAnalytic.objects.get(pk=task_id)

        balance = get_points_balance(user_id)
        points = cls.get_number_points(user_id)
        updated_balance = balance + points

        query = Points.objects.create(
            user=user,
            task=task,
            award=points,
            balance=updated_balance,
        )
        query.save()
