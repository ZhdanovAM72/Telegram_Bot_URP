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
from bot.content_processor.text.application_forms.transfer_vacation import TransferExtensionVacation
from bot.content_processor.text.application_forms.vacation_without_pay import VacationWithoutPay
from bot.content_processor.text.application_forms.cancellation_vacation import CancellationRecallVacation
from bot.content_processor.text.application_forms.other_types_vacation import OtherTypesVacation
from bot.content_processor.text.application_forms.change_employment_contract import ChangeEmploymentContract
from bot.content_processor.text.application_forms.working_hours import WorkingHours
from bot.content_processor.text.application_forms.transfers import Transfers
from bot.content_processor.text.application_forms.extra_work import ExtraWork
from bot.content_processor.text.application_forms.bank_details import BankDetails


class ApplicationFormsBase(
    ApplicationForms, AdvanceReport, WorkSchedule, TimeTracking, DayOffWorking, DelayTransit,
    GovernmentDuties, BirthChild, TerminationEmploymentContract, VacationRegistration, BloodDonation,
    TransferExtensionVacation, VacationWithoutPay, CancellationRecallVacation, OtherTypesVacation,
    ChangeEmploymentContract, WorkingHours, Transfers, ExtraWork, BankDetails,
):
    pass
