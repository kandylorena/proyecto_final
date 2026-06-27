# E-Commerce MVP

Aplicación web de comercio electrónico desarrollada con Django y Bootstrap. Proyecto de portafolio que integra catálogo dinámico, carrito de compras, flujo de checkout completo y panel de administración.

## Tecnologías

- **Backend:** Django 5.0 + SQLite3
- **Frontend:** Bootstrap 5
- **Producción:** Gunicorn + WhiteNoise
- **Despliegue:** Render (con Disco Persistente)

## Estructura del Proyecto

```
Proyecto_final/
├── manage.py                  # CLI de Django
├── requirements.txt           # Dependencias
├── db.sqlite3                 # Base de datos local
├── seed_data.py               # Script de seed (alternativo)
├── ecommerce/                 # Configuración del proyecto
│   ├── settings.py            # Settings con soporte Render
│   ├── urls.py                # Rutas principales
│   └── wsgi.py                # WSGI para producción
├── apps/
│   ├── accounts/              # Registro, Login, Logout
│   ├── catalog/               # Productos + CRUD admin
│   │   ├── models.py          # Product (name, desc, price, stock, image)
│   │   ├── management/        # Comando seed_data
│   │   └── signals.py         # Auto-seed post_migrate
│   ├── cart/                  # Carrito de compras (sesión)
│   │   ├── cart.py            # Lógica del carrito
│   │   └── context_processors.py  # Contador carrito en navbar
│   └── orders/                # Órdenes y checkout
│       ├── models.py          # Order, OrderItem
│       └── views.py           # Checkout atómico
├── templates/                 # Templates globales
│   └── base.html              # Navbar dinámica + Bootstrap
├── static/                    # Archivos estáticos
└── media/                     # Archivos multimedia
```

## Instalación Local

### 1. Clonar el repositorio

```bash
git clone <tu-repo-url>
cd Proyecto_final
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones y seed

```bash
python manage.py migrate
python manage.py seed_data
```

> El seed se ejecuta automáticamente con `migrate` si la base de datos está vacía (vía señal `post_migrate`).

### 5. Iniciar servidor

```bash
python manage.py runserver
```

### 6. Acceder

- **Catálogo:** http://localhost:8000/
- **Admin Django:** http://localhost:8000/admin/

## Usuarios de Prueba (Seed)

| Usuario    | Contraseña  | Rol    |
|------------|-------------|--------|
| admin      | admin123    | Staff  |
| cliente1   | cliente123  | Cliente|
| cliente2   | cliente123  | Cliente|
| cliente3   | cliente123  | Cliente|

## Funcionalidades

### Roles y Permisos

| Funcionalidad               | Invitado | Cliente | Admin |
|-----------------------------|:--------:|:-------:|:-----:|
| Ver catálogo                | ✓        | ✓       | ✓     |
| Ver detalle de producto     | ✓        | ✓       | ✓     |
| Registrarse                 | ✓        | -       | -     |
| Iniciar sesión              | ✓        | -       | -     |
| Añadir al carrito           | ✗        | ✓       | ✗     |
| Modificar carrito           | ✗        | ✓       | ✗     |
| Confirmar compra            | ✗        | ✓       | ✗     |
| CRUD de productos           | ✗        | ✗       | ✓     |

### Catálogo (RF-2)

- Los productos se renderizan dinámicamente mediante ORM.
- Cada producto tiene: nombre, descripción, precio, stock e imagen (URL externa).
- El administrador dispone de vistas CRUD completas protegidas.

### Carrito de Compras (RF-3)

- Cliente autenticado puede añadir/remover/actualizar cantidades.
- Subtotal por producto y total general calculados en tiempo real.
- Validación de stock antes de añadir y al confirmar compra.

### Checkout (RF-3.4)

- Creación atómica de Orden + Items (con snapshots de precio).
- Descuento de stock en cada producto.
- Vaciado del carrito tras confirmar.

### Autenticación (RF-1)

- Login/Logout nativos de Django.
- Formulario de registro público disponible.
- Rutas protegidas: carrito requiere `@login_required`, CRUD requiere `is_staff`.

### Validaciones (RF-5)

- Precio mínimo: 0.01 (validador `MinValueValidator`).
- Stock mínimo: 0 (`PositiveIntegerField`).
- Mensajes flash con Django Messages Framework.

### Navbar Dinámica (RF-4.2)

- **Invitado:** Catálogo + Login + Registro
- **Cliente:** Catálogo + Carrito (con badge) + Mis Órdenes + Logout
- **Admin:** Catálogo + Admin Productos + Logout

## Despliegue en Render

### Requisitos

- Repositorio en GitHub
- Cuenta en [render.com](https://render.com)

### Pasos

1. **Crear Web Service:** New + Web Service, conectar repositorio.

2. **Configurar servicio:**

   | Parámetro       | Valor |
   |----------------|-------|
   | Name           | tu-ecommerce |
   | Language       | Python |
   | Branch         | main |
   | Build Command  | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
   | Start Command  | `gunicorn ecommerce.wsgi:application` |

3. **Crear Disco Persistente (Volume):**
   - Ir a pestaña **Disks** → **Add Disk**
   - Name: `sqlite-data`
   - Mount Path: `/data`
   - Size: 1 GB

4. **Variables de Entorno:**
   - `DEBUG` = `False`
   - `SECRET_KEY` = (cadena aleatoria compleja)
   - `ALLOWED_HOSTS` = `.onrender.com` (o la URL de tu servicio)

5. **Desplegar:** El servicio se construye automáticamente.

> **Nota:** El archivo SQLite3 se almacena en `/data/db.sqlite3` (volumen persistente). Sin un volume, los datos se pierden al redeploy.

### Seed en Producción

Si necesitas sembrar datos en producción tras el despliegue:

```bash
# Desde Render Shell:
python manage.py seed_data
```

O incluye `&& python manage.py seed_data` al final del **Build Command**.

## Licencia

Proyecto académico de portafolio personal.
