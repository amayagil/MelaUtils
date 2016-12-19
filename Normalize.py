import re
import os
import sys
import logging

DIR = "/Users/Cibeles/PycharmProjects/MelaUtils/Series"
LOGFILE = "/Users/Cibeles/PycharmProjects/MelaUtils/flexget/flexget.log"
LOGFORMAT = "[%(asctime)s - %(levelname)s] %(message)s"

#DIR = "/Volumes/Vault/Series/"
#LOGFILE = "/Volumes/Vault/flexget/flexget.log"

formatter = logging.Formatter(LOGFORMAT)
logger = logging.getLogger()
formatter = logging.Formatter(LOGFORMAT)
fobj = sys.stdout

# file handler
file = logging.FileHandler(LOGFILE)
file.setFormatter(formatter)
logger.addHandler(file)

# console handler
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)

def normalize_dir(dirname, cwd):
    season_no = re.findall("[0-9].*", dirname)
    if season_no:
        final_season = "S" + season_no[0] if len(season_no[0]) > 1 else 'S0' + season_no[0]
        os.rename(cwd + dirname, cwd + final_season)
        logger.info("[NORMALIZE] Directorio " + dirname + " renombrado a " + final_season)

nombre_serie = os.listdir(DIR)
t_reg_ex = re.compile("[s|S][0-9]{2}")

try:
    fobj = open(LOGFILE, 'a')
except Exception as e:
    if e.errno == 2:
        print "No se pueden escribir logs, el path no existe: " + e.strerror

for serie in nombre_serie:
    cwd = DIR + '/' + serie + '/'
    if os.path.isdir(cwd):
        episodios = os.listdir(cwd)
        for item in episodios:
            if os.path.isdir(cwd + item) and not t_reg_ex.match(item):
                normalize_dir(item, cwd)
            else:
                logger.info("[NORMALIZE] Nada que normalizar en " + cwd + item)