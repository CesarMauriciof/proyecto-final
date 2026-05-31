from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from config import Config
from datetime import date

# Se crea la instancia de la aplicación Flask
app = Flask(__name__)
# Carga la configuración desde el objeto Config (definido en config.py)
app.config.from_object(Config)
# Se establece una clave secreta para la gestión de sesiones y mensajes flash.
# Es crucial para la seguridad de la aplicación.
app.secret_key = 'supersecretkey'  

# Función para obtener una conexión a la base de datos MySQL
def get_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],        # Host de la base de datos (ej. 'localhost')
        user=app.config['MYSQL_USER'],        # Usuario de la base de datos
        password=app.config['MYSQL_PASSWORD'],    # Contraseña del usuario
        database=app.config['MYSQL_DB']       # Nombre de la base de datos a la que conectarse
    )

# --- Rutas Generales ---

# Ruta principal de la aplicación
@app.route('/')
def inicio():
    # Renderiza la plantilla 'index.html' para la página de inicio de la aplicación.
    return render_template('index.html')

# --- CRUD para Categorías ---

# Ruta para listar todas las categorías
@app.route('/categorias')
def categorias():
    conn = get_connection() # Obtiene una conexión a la base de datos
    cur = conn.cursor()     # Crea un objeto cursor para ejecutar comandos SQL
    # Ejecuta una consulta SQL para seleccionar todas las categorías
    cur.execute("SELECT id_categoria, nombre, descripcion FROM categorias") 
    categorias = cur.fetchall() # Recupera todas las filas del resultado de la consulta
    cur.close()             # Cierra el cursor para liberar recursos
    conn.close()            # Cierra la conexión a la base de datos
    # Renderiza la plantilla 'categorias/categorias.html' pasando la lista de categorías obtenida
    return render_template('categorias/categorias.html', categorias=categorias)

# Ruta para crear una nueva categoría (maneja GET para mostrar formulario y POST para procesar datos)
@app.route('/categorias/crear', methods=['GET', 'POST'])
def crear_categoria():
    if request.method == 'POST':
        # Si la solicitud es POST, se obtienen los datos del formulario
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        # Validación de campos requeridos: el nombre de la categoría no puede estar vacío
        if not nombre:
            # Si falta el nombre, se muestra un mensaje de error usando flash
            flash('El nombre de la categoría es requerido.', 'danger') 
            # Se vuelve a renderizar el formulario con los datos ya ingresados para evitar que el usuario los pierda
            return render_template('categorias/crear_categoria.html',
                                   nombre=nombre, descripcion=descripcion)

        conn = get_connection()
        cur = conn.cursor()
        try:
            # Ejecuta la inserción en la base de datos con los datos del formulario
            cur.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)",
                        (nombre, descripcion))
            conn.commit() # Confirma los cambios en la base de datos
            flash('Categoría creada exitosamente!', 'success') # Muestra un mensaje de éxito
            return redirect(url_for('categorias')) # Redirige a la lista de categorías
        except mysql.connector.Error as err:
            # Si ocurre un error en la base de datos, se muestra un mensaje de error
            flash(f"Error al crear categoría: {err}", 'danger') 
            conn.rollback() # Deshace los cambios en la base de datos si hubo un error
            # Vuelve a renderizar el formulario con los datos ingresados
            return render_template('categorias/crear_categoria.html',
                                   nombre=nombre, descripcion=descripcion)
        finally:
            cur.close() # Asegura que el cursor se cierre
            conn.close() # Asegura que la conexión se cierre
    # Si la solicitud es GET, simplemente muestra el formulario vacío para crear una categoría
    return render_template('categorias/crear_categoria.html')

# Ruta para editar una categoría existente (maneja GET para mostrar formulario y POST para procesar datos)
@app.route('/categorias/editar/<int:id_categoria>', methods=['GET', 'POST'])
def editar_categoria(id_categoria):
    conn = get_connection()
    cur = conn.cursor()
    categoria = None # Variable para almacenar los datos de la categoría

    if request.method == 'GET':
        # Si la solicitud es GET, busca la categoría por su ID para pre-llenar el formulario de edición
        cur.execute("SELECT id_categoria, nombre, descripcion FROM categorias WHERE id_categoria = %s", (id_categoria,))
        categoria = cur.fetchone() # Obtiene una sola fila de resultado
        cur.close()
        conn.close()
        if not categoria:
            # Si la categoría no se encuentra, muestra un mensaje y redirige a la lista
            flash('Categoría no encontrada.', 'danger')
            return redirect(url_for('categorias'))
        # Renderiza el formulario de edición con los datos actuales de la categoría
        return render_template('categorias/editar_categoria.html', categoria=categoria)

    elif request.method == 'POST':
        # Si la solicitud es POST, se obtienen los datos actualizados del formulario
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        # Validación de campos requeridos
        if not nombre:
            flash('El nombre de la categoría es requerido.', 'danger')
            # Si hay un error, se vuelve a buscar la categoría para re-llenar el formulario con los datos originales
            conn_fetch = get_connection()
            cur_fetch = conn_fetch.cursor()
            cur_fetch.execute("SELECT id_categoria, nombre, descripcion FROM categorias WHERE id_categoria = %s",
                              (id_categoria,))
            categoria = cur_fetch.fetchone()
            cur_fetch.close()
            conn_fetch.close()
            return render_template('categorias/editar_categoria.html', categoria=categoria)

        conn_post = get_connection()
        cur_post = conn_post.cursor()
        try:
            # Ejecuta la actualización en la base de datos
            cur_post.execute("UPDATE categorias SET nombre = %s, descripcion = %s WHERE id_categoria = %s",
                             (nombre, descripcion, id_categoria))
            conn_post.commit() # Confirma los cambios
            flash('Categoría actualizada exitosamente!', 'success')
            return redirect(url_for('categorias')) # Redirige a la lista de categorías
        except mysql.connector.Error as err:
            flash(f"Error al actualizar categoría: {err}", 'danger')
            conn_post.rollback() # Deshace los cambios si hay un error
            # Si hay un error, se vuelve a buscar la categoría para re-llenar el formulario
            conn_fetch = get_connection()
            cur_fetch = conn_fetch.cursor()
            cur_fetch.execute("SELECT id_categoria, nombre, descripcion FROM categorias WHERE id_categoria = %s",
                              (id_categoria,))
            categoria = cur_fetch.fetchone()
            cur_fetch.close()
            conn_fetch.close()
            return render_template('categorias/editar_categoria.html', categoria=categoria)
        finally:
            cur_post.close()
            conn_post.close()

# Ruta para eliminar una categoría (solo acepta solicitudes POST para mayor seguridad)
@app.route('/categorias/eliminar/<int:id_categoria>', methods=['POST'])
def eliminar_categoria(id_categoria):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Ejecuta la eliminación de la categoría por su ID
        cur.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,))
        conn.commit() # Confirma la eliminación
        flash('Categoría eliminada exitosamente!', 'success')
    except mysql.connector.Error as err:
        flash(f"Error al eliminar categoría: {err}", 'danger')
        conn.rollback() # Deshace si hay un error
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('categorias')) # Redirige a la lista de categorías


# --- CRUD para Clientes ---

# Ruta para listar todos los clientes
@app.route('/clientes')
def clientes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_customer, nombre, apellido, telefono, email FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('clientes/clientes.html', clientes=clientes)

# Ruta para crear un nuevo cliente
@app.route('/clientes/crear', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        email = request.form.get('email')

        # Validación de campos requeridos
        if not nombre or not apellido:
            flash('Nombre y apellido del cliente son requeridos.', 'danger')
            return render_template('clientes/crear_cliente.html',
                                   nombre=nombre, apellido=apellido, telefono=telefono, email=email)

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO clientes (nombre, apellido, telefono, email) VALUES (%s, %s, %s, %s)",
                        (nombre, apellido, telefono, email))
            conn.commit()
            flash('Cliente creado exitosamente!', 'success')
            return redirect(url_for('clientes'))
        except mysql.connector.Error as err:
            flash(f"Error al crear cliente: {err}", 'danger')
            conn.rollback()
            return render_template('clientes/crear_cliente.html',
                                   nombre=nombre, apellido=apellido, telefono=telefono, email=email)
        finally:
            cur.close()
            conn.close()
    return render_template('clientes/crear_cliente.html')

# Ruta para editar un cliente existente
@app.route('/clientes/editar/<int:id_customer>', methods=['GET', 'POST'])
def editar_cliente(id_customer):
    conn = get_connection()
    cur = conn.cursor()
    cliente = None

    if request.method == 'GET':
        cur.execute("SELECT id_customer, nombre, apellido, telefono, email FROM clientes WHERE id_customer = %s",
                    (id_customer,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        if not cliente:
            flash('Cliente no encontrado.', 'danger')
            return redirect(url_for('clientes'))
        return render_template('clientes/editar_cliente.html', cliente=cliente)

    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        email = request.form.get('email')

        if not nombre or not apellido:
            flash('Nombre y apellido del cliente son requeridos.', 'danger')
            # Se vuelve a buscar el cliente para re-llenar el formulario
            conn_fetch = get_connection()
            cur_fetch = conn_fetch.cursor()
            cur_fetch.execute(
                "SELECT id_customer, nombre, apellido, telefono, email FROM clientes WHERE id_customer = %s",
                (id_customer,))
            cliente = cur_fetch.fetchone()
            cur_fetch.close()
            conn_fetch.close()
            return render_template('clientes/editar_cliente.html', cliente=cliente)

        conn_post = get_connection()
        cur_post = conn_post.cursor()
        try:
            cur_post.execute(
                "UPDATE clientes SET nombre = %s, apellido = %s, telefono = %s, email = %s WHERE id_customer = %s",
                (nombre, apellido, telefono, email, id_customer))
            conn_post.commit()
            flash('Cliente actualizado exitosamente!', 'success')
            return redirect(url_for('clientes'))
        except mysql.connector.Error as err:
            flash(f"Error al actualizar cliente: {err}", 'danger')
            conn_post.rollback()
            # Se vuelve a buscar el cliente para re-llenar el formulario
            conn_fetch = get_connection()
            cur_fetch = conn_fetch.cursor()
            cur_fetch.execute(
                "SELECT id_customer, nombre, apellido, telefono, email FROM clientes WHERE id_customer = %s",
                (id_customer,))
            cliente = cur_fetch.fetchone()
            cur_fetch.close()
            conn_fetch.close()
            return render_template('clientes/editar_cliente.html', cliente=cliente)
        finally:
            cur_post.close()
            conn_post.close()

# Ruta para eliminar un cliente
@app.route('/clientes/eliminar/<int:id_customer>', methods=['POST'])
def eliminar_cliente(id_customer):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM clientes WHERE id_customer = %s", (id_customer,))
        conn.commit()
        flash('Cliente eliminado exitosamente!', 'success')
    except mysql.connector.Error as err:
        flash(f"Error al eliminar cliente: {err}", 'danger')
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('clientes'))


# --- CRUD para Proveedores ---

# Ruta para listar todos los proveedores
@app.route('/proveedores')
def proveedores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_proveedor, nombre_empresa, contacto, telefono, email FROM proveedores")
    proveedores = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('proveedores/proveedores.html', proveedores=proveedores)

# Ruta para crear un nuevo proveedor
@app.route('/proveedores/crear', methods=['GET', 'POST'])
def crear_proveedor():
    if request.method == 'POST':
        nombre_empresa = request.form.get('nombre_empresa')
        contacto = request.form.get('contacto')
        telefono = request.form.get('telefono')
        email = request.form.get('email')

        if not nombre_empresa or not contacto:
            flash('Nombre de la empresa y contacto son requeridos.', 'danger')
            return render_template('proveedores/crear_proveedor.html',
                                   nombre_empresa=nombre_empresa, contacto=contacto, telefono=telefono, email=email)

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO proveedores (nombre_empresa, contacto, telefono, email) VALUES (%s, %s, %s, %s)",
                        (nombre_empresa, contacto, telefono, email))
            conn.commit()
            flash('Proveedor creado exitosamente!', 'success')
            return redirect(url_for('proveedores'))
        except mysql.connector.Error as err:
            flash(f"Error al crear proveedor: {err}", 'danger')
            conn.rollback()
            return render_template('proveedores/crear_proveedor.html',
                                   nombre_empresa=nombre_empresa, contacto=contacto, telefono=telefono, email=email)
        finally:
            cur.close()
            conn.close()
    return render_template('proveedores/crear_proveedor.html')

# Ruta para editar un proveedor existente
@app.route('/proveedores/editar/<int:id_proveedor>', methods=['GET', 'POST'])
def editar_proveedor(id_proveedor):
    conn = get_connection()
    cur = conn.cursor()
    proveedor = None

    if request.method == 'GET':
        cur.execute(
            "SELECT id_proveedor, nombre_empresa, contacto, telefono, email FROM proveedores WHERE id_proveedor = %s",
            (id_proveedor,))
        proveedor = cur.fetchone()
        cur.close()
        conn.close()
        if not proveedor:
            flash('Proveedor no encontrado.', 'danger')
            return redirect(url_for('proveedores'))
        return render_template('proveedores/editar_proveedor.html', proveedor=proveedor)

    elif request.method == 'POST':
        nombre_empresa = request.form.get('nombre_empresa')
        contacto = request.form.get('contacto')
        telefono = request.form.get('telefono')
        email = request.form.get('email')

        if not nombre_empresa or not contacto:
            flash('Nombre de la empresa y contacto son requeridos.', 'danger')
            # Re-fetch supplier data to re-populate the form for the user
            conn_fetch = get_connection()
            cur_fetch = conn_fetch.cursor()
            cur_fetch.execute(
                "SELECT id_proveedor, nombre_empresa, contacto, telefono, email FROM proveedores WHERE id_proveedor = %s",
                (id_proveedor,))
            proveedor = cur_fetch.fetchone()
            cur_fetch.close()
            conn_fetch.close()
            return render_template('proveedores/editar_proveedor.html', proveedor=proveedor)

        conn_post = get_connection()
        cur_post = conn_post.cursor()
        try:
            cur_post.execute(
                "UPDATE proveedores SET nombre_empresa = %s, contacto = %s, telefono = %s, email = %s WHERE id_proveedor = %s",
                (nombre_empresa, contacto, telefono, email, id_proveedor))
            conn_post.commit()
            flash('Proveedor actualizado exitosamente!', 'success')
            return redirect(url_for('proveedores'))
        except mysql.connector.Error as err:
            flash(f"Error al actualizar proveedor: {err}", 'danger')
            conn_post.rollback()
            # Re-fetch supplier data to re-populate the form for the user
            conn_fetch = get_connection()
            cur_fetch = conn_fetch.cursor()
            cur_fetch.execute(
                "SELECT id_proveedor, nombre_empresa, contacto, telefono, email FROM proveedores WHERE id_proveedor = %s",
                (id_proveedor,))
            proveedor = cur_fetch.fetchone()
            cur_fetch.close()
            conn_fetch.close()
            return render_template('proveedores/editar_proveedor.html', proveedor=proveedor)
        finally:
            cur_post.close()
            conn_post.close()

# Ruta para eliminar un proveedor
@app.route('/proveedores/eliminar/<int:id_proveedor>', methods=['POST'])
def eliminar_proveedor(id_proveedor):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
        conn.commit()
        flash('Proveedor eliminado exitosamente!', 'success')
    except mysql.connector.Error as err:
        flash(f"Error al eliminar proveedor: {err}", 'danger')
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('proveedores'))


# --- CRUD para Productos ---

# Ruta para listar todos los productos
@app.route('/productos')
def productos():
    conn = get_connection()
    cur = conn.cursor()
    # Consulta para obtener productos con el nombre de su categoría y proveedor
    cur.execute("""
        SELECT 
            p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, 
            c.nombre AS categoria_nombre, pr.nombre_empresa AS proveedor_nombre
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
    """)
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('productos/productos.html', productos=productos)

# Ruta para crear un nuevo producto
@app.route('/productos/crear', methods=['GET', 'POST'])
def crear_producto():
    conn = get_connection()
    cur = conn.cursor()
    # Obtiene categorías y proveedores para los dropdowns del formulario
    cur.execute("SELECT id_categoria, nombre FROM categorias")
    categorias = cur.fetchall()
    cur.execute("SELECT id_proveedor, nombre_empresa FROM proveedores")
    proveedores = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == 'POST':
        # Obtiene los datos del formulario
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_str = request.form.get('precio')
        stock_str = request.form.get('stock')
        id_categoria_str = request.form.get('id_categoria')
        id_proveedor_str = request.form.get('id_proveedor')

        errors = [] # Lista para acumular errores de validación

        # Validación de campos requeridos
        if not nombre:
            errors.append('El nombre del producto es requerido.')
        if not precio_str:
            errors.append('El precio del producto es requerido.')
        if not stock_str:
            errors.append('El stock del producto es requerido.')
        if not id_categoria_str:
            errors.append('La categoría del producto es requerida.')
        if not id_proveedor_str:
            errors.append('El proveedor del producto es requerido.')

        precio = 0.0
        stock = 0
        id_categoria = None
        id_proveedor = None

        try:
            # Intenta convertir a los tipos de datos correctos
            if precio_str:
                precio = float(precio_str)
            if stock_str:
                stock = int(stock_str)
            if id_categoria_str:
                id_categoria = int(id_categoria_str)
            if id_proveedor_str:
                id_proveedor = int(id_proveedor_str)

            # Validación de valores numéricos
            if precio <= 0:
                errors.append('El precio debe ser un número positivo.')
            if stock < 0:
                errors.append('El stock no puede ser negativo.')
        except ValueError:
            errors.append('Precio, stock, categoría o proveedor deben ser números válidos.')

        if errors:
            # Si hay errores, muestra los mensajes flash y vuelve a renderizar el formulario
            for error in errors:
                flash(error, 'danger')
            return render_template('productos/crear_producto.html',
                                   categorias=categorias, proveedores=proveedores, # Se pasan de nuevo para los dropdowns
                                   nombre=nombre, descripcion=descripcion, precio=precio_str, stock=stock_str,
                                   id_categoria=id_categoria_str, id_proveedor=id_proveedor_str)

        conn_post = get_connection()
        cur_post = conn_post.cursor()
        try:
            cur_post.execute("""
                INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, id_proveedor) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, descripcion, precio, stock, id_categoria, id_proveedor))
            conn_post.commit()
            flash('Producto creado exitosamente!', 'success')
            return redirect(url_for('productos'))
        except mysql.connector.Error as err:
            flash(f"Error al crear producto: {err}", 'danger')
            conn_post.rollback()
            return render_template('productos/crear_producto.html',
                                   categorias=categorias, proveedores=proveedores,
                                   nombre=nombre, descripcion=descripcion, precio=precio_str, stock=stock_str,
                                   id_categoria=id_categoria_str, id_proveedor=id_proveedor_str)
        finally:
            cur_post.close()
            conn_post.close()

    # Si es una solicitud GET, muestra el formulario vacío con los dropdowns
    return render_template('productos/crear_producto.html', categorias=categorias, proveedores=proveedores)

# Ruta para editar un producto existente
@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    conn = get_connection()
    cur = conn.cursor()
    producto = None
    categorias = []
    proveedores = []

    if request.method == 'GET':
        # Busca el producto por su ID
        cur.execute("""
            SELECT 
                id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor
            FROM productos 
            WHERE id_producto = %s
        """, (id_producto,))
        producto = cur.fetchone()
        if not producto:
            flash('Producto no encontrado.', 'danger')
            cur.close()
            conn.close()
            return redirect(url_for('productos'))

        # Obtiene categorías y proveedores para los dropdowns del formulario
        cur.execute("SELECT id_categoria, nombre FROM categorias")
        categorias = cur.fetchall()
        cur.execute("SELECT id_proveedor, nombre_empresa FROM proveedores")
        proveedores = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('productos/editar_producto.html', producto=producto, categorias=categorias,
                               proveedores=proveedores)

    elif request.method == 'POST':
        # Obtiene los datos del formulario
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_str = request.form.get('precio')
        stock_str = request.form.get('stock')
        id_categoria_str = request.form.get('id_categoria')
        id_proveedor_str = request.form.get('id_proveedor')

        errors = [] # Lista para acumular errores de validación

        # Validación de campos requeridos
        if not nombre:
            errors.append('El nombre del producto es requerido.')
        if not precio_str:
            errors.append('El precio del producto es requerido.')
        if not stock_str:
            errors.append('El stock del producto es requerido.')
        if not id_categoria_str:
            errors.append('La categoría del producto es requerida.')
        if not id_proveedor_str:
            errors.append('El proveedor del producto es requerido.')

        precio = 0.0
        stock = 0
        id_categoria = None
        id_proveedor = None

        try:
            # Intenta convertir a los tipos de datos correctos
            if precio_str:
                precio = float(precio_str)
            if stock_str:
                stock = int(stock_str)
            if id_categoria_str:
                id_categoria = int(id_categoria_str)
            if id_proveedor_str:
                id_proveedor = int(id_proveedor_str)

            # Validación de valores numéricos
            if precio <= 0:
                errors.append('El precio debe ser un número positivo.')
            if stock < 0:
                errors.append('El stock no puede ser negativo.')
        except ValueError:
            errors.append('Precio, stock, categoría o proveedor deben ser números válidos.')

        # Se vuelven a obtener categorías y proveedores para los dropdowns en caso de error
        conn_fetch_dropdowns = get_connection()
        cur_fetch_dropdowns = conn_fetch_dropdowns.cursor()
        cur_fetch_dropdowns.execute("SELECT id_categoria, nombre FROM categorias")
        categorias = cur_fetch_dropdowns.fetchall()
        cur_fetch_dropdowns.execute("SELECT id_proveedor, nombre_empresa FROM proveedores")
        proveedores = cur_fetch_dropdowns.fetchall()
        cur_fetch_dropdowns.close()
        conn_fetch_dropdowns.close()

        if errors:
            for error in errors:
                flash(error, 'danger')
            # Si hay errores, se vuelve a buscar el producto para re-llenar el formulario
            conn_fetch_product = get_connection()
            cur_fetch_product = conn_fetch_product.cursor()
            cur_fetch_product.execute("""
                SELECT 
                    id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor
                FROM productos 
                WHERE id_producto = %s
            """, (id_producto,))
            producto = cur_fetch_product.fetchone()
            cur_fetch_product.close()
            conn_fetch_product.close()
            return render_template('productos/editar_producto.html',
                                   producto=producto, categorias=categorias, proveedores=proveedores)

        conn_post = get_connection()
        cur_post = conn_post.cursor()
        try:
            cur_post.execute("""
                UPDATE productos 
                SET nombre = %s, descripcion = %s, precio = %s, stock = %s, id_categoria = %s, id_proveedor = %s
                WHERE id_producto = %s
            """, (nombre, descripcion, precio, stock, id_categoria, id_proveedor, id_producto))
            conn_post.commit()
            flash('Producto actualizado exitosamente!', 'success')
            return redirect(url_for('productos'))
        except mysql.connector.Error as err:
            flash(f"Error al actualizar producto: {err}", 'danger')
            conn_post.rollback()
            # Si hay un error, se vuelve a buscar el producto para re-llenar el formulario
            conn_fetch_product = get_connection()
            cur_fetch_product = conn_fetch_product.cursor()
            cur_fetch_product.execute("""
                SELECT 
                    id_producto, nombre, descripcion, precio, stock, id_categoria, id_proveedor
                FROM productos 
                WHERE id_producto = %s
            """, (id_producto,))
            producto = cur_fetch_product.fetchone()
            cur_fetch_product.close()
            conn_fetch_product.close()
            return render_template('productos/editar_producto.html',
                                   producto=producto, categorias=categorias, proveedores=proveedores)
        finally:
            cur_post.close()
            conn_post.close()

# Ruta para eliminar un producto
@app.route('/productos/eliminar/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conn.commit()
        flash('Producto eliminado exitosamente!', 'success')
    except mysql.connector.Error as err:
        flash(f"Error al eliminar producto: {err}", 'danger')
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('productos'))


# --- Flujo de Ventas ---

# Ruta para listar todas las ventas
@app.route('/ventas')
def ventas():
    conn = get_connection()
    cur = conn.cursor()
    # Consulta para obtener ventas con el nombre y apellido del cliente
    cur.execute("""
        SELECT 
            v.id_venta, v.fecha_venta, c.nombre, c.apellido, v.total
        FROM ventas v
        JOIN clientes c ON v.id_customer = c.id_customer
        ORDER BY v.fecha_venta DESC
    """)
    ventas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('ventas/ventas.html', ventas=ventas)

# Ruta para ver el detalle de una venta específica
@app.route('/ventas/<int:id_venta>')
def detalle_venta(id_venta):
    conn = get_connection()
    # Usamos dictionary=True para que los resultados se devuelvan como diccionarios (más fácil de acceder por nombre de columna)
    cur = conn.cursor(dictionary=True) 

    # Obtiene los detalles de la venta y del cliente asociado
    cur.execute("""
        SELECT 
            v.id_venta, v.fecha_venta, v.total,
            c.nombre AS cliente_nombre, c.apellido AS cliente_apellido, c.email AS cliente_email, c.telefono AS cliente_telefono
        FROM ventas v
        JOIN clientes c ON v.id_customer = c.id_customer
        WHERE v.id_venta = %s
    """, (id_venta,))
    venta = cur.fetchone()

    if not venta:
        flash('Venta no encontrada.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('ventas'))

    # Obtiene los productos y sus cantidades vendidas en esta venta
    cur.execute("""
        SELECT
            dv.cantidad, dv.precio_unitario,
            p.nombre AS producto_nombre, p.descripcion AS producto_descripcion
        FROM detalle_ventas dv
        JOIN productos p ON dv.id_producto = p.id_producto
        WHERE dv.id_venta = %s
    """, (id_venta,))
    detalle_productos = cur.fetchall()

    cur.close()
    conn.close()
    # Renderiza la plantilla de detalle de venta con la información obtenida
    return render_template('ventas/detalle_venta.html', venta=venta, detalle_productos=detalle_productos)

# Ruta para crear una nueva venta (maneja GET para mostrar formulario y POST para procesar datos)
@app.route('/ventas/crear', methods=['GET', 'POST'])
def crear_venta():
    if request.method == 'GET':
        conn = get_connection()
        cur = conn.cursor()
        # Obtiene clientes y productos para los dropdowns del formulario
        cur.execute("SELECT id_customer, nombre, apellido FROM clientes")
        clientes = cur.fetchall()
        cur.execute("SELECT id_producto, nombre, precio, stock FROM productos")
        productos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('ventas/crear_venta.html', clientes=clientes, productos=productos)

    elif request.method == 'POST':
        id_customer = request.form.get('id_customer')
        productos_seleccionados = request.form.getlist('producto_id[]') # Lista de IDs de productos seleccionados
        cantidades = request.form.getlist('cantidad[]') # Lista de cantidades correspondientes a los productos

        # --- Validación inicial de los datos del formulario ---
        errors = []
        if not id_customer:
            errors.append('Debe seleccionar un cliente.')
        if not productos_seleccionados:
            errors.append('Debe seleccionar al menos un producto para la venta.')
        
        # Se vuelven a obtener clientes y productos para re-renderizar el formulario en caso de error
        # Esto es importante para que el usuario no pierda las opciones de los dropdowns si hay un fallo
        conn_fetch_data = get_connection()
        cur_fetch_data = conn_fetch_data.cursor()
        cur_fetch_data.execute("SELECT id_customer, nombre, apellido FROM clientes")
        clientes = cur_fetch_data.fetchall()
        cur_fetch_data.execute("SELECT id_producto, nombre, precio, stock FROM productos")
        productos = cur_fetch_data.fetchall()
        cur_fetch_data.close()
        conn_fetch_data.close()

        if errors:
            # Si hay errores de validación inicial, se muestran y se vuelve a cargar el formulario
            for error in errors:
                flash(error, 'danger')
            return render_template('ventas/crear_venta.html', clientes=clientes, productos=productos)

        total_venta = 0
        detalle_productos_para_db = [] # Lista para almacenar los detalles de los productos validados para la inserción en DB

        conn_transaction = get_connection()
        cur_transaction = conn_transaction.cursor()
        try:
            # Inicia una transacción SQL. Esto asegura que todas las operaciones (insertar venta, detalle y actualizar stock)
            # se completen con éxito o ninguna de ellas lo haga (atomicidad).
            conn_transaction.start_transaction() 

            # Valida cada producto y cantidad seleccionada por el usuario
            for i in range(len(productos_seleccionados)):
                producto_id_str = productos_seleccionados[i]
                cantidad_str = cantidades[i]

                if not producto_id_str or not cantidad_str:
                    raise ValueError("Producto o cantidad inválidos en la selección.")

                try:
                    producto_id = int(producto_id_str)
                    cantidad = int(cantidad_str)
                except ValueError:
                    raise ValueError("ID de producto o cantidad deben ser números enteros válidos.")

                if cantidad <= 0:
                    raise ValueError(f"La cantidad para el producto (ID: {producto_id}) debe ser mayor que cero.")

                # Consulta el producto en la base de datos para obtener su precio y stock actual
                cur_transaction.execute("SELECT nombre, precio, stock FROM productos WHERE id_producto = %s",
                                        (producto_id,))
                producto_info = cur_transaction.fetchone()

                if not producto_info:
                    raise ValueError(f"Producto con ID {producto_id} no encontrado.")
                
                nombre_producto, precio_unitario, stock_disponible = producto_info

                # Verifica si hay suficiente stock para la cantidad solicitada
                if cantidad > stock_disponible:
                    raise ValueError(
                        f"Stock insuficiente para el producto '{nombre_producto}'. Disponible: {stock_disponible}, Solicitado: {cantidad}")

                # Calcula el subtotal y lo añade al total de la venta
                subtotal = precio_unitario * cantidad
                total_venta += subtotal
                # Almacena los detalles del producto para la inserción en detalle_ventas
                detalle_productos_para_db.append({
                    'id_producto': producto_id,
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal
                })

            # Inserta la nueva venta en la tabla 'ventas'
            fecha_venta = date.today() # La fecha de la venta es la fecha actual
            cur_transaction.execute("INSERT INTO ventas (fecha_venta, id_customer, total) VALUES (%s, %s, %s)",
                                    (fecha_venta, id_customer, total_venta))
            # Obtiene el ID de la venta recién insertada, necesario para el detalle_ventas
            id_venta = cur_transaction.lastrowid  

            # Itera sobre los productos validados para insertarlos en 'detalle_ventas' y actualizar el stock
            for item in detalle_productos_para_db:
                cur_transaction.execute(
                    "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                    (id_venta, item['id_producto'], item['cantidad'], item['precio_unitario']))

                # Actualiza el stock del producto en la tabla 'productos'
                cur_transaction.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                                        (item['cantidad'], item['id_producto']))

            conn_transaction.commit() # Si todas las operaciones fueron exitosas, se confirman los cambios
            flash(f'Venta {id_venta} creada exitosamente por un total de {total_venta:.2f}!', 'success')
            return redirect(url_for('ventas')) # Redirige a la lista de ventas

        except ValueError as ve:
            # Captura errores de validación de lógica de negocio (ej. stock insuficiente)
            flash(f"Error en la venta: {ve}", 'danger')
            conn_transaction.rollback() # Deshace toda la transacción
            return render_template('ventas/crear_venta.html', clientes=clientes, productos=productos)
        except mysql.connector.Error as err:
            # Captura errores de la base de datos
            flash(f"Error en la base de datos durante la venta: {err}", 'danger')
            conn_transaction.rollback() # Deshace toda la transacción
            return render_template('ventas/crear_venta.html', clientes=clientes, productos=productos)
        finally:
            cur_transaction.close() # Asegura el cierre del cursor
            conn_transaction.close() # Asegura el cierre de la conexión

# Iniciar servidor de desarrollo
if __name__ == "__main__":
    # Ejecuta la aplicación Flask en modo depuración.
    # 'debug=True' permite recarga automática y muestra un depurador interactivo en el navegador.
    app.run(debug=True)