class Field:
    START = 'start'
    END = 'end'
    TUID = 'tuid'
    SRC = 'src'
    TARGET = 'target'
    SRC_LANG = 'src_lang'
    TARGET_LANG = 'target_lang'
    RAW = 'raw'
    JSON = 'json'
class Parameters:
    GROUP_ID = 'lengoo_mtx'
    BROKERS = 'kafka://broker-1:9092;kafka://broker-3:9092;kafka://broker-3:9092'
    TOPIC = 'rawdata'
    PATTERNS = [['<', '</', '>', '/>'], ['&lt;', 'br/', '&gt'], ['%link_start%', '%link_end%']]
    ES_INDEX = 'tmx_data'
    ES_BROKER = 'http://gs-search:9200/'

class Tag:
    TU = 'tu'
    TUV = 'tuv'
    TUID = 'tuid'
    SEG = 'seg'

class ErrorMessage:
    FILE_NOT_FOUND = 'file_not_found in given path'

