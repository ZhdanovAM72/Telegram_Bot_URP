from bot.content_processor.text.application_forms.main_forms import ApplicationForms
from bot.content_processor.text.application_forms.advance_report import AdvanceReport
from bot.content_processor.text.application_forms.time_tracking import TimeTracking
from bot.content_processor.text.application_forms.work_schedule import WorkSchedule
from bot.content_processor.text.application_forms.day_off_working import DayOffWorking
from bot.content_processor.text.application_forms.delay_in_transit import DelayTransit
from bot.content_processor.text.application_forms.government_duties import GovernmentDuties
from bot.content_processor.text.application_forms.birth_child import BirthChild
from bot.content_processor.text.application_forms.termination_contract import TerminationEmploymentContract
from bot.content_processor.text.application_forms.vacation_registration import VacationRegistration
from bot.content_processor.text.application_forms.blood_donation import BloodDonation


class ApplicationFormsBase(
    ApplicationForms, AdvanceReport, WorkSchedule, TimeTracking, DayOffWorking, DelayTransit,
    GovernmentDuties, BirthChild, TerminationEmploymentContract, VacationRegistration, BloodDonation,
):
    pass
