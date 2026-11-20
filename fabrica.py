import argparse
import os
import re
import subprocess
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PLANTILLAS = os.path.join(BASE, "plantillas")
LOGS = os.path.join(BASE, "logs")


def ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def registrar(texto, archivo="fabrica.log"):
    os.makedirs(LOGS, exist_ok=True)
    with open(os.path.join(LOGS, archivo), "a", encoding="utf-8") as f:
        f.write(ahora() + " - " + texto + "\n")


def cursos():
    return sorted(f[:-5] for f in os.listdir(PLANTILLAS) if f.endswith(".yaml"))


def validar(curso):
    if curso not in cursos():
        print("Curso no valido. Disponibles: " + ", ".join(cursos()))
        sys.exit(1)


def maquinas(curso):
    ruta = os.path.join(PLANTILLAS, curso + ".yaml")
    with open(ruta, encoding="utf-8") as f:
        return re.findall(r"^\s*-\s*nombre:\s*(\S+)", f.read(), re.M)


def vagrant(curso, *args):
    validar(curso)
    env = dict(os.environ, CURSO=curso)
    cmd = ["vagrant"] + list(args)
    registrar("curso=%s comando=%s" % (curso, " ".join(cmd)))
    return subprocess.run(cmd, cwd=BASE, env=env, shell=True).returncode


def listar(curso=None):
    for c in cursos():
        print("\n=== Curso: %s | Maquinas: %s ===" % (c, ", ".join(maquinas(c))))
        vagrant(c, "status")


def medir(curso):
    validar(curso)
    env = dict(os.environ, CURSO=curso)
    for m in maquinas(curso):
        r = subprocess.run(
            ["vagrant", "ssh", m, "-c", "free -m; df -h /; uptime"],
            cwd=BASE, env=env, shell=True, capture_output=True,
            text=True, encoding="utf-8", errors="replace")
        salida = "== %s / %s ==\n%s%s" % (curso, m, r.stdout, r.stderr)
        print(salida)
        registrar(salida, "consumo.log")


def main():
    p = argparse.ArgumentParser(description="Fabrica de maquinas virtuales para laboratorios")
    sub = p.add_subparsers(dest="accion", required=True)

    sub.add_parser("listar", help="Lista cursos y estado de sus maquinas")
    for nombre, ayuda in [
        ("crear", "Crea y configura las maquinas del curso"),
        ("encender", "Enciende las maquinas ya creadas"),
        ("apagar", "Apaga las maquinas del curso"),
        ("destruir", "Elimina las maquinas del curso"),
        ("medir", "Mide RAM, disco y carga de cada maquina"),
    ]:
        s = sub.add_parser(nombre, help=ayuda)
        s.add_argument("curso")
    for nombre, ayuda in [
        ("snapshot", "Guarda un estado limpio"),
        ("restaurar", "Vuelve a un estado guardado"),
    ]:
        s = sub.add_parser(nombre, help=ayuda)
        s.add_argument("curso")
        s.add_argument("nombre", nargs="?", default="limpio")

    a = p.parse_args()
    if a.accion == "listar":
        listar()
    elif a.accion == "crear":
        vagrant(a.curso, "up")
    elif a.accion == "encender":
        vagrant(a.curso, "up", "--no-provision")
    elif a.accion == "apagar":
        vagrant(a.curso, "halt")
    elif a.accion == "destruir":
        vagrant(a.curso, "destroy", "-f")
    elif a.accion == "medir":
        medir(a.curso)
    elif a.accion == "snapshot":
        vagrant(a.curso, "snapshot", "save", "--force", a.nombre)
    elif a.accion == "restaurar":
        vagrant(a.curso, "snapshot", "restore", "--no-provision", a.nombre)


if __name__ == "__main__":
    main()
