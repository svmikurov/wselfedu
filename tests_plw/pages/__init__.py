"""The page representations of Page Object Model testing."""

from tests_plw.pages.about import AboutPage
from tests_plw.pages.foreign import ForeignMainPage
from tests_plw.pages.foreign_category import ForeignCategoryPage
from tests_plw.pages.foreign_create import ForeignCreatePage
from tests_plw.pages.foreign_exercise_params import ForeignExerciseParamsPage
from tests_plw.pages.foreign_list import ForeignListPage
from tests_plw.pages.foreign_source import ForeignSourcePage
from tests_plw.pages.glossary import GlossaryPage
from tests_plw.pages.glossary_category import TermCategoryPage
from tests_plw.pages.glossary_create import TermCreatePage
from tests_plw.pages.glossary_exercise import GlossaryExercisePage
from tests_plw.pages.glossary_list import TermListPage
from tests_plw.pages.glossary_source import TermSourcePage
from tests_plw.pages.home import HomePage
from tests_plw.pages.login import LoginPage
from tests_plw.pages.mathematics import MathPage
from tests_plw.pages.mathematics_exercise_mentor import (
    MathCalculateExercisePage,
)
from tests_plw.pages.mathematics_exercise_params import MathExerciseParamsPage
from tests_plw.pages.mentorship import MentorshipProfilePage
from tests_plw.pages.mobile import MobilePage
from tests_plw.pages.profile import ProfilePage

__all__ = (
    'AboutPage',
    'ForeignCategoryPage',
    'ForeignCreatePage',
    'ForeignExerciseParamsPage',
    'ForeignListPage',
    'ForeignMainPage',
    'ForeignSourcePage',
    'GlossaryExercisePage',
    'GlossaryPage',
    'HomePage',
    'LoginPage',
    'MathCalculateExercisePage',
    'MathExerciseParamsPage',
    'MathPage',
    'MentorshipProfilePage',
    'MobilePage',
    'ProfilePage',
    'RegistrationPage',
    'TermCategoryPage',
    'TermCreatePage',
    'TermListPage',
    'TermSourcePage',
)

from tests_plw.pages.registration import RegistrationPage
