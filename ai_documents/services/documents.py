DOCUMENT_TYPES = {
    "Трудовой договор.docx": {
        "title": "Трудовой договор",
        "fields": [
            {"key": "contract_number", "label": "Номер договора", "hint": "Введите номер договора", "required": True},
            {"key": "city", "label": "Город", "hint": "Введите город", "required": True},
            {"key": "document_date", "label": "Дата документа", "hint": "Например: 01.05.2026", "required": True},
            {"key": "employer_name", "label": "Работодатель", "hint": "Введите наименование работодателя", "required": True},
            {"key": "employer_representative", "label": "Представитель работодателя", "hint": "ФИО и должность подписанта", "required": True},
            {"key": "representative_basis", "label": "Основание полномочий", "hint": "Устав / доверенность", "required": True},
            {"key": "employee_full_name", "label": "Работник", "hint": "ФИО работника", "required": True},
            {"key": "position", "label": "Должность", "hint": "Введите должность", "required": True},
            {"key": "workplace", "label": "Место работы", "hint": "Введите место работы", "required": True},
            {"key": "start_date", "label": "Дата начала работы", "hint": "Например: 05.05.2026", "required": True},
        ]
    },
    "Договор о полной материальной ответственности.docx": {
    "title": "Договор о полной материальной ответственности",
    "fields": [
      {
        "key": "contract_number",
        "label": "Номер договора",
        "hint": "Номер договора",
        "required": True
      },
      {
        "key": "city",
        "label": "Город",
        "hint": "Город составления документа",
        "required": True
      },
      {
        "key": "document_date",
        "label": "Дата документа",
        "hint": "Дата составления документа, например 01.05.2026",
        "required": True
      },
      {
        "key": "employer_name",
        "label": "Работодатель",
        "hint": "Наименование работодателя",
        "required": True
      },
      {
        "key": "employee_full_name",
        "label": "Работник",
        "hint": "ФИО работника",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Доверенность на представительство в Конституционном Суде.docx": {
    "title": "Доверенность на представительство в Конституционном Суде",
    "fields": [
      {
        "key": "city",
        "label": "Город",
        "hint": "Город составления документа",
        "required": True
      },
      {
        "key": "document_date",
        "label": "Дата документа",
        "hint": "Дата составления документа, например 01.05.2026",
        "required": True
      },
      {
        "key": "principal_full_name",
        "label": "Principal full name",
        "hint": "Principal full name",
        "required": True
      },
      {
        "key": "principal_iin",
        "label": "Principal iin",
        "hint": "Principal iin",
        "required": True
      },
      {
        "key": "principal_birth_info",
        "label": "Principal birth info",
        "hint": "Principal birth info",
        "required": True
      },
      {
        "key": "principal_address",
        "label": "Principal address",
        "hint": "Principal address",
        "required": True
      },
      {
        "key": "representative_full_name",
        "label": "Representative full name",
        "hint": "Representative full name",
        "required": True
      },
      {
        "key": "representative_iin",
        "label": "Representative iin",
        "hint": "Representative iin",
        "required": True
      },
      {
        "key": "representative_address",
        "label": "Representative address",
        "hint": "Representative address",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Брачный договор с разделным режимом имущества супругов.docx": {
    "title": "Брачный договор с раздельным режимом имущества супругов",
    "fields": [
      {
        "key": "city",
        "label": "Город",
        "hint": "Город составления документа",
        "required": True
      },
      {
        "key": "document_date",
        "label": "Дата документа",
        "hint": "Дата составления документа, например 01.05.2026",
        "required": True
      },
      {
        "key": "spouse1_full_name",
        "label": "Spouse1 full name",
        "hint": "Spouse1 full name",
        "required": True
      },
      {
        "key": "spouse1_birth_place",
        "label": "Spouse1 birth place",
        "hint": "Spouse1 birth place",
        "required": True
      },
      {
        "key": "spouse1_birth_date",
        "label": "Spouse1 birth date",
        "hint": "Spouse1 birth date",
        "required": True
      },
      {
        "key": "spouse1_address",
        "label": "Spouse1 address",
        "hint": "Spouse1 address",
        "required": True
      },
      {
        "key": "spouse2_full_name",
        "label": "Spouse2 full name",
        "hint": "Spouse2 full name",
        "required": True
      },
      {
        "key": "spouse2_birth_place",
        "label": "Spouse2 birth place",
        "hint": "Spouse2 birth place",
        "required": True
      },
      {
        "key": "spouse2_birth_date",
        "label": "Spouse2 birth date",
        "hint": "Spouse2 birth date",
        "required": True
      },
      {
        "key": "spouse2_address",
        "label": "Spouse2 address",
        "hint": "Spouse2 address",
        "required": True
      },
      {
        "key": "marriage_date",
        "label": "Marriage date",
        "hint": "Marriage date",
        "required": True
      },
      {
        "key": "certificate_series",
        "label": "Certificate series",
        "hint": "Certificate series",
        "required": True
      },
      {
        "key": "certificate_number",
        "label": "Certificate number",
        "hint": "Certificate number",
        "required": True
      },
      {
        "key": "registry_office",
        "label": "Registry office",
        "hint": "Registry office",
        "required": True
      },
      {
        "key": "registration_date",
        "label": "Registration date",
        "hint": "Registration date",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Договор залога автомобиля.docx": {
    "title": "Договор залога автомобиля",
    "fields": [
      {
        "key": "city",
        "label": "Город",
        "hint": "Город составления документа",
        "required": True
      },
      {
        "key": "document_date",
        "label": "Дата документа",
        "hint": "Дата составления документа, например 01.05.2026",
        "required": True
      },
      {
        "key": "pledgee_name",
        "label": "Pledgee name",
        "hint": "Pledgee name",
        "required": True
      },
      {
        "key": "pledgor_name",
        "label": "Pledgor name",
        "hint": "Pledgor name",
        "required": True
      },
      {
        "key": "loan_agreement_date",
        "label": "Loan agreement date",
        "hint": "Loan agreement date",
        "required": True
      },
      {
        "key": "loan_amount_number",
        "label": "Loan amount number",
        "hint": "Loan amount number",
        "required": True
      },
      {
        "key": "loan_amount_words",
        "label": "Loan amount words",
        "hint": "Loan amount words",
        "required": True
      },
      {
        "key": "payment1_date",
        "label": "Payment1 date",
        "hint": "Payment1 date",
        "required": True
      },
      {
        "key": "payment1_amount_number",
        "label": "Payment1 amount number",
        "hint": "Payment1 amount number",
        "required": True
      },
      {
        "key": "payment1_amount_words",
        "label": "Payment1 amount words",
        "hint": "Payment1 amount words",
        "required": True
      },
      {
        "key": "payment2_date",
        "label": "Payment2 date",
        "hint": "Payment2 date",
        "required": True
      },
      {
        "key": "payment2_amount_number",
        "label": "Payment2 amount number",
        "hint": "Payment2 amount number",
        "required": True
      },
      {
        "key": "payment2_amount_words",
        "label": "Payment2 amount words",
        "hint": "Payment2 amount words",
        "required": True
      },
      {
        "key": "payment3_date",
        "label": "Payment3 date",
        "hint": "Payment3 date",
        "required": True
      },
      {
        "key": "payment3_amount_number",
        "label": "Payment3 amount number",
        "hint": "Payment3 amount number",
        "required": True
      },
      {
        "key": "payment3_amount_words",
        "label": "Payment3 amount words",
        "hint": "Payment3 amount words",
        "required": True
      },
      {
        "key": "car_make",
        "label": "Car make",
        "hint": "Car make",
        "required": True
      },
      {
        "key": "car_year",
        "label": "Car year",
        "hint": "Car year",
        "required": True
      },
      {
        "key": "car_plate",
        "label": "Car plate",
        "hint": "Car plate",
        "required": True
      },
      {
        "key": "car_vin",
        "label": "Car vin",
        "hint": "Car vin",
        "required": True
      },
      {
        "key": "car_color",
        "label": "Car color",
        "hint": "Car color",
        "required": True
      },
      {
        "key": "vehicle_certificate_series",
        "label": "Vehicle certificate series",
        "hint": "Vehicle certificate series",
        "required": True
      },
      {
        "key": "vehicle_certificate_number",
        "label": "Vehicle certificate number",
        "hint": "Vehicle certificate number",
        "required": True
      },
      {
        "key": "vehicle_certificate_date",
        "label": "Vehicle certificate date",
        "hint": "Vehicle certificate date",
        "required": True
      },
      {
        "key": "vehicle_certificate_issuer",
        "label": "Vehicle certificate issuer",
        "hint": "Vehicle certificate issuer",
        "required": True
      },
      {
        "key": "car_value_number",
        "label": "Car value number",
        "hint": "Car value number",
        "required": True
      },
      {
        "key": "car_value_words",
        "label": "Car value words",
        "hint": "Car value words",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Приказ об отпуске без сохранения заработной платы.docx": {
    "title": "Приказ об отпуске без сохранения заработной платы",
    "fields": [
      {
        "key": "company_name",
        "label": "Организация",
        "hint": "Наименование организации",
        "required": True
      },
      {
        "key": "order_number",
        "label": "Order number",
        "hint": "Order number",
        "required": True
      },
      {
        "key": "city",
        "label": "Город",
        "hint": "Город составления документа",
        "required": True
      },
      {
        "key": "document_date",
        "label": "Дата документа",
        "hint": "Дата составления документа, например 01.05.2026",
        "required": True
      },
      {
        "key": "employee_full_name",
        "label": "Работник",
        "hint": "ФИО работника",
        "required": True
      },
      {
        "key": "application_date",
        "label": "Application date",
        "hint": "Application date",
        "required": True
      },
      {
        "key": "vacation_start_date",
        "label": "Vacation start date",
        "hint": "Vacation start date",
        "required": True
      },
      {
        "key": "vacation_end_date",
        "label": "Vacation end date",
        "hint": "Vacation end date",
        "required": True
      },
      {
        "key": "director_name",
        "label": "Директор",
        "hint": "ФИО директора",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Мировое соглашение.docx": {
    "title": "Мировое соглашение",
    "fields": [
      {
        "key": "city",
        "label": "Город",
        "hint": "Город составления документа",
        "required": True
      },
      {
        "key": "document_date",
        "label": "Дата документа",
        "hint": "Дата составления документа, например 01.05.2026",
        "required": True
      },
      {
        "key": "court_name",
        "label": "Суд",
        "hint": "Наименование суда",
        "required": True
      },
      {
        "key": "court_city",
        "label": "Город суда",
        "hint": "Город суда",
        "required": True
      },
      {
        "key": "case_number",
        "label": "Номер дела",
        "hint": "Номер гражданского дела",
        "required": True
      },
      {
        "key": "claim_subject",
        "label": "Предмет иска",
        "hint": "О чем спор или иск",
        "required": True
      },
      {
        "key": "claimant_company",
        "label": "Claimant company",
        "hint": "Claimant company",
        "required": True
      },
      {
        "key": "claimant_director",
        "label": "Claimant director",
        "hint": "Claimant director",
        "required": True
      },
      {
        "key": "respondent_company",
        "label": "Respondent company",
        "hint": "Respondent company",
        "required": True
      },
      {
        "key": "respondent_director",
        "label": "Respondent director",
        "hint": "Respondent director",
        "required": True
      },
      {
        "key": "payment_due_date",
        "label": "Payment due date",
        "hint": "Payment due date",
        "required": True
      },
      {
        "key": "debt_amount_number",
        "label": "Debt amount number",
        "hint": "Debt amount number",
        "required": True
      },
      {
        "key": "representative_costs_number",
        "label": "Representative costs number",
        "hint": "Representative costs number",
        "required": True
      },
      {
        "key": "total_amount_number",
        "label": "Total amount number",
        "hint": "Total amount number",
        "required": True
      },
      {
        "key": "total_amount_words",
        "label": "Total amount words",
        "hint": "Total amount words",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Ходатаство в суд об ознакомлении с материалами дела.docx": {
    "title": "Ходатайство в суд об ознакомлении с материалами дела",
    "fields": [
      {
        "key": "court_name",
        "label": "Суд",
        "hint": "Наименование суда",
        "required": True
      },
      {
        "key": "court_city",
        "label": "Город суда",
        "hint": "Город суда",
        "required": True
      },
      {
        "key": "judge_name",
        "label": "Судья",
        "hint": "ФИО судьи",
        "required": True
      },
      {
        "key": "case_number",
        "label": "Номер дела",
        "hint": "Номер гражданского дела",
        "required": True
      },
      {
        "key": "claimant_name",
        "label": "Истец",
        "hint": "ФИО или наименование истца",
        "required": True
      },
      {
        "key": "claimant_iin",
        "label": "ИИН истца",
        "hint": "ИИН истца",
        "required": True
      },
      {
        "key": "claimant_address",
        "label": "Адрес истца",
        "hint": "Адрес истца",
        "required": True
      },
      {
        "key": "claimant_phone",
        "label": "Телефон истца",
        "hint": "Телефон истца",
        "required": True
      },
      {
        "key": "claimant_email",
        "label": "Email истца",
        "hint": "Электронный адрес истца",
        "required": True
      },
      {
        "key": "respondent_name",
        "label": "Ответчик",
        "hint": "ФИО или наименование ответчика",
        "required": True
      },
      {
        "key": "respondent_iin",
        "label": "ИИН ответчика",
        "hint": "ИИН ответчика",
        "required": True
      },
      {
        "key": "respondent_address",
        "label": "Адрес ответчика",
        "hint": "Адрес ответчика",
        "required": True
      },
      {
        "key": "respondent_phone",
        "label": "Телефон ответчика",
        "hint": "Телефон ответчика",
        "required": True
      },
      {
        "key": "respondent_email",
        "label": "Email ответчика",
        "hint": "Электронный адрес ответчика",
        "required": True
      },
      {
        "key": "claim_subject",
        "label": "Предмет иска",
        "hint": "О чем спор или иск",
        "required": True
      },
      {
        "key": "signing_date",
        "label": "Дата подписания",
        "hint": "Дата подписания документа, например 01.05.2026",
        "required": True
      },
      {
        "key": "case_court_name",
        "label": "Case Court Name",
        "hint": "Контекст шаблона: ondent_phone }} Электронный адрес: {{ respondent_email }} ХОДАТАЙСТВО об ознакомлении с материалами дела В производстве {{ case_court_name }} суда города {{ case_court_city }} находится гражданское дело № {{ case_number }} по иску {{ claimant_name }} (далее – И",
        "required": True
      },
      {
        "key": "case_court_city",
        "label": "Case Court City",
        "hint": "Контекст шаблона: {{ respondent_email }} ХОДАТАЙСТВО об ознакомлении с материалами дела В производстве {{ case_court_name }} суда города {{ case_court_city }} находится гражданское дело № {{ case_number }} по иску {{ claimant_name }} (далее – Истец) к {{ respondent_name }} (дал",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Заявление в суд о дистанционном ознакомлении с материалами дела.docx": {
    "title": "Заявление в суд о дистанционном ознакомлении с материалами дела",
    "fields": [
      {
        "key": "court_district",
        "label": "Район суда",
        "hint": "Районный суд или район суда",
        "required": True
      },
      {
        "key": "court_city",
        "label": "Город суда",
        "hint": "Город суда",
        "required": True
      },
      {
        "key": "court_extra",
        "label": "Дополнение по суду",
        "hint": "Дополнительная строка по суду, если нужна",
        "required": True
      },
      {
        "key": "judge_name",
        "label": "Судья",
        "hint": "ФИО судьи",
        "required": True
      },
      {
        "key": "case_number",
        "label": "Номер дела",
        "hint": "Номер гражданского дела",
        "required": True
      },
      {
        "key": "claimant_name",
        "label": "Истец",
        "hint": "ФИО или наименование истца",
        "required": True
      },
      {
        "key": "claimant_iin",
        "label": "ИИН истца",
        "hint": "ИИН истца",
        "required": True
      },
      {
        "key": "claimant_address",
        "label": "Адрес истца",
        "hint": "Адрес истца",
        "required": True
      },
      {
        "key": "claimant_phone",
        "label": "Телефон истца",
        "hint": "Телефон истца",
        "required": True
      },
      {
        "key": "claimant_email",
        "label": "Email истца",
        "hint": "Электронный адрес истца",
        "required": True
      },
      {
        "key": "respondent_name",
        "label": "Ответчик",
        "hint": "ФИО или наименование ответчика",
        "required": True
      },
      {
        "key": "respondent_iin",
        "label": "ИИН ответчика",
        "hint": "ИИН ответчика",
        "required": True
      },
      {
        "key": "respondent_address",
        "label": "Адрес ответчика",
        "hint": "Адрес ответчика",
        "required": True
      },
      {
        "key": "respondent_phone",
        "label": "Телефон ответчика",
        "hint": "Телефон ответчика",
        "required": True
      },
      {
        "key": "respondent_email",
        "label": "Email ответчика",
        "hint": "Электронный адрес ответчика",
        "required": True
      },
      {
        "key": "claim_amount",
        "label": "Сумма иска",
        "hint": "Сумма требований",
        "required": True
      },
      {
        "key": "signing_date",
        "label": "Дата подписания",
        "hint": "Дата подписания документа, например 01.05.2026",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Заявление об ознакомлении с материалами дела.docx": {
    "title": "Заявление об ознакомлении с материалами дела",
    "fields": [
      {
        "key": "court_district",
        "label": "Район суда",
        "hint": "Районный суд или район суда",
        "required": True
      },
      {
        "key": "court_city",
        "label": "Город суда",
        "hint": "Город суда",
        "required": True
      },
      {
        "key": "court_extra",
        "label": "Дополнение по суду",
        "hint": "Дополнительная строка по суду, если нужна",
        "required": True
      },
      {
        "key": "judge_name",
        "label": "Судья",
        "hint": "ФИО судьи",
        "required": True
      },
      {
        "key": "claimant_name",
        "label": "Истец",
        "hint": "ФИО или наименование истца",
        "required": True
      },
      {
        "key": "respondent_name",
        "label": "Ответчик",
        "hint": "ФИО или наименование ответчика",
        "required": True
      },
      {
        "key": "case_number",
        "label": "Номер дела",
        "hint": "Номер гражданского дела",
        "required": True
      },
      {
        "key": "claimant_company",
        "label": "Claimant company",
        "hint": "Claimant company",
        "required": True
      },
      {
        "key": "respondent_company",
        "label": "Respondent company",
        "hint": "Respondent company",
        "required": True
      },
      {
        "key": "claim_amount",
        "label": "Сумма иска",
        "hint": "Сумма требований",
        "required": True
      },
      {
        "key": "decision_date",
        "label": "Decision date",
        "hint": "Decision date",
        "required": True
      },
      {
        "key": "awarded_amount",
        "label": "Awarded amount",
        "hint": "Awarded amount",
        "required": True
      },
      {
        "key": "respondent_representative",
        "label": "Respondent representative",
        "hint": "Respondent representative",
        "required": True
      },
      {
        "key": "respondent_email",
        "label": "Email ответчика",
        "hint": "Электронный адрес ответчика",
        "required": True
      },
      {
        "key": "signing_date",
        "label": "Дата подписания",
        "hint": "Дата подписания документа, например 01.05.2026",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Письменное пояснение на уведомление налогового органа об устранении нарушений.docx": {
    "title": "Письменное пояснение на уведомление налогового органа об устранении нарушений",
    "fields": [
      {
        "key": "tax_city",
        "label": "Tax city",
        "hint": "Tax city",
        "required": True
      },
      {
        "key": "tax_region",
        "label": "Tax region",
        "hint": "Tax region",
        "required": True
      },
      {
        "key": "company_name",
        "label": "Организация",
        "hint": "Наименование организации",
        "required": True
      },
      {
        "key": "company_city",
        "label": "Company city",
        "hint": "Company city",
        "required": True
      },
      {
        "key": "company_street",
        "label": "Company street",
        "hint": "Company street",
        "required": True
      },
      {
        "key": "company_phone",
        "label": "Company phone",
        "hint": "Company phone",
        "required": True
      },
      {
        "key": "company_email",
        "label": "Company email",
        "hint": "Company email",
        "required": True
      },
      {
        "key": "company_bin",
        "label": "Company bin",
        "hint": "Company bin",
        "required": True
      },
      {
        "key": "notice_date",
        "label": "Notice date",
        "hint": "Notice date",
        "required": True
      },
      {
        "key": "notice_number",
        "label": "Notice number",
        "hint": "Notice number",
        "required": True
      },
      {
        "key": "violation_description",
        "label": "Violation description",
        "hint": "Violation description",
        "required": True
      },
      {
        "key": "explanation_text",
        "label": "Explanation text",
        "hint": "Explanation text",
        "required": True
      },
      {
        "key": "attachments",
        "label": "Attachments",
        "hint": "Attachments",
        "required": False
      },
      {
        "key": "director_name",
        "label": "Директор",
        "hint": "ФИО директора",
        "required": True
      },
      {
        "key": "signing_date",
        "label": "Дата подписания",
        "hint": "Дата подписания документа, например 01.05.2026",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Претензия о замене некачественного товара.docx": {
    "title": "Претензия потребителя о замене некачественного товара",
    "fields": [
      {
        "key": "seller_name",
        "label": "Seller name",
        "hint": "Seller name",
        "required": True
      },
      {
        "key": "seller_bin",
        "label": "Seller bin",
        "hint": "Seller bin",
        "required": True
      },
      {
        "key": "seller_address",
        "label": "Seller address",
        "hint": "Seller address",
        "required": True
      },
      {
        "key": "seller_phone",
        "label": "Seller phone",
        "hint": "Seller phone",
        "required": True
      },
      {
        "key": "seller_email",
        "label": "Seller email",
        "hint": "Seller email",
        "required": True
      },
      {
        "key": "buyer_name",
        "label": "Buyer name",
        "hint": "Buyer name",
        "required": True
      },
      {
        "key": "buyer_iin",
        "label": "Buyer iin",
        "hint": "Buyer iin",
        "required": True
      },
      {
        "key": "buyer_address",
        "label": "Buyer address",
        "hint": "Buyer address",
        "required": True
      },
      {
        "key": "buyer_phone",
        "label": "Buyer phone",
        "hint": "Buyer phone",
        "required": True
      },
      {
        "key": "buyer_email",
        "label": "Buyer email",
        "hint": "Buyer email",
        "required": True
      },
      {
        "key": "purchase_date",
        "label": "Purchase date",
        "hint": "Purchase date",
        "required": True
      },
      {
        "key": "store_name",
        "label": "Store name",
        "hint": "Store name",
        "required": True
      },
      {
        "key": "store_city",
        "label": "Store city",
        "hint": "Store city",
        "required": True
      },
      {
        "key": "store_street",
        "label": "Store street",
        "hint": "Store street",
        "required": True
      },
      {
        "key": "mall_name",
        "label": "Mall name",
        "hint": "Mall name",
        "required": True
      },
      {
        "key": "product_name",
        "label": "Product name",
        "hint": "Product name",
        "required": True
      },
      {
        "key": "product_price",
        "label": "Product price",
        "hint": "Product price",
        "required": True
      },
      {
        "key": "defects",
        "label": "Defects",
        "hint": "Defects",
        "required": True
      },
      {
        "key": "service_center_name",
        "label": "Service center name",
        "hint": "Service center name",
        "required": True
      },
      {
        "key": "service_center_report_date",
        "label": "Service center report date",
        "hint": "Service center report date",
        "required": True
      },
      {
        "key": "moral_damage_amount",
        "label": "Moral damage amount",
        "hint": "Moral damage amount",
        "required": True
      },
      {
        "key": "replacement_product",
        "label": "Replacement product",
        "hint": "Replacement product",
        "required": True
      },
      {
        "key": "penalty_amount",
        "label": "Penalty amount",
        "hint": "Penalty amount",
        "required": True
      },
      {
        "key": "signing_date",
        "label": "Дата подписания",
        "hint": "Дата подписания документа, например 01.05.2026",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Претензия о замене товара ненадлежащего качества.docx": {
    "title": "Претензия по качеству товара",
    "fields": [
      {
        "key": "supplier_name",
        "label": "Supplier name",
        "hint": "Supplier name",
        "required": True
      },
      {
        "key": "supplier_bin",
        "label": "Supplier bin",
        "hint": "Supplier bin",
        "required": True
      },
      {
        "key": "supplier_address",
        "label": "Supplier address",
        "hint": "Supplier address",
        "required": True
      },
      {
        "key": "supplier_director",
        "label": "Supplier director",
        "hint": "Supplier director",
        "required": True
      },
      {
        "key": "supplier_phone",
        "label": "Supplier phone",
        "hint": "Supplier phone",
        "required": True
      },
      {
        "key": "supplier_email",
        "label": "Supplier email",
        "hint": "Supplier email",
        "required": True
      },
      {
        "key": "buyer_name",
        "label": "Buyer name",
        "hint": "Buyer name",
        "required": True
      },
      {
        "key": "buyer_bin",
        "label": "Buyer bin",
        "hint": "Buyer bin",
        "required": True
      },
      {
        "key": "buyer_address",
        "label": "Buyer address",
        "hint": "Buyer address",
        "required": True
      },
      {
        "key": "contract_date",
        "label": "Contract date",
        "hint": "Contract date",
        "required": True
      },
      {
        "key": "contract_number",
        "label": "Номер договора",
        "hint": "Номер договора",
        "required": True
      },
      {
        "key": "product_name",
        "label": "Product name",
        "hint": "Product name",
        "required": True
      },
      {
        "key": "contract_clause",
        "label": "Contract clause",
        "hint": "Contract clause",
        "required": True
      },
      {
        "key": "product_price",
        "label": "Product price",
        "hint": "Product price",
        "required": True
      },
      {
        "key": "delivery_date",
        "label": "Delivery date",
        "hint": "Delivery date",
        "required": True
      },
      {
        "key": "invoice_name",
        "label": "Invoice name",
        "hint": "Invoice name",
        "required": True
      },
      {
        "key": "invoice_number",
        "label": "Invoice number",
        "hint": "Invoice number",
        "required": True
      },
      {
        "key": "invoice_date",
        "label": "Invoice date",
        "hint": "Invoice date",
        "required": True
      },
      {
        "key": "defect_1",
        "label": "Defect 1",
        "hint": "Defect 1",
        "required": True
      },
      {
        "key": "defect_2",
        "label": "Defect 2",
        "hint": "Defect 2",
        "required": True
      },
      {
        "key": "defect_3",
        "label": "Defect 3",
        "hint": "Defect 3",
        "required": True
      },
      {
        "key": "defect_4",
        "label": "Defect 4",
        "hint": "Defect 4",
        "required": True
      },
      {
        "key": "defect_5",
        "label": "Defect 5",
        "hint": "Defect 5",
        "required": True
      },
      {
        "key": "replacement_deadline_days",
        "label": "Replacement deadline days",
        "hint": "Replacement deadline days",
        "required": True
      },
      {
        "key": "attachments",
        "label": "Attachments",
        "hint": "Attachments",
        "required": False
      },
      {
        "key": "director_name",
        "label": "Директор",
        "hint": "ФИО директора",
        "required": True
      },
      {
        "key": "signing_date",
        "label": "Дата подписания",
        "hint": "Дата подписания документа, например 01.05.2026",
        "required": True
      }
    ],
    "source": "manual_placeholders"
  },
  "Исковое заявление об изменении размера алиментов.docx": {
    "title": "Исковое заявление об изменении размера алиментов",
    "fields": [
      {
        "key": "court_name",
        "label": "Court name",
        "hint": "Court name",
        "required": True
      },
      {
        "key": "court_address",
        "label": "Court address",
        "hint": "Court address",
        "required": True
      },
      {
        "key": "plaintiff_full_name",
        "label": "Plaintiff full name",
        "hint": "Plaintiff full name",
        "required": True
      },
      {
        "key": "defendant_full_name",
        "label": "Defendant full name",
        "hint": "Defendant full name",
        "required": True
      },
      {
        "key": "plaintiff_iin",
        "label": "Plaintiff iin",
        "hint": "Plaintiff iin",
        "required": True
      },
      {
        "key": "defendant_iin",
        "label": "Defendant iin",
        "hint": "Defendant iin",
        "required": True
      },
      {
        "key": "plaintiff_address",
        "label": "Plaintiff address",
        "hint": "Plaintiff address",
        "required": True
      },
      {
        "key": "defendant_address",
        "label": "Defendant address",
        "hint": "Defendant address",
        "required": True
      },
      {
        "key": "plaintiff_phone",
        "label": "Plaintiff phone",
        "hint": "Plaintiff phone",
        "required": True
      },
      {
        "key": "defendant_phone",
        "label": "Defendant phone",
        "hint": "Defendant phone",
        "required": True
      },
      {
        "key": "representative_full_name",
        "label": "Representative full name",
        "hint": "Representative full name",
        "required": True
      },
      {
        "key": "defendant2_full_name",
        "label": "Defendant2 full name",
        "hint": "Defendant2 full name",
        "required": True
      },
      {
        "key": "defendant2_iin",
        "label": "Defendant2 iin",
        "hint": "Defendant2 iin",
        "required": True
      },
      {
        "key": "defendant2_address",
        "label": "Defendant2 address",
        "hint": "Defendant2 address",
        "required": True
      },
      {
        "key": "defendant2_phone",
        "label": "Defendant2 phone",
        "hint": "Defendant2 phone",
        "required": True
      },
      {
        "key": "marriage_date",
        "label": "Marriage date",
        "hint": "Marriage date",
        "required": True
      },
      {
        "key": "child_full_name",
        "label": "Child full name",
        "hint": "Child full name",
        "required": True
      },
      {
        "key": "child_birth_date",
        "label": "Child birth date",
        "hint": "Child birth date",
        "required": True
      },
      {
        "key": "divorce_date",
        "label": "Divorce date",
        "hint": "Divorce date",
        "required": True
      },
      {
        "key": "previous_court_decision_date",
        "label": "Дата предыдущего решения суда",
        "hint": "Дата решения суда",
        "required": True
      },
      {
        "key": "alimony_current_amount",
        "label": "Alimony current amount",
        "hint": "Alimony current amount",
        "required": True
      },
      {
        "key": "alimony_requested_amount",
        "label": "Alimony requested amount",
        "hint": "Alimony requested amount",
        "required": True
      },
      {
        "key": "monthly_income",
        "label": "Monthly income",
        "hint": "Monthly income",
        "required": True
      },
      {
        "key": "claim_request",
        "label": "Claim request",
        "hint": "Claim request",
        "required": True
      },
      {
        "key": "claim_facts",
        "label": "Claim facts",
        "hint": "Claim facts",
        "required": True
      },
      {
        "key": "claim_basis",
        "label": "Claim basis",
        "hint": "Claim basis",
        "required": True
      },
      {
        "key": "evidence",
        "label": "Evidence",
        "hint": "Evidence",
        "required": True
      },
      {
        "key": "attachments",
        "label": "Attachments",
        "hint": "Attachments",
        "required": True
      },
      {
        "key": "filing_date",
        "label": "Filing date",
        "hint": "Filing date",
        "required": True
      },
      {
        "key": "unused_blank_032",
        "label": "Дополнительное поле 30",
        "hint": "Контекст шаблона: m_basis }} ИИН {{ evidence }} {{ claim_request }} {{ attachments }} {{ filing_date }} абонентский номер сотовой связи : {{ unused_blank_032 }} электронн ый адрес : {{ unused_blank_033 }} {{ unused_blank_034 }} {{ unused_blank_035 }} (если ИИН, абонентский номер",
        "required": True
      },
      {
        "key": "unused_blank_033",
        "label": "Дополнительное поле 31",
        "hint": "Контекст шаблона: st }} {{ attachments }} {{ filing_date }} абонентский номер сотовой связи : {{ unused_blank_032 }} электронн ый адрес : {{ unused_blank_033 }} {{ unused_blank_034 }} {{ unused_blank_035 }} (если ИИН, абонентский номер сотовой связи и э лектронный адрес известны",
        "required": True
      },
      {
        "key": "unused_blank_034",
        "label": "Дополнительное поле 32",
        "hint": "Контекст шаблона: {{ filing_date }} абонентский номер сотовой связи : {{ unused_blank_032 }} электронн ый адрес : {{ unused_blank_033 }} {{ unused_blank_034 }} {{ unused_blank_035 }} (если ИИН, абонентский номер сотовой связи и э лектронный адрес известны истцу) ИСК (об изменени",
        "required": True
      },
      {
        "key": "unused_blank_035",
        "label": "Дополнительное поле 33",
        "hint": "Контекст шаблона: ентский номер сотовой связи : {{ unused_blank_032 }} электронн ый адрес : {{ unused_blank_033 }} {{ unused_blank_034 }} {{ unused_blank_035 }} (если ИИН, абонентский номер сотовой связи и э лектронный адрес известны истцу) ИСК (об изменении размера алиментов) В",
        "required": True
      },
      {
        "key": "unused_blank_036",
        "label": "Дополнительное поле 34",
        "hint": "Контекст шаблона: (если ИИН, абонентский номер сотовой связи и э лектронный адрес известны истцу) ИСК (об изменении размера алиментов) В {{ unused_blank_036 }} году я вступил в зарегистрированный брак с {{ unused_blank_037 }} (Ф.И.О.) и от совместного брака имеем сына {{ unused_",
        "required": True
      },
      {
        "key": "unused_blank_037",
        "label": "Дополнительное поле 35",
        "hint": "Контекст шаблона: звестны истцу) ИСК (об изменении размера алиментов) В {{ unused_blank_036 }} году я вступил в зарегистрированный брак с {{ unused_blank_037 }} (Ф.И.О.) и от совместного брака имеем сына {{ unused_blank_038 }} (Ф.И.О.), {{ unused_blank_039 }} года рождения. Брак",
        "required": True
      },
      {
        "key": "unused_blank_038",
        "label": "Дополнительное поле 36",
        "hint": "Контекст шаблона: ank_036 }} году я вступил в зарегистрированный брак с {{ unused_blank_037 }} (Ф.И.О.) и от совместного брака имеем сына {{ unused_blank_038 }} (Ф.И.О.), {{ unused_blank_039 }} года рождения. Брак расторгнут {{ unused_blank_040 }} (дата). На основании решения суд",
        "required": True
      },
      {
        "key": "unused_blank_039",
        "label": "Дополнительное поле 37",
        "hint": "Контекст шаблона: истрированный брак с {{ unused_blank_037 }} (Ф.И.О.) и от совместного брака имеем сына {{ unused_blank_038 }} (Ф.И.О.), {{ unused_blank_039 }} года рождения. Брак расторгнут {{ unused_blank_040 }} (дата). На основании решения суда от {{ unused_blank_041 }} (дата",
        "required": True
      },
      {
        "key": "unused_blank_040",
        "label": "Дополнительное поле 38",
        "hint": "Контекст шаблона: от совместного брака имеем сына {{ unused_blank_038 }} (Ф.И.О.), {{ unused_blank_039 }} года рождения. Брак расторгнут {{ unused_blank_040 }} (дата). На основании решения суда от {{ unused_blank_041 }} (дата) я выплачиваю алименты на содержание сына {{ unused_b",
        "required": True
      },
      {
        "key": "unused_blank_041",
        "label": "Дополнительное поле 39",
        "hint": "Контекст шаблона: .О.), {{ unused_blank_039 }} года рождения. Брак расторгнут {{ unused_blank_040 }} (дата). На основании решения суда от {{ unused_blank_041 }} (дата) я выплачиваю алименты на содержание сына {{ unused_blank_042 }} Ф.И.О., {{ unused_blank_043 }}, года рождения, в",
        "required": True
      },
      {
        "key": "unused_blank_042",
        "label": "Дополнительное поле 40",
        "hint": "Контекст шаблона: lank_040 }} (дата). На основании решения суда от {{ unused_blank_041 }} (дата) я выплачиваю алименты на содержание сына {{ unused_blank_042 }} Ф.И.О., {{ unused_blank_043 }}, года рождения, в размере 1/4 части заработной платы. В {{ unused_blank_044 }} году я вс",
        "required": True
      },
      {
        "key": "unused_blank_043",
        "label": "Дополнительное поле 41",
        "hint": "Контекст шаблона: и решения суда от {{ unused_blank_041 }} (дата) я выплачиваю алименты на содержание сына {{ unused_blank_042 }} Ф.И.О., {{ unused_blank_043 }}, года рождения, в размере 1/4 части заработной платы. В {{ unused_blank_044 }} году я вступил в брак с ответчиком {{ un",
        "required": True
      },
      {
        "key": "unused_blank_044",
        "label": "Дополнительное поле 42",
        "hint": "Контекст шаблона: ание сына {{ unused_blank_042 }} Ф.И.О., {{ unused_blank_043 }}, года рождения, в размере 1/4 части заработной платы. В {{ unused_blank_044 }} году я вступил в брак с ответчиком {{ unused_blank_045 }} (Ф.И.О.) и от совместного брака имеем дочь - {{ unused_blank_",
        "required": True
      },
      {
        "key": "unused_blank_045",
        "label": "Дополнительное поле 43",
        "hint": "Контекст шаблона: 43 }}, года рождения, в размере 1/4 части заработной платы. В {{ unused_blank_044 }} году я вступил в брак с ответчиком {{ unused_blank_045 }} (Ф.И.О.) и от совместного брака имеем дочь - {{ unused_blank_046 }} (Ф.И.О.), {{ unused_blank_047 }} года рождения, на",
        "required": True
      },
      {
        "key": "unused_blank_046",
        "label": "Дополнительное поле 44",
        "hint": "Контекст шаблона: sed_blank_044 }} году я вступил в брак с ответчиком {{ unused_blank_045 }} (Ф.И.О.) и от совместного брака имеем дочь - {{ unused_blank_046 }} (Ф.И.О.), {{ unused_blank_047 }} года рождения, на содержание которой я также на основании решения суда выплачиваю алим",
        "required": True
      },
      {
        "key": "unused_blank_047",
        "label": "Дополнительное поле 45",
        "hint": "Контекст шаблона: брак с ответчиком {{ unused_blank_045 }} (Ф.И.О.) и от совместного брака имеем дочь - {{ unused_blank_046 }} (Ф.И.О.), {{ unused_blank_047 }} года рождения, на содержание которой я также на основании решения суда выплачиваю алименты в размере 1/4 части заработн",
        "required": True
      },
      {
        "key": "unused_blank_048",
        "label": "Дополнительное поле 46",
        "hint": "Контекст шаблона: раке (супружестве) и семье», статьями 148-149 Гражданского процессуального кодекса Республики Казахстан, П Р О Ш У: Иск {{ unused_blank_048 }} ( Ф.И.О. ) к {{ unused_blank_049 }} ( Ф.И.О. ответчиков ) об изменении размера алиментов – удовлетворить. Изменить разм",
        "required": True
      },
      {
        "key": "unused_blank_049",
        "label": "Дополнительное поле 47",
        "hint": "Контекст шаблона: и 148-149 Гражданского процессуального кодекса Республики Казахстан, П Р О Ш У: Иск {{ unused_blank_048 }} ( Ф.И.О. ) к {{ unused_blank_049 }} ( Ф.И.О. ответчиков ) об изменении размера алиментов – удовлетворить. Изменить размер алиментов, взыскиваемых в пользу:",
        "required": True
      },
      {
        "key": "unused_blank_050",
        "label": "Дополнительное поле 48",
        "hint": "Контекст шаблона: тветчиков ) об изменении размера алиментов – удовлетворить. Изменить размер алиментов, взыскиваемых в пользу: ответчика {{ unused_blank_050 }} (Ф.И.О.) на содержание сына {{ unused_blank_051 }} (Ф.И.О.), {{ unused_blank_052 }} года рождения, в пользу ответчика {",
        "required": True
      },
      {
        "key": "unused_blank_051",
        "label": "Дополнительное поле 49",
        "hint": "Контекст шаблона: творить. Изменить размер алиментов, взыскиваемых в пользу: ответчика {{ unused_blank_050 }} (Ф.И.О.) на содержание сына {{ unused_blank_051 }} (Ф.И.О.), {{ unused_blank_052 }} года рождения, в пользу ответчика {{ unused_blank_053 }} (Ф.И.О.) на содержание дочери",
        "required": True
      },
      {
        "key": "unused_blank_052",
        "label": "Дополнительное поле 50",
        "hint": "Контекст шаблона: в, взыскиваемых в пользу: ответчика {{ unused_blank_050 }} (Ф.И.О.) на содержание сына {{ unused_blank_051 }} (Ф.И.О.), {{ unused_blank_052 }} года рождения, в пользу ответчика {{ unused_blank_053 }} (Ф.И.О.) на содержание дочери - {{ unused_blank_054 }} (Ф.И.О.",
        "required": True
      },
      {
        "key": "unused_blank_053",
        "label": "Дополнительное поле 51",
        "hint": "Контекст шаблона: } (Ф.И.О.) на содержание сына {{ unused_blank_051 }} (Ф.И.О.), {{ unused_blank_052 }} года рождения, в пользу ответчика {{ unused_blank_053 }} (Ф.И.О.) на содержание дочери - {{ unused_blank_054 }} (Ф.И.О.), {{ unused_blank_055 }} года рождения с 1/4 части зараб",
        "required": True
      },
      {
        "key": "unused_blank_054",
        "label": "Дополнительное поле 52",
        "hint": "Контекст шаблона: .И.О.), {{ unused_blank_052 }} года рождения, в пользу ответчика {{ unused_blank_053 }} (Ф.И.О.) на содержание дочери - {{ unused_blank_054 }} (Ф.И.О.), {{ unused_blank_055 }} года рождения с 1/4 части заработной платы на 1/6 часть заработной платы. Перечень при",
        "required": True
      },
      {
        "key": "unused_blank_055",
        "label": "Дополнительное поле 53",
        "hint": "Контекст шаблона: да рождения, в пользу ответчика {{ unused_blank_053 }} (Ф.И.О.) на содержание дочери - {{ unused_blank_054 }} (Ф.И.О.), {{ unused_blank_055 }} года рождения с 1/4 части заработной платы на 1/6 часть заработной платы. Перечень прилагаемых к исковому заявлению док",
        "required": True
      },
      {
        "key": "unused_blank_056",
        "label": "Дополнительное поле 54",
        "hint": "Контекст шаблона: заявлению документов: К опии иска ; Квитанция об оплате госпошлины; Копия свидетельства о браке; Копия решения суда от {{ unused_blank_056 }} года; Копия решения суда от {{ unused_blank_057 }} года; Справка о заработной плате истца и удержаниях алиментов; Копия",
        "required": True
      },
      {
        "key": "unused_blank_057",
        "label": "Дополнительное поле 55",
        "hint": "Контекст шаблона: плате госпошлины; Копия свидетельства о браке; Копия решения суда от {{ unused_blank_056 }} года; Копия решения суда от {{ unused_blank_057 }} года; Справка о заработной плате истца и удержаниях алиментов; Копия удостоверения личности истца; Адресная справка . И",
        "required": True
      },
      {
        "key": "unused_blank_058",
        "label": "Дополнительное поле 56",
        "hint": "Контекст шаблона: нтов; Копия удостоверения личности истца; Адресная справка . Истец: (подпись) ( указать фамилию и инициалы истца ) Дата {{ unused_blank_058 }}",
        "required": True
      }
    ],
  },
}


def get_documents_list():
    return [
        {
            "template_name": template_name,
            "title": data["title"]
        }
        for template_name, data in DOCUMENT_TYPES.items()
    ]


def get_document(template_name):
    return DOCUMENT_TYPES.get(template_name)