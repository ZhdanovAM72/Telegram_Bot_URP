from bot.content_processor.text.application_forms.main_forms import ApplicationForms
from bot.content_processor.text.application_forms.advance_report import AdvanceReport
from bot.content_processor.text.application_forms.time_tracking import TimeTracking
from bot.content_processor.text.application_forms.work_schedule import WorkSchedule


class ApplicationFormsBase(ApplicationForms, AdvanceReport, WorkSchedule, TimeTracking):
    pass
