"""User points."""

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction

from users.models import UserApp


class Transaction(models.Model):
    """Transaction model."""

    class TransactionType(models.TextChoices):
        """Transaction type choices."""

        AWARD = 'award', 'Вознаграждение'
        WRITEOFF = 'writeoff', 'Списание'

    account = models.ForeignKey(
        'UserAccount',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Счет',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        verbose_name='Тип операции',
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время',
    )

    class Meta:
        """Set up transaction."""

        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['transaction_type']),
        ]


class UserAccount(models.Model):
    """User point account model."""

    user = models.OneToOneField(
        UserApp,
        on_delete=models.CASCADE,
        related_name='account',
        verbose_name='Пользователь',
    )
    balance = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Баланс',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    def add_award(self, amount: int) -> Transaction:
        """Add award to user account."""
        if amount <= 0:
            raise ValidationError('Award amount must be positive')

        with transaction.atomic():
            account = UserAccount.objects.select_for_update().get(pk=self.pk)
            account.balance += amount
            account.save()

            return Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type=Transaction.TransactionType.AWARD,
            )

    def write_off(self, amount: int) -> None:
        """Write-off user award."""
        if amount <= 0:
            raise ValidationError('Write-off amount must be positive')

        elif self.balance < amount:
            raise ValueError('Not enough points')

        with transaction.atomic():
            account = UserAccount.objects.select_for_update().get(pk=self.pk)
            account.balance -= amount
            account.save()

            Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type=Transaction.TransactionType.WRITEOFF,
            )


def get_points_balance(user_id: int) -> int:
    """Get user points balance."""
    try:
        balance = UserAccount.objects.get(user=user_id).balance
    except AttributeError:
        balance = 0
    except UserApp.DoesNotExist:
        balance = 0
    return balance
