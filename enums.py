#################################################################




#################################################################
# описание класса:
# - класс для объявления глобальных ENUM
#################################################################

class ENM_MACHINE_TOOL_CLASSES():

    UNKNOWN                     = 0
    PUNCH                       = 1
    BEND                        = 2
    WELD                        = 3
    PAINT                       = 4
    CLASS_5                     = 5

class ENM_MACHINE_TOOLS():

    UNKNOWN                     = 0
    STAMP_M1_SALVAGNINI_GREY    = 1
    STAMP_M2_SALVAGNINI_GREEN   = 2
    STAMP_M3_TRUMPF_600         = 3
    STAMP_M3_TRUMPF_3000        = 4
    STAMP_M4_TRUMPF_6000        = 5
    BEND_P1_STARMATIC_ROBOT     = 6
    BEND_P2_COLGAR_BIG_1        = 7
    BEND_P2_COLGAR_BIG_2        = 8
    BEND_P3_COLGAR_MEDIUM       = 9
    BEND_P4_COLGAR_SMALL        = 10
    BEND_P5_COLGAR_BIG_3        = 11
    BEND_P6_TRUBEND             = 12
    BEND_P7_SALVAGNINI_GREEN    = 13
    BEND_P8_SALVAGNINI_YELLOW   = 14
    WELD_SV2_ABB_ROBOT          = 15
    COAT_N_POWDER_COAT          = 16
    MT_17                       = 17
    MT_18                       = 18
    MT_19                       = 19
    MT_20                       = 20
    MT_21                       = 21
    MT_22                       = 22
    MT_23                       = 23
    MT_24                       = 24
    MT_25                       = 25

#################################################################

class ENM_FIELD_STATION_SIGNALS(): # произвести ревизию, не укладывается в концепцию !!!

    UNKNOWN                          = 0
    BUTTON_ALARM_ON_FAILURE          = 1
    BUTTON_ALARM_ON_MATERIAL         = 2
    BUTTON_STOP_ON_FAILURE           = 3
    BUTTON_STOP_ON_MATERIAL          = 4
    BUTTON_STOP_ON_PROCESS           = 5
    BUTTON_STOP_ON_QUALITY           = 6
    AUX_1                            = 7
    AUX_2                            = 8

#################################################################

class ENM_APP_TABLES():

    UNKNOWN                         = 0
    MACHINE_TOOL_CLASSES            = 1
    MACHINE_TOOLS                   = 2

#################################################################

class ENM_DB_TABLES():

    TABLE_UNKNOWN                   = 0
    TABLE_MACHINE_TOOL_CLASSES      = 1
    TABLE_MACHINE_TOOLS             = 2

#################################################################

class ENM_ARGATE_PANES():

    PANE_UNKNOWN                    = 0
    PANE_MAIN                       = 1
    PANE_SETTINGS                   = 2
    PANE_TESTS                      = 3
    PANE_APP_MONITOR                = 4
    PANE_FIELDACCESS_MONITOR        = 5
    PANE_DBACCESS_MONITOR           = 6
    PANE_REPORT_GENERATION_MONITOR  = 7

#################################################################

class ENM_ARTERM_PANES():

    PANE_UNKNOWN                    = 0
    PANE_BASIC                      = 1
    PANE_FIELD_MONITOR              = 2
    PANE_DAY_VIEWER                 = 3
    PANE_DETAILED_REP               = 4
    PANE_SERVICE_SETTINGS           = 5
    PANE_SERVICE_ARBMON             = 6

#################################################################

class ENM_STATE_TYPES():

    UNKNOWN                         = 0
    BUTTON_ALARM_ON_FAILURE         = 1
    BUTTON_ALARM_ON_MATERIAL        = 2
    BUTTON_STOP_ON_FAILURE          = 3
    BUTTON_STOP_ON_MATERIAL         = 4
    BUTTON_STOP_ON_PROCESS          = 5
    BUTTON_STOP_ON_QUALITY          = 6
    OPERATION                       = 7

#################################################################

class ENM_TABLE_DATA_TYPE():

    UNKNOWN                         = 0
    BOOL                            = 1
    INT                             = 2
    REAL_1                          = 3  # 1 знак после запятой
    REAL_2                          = 4  # 2 знака после запятой
    REAL_3                          = 5  # 3 знака после запятой
    STRING                          = 6
    TEXT                            = 7
    IP_ADDRESS                      = 8
    DATE                            = 9
    TIME                            = 10
    DATETIME                        = 11
    ENUM                            = 12

#################################################################

class ENM_WEEKDAYS():

    UNKNOWN                         = 0
    MONDAY                          = 1
    TUESDAY                         = 2
    WEDNESDAY                       = 3
    THIRSDAY                        = 4
    FRIDAY                          = 5
    SATURDAY                        = 6
    SUNDAY                          = 7

#################################################################

class ENM_WEEKEND_DAY():

    SATURDAY                        = 1
    SUNDAY                          = 2

#################################################################

class ENM_R02_RECTYPE_ID():

    INVALID                         = -1
    UNKNOWN                         = 0
    DAILY_DATA                      = 1
    SUM_BY_MONTH                    = 2
    MONTHLY_DATA                    = 3
    SUM_BY_YEAR                     = 4
    YEARLY_DATA                     = 5
    SUM_OVERALL                     = 6 # not used

#################################################################

class ENM_ALARM_PANE_TYPE():

    UNKNOWN                         = 0
    ALR_FAILURE                     = 1
    ALR_MATERIAL                    = 2
    STP_FAILURE                     = 3
    STP_MATERIAL                    = 4
    STP_QUALITY                     = 5
    STP_PROCESS                     = 6

#################################################################

class ENM_MT_STAT_COLUMN():

    # БД поддерживает максимально:
    # - 23 станка
    # - 5 классов

    MT01                           = 0
    MT02                           = 1
    MT03                           = 2
    MT04                           = 3
    MT05                           = 4
    MT06                           = 5
    MT07                           = 6
    MT08                           = 7
    MT09                           = 8
    MT10                           = 9
    MT11                           = 10
    MT12                           = 11
    MT13                           = 12
    MT14                           = 13
    MT15                           = 14
    MT16                           = 15
    MT17                           = 16
    MT18                           = 17
    MT19                           = 18
    MT20                           = 19
    MT21                           = 20
    MT22                           = 21
    MT23                           = 22
    CL1                            = 23
    CL2                            = 24
    CL3                            = 25
    CL4                            = 26
    CL5                            = 27

#################################################################

class ENM_LAMP_SHAPE():
    UNKNOWN = 0
    ROUND = 1
    SQUARED = 2

#################################################################

class ENM_LAMP_COLOR():
    UNKNOWN = 0
    GREY = 1
    GREEN = 2
    YELLOW = 3
    RED = 4

#################################################################








