# ARN_SUITE

Набор утилит ARN_SUITE

Назначение:

Контроль работы за промышленным оборудованием. Данные собираются с локальных станций сбора данных
по протоколу OPC UA и аккумулируются в БД PostgreSQL

Состав:

Набор утилит включает три утилиты:

- argate.exe - запускатеся на центральной машине-сервере, опрашивает станции сбора данных,
сохраняет данные в БД, осуществляет автоматическую (по времени) генерацию отчётов
(отчёты сохраняются в файлы *.xlsx и рассылаются по e-mail)

- arbmon.exe - большой центральный монтитор - запускается на клиентской машине
(4 монитора разрешением Ultra HD 4K 3840×2160) на котором отображаются real-time данные
читает данные из БД

- arterm.exe - локальный терминал, запускается на клиентской машине (на рабочем месте
пользователя)
читает/пишет данные из/в БД

Скомпилированные утилиты лежат в директории ..\dist\ARNEG_ESMS

