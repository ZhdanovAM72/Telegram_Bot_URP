# Константы проекта
MAX_MESSAGE_SYMBOLS = 500
ES = 'ООО "Газпромнефть Энергосистемы"'
ITS = 'ООО "Инженерно-технологический сервис"'
NR = 'ООО "Нефтесервисные решения"'
NNGGF = 'ООО "ННГГФ"'
ST = 'ООО "Газпромнефть Сервисные технологии"'
NO_ADMIN_RIGHTS = 'У Вас нет административных прав!'
NO_MODERATOR_RIGHTS = 'У Вас нет прав модератора!'
NOT_REGISTERED = 'Вы не зарегистрированны в системе!'
ADMIN_COMMANDS = (
    '''
    Для Вас доступны следующие команды:
    \n1. Выгрузка, базы данных.\n/dbinfo
    \n2. Выгрузка лог-файлов.\n/logs_info
    \n3.1 Создание учетных записей для регистрации новых сотрудников.
    \n\t/create_user_data, ivanov.ii, Иванов Иван Иванович
    \n3.2 Загрузка списка сотрудников из файла excel:
    \n\tсначала вводим команду - /add_new_users
    \n\tпосле запроса от бота отправляем файл в чат
    \n4. Удаление пользователя по email.\n/delete_email user_email
    \n5. Назначение администратора.\n/create_admin user_email
    \n6. Удаление прав администратора.\n/delete_admin user_email
    \n7. Назначение модератора.\n/create_moderator user_email
    \n8. Удаление прав модератора.\n/delete_moderator user_email
    \n9. Заготовленное сообщение об обновлении чат-бота:\n/updates
    \n10. Массовое сообщение пользователям чат-бота:\n/massmess your_message_here
    '''
)
MODERATOR_COMMANDS = (
    '''
    Для Вас доступны следующие команды:
    \n1. Выгрузка, базы данных и лог-файлов.\n/dbinfo
    \n2. Создание учетных записей для регистрации новых сотрудников.
    \n/create_user_data, ivanov.ii, Иванов Иван Иванович
    \n3. Удаление пользователя по email.\n/delete_email user_email
    \n4. Назначение модератора.\n/create_moderator user_email
    \n5. Удаление прав модератора.\n/delete_moderator user_email
    '''
)

# Большие сообщения в меню чат-бота
ABOUT_NTK = (
    'Научно – техническая конференция – это мероприятие, '
    'проводящееся на ежегодной основе, с целью продвижения '
    'научного потенциала молодых специалистов и работников компании,'
    ' а также с целью обмена опытом между молодыми специалистами '
    'дочерних обществ и совместных предприятий, демонстрации '
    'инноваций, апробирования новых технологий и процессов, '
    'укрепления имиджа компании и повышения заинтересованности '
    'работников в совершенствовании профессиональных навыков.\n'
    '\nНТК проводится в 3 этапа:\n'
    'Локальная НТК\n'
    'НТК Блока разведки и добычи\n'
    'Корпоративный финал НТК \n'
    '\nПочему стоит принять участие в конференции?\n'
    '-  Возможность раскрыть потенциал и заявить о себе;\n'
    '-  Возможность повысить экспертизу в рамках направления своей '
    'деятельности;\n'
    '-  Возможность принять участие в дальнейшей реализации '
    'проектов;\n'
    '-  Возможность найти единомышленников.'
)
