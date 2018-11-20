import logging
import logging.handlers

# 20180228 https://stackoverflow.com/questions/1383254/logging-streamhandler-and-standard-streams
from time import monotonic, sleep


class SingleLevelFilter( logging.Filter ):
    def __init__( self, passLevel, onlyThisLevel, passLogName = "" ):
        super().__init__()
        self.passLevel = passLevel
        self.onlyThisLevel = onlyThisLevel

        self.passLogName = passLogName
        if passLogName == "root":
            self.passLogName = ""

    def filter( self, record ):
        recordName = record.name
        if recordName == "root":
            recordName = ""
        if self.onlyThisLevel:
            return (recordName == self.passLogName) and (record.levelno == self.passLevel)
        else:
            return (recordName == self.passLogName) and (record.levelno != self.passLevel)


# Ротируемые Лог файлы с кастомным выводом в различные файлы, в зависимости от имени файла и типа сообщения
# loggerName - Название Логгера, по нему работает фильтр для конкретного Логгера
# INFO - идут в один файл - logNameInfo
# Остальные - идут в другой файл - logNameOther
# Время ротации пока прописано жестко, один раз в час, но можно расширить если нужно, добавив в конструктор доп. параметры
class LoggerInstance:
    loggerInstance = { }

    def __init__( self, logNameInfo, logNameOther, loggerName = "" ):
        self.logNameInfo = logNameInfo
        self.logNameOther = logNameOther
        self.loggerName = loggerName

        rootLogger = logging.getLogger( loggerName )

        formatter = logging.Formatter( "%(asctime)s\t%(levelname)s\t%(message)s" )  # "\t%(name)s"

        # h1 = logging.FileHandler( logNameInfo )
        h1 = logging.handlers.TimedRotatingFileHandler( logNameInfo, when = "H", interval = 1 )  # when = "MIDNIGHT", when = "M"
        h1.suffix = "%Y-%m-%d_%H-%M.rot"  # "%Y-%m-%d"
        f1 = SingleLevelFilter( logging.INFO, True, loggerName )
        h1.addFilter( f1 )
        rootLogger.addHandler( h1 )

        # h2 = logging.FileHandler( logNameOther )
        h2 = logging.handlers.TimedRotatingFileHandler( logNameOther, when = "H", interval = 1 )  # when = "MIDNIGHT", when = "M"
        h2.suffix = "%Y-%m-%d_%H-%M.rot"  # "%Y-%m-%d"
        f2 = SingleLevelFilter( logging.INFO, False, loggerName )
        h2.addFilter( f2 )
        rootLogger.addHandler( h2 )

        h1.setFormatter( formatter )
        h2.setFormatter( formatter )

        # , format = '%(asctime)s\t%(levelname)s\t%(message)s'

        self.logger = rootLogger
        self.logger.setLevel( logging.DEBUG )

    @classmethod
    def getLoggerInstance( cls, logNameInfo, logNameOther, loggerName ):
        if loggerName not in cls.loggerInstance:
            cls.loggerInstance[ loggerName ] = cls( logNameInfo = logNameInfo, logNameOther = logNameOther, loggerName = loggerName )
        return cls.loggerInstance[ loggerName ]

    # если не нужно создавать кастомный логгер, то вызываю стандартный логгер так: logging.getLogger( loggerName )
    @classmethod
    def getLogger( cls, logNameInfo, logNameOther, loggerName ):
        return cls.getLoggerInstance( logNameInfo, logNameOther, loggerName ).logger


# старый вариант, оставлен для совместимости
def setupLogger( logNameInfo, logNameOther, loggerName ):
    rootLogger = logging.getLogger()

    formatter = logging.Formatter( '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s' )

    h1 = logging.FileHandler( logNameInfo )
    f1 = SingleLevelFilter( logging.INFO, True, loggerName )
    h1.addFilter( f1 )
    rootLogger.addHandler( h1 )

    h2 = logging.FileHandler( logNameOther )
    f2 = SingleLevelFilter( logging.INFO, False, loggerName )
    h2.addFilter( f2 )
    rootLogger.addHandler( h2 )

    h1.setFormatter( formatter )
    h2.setFormatter( formatter )

    # , format = '%(asctime)s\t%(levelname)s\t%(message)s'

    loggerLocal = logging.getLogger( loggerName )
    loggerLocal.setLevel( logging.DEBUG )
    return loggerLocal


if __name__ == "__main__":

    timeStart = monotonic()

    loggerStatic = LoggerInstance.getLogger( "logs/static-info", "logs/static-other", "static-1" )
    loggerStatic.info( "loggerStatic - A INFO message - Start" )
    loggerStatic.debug( "loggerStatic - A DEBUG message - Start" )

    loggerInstance = LoggerInstance( "logs/info", "logs/other", "" )
    loggerInstance.logger.info( "An INFO message" )
    loggerInstance.logger.debug( "A DEBUG message" )
    loggerInstance.logger.warning( "A WARNING message" )
    loggerInstance.logger.error( "An ERROR message" )
    loggerInstance.logger.critical( "A CRITICAL message" )

    loggerInstance2 = LoggerInstance( "logs/info2", "logs/other2", "log2" )
    loggerInstance2.logger.info( "! 2 An INFO message" )
    loggerInstance2.logger.debug( "! 2 A DEBUG message" )

    if 1 == 1:
        while True:
            timeCurrent = monotonic()
            delta = (timeCurrent - timeStart)
            loggerInstance.logger.info( "An INFO message" + " " + str( timeCurrent ) + " " + str( int( delta ) ) )
            loggerInstance.logger.debug( "A DEBUG message" + " " + str( timeCurrent ) + " " + str( int( delta ) ) )
            if delta > 65:
                break
            sleep( 15 )

    loggerInstance2.logger.info( "! FINAL 2 An INFO message" )
    loggerInstance2.logger.debug( "! FINAL 2 A DEBUG message" )

    loggerInstance3 = LoggerInstance( "logs/info3", "logs/other3", "log3" )
    loggerInstance3.logger.info( "! 3 An INFO message" )
    loggerInstance3.logger.debug( "! 3 A DEBUG message" )

    loggerTmp = logging.getLogger()
    loggerTmp.info( "!!!! !!!! GLOBAL INFO" )
    loggerTmp.debug( "!!!! !!!! GLOBAL DEBUG" )

    loggerStatic.debug( "loggerStatic - A DEBUG message - Finish" )
    loggerStatic.info( "loggerStatic - A DEBUG message - Finish" )
