"""Mathematics app exercise."""

from mathematics.exercise.calculation import CalcExercise
from mathematics.models import MathematicsAnalytic

EXERCISES = {
    'add': CalcExercise,
    'sub': CalcExercise,
    'mul': CalcExercise,
}
