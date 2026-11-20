# Transacciones Bancarias

Aplicación web desarrollada con Flask para analizar transacciones bancarias mediante un analizador léxico y un intérprete basado en autómatas.

## Características

- Analiza texto mediante un analizador léxico.
- Procesa depósitos y retiros con un intérprete basado en estados.
- Calcula el saldo acumulado después de cada movimiento.
- Permite escribir o cargar transacciones desde un archivo.
- Muestra los tokens reconocidos y el resultado final.

## Tecnologías

- Python 3
- Flask
- HTML y CSS

## Requisitos

- Python 3.10 o superior
- Pip
- Git

Comprueba las instalaciones con:

```bash
python --version
pip --version
git --version
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Edom1020/TCC-Automatas.git
cd TCC-Automatas
```

### 2. Crear un entorno virtual

En Windows:

```powershell
python -m venv .venv
```

En Linux o macOS:

```bash
python3 -m venv .venv
```

### 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

En Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar las dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecutar la aplicación

Desde la raíz del proyecto:

```bash
python app.py
```

Abre esta dirección en el navegador:

```text
http://127.0.0.1:5000
```

Para detener el servidor, presiona `Ctrl+C` en la terminal.

## Formato de entrada

Cada movimiento debe tener la siguiente estructura:

```text
<mov>Tipo: Deposito; Valor: 500</mov>
<mov>Tipo: Retiro; Valor: 200</mov>
<mov>Tipo: Deposito; Valor: 100</mov>
```

Tipos admitidos:

- `Deposito`: suma el valor al saldo.
- `Retiro`: resta el valor al saldo.

En el ejemplo anterior, el saldo final es `400`.

## Uso por consola

También se puede ejecutar el procesamiento desde la terminal:

```bash
python transacciones.py
```

Para procesar un archivo de texto:

```bash
python transacciones.py archivo.txt
```

## Estructura del proyecto

```text
TCC-Automatas/
├── app.py
├── transacciones.py
├── requirements.txt
├── templates/
│   └── index.html
├── .gitignore
└── README.md
```

## Archivos principales

- `app.py`: inicia la aplicación web con Flask.
- `transacciones.py`: contiene el analizador léxico y el intérprete.
- `templates/index.html`: interfaz web.
- `requirements.txt`: dependencias del proyecto.

## Solución de problemas

### PowerShell impide activar el entorno virtual

Permite la activación solo en la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### Flask no se reconoce

Verifica que el entorno virtual esté activo y ejecuta:

```bash
python -m pip install -r requirements.txt
```

## Autor

Edom1020
