# ARN_SUITE 
(ru_ru)

Набор утилит ARN_SUITE

### Назначение:

Контроль (мониторинг) работы промышленного оборудованием. Данные собираются с локальных станций сбора данных
по протоколу OPC UA и аккумулируются в БД PostgreSQL

### Состав:

Набор утилит включает три утилиты:

- **argate.exe** - запускается на центральной машине-сервере, опрашивает станции сбора данных,
сохраняет данные в БД, осуществляет автоматическую (по времени) генерацию отчётов
(отчёты сохраняются в файлы \*.xlsx и рассылаются по e-mail)

- **arbmon.exe** - большой центральный монтитор - запускается на клиентской машине
(4 монитора разрешением Ultra HD 4K 3840×2160 - см.фото) на котором отображаются real-time данные
читает данные из БД

- **arterm.exe** - локальный терминал, запускается на клиентской машине (на рабочем месте
пользователя)
читает/пишет данные из/в БД

### Дополнительные директории:

**..\dist\ARNEG_ESMS** - скомпилированные утилиты<br/>
**..\PICS** - фото центрального монитора<br/>

---

# ARN_SUITE
(en_en)

Utility kit ARN_SUITE

### Purpose:

Industrial machine tools operation online monitoring. The data is obtained from distributed local I/O stations
via OPC UA protocol and is stored into PostgreSQL DB

### Composition:

THe kit includes three utility:

- **argate.exe** - runs on the server PC, fetches data from I/O stations,
stores the data into DB, implements automatic time-periodical report generation
(reports are stored into \*.xlsx files and sent via e-mail)

- **arbmon.exe** - big central display - runs on a client PC
( 4 displays Ultra HD 4K 3840×2160 resolution - see pics) and shows real-time data
(reads data from DB)

- **arterm.exe** - local terminal, runs on a client PC (operator's seat)
(reads/writes data from/into DB)

### Auxilliary folders:

**..\dist\ARNEG_ESMS** - compiled programs<br/>
**..\PICS** - big central display on-site pitures<br/>





