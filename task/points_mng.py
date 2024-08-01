"""Points manager modul."""

from task.models import Points, MathematicalExercise
from users.models import UserModel


class PointsManager:
    """Points manager class.
    """

    @staticmethod
    def get_number_points(user_id: int) -> int:
        """Get number points for specific user.

        The amount of reward points may differ among users.

        Parameters
        ----------
        user_id : `id`
            The user id to whom points are awarded.

        Return
        ------
        number_points : `int`
            The number of points as a reward for success task solution.
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
        """Add points to the user's account.

        Adds user points to :ref:`Points <_Points>` DB table.
        """
        user = UserModel.objects.get(pk=user_id)
        task = MathematicalExercise.objects.get(pk=task_id)
        # The user may not have any records in the table.
        try:
            balance = Points.objects.filter(user=user).last().balance
        except AttributeError:
            balance = 0

        points = cls.get_number_points(user_id)
        updated_balance = balance + points

        query = Points.objects.create(
            user=user,
            task=task,
            award=points,
            balance=updated_balance,
        )
        query.save()
