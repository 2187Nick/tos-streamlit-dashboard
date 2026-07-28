# TOS Streamlit Dashboard

Un panel de control en tiempo real que utiliza el RTD (Real-Time Data) de ThinkorSwim y Streamlit.

## Demo
https://github.com/user-attachments/assets/1d6446e0-5c49-4208-872f-f63a55da36a5


## Prerrequisitos

- Sistema Operativo Windows (requerido para ThinkorSwim RTD)
- Python 3.10 a 3.13. Streamlit no es compatible con 3.14
- Aplicación de escritorio de ThinkorSwim instalada y ejecutándose

## Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/2187Nick/tos-streamlit-dashboard
```
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Iniciar la aplicación de escritorio de ThinkorSwim e iniciar sesión
2. Ejecutar el panel de control:
```bash
streamlit run app.py
```
3. Abrir el navegador y navegar a `http://localhost:8501`

## Controles de la Interfaz


- **Symbol**: Símbolo del ticker (ej. "SPY")
- **Expiry Date**: Fecha de vencimiento del contrato (Por defecto el viernes más cercano)
- **Strike Range**: Rango de strikes a monitorear (Por defecto +- $10)
- **Strike Spacing**: Espaciado entre strikes (Por defecto 1)
- **Refresh Rate**: Tasa de refresco de datos (Por defecto 15 segundos)
- **Start/Stop**: Alternar la transmisión de datos

## Notas

- Esto funciona con Ondemand. Puede usarse los fines de semana para revisar datos históricos.
- Los valores de Gamma se muestran en millones de dólares por cada movimiento del 1% en el activo subyacente.

## Construcción
- Este repositorio es un ejemplo básico. Esperamos que construyas sobre él y lo adaptes a tus necesidades.
- Si construyes algo, compártelo y podemos mantener un directorio de proyectos.

## Créditos
Backend:

[@FollowerOfFlow](https://x.com/FollowerOfFlow) hizo algo de magia para lograr que TOS RTD funcione directamente con Python.

Échale un vistazo aquí: [pyrtdc](https://github.com/tifoji/pyrtdc/)

Cálculos de Exposición Gamma: [perfiliev](https://perfiliev.com/blog/how-to-calculate-gamma-exposure-and-zero-gamma-level/)

## Soporte
[@2187Nick](https://x.com/2187Nick)

[Discord](https://discord.com/invite/vxKepZ6XNC)

<br />
<div align="center">
  <p>¿Encuentras valor en mi trabajo?</p>
  <a href="https://www.buymeacoffee.com/2187Nick" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</div>
