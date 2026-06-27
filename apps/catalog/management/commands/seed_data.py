from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from apps.catalog.models import Product


PRODUCTS = [
    {'name': 'Auriculares Bluetooth Pro', 'description': 'Auriculares inalámbricos con cancelación de ruido activa y 30 horas de batería.', 'price': 45000, 'stock': 25, 'image': 'https://picsum.photos/seed/auriculares/400/400'},
    {'name': 'Teclado Mecánico RGB', 'description': 'Teclado mecánico gaming con switches Cherry MX y retroiluminación RGB personalizable.', 'price': 38000, 'stock': 30, 'image': 'https://picsum.photos/seed/teclado/400/400'},
    {'name': 'Monitor 27" 4K UHD', 'description': 'Monitor IPS 27 pulgadas con resolución 4K, HDR10 y puerto USB-C.', 'price': 185000, 'stock': 10, 'image': 'https://picsum.photos/seed/monitor/400/400'},
    {'name': 'Mouse Ergonómico Vertical', 'description': 'Mouse vertical inalámbrico con diseño ergonómico para reducir la fatiga.', 'price': 22000, 'stock': 40, 'image': 'https://picsum.photos/seed/mouse/400/400'},
    {'name': 'Cámara Web HD 1080p', 'description': 'Cámara web con resolución Full HD, micrófono integrado y corrección de luz.', 'price': 28000, 'stock': 20, 'image': 'https://picsum.photos/seed/camara/400/400'},
    {'name': 'Silla Gamer Ergonómica', 'description': 'Silla ajustable con soporte lumbar, reposabrazos 4D y base reforzada.', 'price': 210000, 'stock': 8, 'image': 'https://picsum.photos/seed/silla/400/400'},
    {'name': 'Cafetera Eléctrica Programable', 'description': 'Cafetera de 12 tazas con temporizador programable y jarra térmica.', 'price': 32000, 'stock': 15, 'image': 'https://picsum.photos/seed/cafetera/400/400'},
    {'name': 'Mochila Antirrobo Laptop', 'description': 'Mochila con compartimiento acolchado para laptop de 15.6", puerto USB y cierre antirrobo.', 'price': 35000, 'stock': 22, 'image': 'https://picsum.photos/seed/mochila/400/400'},
    {'name': 'Smartwatch Deportivo', 'description': 'Reloj inteligente con GPS, monitor cardíaco y resistencia al agua 5 ATM.', 'price': 65000, 'stock': 18, 'image': 'https://picsum.photos/seed/smartwatch/400/400'},
    {'name': 'Lámpara LED Escritorio', 'description': 'Lámpara LED con brazo articulado, temperatura de color ajustable y carga USB.', 'price': 18000, 'stock': 35, 'image': 'https://picsum.photos/seed/lampara/400/400'},
    {'name': 'Parlante Portátil Bluetooth', 'description': 'Parlante portátil resistente al agua con sonido estéreo y 12 horas de reproducción.', 'price': 25000, 'stock': 28, 'image': 'https://picsum.photos/seed/parlante/400/400'},
    {'name': 'Hub USB-C 7 en 1', 'description': 'Hub multipuerto USB-C con HDMI 4K, lectores de tarjetas y puertos USB 3.0.', 'price': 15000, 'stock': 45, 'image': 'https://picsum.photos/seed/hub/400/400'},
    {'name': 'Tablet 10" WiFi', 'description': 'Tablet Android con pantalla 10 pulgadas, 64GB almacenamiento y WiFi.', 'price': 120000, 'stock': 12, 'image': 'https://picsum.photos/seed/tablet/400/400'},
    {'name': 'Kit de Herramientas Precision', 'description': 'Set de 50 herramientas de precisión para reparación de electrónica.', 'price': 12000, 'stock': 50, 'image': 'https://picsum.photos/seed/herramientas/400/400'},
    {'name': 'Cargador Solar Portátil', 'description': 'Panel solar plegable de 21W con puertos USB para carga de dispositivos.', 'price': 29000, 'stock': 14, 'image': 'https://picsum.photos/seed/cargador/400/400'},
    {'name': 'Audífonos Deportivos Inalámbricos', 'description': 'Audífonos deportivos con gancho de oreja, resistentes al sudor y 8h de batería.', 'price': 20000, 'stock': 33, 'image': 'https://picsum.photos/seed/audifonos/400/400'},
    {'name': 'Base Notebook Ajustable', 'description': 'Soporte ajustable de aluminio para notebook, mejora la postura y ventilación.', 'price': 16000, 'stock': 27, 'image': 'https://picsum.photos/seed/base/400/400'},
    {'name': 'Webcam con Anillo de Luz', 'description': 'Cámara web 2K con anillo de luz LED integrado y micrófono estéreo.', 'price': 32000, 'stock': 16, 'image': 'https://picsum.photos/seed/webcam/400/400'},
    {'name': 'Adaptador Bluetooth USB', 'description': 'Adaptador Bluetooth 5.0 USB para PC, alcance de 20 metros.', 'price': 5000, 'stock': 60, 'image': 'https://picsum.photos/seed/bluetooth/400/400'},
    {'name': 'Organizador de Escritorio', 'description': 'Organizador multifuncional de bambú para escritorio con compartimentos ajustables.', 'price': 14000, 'stock': 38, 'image': 'https://picsum.photos/seed/organizador/400/400'},
]


class Command(BaseCommand):
    help = 'Siembra la base de datos con productos de ejemplo, admin y clientes de prueba.'

    def handle(self, *args, **options):
        self._seed_users()
        self._seed_products()
        self.stdout.write(self.style.SUCCESS('Seed completado exitosamente.'))

    def _seed_users(self):
        if User.objects.filter(username='admin').exists():
            self.stdout.write('  Usuarios ya existen, saltando...')
            return

        User.objects.create_superuser('admin', 'admin@ecommerce.cl', 'admin123')
        self.stdout.write(f'  Admin creado: admin / admin123')

        for i in range(1, 4):
            username = f'cliente{i}'
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, f'{username}@mail.cl', 'cliente123')
                self.stdout.write(f'  Cliente creado: {username} / cliente123')

        self.stdout.write(self.style.SUCCESS('  Usuarios creados correctamente.'))

    def _seed_products(self):
        if Product.objects.exists():
            self.stdout.write('  Productos ya existen, saltando...')
            return

        products_to_create = []
        for data in PRODUCTS:
            products_to_create.append(Product(**data))

        Product.objects.bulk_create(products_to_create)
        self.stdout.write(self.style.SUCCESS(f'  {len(PRODUCTS)} productos creados correctamente.'))
