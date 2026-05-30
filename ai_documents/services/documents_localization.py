"""
Kazakh localization for DOCUMENT_TYPES.

Important:
- template_name is NOT translated. It must stay equal to the real .docx key.
- Only title, label and hint are localized.
- Supports language values: "kz", "kk", "kaz".
"""

from copy import deepcopy


KZ_DOCUMENT_TITLES = {
    "Брачный договор с разделным режимом имущества супругов.docx": "Ерлі-зайыптылар мүлкінің бөлек режимі туралы неке шарты",
    "Доверенность на представительство в Конституционном Суде.docx": "Конституциялық Сотта өкілдік етуге сенімхат",
    "Договор залога автомобиля.docx": "Автокөлік кепілі шарты",
    "Договор о полной материальной ответственности.docx": "Толық материалдық жауапкершілік туралы шарт",
    "Заявление в суд о дистанционном ознакомлении с материалами дела.docx": "Іс материалдарымен қашықтан танысу туралы сотқа арыз",
    "Заявление о взыскании алиментов.docx": "Алимент өндіріп алу туралы арыз",
    "Заявление о возврате иска.docx": "Талап қоюды қайтару туралы арыз",
    "Заявление о признании гражданина безвестно отсутствующим.docx": "Азаматты хабар-ошарсыз кетті деп тану туралы арыз",
    "Заявление о признании гражданина недееспособным.docx": "Азаматты әрекетке қабілетсіз деп тану туралы арыз",
    "Заявление о признании гражданина ограниченно дееспособным.docx": "Азаматты әрекет қабілеттілігі шектеулі деп тану туралы арыз",
    "Заявление об ознакомлении с материалами дела.docx": "Іс материалдарымен танысу туралы арыз",
    "Заявление об отказе от иска.docx": "Талап қоюдан бас тарту туралы арыз",
    "Заявление об установлении факта принятия наследства.docx": "Мұраны қабылдау фактісін анықтау туралы арыз",
    "Заявление об установлении факта родственных отношений.docx": "Туыстық қатынастар фактісін анықтау туралы арыз",
    "Заявление об установлении факта смерти.docx": "Қайтыс болу фактісін анықтау туралы арыз",
    "Заявление об установлении факта, имеющего юридическое значение.docx": "Заңдық маңызы бар фактіні анықтау туралы арыз",

    "Иск о взыскании алиментов в твердой денежной сумме.docx": "Алиментті тұрақты ақшалай сомада өндіріп алу туралы талап қою",
    "Иск о взыскании алиментов за прошедший период в твердой денежной сумме.docx": "Өткен кезең үшін алиментті тұрақты ақшалай сомада өндіріп алу туралы талап қою",
    "Иск о взыскании задолженности по договору аренды.docx": "Жалдау шарты бойынша берешекті өндіріп алу туралы талап қою",
    "Иск о взыскании задолженности по договору.docx": "Шарт бойынша берешекті өндіріп алу туралы талап қою",
    "Иск о взыскании задолженности.docx": "Берешекті өндіріп алу туралы талап қою",
    "Иск о взыскании заработной платы.docx": "Жалақыны өндіріп алу туралы талап қою",
    "Иск о взыскании средств на содержание родителя.docx": "Ата-ананы асырауға арналған қаражатты өндіріп алу туралы талап қою",
    "Иск о возмещении вреда в связи со смертью кормильца.docx": "Асыраушының қайтыс болуына байланысты зиянды өтеу туралы талап қою",
    "Иск о возмещении вреда, причиненного повреждением здоровья.docx": "Денсаулыққа келтірілген зиянды өтеу туралы талап қою",
    "Иск о возмещении морального вреда.docx": "Моральдық зиянды өтеу туралы талап қою",
    "Иск о возмещении ущерба при ДТП.docx": "ЖКО кезінде келтірілген залалды өтеу туралы талап қою",
    "Иск о восстановлении на работе и взыскании заработной платы.docx": "Жұмысқа қайта орналастыру және жалақыны өндіріп алу туралы талап қою",
    "Иск о восстановлении на работе и взыскании премии.docx": "Жұмысқа қайта орналастыру және сыйақыны өндіріп алу туралы талап қою",
    "Иск о восстановлении срока для принятия наследства (2).docx": "Мұраны қабылдау мерзімін қалпына келтіру туралы талап қою (2)",
    "Иск о восстановлении срока для принятия наследства.docx": "Мұраны қабылдау мерзімін қалпына келтіру туралы талап қою",
    "Иск о выселении.docx": "Тұрғын үйден шығару туралы талап қою",
    "Иск о прекращении права собственности.docx": "Меншік құқығын тоқтату туралы талап қою",
    "Иск о признании гражданина недостойным наследником.docx": "Азаматты лайықсыз мұрагер деп тану туралы талап қою",
    "Иск о признании действительным акта выполненных работ.docx": "Орындалған жұмыстар актісін жарамды деп тану туралы талап қою",
    "Иск о признании завещания недействительным.docx": "Өсиетті жарамсыз деп тану туралы талап қою",
    "Иск о признании недействительным договора и взыскании суммы.docx": "Шартты жарамсыз деп тану және соманы өндіріп алу туралы талап қою",
    "Иск о признании недействительным свидетельства о праве на наследство.docx": "Мұраға құқық туралы куәлікті жарамсыз деп тану туралы талап қою",
    "Иск о признании незаконным расторжения договора.docx": "Шартты бұзуды заңсыз деп тану туралы талап қою",
    "Иск о признании обязательства исполненным.docx": "Міндеттемені орындалды деп тану туралы талап қою",
    "Иск о признании права долевой собственности.docx": "Үлестік меншік құқығын тану туралы талап қою",
    "Иск о признании права собственности на самовольную постройку.docx": "Өз бетінше салынған құрылысқа меншік құқығын тану туралы талап қою",
    "Иск о признании права собственности по приобретательной давности.docx": "Иелену мерзімі бойынша меншік құқығын тану туралы талап қою",
    "Иск о признании права собственности.docx": "Меншік құқығын тану туралы талап қою",
    "Иск о разделе имущества супругов.docx": "Ерлі-зайыптылардың мүлкін бөлу туралы талап қою",
    "Иск о разделе наследственного имущества.docx": "Мұрагерлік мүлікті бөлу туралы талап қою",
    "Иск о расторжении брака.docx": "Некені бұзу туралы талап қою",
    "Иск о сносе.docx": "Құрылысты бұзу туралы талап қою",
    "Иск об истребовании имущества из чужого незаконного владения.docx": "Бөтеннің заңсыз иеленуінен мүлікті талап етіп алу туралы талап қою",
    "Иск об определении места жительства ребенка.docx": "Баланың тұрғылықты жерін анықтау туралы талап қою",
    "Иск об освобождении имущества от ареста.docx": "Мүлікті тыйым салудан босату туралы талап қою",
    "Иск об отмене приказа об увольнении и восстановлении на работе.docx": "Жұмыстан шығару туралы бұйрықтың күшін жою және жұмысқа қайта орналастыру туралы талап қою",
    "Иск об уменьшении размера алиментов.docx": "Алимент мөлшерін азайту туралы талап қою",
    "Иск об установлении отцовства и взыскании алиментов.docx": "Әкелікті анықтау және алимент өндіріп алу туралы талап қою",
    "Иск об устранении нарушений, не связанных с лишением владения.docx": "Иеленуден айырумен байланысты емес бұзушылықтарды жою туралы талап қою",
    "Исковое заявление о взыскании материального ущерба.docx": "Материалдық залалды өндіріп алу туралы талап арыз",
    "Исковое заявление об изменении размера алиментов.docx": "Алимент мөлшерін өзгерту туралы талап арыз",

    "Мировое соглашение.docx": "Татуласу келісімі",
    "Письменное пояснение на уведомление налогового органа об устранении нарушений.docx": "Салық органының бұзушылықтарды жою туралы хабарламасына жазбаша түсініктеме",
    "Претензия о замене некачественного товара.docx": "Сапасыз тауарды ауыстыру туралы претензия",
    "Претензия о замене товара ненадлежащего качества.docx": "Тиісті сапада емес тауарды ауыстыру туралы претензия",
    "Приказ об отпуске без сохранения заработной платы.docx": "Жалақы сақталмайтын демалыс туралы бұйрық",
    "Трудовой договор.docx": "Еңбек шарты",
    "Ходатаство в суд об ознакомлении с материалами дела.docx": "Іс материалдарымен танысу туралы сотқа өтінішхат",
}


KZ_FIELD_LABELS = {
    "contract_number": "Шарт нөмірі",
    "city": "Қала",
    "document_date": "Құжат күні",
    "employer_name": "Жұмыс беруші",
    "employer_representative": "Жұмыс берушінің өкілі",
    "representative_basis": "Өкілеттік негізі",
    "employee_full_name": "Қызметкердің толық аты-жөні",
    "position": "Лауазымы",
    "workplace": "Жұмыс орны",
    "start_date": "Басталу күні",
    "company_name": "Ұйым атауы",
    "order_number": "Бұйрық нөмірі",
    "application_date": "Арыз күні",
    "vacation_start_date": "Демалыстың басталу күні",
    "vacation_end_date": "Демалыстың аяқталу күні",
    "director_name": "Директордың толық аты-жөні",
    "court_name": "Сот атауы",
    "court_address": "Сот мекенжайы",
    "court_city": "Сот орналасқан қала",
    "court_region": "Сот өңірі",
    "court_district": "Сот ауданы",
    "court_extra": "Сот туралы қосымша мәлімет",
    "judge_name": "Судьяның толық аты-жөні",
    "case_number": "Іс нөмірі",
    "claim_subject": "Талап қою нысанасы",
    "claim_request": "Талап қою талабы",
    "claim_facts": "Істің мән-жайлары",
    "claim_basis": "Құқықтық негіздеме",
    "evidence": "Дәлелдемелер",
    "attachments": "Қосымшалар",
    "filing_date": "Берілген күні",
    "signing_date": "Қол қойылған күн",
    "claim_amount": "Талап сомасы",
    "claim_price": "Талап қою бағасы",
    "state_fee": "Мемлекеттік баж",
    "plaintiff_full_name": "Талап қоюшының толық аты-жөні",
    "plaintiff_iin": "Талап қоюшының ЖСН",
    "plaintiff_bin": "Талап қоюшының БСН",
    "plaintiff_address": "Талап қоюшының мекенжайы",
    "plaintiff_phone": "Талап қоюшының телефоны",
    "plaintiff_email": "Талап қоюшының email мекенжайы",
    "plaintiff_city": "Талап қоюшының қаласы",
    "plaintiff_street": "Талап қоюшының көшесі",
    "plaintiff_house": "Талап қоюшының үйі",
    "plaintiff_apartment": "Талап қоюшының пәтері",
    "plaintiff_company": "Талап қоюшы компания",
    "defendant_full_name": "Жауапкердің толық аты-жөні",
    "defendant_iin": "Жауапкердің ЖСН",
    "defendant_bin": "Жауапкердің БСН",
    "defendant_address": "Жауапкердің мекенжайы",
    "defendant_phone": "Жауапкердің телефоны",
    "defendant_email": "Жауапкердің email мекенжайы",
    "defendant_city": "Жауапкердің қаласы",
    "defendant_street": "Жауапкердің көшесі",
    "defendant_house": "Жауапкердің үйі",
    "defendant_apartment": "Жауапкердің пәтері",
    "defendant_company": "Жауапкер компания",
    "claimant_name": "Талапкер",
    "claimant_iin": "Талапкердің ЖСН",
    "claimant_address": "Талапкердің мекенжайы",
    "claimant_phone": "Талапкердің телефоны",
    "claimant_email": "Талапкердің email мекенжайы",
    "claimant_company": "Талапкер компания",
    "respondent_name": "Жауапкер",
    "respondent_iin": "Жауапкердің ЖСН",
    "respondent_address": "Жауапкердің мекенжайы",
    "respondent_phone": "Жауапкердің телефоны",
    "respondent_email": "Жауапкердің email мекенжайы",
    "respondent_company": "Жауапкер компания",
    "respondent_director": "Жауапкер директоры",
    "representative_full_name": "Өкілдің толық аты-жөні",
    "representative_iin": "Өкілдің ЖСН",
    "representative_address": "Өкілдің мекенжайы",
    "representative_phone": "Өкілдің телефоны",
    "marriage_date": "Неке тіркелген күн",
    "divorce_date": "Некені бұзу күні",
    "divorce_reason": "Некені бұзу себебі",
    "spouse_full_name": "Жұбайының толық аты-жөні",
    "children_info": "Балалар туралы мәлімет",
    "child_full_name": "Баланың толық аты-жөні",
    "child_birth_date": "Баланың туған күні",
    "current_child_residence": "Баланың қазіргі тұрғылықты жері",
    "guardianship_department": "Қорғаншылық және қамқоршылық органы",
    "property_description": "Мүліктің сипаттамасы",
    "property_address": "Мүліктің мекенжайы",
    "property_value": "Мүлік құны",
    "ownership_basis": "Меншік құқығының негізі",
    "ownership_share": "Меншік үлесі",
    "ownership_source": "Меншік құқығының шығу негізі",
    "damage_date": "Залал келтірілген күн",
    "damage_reason": "Залал себебі",
    "damage_amount": "Залал сомасы",
    "moral_damage_amount": "Моральдық зиян сомасы",
    "debt_amount": "Берешек сомасы",
    "debt_amount_number": "Берешек сомасы цифрмен",
    "total_amount_number": "Жалпы сома цифрмен",
    "total_amount_words": "Жалпы сома жазбаша",
    "paid_amount": "Төленген сома",
    "contract_date": "Шарт күні",
    "contract_subject": "Шарт нысанасы",
    "contract_amount": "Шарт сомасы",
    "contract_clause": "Шарт тармағы",
    "termination_date": "Шартты бұзу күні",
    "obligation_description": "Міндеттеменің сипаттамасы",
    "performance_date": "Орындау күні",
    "alimony_current_amount": "Қазіргі алимент мөлшері",
    "alimony_requested_amount": "Сұралатын алимент мөлшері",
    "monthly_income": "Айлық табыс",
    "monthly_salary_amount": "Айлық жалақы мөлшері",
    "salary": "Жалақы",
    "bonus_amount": "Сыйақы мөлшері",
    "dismissal_date": "Жұмыстан босату күні",
    "dismissal_reason": "Жұмыстан босату себебі",
    "death_date": "Қайтыс болған күн",
    "death_year": "Қайтыс болған жыл",
    "testator_full_name": "Мұра қалдырушының толық аты-жөні",
    "heir_full_name": "Мұрагердің толық аты-жөні",
    "heirs_info": "Мұрагерлер туралы мәлімет",
    "inheritance_property": "Мұрагерлік мүлік",
    "inheritance_share": "Мұрадағы үлес",
    "inheritance_case_number": "Мұрагерлік іс нөмірі",
    "inheritance_certificate_date": "Мұраға құқық туралы куәлік күні",
    "inheritance_registry_number": "Мұра тізілімінің нөмірі",
    "notary_name": "Нотариустың аты-жөні",
    "registry_number": "Тізілім нөмірі",
    "will_date": "Өсиет күні",
    "seller_name": "Сатушы атауы",
    "seller_bin": "Сатушының БСН",
    "seller_address": "Сатушының мекенжайы",
    "seller_phone": "Сатушының телефоны",
    "seller_email": "Сатушының email мекенжайы",
    "buyer_name": "Сатып алушы атауы",
    "buyer_iin": "Сатып алушының ЖСН",
    "buyer_bin": "Сатып алушының БСН",
    "buyer_address": "Сатып алушының мекенжайы",
    "buyer_phone": "Сатып алушының телефоны",
    "buyer_email": "Сатып алушының email мекенжайы",
    "product_name": "Тауар атауы",
    "product_price": "Тауар бағасы",
    "defects": "Кемшіліктер",
    "purchase_date": "Сатып алу күні",
    "replacement_product": "Ауыстырылатын тауар",
    "penalty_amount": "Айыппұл сомасы",
    "car_make": "Автокөлік маркасы",
    "car_year": "Автокөлік жылы",
    "car_plate": "Мемлекеттік нөмірі",
    "car_vin": "VIN коды",
    "car_color": "Автокөлік түсі",
    "car_value_number": "Автокөлік құны цифрмен",
    "car_value_words": "Автокөлік құны жазбаша",
    "vehicle_certificate_series": "Көлік куәлігінің сериясы",
    "vehicle_certificate_number": "Көлік куәлігінің нөмірі",
    "vehicle_certificate_date": "Көлік куәлігінің күні",
    "vehicle_certificate_issuer": "Көлік куәлігін берген орган"
}


LANG_KZ = {"kz", "kk", "kaz", "қаз", "каз"}


FIELD_PREFIX_KZ = {
    "plaintiff": "Талап қоюшы",
    "defendant": "Жауапкер",
    "defendant2": "Екінші жауапкер",
    "claimant": "Талапкер",
    "respondent": "Жауапкер",
    "applicant": "Өтініш беруші",
    "representative": "Өкіл",
    "principal": "Сенім білдіруші",
    "employee": "Қызметкер",
    "employer": "Жұмыс беруші",
    "company": "Компания",
    "seller": "Сатушы",
    "buyer": "Сатып алушы",
    "supplier": "Жеткізуші",
    "spouse": "Жұбайы",
    "spouse1": "Бірінші жұбай",
    "spouse2": "Екінші жұбай",
    "child": "Бала",
    "parent": "Ата-ана",
    "testator": "Мұра қалдырушы",
    "heir": "Мұрагер",
    "deceased": "Қайтыс болған адам",
    "court": "Сот",
    "case": "Іс",
    "claim": "Талап",
    "contract": "Шарт",
    "property": "Мүлік",
    "inheritance": "Мұра",
    "vehicle": "Көлік",
    "car": "Автокөлік",
    "tax": "Салық органы",
    "store": "Дүкен",
    "service": "Сервис орталығы",
}


FIELD_SUFFIX_KZ = {
    "full_name": "толық аты-жөні",
    "name": "атауы",
    "iin": "ЖСН",
    "bin": "БСН",
    "address": "мекенжайы",
    "phone": "телефоны",
    "email": "email мекенжайы",
    "city": "қаласы",
    "street": "көшесі",
    "house": "үйі",
    "apartment": "пәтері",
    "date": "күні",
    "year": "жылы",
    "number": "нөмірі",
    "series": "сериясы",
    "amount": "сомасы",
    "amount_number": "сомасы цифрмен",
    "amount_words": "сомасы жазбаша",
    "description": "сипаттамасы",
    "info": "туралы мәлімет",
    "basis": "негізі",
    "reason": "себебі",
    "request": "талабы",
    "facts": "мән-жайлары",
    "subject": "нысанасы",
    "price": "бағасы",
    "value": "құны",
    "director": "директоры",
    "representative": "өкілі",
}


GENERIC_KEY_TRANSLATIONS = {
    "accident": "ЖКО",
    "act": "акт",
    "alimony": "алимент",
    "application": "арыз",
    "attachments": "қосымшалар",
    "auction": "сауда-саттық",
    "awarded": "өндірілген",
    "bailiff": "сот орындаушысы",
    "bonus": "сыйақы",
    "certificate": "куәлік",
    "children": "балалар",
    "cohabitation": "бірге тұру",
    "conciliation": "татуласу",
    "construction": "құрылыс",
    "current": "қазіргі",
    "damage": "залал",
    "death": "қайтыс болу",
    "debt": "берешек",
    "decision": "шешім",
    "defect": "кемшілік",
    "delivery": "жеткізу",
    "dependency": "асырауда болу",
    "dependents": "асырауындағы адамдар",
    "director": "директор",
    "disability": "мүгедектік",
    "dismissal": "жұмыстан босату",
    "divorce": "некені бұзу",
    "document": "құжат",
    "encumbrance": "ауыртпалық",
    "eviction": "көшіру",
    "evidence": "дәлелдемелер",
    "expert": "сарапшы",
    "explanation": "түсініктеме",
    "fact": "факт",
    "family": "отбасы",
    "financial": "қаржылық",
    "filing": "беру",
    "forced": "мәжбүрлі",
    "absence": "болмау",
    "guardianship": "қорғаншылық",
    "hire": "жұмысқа қабылдау",
    "illegal": "заңсыз",
    "incident": "оқиға",
    "income": "табыс",
    "injury": "денсаулыққа зиян",
    "interested": "мүдделі",
    "invoice": "шот-фактура",
    "labor": "еңбек",
    "land": "жер",
    "last": "соңғы",
    "loan": "қарыз",
    "lost": "жоғалған",
    "mall": "сауда орталығы",
    "manager": "басшы",
    "medical": "медициналық",
    "memo": "қызметтік жазба",
    "missed": "өткізіп алынған",
    "missing": "хабар-ошарсыз кеткен",
    "monthly": "айлық",
    "moral": "моральдық",
    "notice": "хабарлама",
    "obligation": "міндеттеме",
    "order": "бұйрық",
    "original": "бастапқы",
    "owner": "меншік иесі",
    "ownership": "меншік құқығы",
    "paid": "төленген",
    "paternity": "әкелік",
    "payment": "төлем",
    "penalty": "айыппұл",
    "performance": "орындау",
    "person": "адам",
    "pledgee": "кепіл ұстаушы",
    "pledgor": "кепіл беруші",
    "position": "лауазым",
    "possession": "иелену",
    "previous": "алдыңғы",
    "product": "тауар",
    "purchase": "сатып алу",
    "purpose": "мақсат",
    "refusal": "бас тарту",
    "registration": "тіркеу",
    "registry": "тізілім",
    "relationship": "туыстық қатынас",
    "relative": "туыс",
    "rent": "жалдау ақысы",
    "replacement": "ауыстыру",
    "requested": "сұралатын",
    "residence": "тұрғылықты жер",
    "return": "қайтару",
    "salary": "жалақы",
    "second": "екінші",
    "signing": "қол қою",
    "state": "мемлекеттік",
    "supplier": "жеткізуші",
    "termination": "бұзу",
    "total": "жалпы",
    "vacation": "демалыс",
    "violation": "бұзушылық",
    "will": "өсиет",
    "work": "жұмыс",
    "workplace": "жұмыс орны",
}


def is_kazakh_language(language: str) -> bool:
    return str(language or "").lower() in LANG_KZ


def humanize_field_key_kz(key: str) -> str:
    """
    Fallback translator for fields that are not in KZ_FIELD_LABELS.
    It avoids English labels like "Plaintiff full name".
    """
    if not key:
        return "Өріс"

    if key.startswith("unused_blank_"):
        number = key.rsplit("_", 1)[-1]
        return f"Қосымша өріс {number}"

    if key in KZ_FIELD_LABELS:
        return KZ_FIELD_LABELS[key]

    parts = key.split("_")

    # prefix + suffix pattern, e.g. plaintiff_full_name, defendant_iin
    for prefix in sorted(FIELD_PREFIX_KZ, key=len, reverse=True):
        if key == prefix:
            return FIELD_PREFIX_KZ[prefix]
        if key.startswith(prefix + "_"):
            suffix = key[len(prefix) + 1:]
            if suffix in FIELD_SUFFIX_KZ:
                return f"{FIELD_PREFIX_KZ[prefix]} {FIELD_SUFFIX_KZ[suffix]}"
            suffix_words = [GENERIC_KEY_TRANSLATIONS.get(p, p) for p in suffix.split("_")]
            return f"{FIELD_PREFIX_KZ[prefix]} {' '.join(suffix_words)}"

    # suffix-only pattern
    for suffix, kz_suffix in sorted(FIELD_SUFFIX_KZ.items(), key=lambda x: len(x[0]), reverse=True):
        if key.endswith("_" + suffix):
            base = key[: -(len(suffix) + 1)]
            base_words = [GENERIC_KEY_TRANSLATIONS.get(p, p) for p in base.split("_")]
            return f"{' '.join(base_words)} {kz_suffix}".strip().capitalize()

    words = [GENERIC_KEY_TRANSLATIONS.get(p, p) for p in parts]
    return " ".join(words).strip().capitalize()


def get_kz_hint(field: dict, label: str) -> str:
    """
    Makes a Kazakh hint. We do not pass Russian/English hints when language=kz.
    """
    key = field.get("key", "")
    original_hint = str(field.get("hint") or "")

    if "01.05.2026" in original_hint or key.endswith("_date") or key in {"document_date", "filing_date", "signing_date"}:
        return f"{label}, мысалы: 01.05.2026"

    if key.startswith("unused_blank_"):
        return label

    return label


def get_localized_documents(document_types: dict, language: str = "ru") -> list[dict]:
    documents = []

    for template_name, data in document_types.items():
        title = data.get("title", template_name)

        if is_kazakh_language(language):
            title = KZ_DOCUMENT_TITLES.get(template_name, title)

        documents.append({
            "template_name": template_name,
            "title": title,
        })

    return documents


def get_localized_document(template_name, document_types, language="ru"):
    language = normalize_language(language)

    document = document_types.get(template_name)

    if not document:
        return None

    title = document.get("title", template_name)

    if language == "kk":
        title = KZ_DOCUMENT_TITLES.get(template_name, title)

    return {
        **document,
        "title": title,
        "fields": get_localized_fields(
            document.get("fields", []),
            language
        )
    }


def get_localized_fields(fields, language="ru"):
    language = normalize_language(language)

    if language != "kk":
        return fields

    localized_fields = []

    for field in fields:
        key = field.get("key")
        kz_label = KZ_FIELD_LABELS.get(key)

        localized_fields.append({
            **field,
            "label": kz_label or field.get("label", key),
            "hint": kz_label or field.get("hint", key),
        })

    return localized_fields


def localize_document_types(document_types: dict, language: str = "ru") -> dict:

    if not is_kazakh_language(language):
        return document_types

    localized = {}

    for template_name, data in document_types.items():
        localized[template_name] = get_localized_document(
            template_name,
            data,
            language,
        )

    return localized


def normalize_language(language):
    if not language:
        return "ru"

    language = str(language).lower().strip()

    if language in ["kz", "kk", "kaz", "қазақша"]:
        return "kk"

    return "ru"