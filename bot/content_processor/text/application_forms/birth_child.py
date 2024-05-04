from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/baby_born/"
BIRTH_CHILD = "Рождение ребенка"
APPLICATION_MATERNITY_LEAVE = "Ш-14.03.06-13 Заявление об отпуске по беременности и родам_2 круг"
APPLICATION_ARLY_STAGES_PREGNANCY = ("Ш-14.03.06-14 Заявление о выплате пособия "
                                     "за постановку на учет в ранние сроки беременности_2 круг")
APPLICATION_PARENTAL_LEAVE = "Ш-14.03.06-15 Заявление об отпуске по уходу за ребенком до 3х лет"
APPLICATION_BENEFIT_BIRTH_CHILD = "Ш-14.03.06-16 Заявление о выплате единовременного пособия по рождению ребенка_2 круг"
APPLICATION_PAYMENT_CHILD_CARE = "Ш-14.03.06-17 Заявление о выплате пособия по уходу за ребенком до 1.5 лет_2 круг"
APPLICATION_EARLY_LEAVE = "Ш-14.03.05-04 Заявление о досрочном выходе из отпуска по уходу за ребенком_ГПН-ННГГФ"
APPLICATION_MATERIAL_ASSISTANCE = "Заявление ГПН-НС_материальная помощь на рождение"


class BirthChild:

    @staticmethod
    def birth_child_main(message: types.Message) -> types.Message:
        buttons = [
            f'{BIRTH_CHILD} {ES}',
            f'{BIRTH_CHILD} {NR}',
            f'{BIRTH_CHILD} {ST}',
            f'{BIRTH_CHILD} {ITS}',
            f'{BIRTH_CHILD} {NNGGF}',
            '🔙 вернуться в раздел Бланки заявлений',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            BIRTH_CHILD,
            reply_markup=markup,
        )

    @staticmethod
    @contextmanager
    def birth_child_es(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ES/rodi.doc", "rb"),
                "caption": APPLICATION_MATERNITY_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/ranie_rodi.doc", "rb"),
                "caption": APPLICATION_ARLY_STAGES_PREGNANCY,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/posobie_3.doc", "rb"),
                "caption": APPLICATION_PARENTAL_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/premia.doc", "rb"),
                "caption": APPLICATION_BENEFIT_BIRTH_CHILD,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/posobie_1.5.doc", "rb"),
                "caption": APPLICATION_PAYMENT_CHILD_CARE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def birth_child_its(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ITS/rodi.doc", "rb"),
                "caption": APPLICATION_MATERNITY_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/ranie_rodi.doc", "rb"),
                "caption": APPLICATION_ARLY_STAGES_PREGNANCY,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/posobie_3.doc", "rb"),
                "caption": APPLICATION_PARENTAL_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/premia.doc", "rb"),
                "caption": APPLICATION_BENEFIT_BIRTH_CHILD,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/posobie_1.5.doc", "rb"),
                "caption": APPLICATION_PAYMENT_CHILD_CARE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def birth_child_st(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ST/rodi.doc", "rb"),
                "caption": APPLICATION_MATERNITY_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/ranie_rodi.doc", "rb"),
                "caption": APPLICATION_ARLY_STAGES_PREGNANCY,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/posobie_3.doc", "rb"),
                "caption": APPLICATION_PARENTAL_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/premia.doc", "rb"),
                "caption": APPLICATION_BENEFIT_BIRTH_CHILD,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/posobie_1.5.doc", "rb"),
                "caption": APPLICATION_PAYMENT_CHILD_CARE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def birth_child_nnggf(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NNGGF/otpusk_rodi.doc", "rb"),
                "caption": APPLICATION_MATERNITY_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/posobie_ranie.doc", "rb"),
                "caption": APPLICATION_ARLY_STAGES_PREGNANCY,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/otpusk_uhod.doc", "rb"),
                "caption": APPLICATION_PARENTAL_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/premia.doc", "rb"),
                "caption": APPLICATION_BENEFIT_BIRTH_CHILD,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/posobie.doc", "rb"),
                "caption": APPLICATION_PAYMENT_CHILD_CARE,
            },
        )
        document = (f"{PARRENT_PATH}NNGGF/prervat_otpusk.docx",)
        caption = ("Ш-14.03.05-04 Заявление о досрочном выходе из отпуска по уходу за ребенком_ГПН-ННГГФ",)
        return (Documents.send_media_group_without_markup(message.chat.id, documents),
                Documents.send_document_with_markup(message.chat.id, document, caption))

    @staticmethod
    def birth_child_nr(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}NR/premia.docx',)
        caption = (APPLICATION_MATERIAL_ASSISTANCE,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)
