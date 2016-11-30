import re
import os
import logging

DIR = "/Users/Cibeles/PycharmProjects/MelaUtils/Series"
LOGFILE = "/Users/Cibeles/PycharmProjects/MelaUtils/flexget/flexget.log"
LOGFORMAT = "[%(asctime)s - %(levelname)s] %(message)s"

#DIR = "/Volumes/Vault/Series/"
#LOGFILE = "/Volumes/Vault/flexget/flexget.log"

formatter = logging.Formatter(LOGFORMAT)
logger = logging.getLogger()

# file handler
file = logging.FileHandler(LOGFILE)
file.setLevel(logging.DEBUG)
file.setFormatter(formatter)
logger.addHandler(file)

# console handler
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)

def normalize_dir(dirname, cwd):
    season_no = re.findall("[0-9].*", dirname)
    final_season = "S" + season_no[0] if len(season_no[0]) > 1 else 'S0' + season_no[0]
    os.rename(cwd + dirname, cwd + final_season)
    logger.info("[NORMALIZE] Directorio " + dirname + " renombrado a " + final_season)

nombre_serie = os.listdir(DIR)
t_reg_ex = re.compile("[s|S][0-9]{2}")

for serie in nombre_serie:
    cwd = DIR + '/' + serie + '/'
    episodios = os.listdir(cwd)
    for item in episodios:
        if not t_reg_ex.match(item):
            normalize_dir(item, cwd)


