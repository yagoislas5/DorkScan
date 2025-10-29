<p align="center">
  <img src="img/DorkScan.png" alt="DorkScan Logo" width="400"/>
</p>

# DorkScan

DorkScan es una herramienta de escaneo automatizado de **Google Dorks** utilizando **Brave Search**. Está diseñada para investigadores de seguridad, profesionales de OSINT y entusiastas del hacking ético que buscan identificar recursos expuestos en dominios específicos.

---

## Índice

* [Características](#características)
* [Requisitos](#requisitos)
* [Archivos incluidos](#archivos-incluidos-en-el-proyecto)
* [Instalación](#instalación)
* [Uso](#uso)
* [Parámetros](#parámetros)
* [Licencia](#licencia)
* [Contacto](#contacto)

---

## Características

* Generación dinámica de dorks personalizados a partir de plantillas.
* Navegación automatizada con Playwright y rotación de User-Agent.
* Validación previa del dominio objetivo antes de iniciar el escaneo.
* Extracción de resultados desde Brave Search.
* Guardado opcional de resultados en archivo local.

---

## Requisitos

* **Python 3.12** o superior.
* Playwright instalado y configurado:

```bash
pip install playwright
playwright install
```

---

## Archivos incluidos en el proyecto

* `dorks.txt` — contiene 45 dorks listos para usar, con `{domain}` como marcador de posición.
* `user-agents.txt` — contiene 30 user agents para rotación automática.
* `results.txt` (opcional) — archivo donde se pueden guardar resultados.
* `DorkScan.py` — script principal.
* `LICENSE` — licencia del proyecto.
* `README.md` — documentación del proyecto.

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/yagoislas5/dorkscan.git
cd dorkscan
```

2. Crear un entorno virtual (opcional pero recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

> Asegúrate de tener Playwright instalado y sus navegadores configurados (`playwright install`) si el script usa navegación real.

---

## Uso

Ejecutar el script principal indicando el dominio objetivo:

```bash
python3 DorkScan.py dominio.com --save
```

---

## Parámetros

* `dominio.com`: dominio objetivo a escanear.
* `--save` o `-OG`: guarda los resultados en el archivo `results.txt`.

El script validará si el dominio está disponible antes de iniciar el escaneo. Los resultados se obtienen desde Brave Search y se filtran para mostrar solo enlaces válidos.

---

## Licencia

Este proyecto se distribuye bajo la **Licencia de Uso No Comercial – Yago 2025**.

* Uso libre para fines personales, educativos o de investigación.
* Prohibido el uso comercial sin autorización expresa del autor.
* Atribución obligatoria con nombre y enlace al perfil de GitHub.

Para más detalles, consulte el archivo `LICENSE`.

---
#### Estado del proyecto
DorkScan se encuentra actualmente fuera de funcionamiento. Google ha detectado el patrón de automatización utilizado por la herramienta y ha implementado un CAPTCHA en sus resultados, lo que impide la ejecución automática de las búsquedas. Estamos evaluando alternativas y motores de búsqueda más permisivos para futuras versiones.

---

## Contacto

Para consultas, colaboraciones o acuerdos comerciales, puede contactar al autor a través de su perfil de GitHub:

[https://github.com/yagoislas5](https://github.com/yagoislas5)
