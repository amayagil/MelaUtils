import re
import os
import sys
import shutil
import logging

#DIR = "/Users/Cibeles/PycharmProjects/MelaUtils/Descargas"
#LOGFILE = "/Users/Cibeles/PycharmProjects/MelaUtils/flexget/flexget.log"
LOGFORMAT = "[%(asctime)s - %(levelname)s] %(message)s"

DIR = "/Volumes/Vault/Descargas/"
LOGFILE = "/Volumes/Vault/flexget/flexget.log"

nombre_dir = os.listdir(DIR)
fobj = sys.stdout
ftype_reg_exp = re.compile('.*\.(avi|mkv|mp4|mpg|mpeg)$')
formatter = logging.Formatter(LOGFORMAT)
logger = logging.getLogger()

# file handler
file = logging.FileHandler(LOGFILE)
file.setLevel(logging.NOTSET)
file.setFormatter(formatter)
logger.addHandler(file)

# console handler
console = logging.StreamHandler()
console.setLevel(logging.NOTSET)
console.setFormatter(formatter)
logger.addHandler(console)

try:
    fobj = open(LOGFILE, 'a')
except Exception as e:
    if e.errno == 2:
        print "No se pueden escribir logs, el path no existe: " + e.strerror

for item in nombre_dir:
    cwd = DIR + '/' + item + '/'
    print "directorio " + cwd
    if os.path.isdir(cwd):
        directorios = os.listdir(cwd)
        try:
            for item in directorios:
                if (os.path.isfile(cwd + item) and ftype_reg_exp.match(cwd + item)):
                    logger.warn("[PURGE DIRS] Directorio con archivos de video, no se borra %s" % (cwd + item))
                    print "directorio " + cwd + item + "con archivos de video"
                    raise Exception
            shutil.rmtree(cwd)
            print "directorio " + cwd + " vacio lo borrare"
            logger.info("[PURGE DIRS] Directorio vacio o sin archivos de video, borrado %s" % cwd)
        except Exception, e:
            print "excepcion " + e.message
            logger.error("[PURGE DIRS] %s" % e.message)
    else:
        print "directorio " + cwd + "estamos en el raiz, no borro"
        logger.info("[PURGE DIRS] Directorio raiz de descargas %s" % cwd)