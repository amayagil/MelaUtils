import re
import os
import time
import sys

DIR = "/Volumes/Vault/Series/"
LOGFILE = "/Volumes/Vault/flexget/flexget.log"

nombre_serie = os.listdir(DIR)
fobj = sys.stdout
ftype_reg_exp = re.compile('.*\.(avi|mkv|mp4)$')

def escribe_log(tipo, mensaje):
    log_msg = time.strftime("[%d/%m/%Y %H:%M:%S] CLASSIFY.")
    log_msg += tipo + " "
    log_msg += mensaje + "\n"
    fobj.write(log_msg)


try:
    fobj = open(LOGFILE, 'a')
except Exception as e:
    if e.errno == 2:
        print "No se pueden escribir logs, path no existe: " + e.strerror

for serie in nombre_serie:
    cwd = DIR + serie + '/'
    if os.path.isdir(cwd):
        episodios = os.listdir(cwd)
        for item in episodios:
            escribe_log("INFO", "Procesando directorio " + cwd)
            if os.path.isfile(cwd + item) and (ftype_reg_exp.match(cwd + item)):
                temporada = re.findall("S|s[0-9]{2}", item)[0]
                try:
                    if os.access(cwd, os.W_OK):
                        os.rename(cwd + item, cwd + temporada.upper() + '/' + item)
                        escribe_log("INFO", "Episodio " + item + " movido a " + temporada.upper())
                    else:
                        escribe_log("ERROR", "Error de permisos, imposible mover fichero")
                except OSError, e:
                    if e.errno == 2:
                        if os.access(cwd, os.W_OK):
                            os.mkdir(cwd + temporada.upper())
                            os.rename(cwd + item, cwd + temporada.upper() + '/' + item)
                            escribe_log("INFO",
                                        "Episodio " + item + " movido a " + temporada.upper() + ", directorio " + temporada.upper() + " creado")
                        else:
                            escribe_log("ERROR", "Error de permisos, imposible crear directorio")
