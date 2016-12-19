import re
import os
import sys
import shutil
import logging

DIR = "/Users/Cibeles/PycharmProjects/MelaUtils/Descargas"
LOGFILE = "/Users/Cibeles/PycharmProjects/MelaUtils/flexget/flexget.log"
LOGFORMAT = "[%(asctime)s - %(levelname)s] %(message)s"
PELIS_HOME="/Users/Cibeles/PycharmProjects/MelaUtils/Pelis"

#DIR = "/Volumes/Vault/Descargas/"
#LOGFILE = "/Volumes/Vault/flexget/flexget.log"
#PELIS_HOME="/Volumes/Vault/Peliculas"

nombre_dir = os.listdir(DIR)
fobj = sys.stdout
ftype_reg_exp = re.compile('.*\.(avi|mkv|mp4|mpg|mpeg)$')
ftype_serie_regex = re.compile('.+(S[0-9]{2}|s[0-9]{2}).*')
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

for peli in nombre_dir:
    cwd = DIR + '/' + peli
    #print "directorio " + cwd
    if not (ftype_serie_regex.match(cwd)):
        #os.path.isdir(cwd) or os.path.isfile(cwd) ) and
        logger.info(cwd + " no es una serie, se movera a " + PELIS_HOME
        print "procesando: " + cwd
        try:
            shutil.move(cwd,PELIS_HOME)
            logger.info(cwd + " movido exitosamente")
        except Exception, e:
            print "Error al mover: " + e.message
           logger.error(cwd + " no se ha podido mover a " + PELIS_HOME + "el directorio ya existe")
    else:
        logger.warn(cwd + " es una serie, no una peli, no se movera.")