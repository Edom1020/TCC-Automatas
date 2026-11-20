# Transacciones Bancarias

Aplicación web desarrollada con Flask para analizar transacciones bancarias mediante un analizador léxico y un intérprete basado en autómatas.

## Características

- Analizador léxico con reconocimiento de tokens.
- Intérprete basado en estados.
- Procesamiento de depósitos y retiros.
- Cálculo del saldo acumulado y final.
- Interfaz web para ingresar texto o cargar archivos.
- Visualización de tokens y movimientos realizados.

## Tecnologías utilizadas

- Python
- Flask
- HTML
- CSS
- JavaScript

## Requisitos

Antes de instalar el proyecto, necesitas tener instalado:

- Python 3.10 o superior
- Pip
- Git

Puedes verificar las versiones con:

```bash
python --version
pip --version
git --version

Instalación
1. Clonar el repositorio

2. Entrar al directorio del proyecto

3. Crear un entorno virtual
Windows

Linux o macOS

4. Activar el entorno virtual
Windows PowerShell

Windows CMD

Linux o macOS

5. Instalar Flask

También puedes instalar Flask con el nombre completo del ejecutable:


Ejecución
Ejecuta el servidor desde la raíz del proyecto:


Luego abre en el navegador:


Para detener la aplicación, presiona CTRL+C en la terminal.

Uso de la aplicación
La aplicación permite:

Procesar el texto de ejemplo.
Escribir transacciones manualmente.
Cargar un archivo .txt.
Visualizar los tokens identificados.
Consultar los depósitos y retiros.
Ver el saldo acumulado después de cada movimiento.
Ver el saldo final.
Formato de las transacciones
Cada transacción debe escribirse dentro de una etiqueta <mov>:


Tipos admitidos
Deposito: suma el valor al saldo.
Retiro: resta el valor al saldo.
Ejemplo del resultado:


Ejecución desde la consola
También puedes ejecutar el programa sin la interfaz web:


Para procesar un archivo de texto:


Estructura del proyecto

Descripción de los archivos
app.py: aplicación web creada con Flask.
transacciones.py: contiene el analizador léxico, las transiciones del autómata y el intérprete.
templates/index.html: interfaz gráfica de la aplicación.
.gitignore: archivos y directorios excluidos de Git.
Solución de problemas
El comando flask no es reconocido
Instala Flask dentro del entorno virtual:


No se activa el entorno virtual en PowerShell
Ejecuta PowerShell como usuario normal y permite scripts temporales:


El puerto 5000 está ocupado
Puedes iniciar Flask con otro puerto modificando temporalmente la ejecución:


También puedes cambiar el puerto en app.py.

Autor
Edom1020
