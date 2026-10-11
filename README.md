# 🍦 Sistema de Gestión de Heladería

**Un sistema integral de gestión empresarial desarrollado con Python y tecnologías web modernas**

---

## 📌 Descripción del Proyecto

Este es un **sistema de gestión completo para una heladería** que automatiza y optimiza todos los procesos operacionales del negocio. La aplicación integra gestión de inventario, administración de pedidos, control de clientes y generación de reportes en una plataforma web intuitiva y profesional.

**Objetivo**: Facilitar la administración eficiente de una heladería mediante herramientas de software escalables y mantenibles.

---

## ✨ Características Principales

✅ **Gestión de Inventario**
- Control de sabores y productos disponibles
- Gestión de tamaños y variantes
- Seguimiento de precios y costos

✅ **Administración de Pedidos**
- Creación y seguimiento de órdenes
- Cálculo automático de totales
- Historial de pedidos

✅ **Gestión de Clientes**
- Base de datos de clientes
- Historial de compras
- Información de contacto y preferencias

✅ **Reportes y Analytics**
- Reportes de ventas
- Análisis de productos más vendidos
- Estadísticas de desempeño

✅ **Interfaz Web Responsiva**
- Diseño moderno y user-friendly
- Acceso desde cualquier dispositivo
- Templates HTML optimizados

---

## 🛠️ Stack Tecnológico

| Tecnología | Descripción | Versión |
|---|---|---|
| **Python** | Lenguaje backend | 3.8+ |
| **Flask/Web Framework** | Framework web | - |
| **HTML/CSS/JavaScript** | Frontend | - |
| **Base de Datos Relacional** | Almacenamiento de datos | SQL |
| **Templates Jinja2** | Motor de plantillas | - |

**Distribución del código**:
- 🔵 Python: 44%
- 🟠 HTML: 56%

---

## 📁 Estructura del Proyecto

```
proyecto-final/
│
├── 📂 python<heladeria>WebApp/
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── PythonWebApp/           # Módulo principal
│   │   ├── __init__.py
│   │   ├── routes.py           # Rutas y endpoints
│   │   └── models.py           # Modelos de datos
│   │
│   └── templates/              # Plantillas HTML
│       ├── base.html           # Template base
│       ├── productos.html      # Gestión de productos
│       ├── pedidos.html        # Gestión de pedidos
│       ├── clientes.html       # Gestión de clientes
│       └── reportes.html       # Reportes y analytics
│
├── 📂 database/
│   ├── schema.sql              # Esquema de base de datos
│   └── config.py               # Configuración de conexión
│
├── README.md                   # Documentación del proyecto
└── requirements.txt            # Dependencias del proyecto
```

---

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Git

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/CesarMauriciof/proyecto-final.git
   cd proyecto-final
   ```

2. **Crear un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**
   ```bash
   # Crear la base de datos
   python database/setup.py
   ```

5. **Ejecutar la aplicación**
   ```bash
   python python<heladeria>WebApp/main.py
   ```

6. **Acceder a la aplicación**
   - Abre tu navegador en: `http://localhost:5000`

---

## 💡 Funcionalidades Clave

### 1. Dashboard Principal
- Vista general del estado del negocio
- Gráficos de ventas
- Alertas de inventario bajo

### 2. Módulo de Productos
- CRUD completo de productos
- Gestión de sabores y tamaños
- Control de precios

### 3. Sistema de Pedidos
- Crear y modificar pedidos
- Seguimiento de estado
- Generar recibos

### 4. Base de Datos de Clientes
- Registrar nuevos clientes
- Historial de compras
- Preferencias personalizadas

### 5. Reportes Avanzados
- Ventas por periodo
- Productos más populares
- Análisis de rentabilidad

---

## 🎓 Aprendizajes y Habilidades Demostradas

Este proyecto demuestra competencia en:

- ✅ **Desarrollo Backend**: Lógica de negocio en Python
- ✅ **Desarrollo Frontend**: HTML, CSS, JavaScript responsivo
- ✅ **Bases de Datos**: Diseño y optimización de esquemas SQL
- ✅ **Arquitectura de Software**: Patrón MVC y separación de responsabilidades
- ✅ **Trabajo en Equipo**: Colaboración con desarrolladores
- ✅ **Versionamiento**: Git y control de cambios
- ✅ **UX/UI**: Interfaz intuitiva y responsive design

---

## 👥 Equipo de Desarrollo

| Desarrollador | Rol |
|---|---|
| **Cesar Mauricio Florez Ruiz** | Lead Developer / Backend |
| **Keiner Buitron** | Developer / Frontend |
| **Esteban Felipe Fernández Castro** | Developer / Database |

---

## 📋 Requisitos Funcionales Implementados

- [x] Gestión completa de productos
- [x] Sistema de pedidos operacional
- [x] Base de datos de clientes
- [x] Interfaz web responsiva
- [x] Reportes de ventas
- [x] Control de inventario
- [x] Autenticación de usuarios (opcional)

---

## 🔍 Casos de Uso

**Escenario 1: Registrar un nuevo pedido**
1. Gerente accede al sistema
2. Selecciona productos y cantidades
3. Sistema calcula total automáticamente
4. Pedido se registra en la base de datos

**Escenario 2: Generar reporte de ventas**
1. Propietario accede a reportes
2. Selecciona rango de fechas
3. Sistema genera gráficos y estadísticas
4. Descarga el reporte en PDF (opcional)

---

## 📈 Resultados y Impacto

- ✅ Reducción de errores en pedidos
- ✅ Mejor control de inventario
- ✅ Decisiones basadas en datos
- ✅ Interfaz intuitiva para usuarios no técnicos
- ✅ Escalabilidad para nuevas funciones

---

## 🔮 Mejoras Futuras

- 📱 Aplicación móvil complementaria
- 🔐 Sistema de autenticación avanzado
- 💳 Integración de pagos en línea
- 📊 Dashboard con métricas en tiempo real
- 📧 Notificaciones por email
- ☁️ Migración a cloud (AWS/Google Cloud)

---

## 📝 Licencia

Este proyecto es de código abierto bajo la licencia MIT.

---

## 📧 Contacto

Para más información o consultas sobre este proyecto:

- **GitHub**: [CesarMauriciof](https://github.com/CesarMauriciof)
- **Proyecto**: [proyecto-final](https://github.com/CesarMauriciof/proyecto-final)

---

## 🙏 Agradecimientos

Agradecemos a nuestro equipo de desarrollo por el compromiso y dedicación en la realización de este proyecto integral.

---

**Última actualización**: Octubre 2026 | **Estado**: ✅ Completado y Funcional
