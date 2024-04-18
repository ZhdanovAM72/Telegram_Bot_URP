from bot.content_processor.text.main_menu import MainMenu
from bot.content_processor.text.about_company import AboutCompany
from bot.content_processor.text.news_feed import NewsFeed
from bot.content_processor.text.employees_services import EmployeesServices
from bot.content_processor.text.adaptation import Adaptation
from bot.content_processor.text.dms import DmsAndRvl
from bot.content_processor.text.career_development import CareerDevelopment
from bot.content_processor.text.talent_management_cycle import TalentManagementCycle
from bot.content_processor.text.internship import Internship
from bot.content_processor.text.education import Education
from bot.content_processor.text.youth_policy import YouthPolicy
from bot.content_processor.text.application_forms.base_forms import ApplicationFormsBase


class BaseTextMenu(
    MainMenu, AboutCompany, NewsFeed, EmployeesServices, Education, YouthPolicy,
    Adaptation, DmsAndRvl, CareerDevelopment, TalentManagementCycle, Internship,
    ApplicationFormsBase,
):
    pass
