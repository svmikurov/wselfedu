"""Test points manager module."""

from django.test import TestCase

from task.models import MathematicalExercise, Points
from task.points_mng import PointsManager
from users.models import UserModel


class TestAddPoint(TestCase):
    """Test add points to Points DB table class.
    """

    user_id = 1

    @classmethod
    def setUpTestData(cls):
        """Setup test data."""
        cls.user1 = UserModel.objects.create(
            username='user1',
        )
        cls.user1_id = cls.user1.pk
        cls.user2 = UserModel.objects.create(
            username='user2',
        )
        cls.user2_id = cls.user2.pk
        cls.task = MathematicalExercise.objects.create(
            user=cls.user1,
            calculation_type='mul',
            first_operand=2,
            second_operand=3,
            user_solution=6,
            is_correctly=True,
            solution_time=3,
        )
        cls.task = MathematicalExercise.objects.create(
            user=cls.user1,
            calculation_type='mul',
            first_operand=3,
            second_operand=3,
            user_solution=9,
            is_correctly=True,
            solution_time=3,
        )
        cls.task = MathematicalExercise.objects.create(
            user=cls.user2,
            calculation_type='mul',
            first_operand=4,
            second_operand=3,
            user_solution=12,
            is_correctly=True,
            solution_time=3,
        )
        super().setUpTestData()

    def test_add_points(self):
        """Test add points to database."""
        points_mng = PointsManager()
        points_mng._add_points(user_id=self.user1_id, task_id=1)
        balance = Points.objects.filter(user=self.user1).last().balance
        assert balance == 40

        # balance is accumulating
        points_mng._add_points(user_id=self.user1_id, task_id=2)
        balance = Points.objects.filter(user=self.user1).last().balance
        assert balance == 80

    def test_add_points_to_any_users(self):
        """Test adding points for multiple users."""
        points_mng = PointsManager()
        points_mng._add_points(user_id=self.user1_id, task_id=1)
        points_mng._add_points(user_id=self.user2_id, task_id=3)

        user1_balance = Points.objects.filter(user=self.user1).last().balance
        assert user1_balance == 40

        user2_balance = Points.objects.filter(user=self.user2).last().balance
        assert user2_balance == 40
