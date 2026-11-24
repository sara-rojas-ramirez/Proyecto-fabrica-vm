
# Plan de pruebas

## 1. Objetivo

Verificar que la fábrica de máquinas virtuales para laboratorios cumple con los objetivos establecidos, comprobando la creación y administración de máquinas virtuales, el aprovisionamiento automático, la configuración de los servicios, la asignación de recursos, la conectividad de red, la recuperación mediante snapshots, la seguridad y el monitoreo.

## 2. Plan de pruebas

| ID | Funcionalidad | Prueba | Comando | Resultado esperado | Evidencia | Estado |
|---|---|---|---|---|---|---|
| PT-01 | Creación de máquinas virtuales | Verificar la creación de la máquina virtual del curso web. | `python fabrica.py crear web` | Se crea la máquina web01 correctamente y queda disponible para su ejecución. | Figura 5. Resultado de la creación y configuración. | Aprobado |
| PT-02 | Creación de máquinas virtuales | Comprobar el estado de las máquinas virtuales creadas. | `python fabrica.py listar` | La CLI muestra los cursos disponibles y el estado de sus máquinas virtuales. | Figura 6. Confirmación del estado de la máquina. | Aprobado |
| PT-03 | Plantillas | Verificar la existencia de las plantillas correspondientes a los cursos web, bd y redes. | `dir plantillas` | Se identifican los archivos YAML correspondientes a los cursos soportados. | Figuras 4 y 5. Contenido del proyecto y resultado de la creación y configuración (plantillas). | Aprobado |
| PT-04 | Configuración al arrancar | Comprobar la creación del usuario estudiante, el funcionamiento de nginx y la configuración de la zona horaria. | `vagrant ssh web01` y `systemctl status nginx` | Existe el usuario estudiante, nginx está activo y la zona horaria corresponde a Colombia (UTC-05). | Figura 7. Verificación dentro de web01. | Aprobado |
| PT-05 | Red privada | Verificar que las máquinas router y cliente se encuentren encendidas. | `vagrant status` | Las máquinas router y cliente aparecen en estado running. | Figura 9. Estado de router y cliente: ambos en running. | Aprobado |
| PT-06 | Red privada | Comprobar la conectividad desde el router hacia el cliente. | `vagrant ssh router -c "ping -c 3 192.168.56.21"` | El router se comunica con el cliente y el ping presenta 0 % de pérdida de paquetes. | Figura 10. Ping desde el router hacia el cliente (192.168.56.21): 0 % de pérdida. | Aprobado |
| PT-07 | Red privada | Comprobar la conectividad desde el cliente hacia el router. | `vagrant ssh cliente -c "ping -c 3 192.168.56.20"` | El cliente se comunica con el router y el ping presenta 0 % de pérdida de paquetes. | Figura 11. Ping desde el cliente hacia el router (192.168.56.20): 0 % de pérdida. | Aprobado |
| PT-08 | Asignación de recursos | Verificar la memoria RAM y el espacio de intercambio asignados a la máquina virtual. | `free -m` | La máquina presenta aproximadamente 457 MB de RAM y 1952 MB de swap. | Figura 2. Recursos después. | Aprobado |
| PT-09 | Asignación de recursos | Comprobar la cantidad de procesadores asignados a la máquina virtual. | `nproc` | La máquina virtual dispone de 1 CPU. | Figura 2. Recursos después. | Aprobado |
| PT-10 | Snapshot y restauración | Crear un snapshot del estado limpio de la máquina web01. | `vagrant snapshot save web01 limpio` | Se guarda correctamente el snapshot con el nombre limpio. | Figura 12. Snapshot del estado limpio. | Aprobado |
| PT-11 | Snapshot y restauración | Simular un daño en la configuración de nginx y verificar que el archivo de configuración ya no se encuentra disponible. | `sudo rm -rf /etc/nginx` y `ls /etc/nginx` | El directorio de configuración de nginx deja de estar disponible, simulando un daño en la máquina. | Figuras 13 y 14. Daño provocado en nginx y comprobación del daño. | Aprobado |
| PT-12 | Snapshot y restauración | Restaurar el snapshot previamente creado. | `vagrant snapshot restore web01 limpio` | La máquina virtual recupera el estado guardado anteriormente. | Figura 15. Restauración del snapshot. | Aprobado |
| PT-13 | Snapshot y restauración | Comprobar que los archivos de configuración de nginx fueron recuperados. | `ls /etc/nginx` | El directorio /etc/nginx vuelve a estar disponible después de la restauración. | Figura 16. Servicio recuperado tras restaurar. | Aprobado |
| PT-14 | CLI en Python | Verificar que la CLI presenta la ayuda y los comandos disponibles. | `python fabrica.py --help` | Se muestran las opciones y los comandos listar, crear, encender, apagar, destruir, medir, snapshot y restaurar. | Figura 18. Comandos disponibles en fabrica.py. | Aprobado |
| PT-15 | CLI en Python | Comprobar que el comando listar identifica los cursos y sus máquinas virtuales. | `python fabrica.py listar` | Se muestran los cursos bd, redes y web con sus respectivas máquinas y estados. | Figura 19. Resultado de python fabrica.py listar. | Aprobado |
| PT-16 | CLI en Python | Verificar que la CLI refleja el estado de una máquina virtual después de encenderla. | `python fabrica.py listar` | El curso web aparece en estado running después de encender la máquina. | Figura 20. Listar con web encendido. | Aprobado |
| PT-17 | CLI en Python | Comprobar que la CLI permite medir los recursos de la máquina virtual. | `python fabrica.py medir web` | Se muestran los valores de memoria, disco y carga promedio de la máquina. | Figura 21. Medición y registro en logs. | Aprobado |
| PT-18 | CLI en Python | Verificar la creación de un snapshot mediante la CLI. | `python fabrica.py snapshot web limpio` | La CLI crea correctamente el snapshot limpio de web01. | Figura 22. Snapshot creado desde la CLI. | Aprobado |
| PT-19 | CLI en Python | Comprobar la restauración del snapshot mediante la CLI. | `python fabrica.py restaurar web limpio` | La máquina virtual recupera el estado anterior y vuelve a disponer de la configuración de nginx. | Figuras 23 y 24. Daño antes de restaurar y restauración desde la CLI. | Aprobado |
| PT-20 | Seguridad | Verificar que el firewall ufw se encuentre activo y tenga las reglas configuradas. | `vagrant ssh web01 -c "sudo ufw status verbose"` | El firewall está activo, deniega conexiones entrantes por defecto y permite las reglas establecidas para los puertos correspondientes. | Figura 26. Estado del firewall ufw. | Aprobado |
| PT-21 | Seguridad | Comprobar que el acceso directo del usuario root mediante SSH esté deshabilitado. | `vagrant ssh web01 -c "grep PermitRootLogin /etc/ssh/sshd_config"` | La configuración muestra `PermitRootLogin no`. | Figura 27. Acceso de root deshabilitado: PermitRootLogin no en sshd_config. | Aprobado |
| PT-22 | Seguridad | Verificar que la autenticación SSH mediante contraseña esté desactivada y se utilicen llaves. | `vagrant ssh-config web01` | La configuración muestra `PasswordAuthentication no` e identifica la llave privada utilizada para la conexión. | Figura 29. Configuración SSH con autenticación por contraseña desactivada. | Aprobado |
| PT-23 | Monitoreo | Comprobar que se registren las acciones realizadas por la CLI. | `type logs/fabrica.log` | El archivo registra las acciones y comandos ejecutados por la fábrica de máquinas virtuales. | Figura 25. Registro de acciones de la CLI. | Aprobado |
| PT-24 | Monitoreo | Verificar que las mediciones de recursos se almacenen con fecha en el archivo de consumo. | `type logs/consumo.log` | Se registran las mediciones de memoria, disco y carga promedio con sus respectivas fechas. | Figura 31. Contenido de logs\consumo.log con mediciones fechadas de memoria, disco y carga. | Aprobado |
| PT-25 | Monitoreo | Comprobar la ejecución de mediciones sucesivas de recursos mediante la CLI. | `python fabrica.py medir web` | La CLI permite realizar mediciones sucesivas de los recursos de la máquina virtual. | Figura 30. Mediciones sucesivas con python fabrica.py medir web. | Aprobado |
| PT-26 | Monitoreo | Verificar que el registro de acciones de Vagrant se almacene en fabrica.log. | `type logs/fabrica.log` | Se identifican registros de comandos como status, up, snapshot y halt. | Figura 32. Registro logs\fabrica.log: comandos que ejecutó la CLI (status, up, snapshot, halt). | Aprobado |

## 3. Criterios de aceptación

- **Aprobado:** La prueba cumple el resultado esperado y cuenta con evidencia documentada.
- **Fallo:** La prueba no cumple el resultado esperado o presenta errores durante su ejecución.

## 4. Resultado general

Las pruebas documentadas permiten verificar las funcionalidades principales de la fábrica de máquinas virtuales, incluyendo la creación y administración de entornos, la configuración automática, la conectividad, la asignación de recursos, la recuperación mediante snapshots, la seguridad y el monitoreo.
