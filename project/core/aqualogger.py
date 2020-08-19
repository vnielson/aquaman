import logging
import sys

aqlog = logging.getLogger('aqualog')
sysoplog = logging.getLogger('SYSTEMOPERATION')
senlog = logging.getLogger('SENSOR')
corelog = logging.getLogger('CORE')
croplog = logging.getLogger('CROP')
valvelog = logging.getLogger('VALVE')
systestlog = logging.getLogger('SYSTEMTEST')
waterlog = logging.getLogger('WATER')
monitorlog = logging.getLogger('MONITOR')
logviewerlog = logging.getLogger('LOGVIEWER')
weatherlog = logging.getLogger('WEATHER')

def init_logger(logger_instance, log_level, log_file_name):

    # logger_instance = logging.getLogger(logger_name)

    # create logger
    logger_instance.setLevel(log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(log_level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
    # formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger_instance.addHandler(ch)

    # Set up the file stream handler
    fh = logging.FileHandler(log_file_name, mode='a', encoding=None, delay=False)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger_instance.addHandler(fh)

    return logger_instance

    # # 'application' code
    # aqlog.debug('debug message')
    # aqlog.info('info message')
    # aqlog.warning('warn message')
    # aqlog.error('error message')
    # aqlog.critical('critical message')


def init_logging_system(for_which_system):
    if (for_which_system == "aquaman"):
        init_logger(aqlog, logging.INFO, "aquaman.log")
        init_logger(sysoplog, logging.INFO, "aquaman.log")
        init_logger(senlog, logging.INFO, "aquaman.log")
        init_logger(corelog, logging.INFO, "aquaman.log")
        init_logger(croplog, logging.INFO, "aquaman.log")
        init_logger(valvelog, logging.INFO, "aquaman.log")
        init_logger(systestlog, logging.INFO, "aquaman.log")
        init_logger(waterlog, logging.INFO, "aquaman.log")
        init_logger(logviewerlog, logging.INFO, "aquaman.log")
        init_logger(weatherlog, logging.DEBUG, "aquaman.log")

    if (for_which_system == "monitor"):
        init_logger(monitorlog, logging.INFO, "/home/pi/projects/aquaman/monitor.log")




