# Virtual Lab: Fábrica de máquinas virtuales para laboratorios

Herramienta que crea laboratorios completos de máquinas virtuales Linux de forma automática, a partir de código. Con una sola orden se obtienen entornos idénticos, configurados y conectados entre sí, listos para usar en minutos.

**Curso:** Sistemas Operativos
**Integrantes:** Daniela Arias Giraldo, Martha Mahecha, Sebastian Osorio Loaiza, Sara Rojas, Scarleth Covos

---

## 1. Problema

Un instituto de formación prepara a mano los computadores de cada curso. Es lento y, con el tiempo, ningún equipo queda igual a otro. Este proyecto automatiza el proceso: se elige el tipo de curso y el sistema fabrica el laboratorio completo.

## 2. Funcionalidades

| N.º | Funcionalidad | Cómo se implementa |
|---|---|---|
| 1 | Crear VMs desde código | `Vagrantfile` con VirtualBox |
| 2 | Plantillas por curso | Archivos YAML en `plantillas/` (web, bd, redes) |
| 3 | Configuración automática al arrancar | `provision/base.sh` (usuarios, paquetes, zona horaria, SSH) |
| 4 | Red privada | IPs fijas en la red `192.168.56.0/24` |
| 5 | Recursos por plantilla y medición | CPU y RAM definidas en cada plantilla; comando `medir` |
| 6 | Snapshot y restauración | `snapshot` y `restaurar` en el CLI |
| 7 | Panel de gestión (CLI) | `fabrica.py` |

Además: seguridad (`provision/seguridad.sh`) y monitoreo (registros en `logs/`).

## 3. Requisitos

- Windows 10/11 con virtualización activada en la BIOS (Intel VT-x o AMD-V).
- [VirtualBox](https://www.virtualbox.org/) 7.x
- [Vagrant](https://developer.hashicorp.com/vagrant/install)
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) 3.8 o superior (no requiere librerías externas)
- RAM: 8 GB recomendados. Enciende **una plantilla a la vez**.
- Disco: 15 a 20 GB libres (la box de Debian y los discos de las VMs).

## 4. Estructura del proyecto

```
fabrica-vm/
├── Vagrantfile           # Lee la plantilla del curso y crea las VMs
├── fabrica.py            # CLI de gestión
├── plantillas/
│   ├── web.yaml
│   ├── bd.yaml
│   └── redes.yaml
├── provision/
│   ├── base.sh           # Usuarios, paquetes, hora, SSH
│   └── seguridad.sh      # Firewall y endurecimiento de SSH
├── logs/                 # fabrica.log y consumo.log
└── docs/
    ├── plan_pruebas.md
    └── documentacion.pdf       # Incluye las evidencias
```

## 5. Instalación

```powershell
git clone https://github.com/USUARIO/fabrica-vm.git
cd fabrica-vm
python fabrica.py --help
```

Reemplaza `USUARIO` por el usuario de GitHub del repositorio. La primera vez que se crea una VM, Vagrant descarga la box `generic/debian12` (varios cientos de MB).

## 6. Uso

Todos los comandos se ejecutan en PowerShell, dentro de la carpeta del proyecto.

| Comando | Qué hace |
|---|---|
| `python fabrica.py listar` | Muestra los cursos y el estado de sus máquinas |
| `python fabrica.py crear <curso>` | Crea y configura las máquinas del curso |
| `python fabrica.py encender <curso>` | Enciende máquinas ya creadas |
| `python fabrica.py apagar <curso>` | Apaga las máquinas del curso |
| `python fabrica.py destruir <curso>` | Elimina las máquinas del curso |
| `python fabrica.py medir <curso>` | Mide RAM, disco y carga, y lo registra |
| `python fabrica.py snapshot <curso> [nombre]` | Guarda un estado limpio (por defecto `limpio`) |
| `python fabrica.py restaurar <curso> [nombre]` | Vuelve a un estado guardado |

Ejemplo:

```powershell
python fabrica.py crear web
python fabrica.py snapshot web limpio
python fabrica.py medir web
python fabrica.py restaurar web limpio
python fabrica.py apagar web
```

Para entrar a una máquina:

```powershell
$env:CURSO="web"
vagrant ssh web01
```

`$env:CURSO` debe tener el valor del curso con el que se creó la máquina, y solo dura mientras la ventana de PowerShell esté abierta.

## 7. Plantillas

| Curso | Máquinas | IP | RAM | CPU | Software |
|---|---|---|---|---|---|
| `web` | web01 | 192.168.56.10 | 512 MB | 1 | nginx |
| `bd` | bd01 | 192.168.56.11 | 768 MB | 1 | mariadb-server |
| `redes` | router, cliente | 192.168.56.20 y .21 | 384 MB c/u | 1 | net-tools, traceroute, tcpdump |

Para crear un curso nuevo basta con agregar un archivo `.yaml` en `plantillas/` con la misma estructura.

## 8. Configuración automática

Al crearse, cada máquina ejecuta `provision/base.sh`, que:

- Configura la zona horaria `America/Bogota`.
- Instala los paquetes de la plantilla.
- Crea el usuario `estudiante`.
- Activa el servicio SSH.
- Registra el resultado en `/var/log/fabrica.log`.

## 9. Seguridad

`provision/seguridad.sh` aplica:

- Firewall `ufw` con política de entrada denegada por defecto; solo se permite SSH (22) y HTTP (80) desde la red privada.
- Inicio de sesión de `root` por SSH deshabilitado.
- Usuario `estudiante` sin privilegios de `sudo`.
- Acceso de administración por **llaves SSH** (Vagrant no usa contraseña).
- Red privada aislada entre las máquinas del laboratorio.

> La contraseña del usuario `estudiante` es una credencial de laboratorio definida en `provision/base.sh`. Debe cambiarse en cualquier uso fuera del entorno académico.

## 10. Monitoreo

- `logs/fabrica.log`: cada comando que ejecuta el CLI, con fecha y hora.
- `logs/consumo.log`: lecturas de RAM, disco y carga de cada máquina (comando `medir`).
- `/var/log/fabrica.log` (dentro de cada VM): resultado del aprovisionamiento.

## 11. Pruebas y evidencias

El plan de pruebas está en [`docs/plan_pruebas.md`](docs/plan_pruebas.md) y la documentación con la evidencia de capturas en [`docs/documentacion.pdf`]).

**Video demostrativo:** _(pegar aquí el enlace de Drive o YouTube)_

## 12. Solución de problemas

| Problema | Solución |
|---|---|
| La VM ignora la RAM o CPU definidas | Verifica que el nombre de la variable sea `vb.memory` y destruye la VM (`destruir`) para recrearla |
| `vagrant up` falla al iniciar la VM | Revisa que la virtualización esté activa y, si usas Hyper-V o WSL2, desactiva `hypervisorlaunchtype` |
| Error de red Host-Only | En VirtualBox, *Herramientas → Redes*, confirma el rango `192.168.56.x` |
| `systemctl status` queda en pantalla | Presiona `q` o usa `--no-pager` |
| `web.yaml` o `Vagrantfile` quedan vacíos | Se crearon con el Bloc de notas sin guardar; recréalos desde PowerShell |

## 13. Responsabilidades

| Integrante | Funcionalidad a cargo |
|---|---|
| Daniela Arias Giraldo | _Video demostrativo_ |
| Martha Mahecha | _Documentación y creación del plan de pruebas_ |
| Sebastian Osorio Loaiza | _Funcionalidad 7_ |
| Sara Rojas | _Funcionalidades 1 a 6_ |
| Scarleth Covos | _Funcionalidades 1 a 6_ |

## 14. Reto extra (grupos de 5)

Comparación del tiempo y los recursos de crear el mismo entorno como máquina virtual y como contenedor Docker. _(Pendiente de completar.)_

## 15. Tecnologías

Linux (Debian 12) · Vagrant · VirtualBox · Bash · Python · Git
