import re
import os
import sys
import logging

DIR = "/Users/Cibeles/PycharmProjects/MelaUtils/Series"
LOGFILE = "/Users/Cibeles/PycharmProjects/MelaUtils/flexget/flexget.log"
LOGFORMAT = "[%(asctime)s - %(levelname)s] %(message)s"

#DIR = "/Volumes/Vault/Series/"
#LOGFILE = "/Volumes/Vault/flexget/flexget.log"

nombre_serie = os.listdir(DIR)
fobj = sys.stdout
ftype_reg_exp = re.compile('.*\.(avi|mkv|mp4|mpg|mpeg)$')
formatter = logging.Formatter(LOGFORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# file handler
file = logging.FileHandler(LOGFILE)
#file.setLevel(logging.INFO)
file.setFormatter(formatter)
logger.addHandler(file)

# console handler
console = logging.StreamHandler()
#console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)

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
            if (os.path.isfile(cwd + item) and ftype_reg_exp.match(cwd + item)) or (os.path.isdir(cwd + item)):
                try:
                    temporada = re.findall("S[0-9]{2}|s[0-9]{2}", item)[0]
                except IndexError:
                    logger.warn("[CLASSIFY] Formato de nombre de capitulo erroneo %s" % (cwd + item))
                    continue
                try:
                    if os.access(cwd, os.W_OK):
                        os.rename(cwd + item, cwd + temporada.upper() + '/' + item)
                        logger.info("[CLASSIFY] Episodio %s movido a %s" % (item, temporada.upper()))
                    else:
                        logger.error("[CLASSIFY] Error de permisos, imposible mover fichero %s" % (cwd + item))
                except OSError, e:
                    if e.errno == 2:
                        if os.access(cwd, os.W_OK):
                            os.mkdir(cwd + temporada.upper())
                            os.rename(cwd + item, cwd + temporada.upper() + '/' + item)
                            logger.info("[CLASSIFY] Episodio %s movido a %s, directorio %s creado" % (item, cwd + temporada.upper(), temporada.upper()))
                        else:
                            logger.error("[CLASSIFY] Error de permisos, imposible crear directorio %s" % (cwd + temporada.upper()))
                            sys.exit(-1)
