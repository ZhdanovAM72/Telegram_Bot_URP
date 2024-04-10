from bot.content_processor.text.main_menu import MainMenu
from bot.content_processor.text.about_company import AboutCompany
from bot.content_processor.text.news_feed import NewsFeed
from bot.content_processor.text.employees_services import EmployeesServices
from bot.content_processor.text.adaptation import Adaptation
from bot.content_processor.text.dms import DmsAndRvl
from bot.content_processor.text.career_development import CareerDevelopment
from bot.content_processor.text.talent_management_cycle import TalentManagementCycle


class BaseTextMenu(
    MainMenu, AboutCompany, NewsFeed, EmployeesServices,
    Adaptation, DmsAndRvl, CareerDevelopment, TalentManagementCycle
):
    pass
