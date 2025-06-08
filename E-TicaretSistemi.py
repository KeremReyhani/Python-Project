import uuid
import datetime
import random
import threading
import hashlib
import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass

# Sipariş durumlarını temsil eden enum sınıfı
class OrderStatus(Enum):
    PENDING = "Beklemede"
    PREPARING = "Hazırlanıyor"
    SHIPPED = "Yolda"
    DISPATCHED = "Dağıtımda"
    DELIVERED = "Teslim Edildi"
    CANCELLED = "İptal Edildi"

    def __str__(self) -> str:
        return self.value

# Sipariş dekoratörleri için soyut temel sınıf
class OrderDecorator(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

# Temel sipariş dekoratörü, siparişin temel maliyetini ve açıklamasını döndürür
class BaseOrder(OrderDecorator):
    def __init__(self, order: 'Order'):
        self._order = order

    def get_cost(self) -> float:
        return self._order.total_cost()

    def get_description(self) -> str:
        return str(self._order)

# Kırılacak eşya koruması için dekoratör sınıfı
class FragileShipping(OrderDecorator):
    def __init__(self, decorated: OrderDecorator):
        self._decorated = decorated

    def get_cost(self) -> float:
        return self._decorated.get_cost() + 10.0

    def get_description(self) -> str:
        return f"{self._decorated.get_description()} + Kırılacak Eşya Koruması"

# Sigortalı kargolama için dekoratör sınıfı
class InsuredShipping(OrderDecorator):
    def __init__(self, decorated: OrderDecorator):
        self._decorated = decorated

    def get_cost(self) -> float:
        return self._decorated.get_cost() + (self._decorated.get_cost() * 0.05)

    def get_description(self) -> str:
        return f"{self._decorated.get_description()} + Sigorta"

# Bildirim gözlemcileri için soyut temel sınıf
class NotificationObserver(ABC):
    @abstractmethod
    def update(self, message: str, customer: 'Customer') -> None:
        pass

class EmailNotification(NotificationObserver):
    def update(self, message: str, customer: 'Customer') -> None:
        print(f"✉️ Email to {customer.email}: {message}")

class SMSNotification(NotificationObserver):
    def update(self, message: str, customer: 'Customer') -> None:
        print(f"📱SMS to {customer.phone}: {message}")

# Bildirim servisi, gözlemcileri yönetir ve bildirim gönderir
class NotificationService:
    def __init__(self):
        self.observers: List[NotificationObserver] = []

    def add_observer(self, observer: NotificationObserver) -> None:
        self.observers.append(observer)

    def notify(self, customer: 'Customer', message: str, template: str = "default") -> None:
        formatted_message = self._format_message(message, template)
        for observer in self.observers:
            observer.update(formatted_message, customer)

    def _format_message(self, message: str, template: str) -> str:
        return f"[GUNCELLEME] {message}" if template == "GUNCELLEME" else message

# Strategy Pattern: Shipping Method
# Kargolama yöntemleri için soyut temel sınıf
class ShippingMethod(ABC):
    @abstractmethod
    def calculate_cost(self, order: 'Order', region: str) -> float:
        pass

    @abstractmethod
    def estimate_delivery_days(self, region: str) -> int:
        pass

    @abstractmethod
    def is_available(self, region: str, weight: float) -> bool:
        pass

class FastShipping(ShippingMethod):
    def calculate_cost(self, order: 'Order', region: str) -> float:
        base_cost = 15.0 if region == "local" else 20.0
        return base_cost + (order.total_weight() * 0.5)

    def estimate_delivery_days(self, region: str) -> int:
        return 3 if region == "local" else 4

    def is_available(self, region: str, weight: float) -> bool:
        return weight <= 20.0

class CheapShipping(ShippingMethod):
    def calculate_cost(self, order: 'Order', region: str) -> float:
        base_cost = 5.0 if region == "local" else 8.0
        return base_cost + (order.total_weight() * 0.2)

    def estimate_delivery_days(self, region: str) -> int:
        return 7 if region == "local" else 10

    def is_available(self, region: str, weight: float) -> bool:
        return True

class DroneShipping(ShippingMethod):
    def calculate_cost(self, order: 'Order', region: str) -> float:
        return 20.0 if order.total_weight() <= 5 else 30.0

    def estimate_delivery_days(self, region: str) -> int:
        return 2 if region == "local" else 3

    def is_available(self, region: str, weight: float) -> bool:
        return weight <= 5.0 and region == "local"

# Singleton deseni kullanılarak envanter yönetimini sağlayan sınıf
class InventoryManager:
    _instance = None
    _lock = threading.Lock()
    _file_lock = threading.Lock()

    def __new__(cls):
        # Singleton desenini uygular, sadece tek bir InventoryManager örneği oluşturur
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(InventoryManager, cls).__new__(cls)
                cls._instance.inventory = {}
                cls._instance.stock = {}
                cls._instance.low_stock_alert = {}
                cls._instance.transaction_log = []
                cls._instance._load_from_json()
            return cls._instance

    def _save_to_json(self, users: List[Dict] = None, orders: List[Dict] = None):
        # Envanter, kullanıcı ve sipariş verilerini JSON dosyasına kaydeder
        data = {
            "users": users or [],
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "category": p.category,
                    "weight": p.weight,
                    "description": p.description,
                    "sku": p.sku,
                    "stock": self.stock[p.id]
                } for p in self.inventory.values()
            ],
            "orders": orders or [],
            "transactions": self.transaction_log
        }
        with self._file_lock:
            with open("siparisdatabase.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_from_json(self):
        # JSON dosyasından ürün ve işlem loglarını yükler
        if not os.path.exists("siparisdatabase.json"):
            return
        with self._file_lock:
            try:
                with open("siparisdatabase.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for product_data in data.get("products", []):
                        product = Product(
                            id=product_data["id"],
                            name=product_data["name"],
                            price=product_data["price"],
                            category=product_data["category"],
                            weight=product_data["weight"],
                            description=product_data["description"],
                            sku=product_data["sku"]
                        )
                        self.inventory[product.id] = product
                        self.stock[product.id] = product_data["stock"]
                        self.low_stock_alert[product.id] = product_data["stock"] < 5
                    self.transaction_log = [
                        {
                            "timestamp": t["timestamp"],
                            "action": t["action"],
                            "details": t["details"]
                        } for t in data.get("transactions", [])
                    ]
            except json.JSONDecodeError:
                print("Uyarı: Bozuk JSON dosyası, boş envanterle başlanıyor")

    def add_product(self, product: 'Product', initial_stock: int) -> None:
        self.inventory[product.id] = product
        self.stock[product.id] = initial_stock
        self.low_stock_alert[product.id] = initial_stock < 5
        self._log_transaction(f"Ürün eklendi: {product.name} (ID: {product.id}, Stok: {initial_stock})")
        self._save_to_json()

    def update_stock(self, product_id: str, quantity: int, restock: bool = False) -> bool:
        if product_id not in self.inventory:
            return False
        if restock:
            self.stock[product_id] += quantity
            self._log_transaction(f"{self.inventory[product_id].name} için {quantity} adet stok eklendi")
        else:
            if self.stock[product_id] >= quantity:
                self.stock[product_id] -= quantity
                self._log_transaction(f"{self.inventory[product_id].name} stoğu {quantity} adet azaltıldı")
            else:
                return False
        self.low_stock_alert[product_id] = self.stock[product_id] < 5
        if self.low_stock_alert[product_id]:
            print(f"Düşük stok uyarısı: {self.inventory[product_id].name} için {self.stock[product_id]} adet kaldı")
        self._save_to_json()
        return True

    def get_product(self, product_id: str) -> Optional['Product']:
        # Belirtilen ürün ID'sine sahip ürünü envanterden döndürür
        return self.inventory.get(product_id)

    def get_stock(self, product_id: str) -> int:
        # Belirtilen ürünün stok miktarını döndürür
        return self.stock.get(product_id, 0)

    def restock_product(self, product_id: str, quantity: int, is_admin: bool = False) -> None:
        if not is_admin:
            raise ValueError("Sadece yönetici stok yenileyebilir")
        self.update_stock(product_id, quantity, restock=True)

    def _log_transaction(self, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_log.append({
            "timestamp": timestamp,
            "action": "INVENTORY",
            "details": message
        })

    def view_transaction_log(self) -> str:
        return "\n".join([f"{t['timestamp']}: {t['action']} - {t['details']}" for t in self.transaction_log])

# Product Class
# Ürün bilgilerini tutan veri sınıfı
@dataclass(frozen=True)
class Product:
    id: str
    name: str
    price: float
    category: str
    weight: float
    description: str
    sku: str

    def __str__(self) -> str:
        return (f"{self.name} (ID: {self.id}, SKU: {self.sku}, Kategori: {self.category}, "
                f"💵 Fiyat: ${self.price:.2f}, Ağırlık: {self.weight}kg)")

# Müşteri bilgilerini ve sipariş geçmişini yöneten sınıf
class Customer:
    def __init__(self, id: str, username: str, name: str, email: str, phone: str, address: str, password_hash: str):
        self.id = id
        self.username = username
        self.name = name
        self.email = email.lower()
        self.phone = phone
        self.address = address
        self._password_hash = password_hash
        self.order_history: List['Order'] = []

    def _hash_password(self, password: str) -> str:
        #Şifreyi SHA-256 ile hash'ler
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, password: str) -> bool:
        # Girilen şifrenin hash'ini mevcut hash ile karşılaştırır
        return self._password_hash == self._hash_password(password)

    def add_order(self, order: 'Order') -> None:
        self.order_history.append(order)

    def view_order_history(self, status: Optional[OrderStatus] = None,
                           start_date: Optional[datetime.datetime] = None) -> str:
        filtered_orders = self.order_history
        if status:
            filtered_orders = [o for o in filtered_orders if o.status == status]
        if start_date:
            filtered_orders = [o for o in filtered_orders if o.created_at >= start_date]
        return "\n".join([f"{str(o)}\n{o.get_estimated_delivery(self._get_system())}" for o in
                          filtered_orders]) or "Sipariş bulunamadı"

    def _get_system(self) -> 'ECommerceSystem':
        # Yeni bir ECommerceSystem örneği döndürür
        return ECommerceSystem()


# Sipariş bilgilerini ve durumunu yöneten sınıf
class Order:
    def __init__(self, id: str, customer: Customer, products: Dict[Product, int], note: str = ""):
        self.id = id
        self.customer = customer
        self.products = products
        self.status = OrderStatus.PENDING
        self.shipping_method: Optional[ShippingMethod] = None
        self.notification_service = NotificationService()
        self.notification_service.add_observer(EmailNotification())
        self.notification_service.add_observer(SMSNotification())
        self.order_note = note
        self.tracking_number = self._generate_tracking_number()
        self.created_at = datetime.datetime.now()
        self.region = customer.address.split(",")[-1].strip().lower()
        self.initial_delivery_days = random.randint(1, 7)  # Default, overridden for express orders
        self.remaining_delivery_days = self.initial_delivery_days

    def total_weight(self) -> float:
        # Siparişteki ürünlerin toplam ağırlığını hesaplar
        return sum(product.weight * quantity for product, quantity in self.products.items())

    def _calculate_base_cost(self) -> float:
        # Siparişteki ürünlerin temel maliyetini hesaplar
        return sum(product.price * quantity for product, quantity in self.products.items())

    def total_cost(self) -> float:
        # Ürün ve kargolama maliyetini birleştirerek toplam sipariş maliyetini döndürür
        product_cost = self._calculate_base_cost()
        shipping_cost = self.shipping_method.calculate_cost(self, self.region) if self.shipping_method else 0
        return max(product_cost + shipping_cost, 0)

    def _generate_tracking_number(self) -> str:
        # Sipariş için benzersiz bir takip numarası oluşturur
        return f"TRK-{uuid.uuid4().hex[:8].upper()}"

    def update_status(self, new_status: OrderStatus, system: 'ECommerceSystem') -> None:
        if self.status in [OrderStatus.CANCELLED, OrderStatus.DELIVERED]:
            raise ValueError("İptal edilmiş veya teslim edilmiş siparişin durumu güncellenemez")
        if new_status not in OrderStatus:
            raise ValueError("Geçersiz durum")
        self.status = new_status
        template = "GUNCELLEME" if new_status in [OrderStatus.SHIPPED, OrderStatus.DISPATCHED,
                                              OrderStatus.DELIVERED] else "default"
        message = f" • Sipariş {self.id} durumu: {str(self.status)}. 🚚 Takip No: {self.tracking_number}"
        self.notification_service.notify(self.customer, message, template)
        system._save_to_json()

    def set_shipping_method(self, shipping_method: ShippingMethod) -> None:
        if not shipping_method.is_available(self.region, self.total_weight()):
            raise ValueError(f"Kargolama yöntemi {type(shipping_method).__name__} uygun değil")
        self.shipping_method = shipping_method
        # Update delivery days based on shipping method
        self.initial_delivery_days = shipping_method.estimate_delivery_days(self.region)
        self.remaining_delivery_days = self.initial_delivery_days
        message = (f" • Sipariş {self.id} için kargolama yöntemi: {type(shipping_method).__name__}. ")  
        #f"Tahmini teslimat: {self.remaining_delivery_days} gün")
        self.notification_service.notify(self.customer, message)

    def cancel(self, system: 'ECommerceSystem') -> None:
        if self.status in [OrderStatus.SHIPPED, OrderStatus.DISPATCHED, OrderStatus.DELIVERED]:
            raise ValueError("Yolda, dağıtımda veya teslim edilmiş sipariş iptal edilemez")
        inventory = InventoryManager()
        for product, quantity in self.products.items():
            inventory.restock_product(product.id, quantity, is_admin=True)
        self.update_status(OrderStatus.CANCELLED, system)

    def get_estimated_delivery(self, system: 'ECommerceSystem') -> str:
        if not self.shipping_method:
            return "Kargolama yöntemi belirlenmedi"
        if self.status == OrderStatus.DELIVERED:
            return "Sipariş teslim edildi"
        if self.status == OrderStatus.CANCELLED:
            return "Sipariş iptal edildi"

        self.remaining_delivery_days = max(0, self.remaining_delivery_days - 1)
        system._save_to_json()

        if self.remaining_delivery_days == 0:
            self.update_status(OrderStatus.DELIVERED, system)
            return "Sipariş teslim edildi"
        elif self.remaining_delivery_days <= int(self.initial_delivery_days * 0.25):
            self.update_status(OrderStatus.DISPATCHED, system)
        elif self.remaining_delivery_days <= int(self.initial_delivery_days * 0.50):
            self.update_status(OrderStatus.SHIPPED, system)
        elif self.remaining_delivery_days <= int(self.initial_delivery_days * 0.75):
            self.update_status(OrderStatus.PREPARING, system)

        estimated_date = datetime.datetime.now() + datetime.timedelta(days=self.remaining_delivery_days)
        return f"• Tahmini teslimat: {self.remaining_delivery_days} gün ({estimated_date.strftime('%Y-%m-%d')})"

    def __str__(self) -> str:
        products_str = "\n".join([f"  {p.name} x{qty}" for p, qty in self.products.items()])
        return (f" • Sipariş {self.id} (Durum: {str(self.status)}, Toplam:💵 ${self.total_cost():.2f}, "
                f"\n• Ürünler:\n{products_str}\n📝 Not: {self.order_note}\n🚚 Takip No: {self.tracking_number}")

# Factory Method: Order Factory
class OrderFactory(ABC):
    @abstractmethod
    def create_order(self, customer: Customer, products: Dict[Product, int], note: str, system: 'ECommerceSystem',
                     **kwargs) -> Order:
        pass

class StandardOrderFactory(OrderFactory):
    def create_order(self, customer: Customer, products: Dict[Product, int], note: str, system: 'ECommerceSystem',
                     **kwargs) -> Order:
        inventory = InventoryManager()
        for product, quantity in products.items():
            if not inventory.update_stock(product_id=product.id, quantity=quantity):
                raise ValueError(f"{product.name} için yeterli stok yok")
        return Order(str(uuid.uuid4()), customer, products, note)

class ExpressOrderFactory(OrderFactory):
    def create_order(self, customer: 'Customer', products: Dict['Product', int], note: str,
                     system: 'ECommerceSystem', **kwargs) -> 'Order':
        # Create standard order
        order = StandardOrderFactory().create_order(customer, products, note, system, **kwargs)

        # Select shipping method based on weight and region
        weight = order.total_weight()
        region = order.region

        # DroneShipping: weight <= 5.0 and region == "local"
        if weight <= 5.0 and region == "local" and "drone" in system.shipping_methods:
            order.set_shipping_method(system.shipping_methods["drone"])
        # FastShipping: weight <= 20.0
        elif weight <= 20.0 and "fast" in system.shipping_methods:
            order.set_shipping_method(system.shipping_methods["fast"])
       
        elif weight > 20.0 and "fast" in system.shipping_methods:
            order.set_shipping_method(system.shipping_methods["cheap"])
        else:
            raise ValueError(f"Sipariş ağırlığı ({weight} kg) için uygun ekspres kargolama yöntemi bulunamadı.")

        return order

# E-commerce System
# E-ticaret sistemini yöneten ana sınıf
class ECommerceSystem:
    def __init__(self):
        self.inventory = InventoryManager()
        self.customers: Dict[str, Customer] = {}
        self.email_index: Dict[str, Customer] = {}
        self.username_index: Dict[str, Customer] = {}
        self.shipping_methods = {
            "fast": FastShipping(),
            "cheap": CheapShipping(),
            "drone": DroneShipping()
        }
        self.order_factories = {
            "standart": StandardOrderFactory(),
            "ekspres": ExpressOrderFactory()
        }
        self.current_user: Optional[Customer] = None
        self._file_lock = threading.Lock()
        self._load_users_and_orders_from_json()
        self._initialize_admin()

    def _save_to_json(self):
        users = [
            {
                "id": c.id,
                "username": c.username,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address,
                "password_hash": c._password_hash
            } for c in self.customers.values()
        ]
        orders = [
            {
                "id": o.id,
                "customer_id": o.customer.id,
                "products": [
                    {"product_id": p.id, "quantity": q} for p, q in o.products.items()
                ],
                "note": o.order_note,
                "status": o.status.name,
                "shipping_method": next((k for k, v in self.shipping_methods.items() if v is o.shipping_method), None),
                "tracking_number": o.tracking_number,
                "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "region": o.region,
                "initial_delivery_days": o.initial_delivery_days,
                "remaining_delivery_days": o.remaining_delivery_days
            } for c in self.customers.values() for o in c.order_history
        ]
        self.inventory._save_to_json(users, orders)

    def _load_users_and_orders_from_json(self) -> None:
        if not os.path.exists("siparisdatabase.json"):
            return
        with self._file_lock:
            try:
                with open("siparisdatabase.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for user_data in data.get("users", []):
                        if user_data["id"] not in self.customers:
                            customer = Customer(
                                id=user_data["id"],
                                username=user_data["username"],
                                name=user_data["name"],
                                email=user_data["email"],
                                phone=user_data["phone"],
                                address=user_data["address"],
                                password_hash=user_data["password_hash"]
                            )
                            self.customers[customer.id] = customer
                            self.email_index[customer.email] = customer
                            self.username_index[customer.username] = customer
                    status_migration = {
                        "Pending": "PENDING",
                        "Preparing": "PREPARING",
                        "Shipped": "SHIPPED",
                        "Delivered": "DELIVERED",
                        "Cancelled": "CANCELLED",
                        "Dispatched": "DISPATCHED"
                    }
                    for order_data in data.get("orders", []):
                        customer = self.customers.get(order_data["customer_id"])
                        if not customer:
                            print(f"Uyarı: Geçersiz müşteri ID'si ile sipariş {order_data['id']} atlanıyor")
                            continue
                        products = {}
                        for prod in order_data["products"]:
                            product = self.inventory.get_product(prod["product_id"])
                            if product:
                                products[product] = prod["quantity"]
                            else:
                                print(f"Uyarı: Sipariş {order_data['id']} içinde ürün {prod['product_id']} atlanıyor")
                                break
                        else:
                            order = Order(
                                id=order_data["id"],
                                customer=customer,
                                products=products,
                                note=order_data["note"]
                            )
                            json_status = order_data["status"]
                            enum_status = status_migration.get(json_status, json_status)
                            try:
                                order.status = OrderStatus[enum_status]
                            except KeyError:
                                print(
                                    f"Uyarı: Sipariş {order_data['id']} için geçersiz durum '{json_status}', PENDING olarak ayarlanıyor")
                                order.status = OrderStatus.PENDING
                            order.tracking_number = order_data["tracking_number"]
                            try:
                                order.created_at = datetime.datetime.strptime(order_data["created_at"],
                                                                              "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                print(
                                    f"Uyarı: Sipariş {order_data['id']} için geçersiz tarih, şimdiki zaman kullanılıyor")
                                order.created_at = datetime.datetime.now()
                            order.region = order_data.get("region", "local")
                            order.initial_delivery_days = order_data.get("initial_delivery_days", random.randint(1, 7))
                            order.remaining_delivery_days = order_data.get("remaining_delivery_days",
                                                                           order.initial_delivery_days)
                            if order_data["shipping_method"]:
                                order.shipping_method = self.shipping_methods.get(order_data["shipping_method"])
                                # Ensure delivery days match shipping method
                                if order.shipping_method:
                                    order.initial_delivery_days = order.shipping_method.estimate_delivery_days(order.region)
                                    if order.remaining_delivery_days > order.initial_delivery_days:
                                        order.remaining_delivery_days = order.initial_delivery_days
                            customer.add_order(order)
            except json.JSONDecodeError:
                print("Uyarı: Bozuk JSON dosyası, boş kullanıcı ve siparişlerle başlanıyor")

    def _initialize_admin(self) -> None:
        # Sistemde bir yönetici kullanıcısı oluşturur
        if "admin@example.com" not in self.email_index:
            admin = Customer(
                id="550e8400-e29b-41d4-a716-446655440000",
                username="admin",
                name="Admin User",
                email="admin@example.com",
                phone="+1234567890",
                address="123 Admin St, local",
                password_hash=hashlib.sha256("admin123".encode()).hexdigest()
            )
            self.customers[admin.id] = admin
            self.email_index[admin.email] = admin
            self.username_index[admin.username] = admin
            self._log_action("Yönetici kullanıcısı oluşturuldu")
            self._save_to_json()

    def _log_action(self, message: str) -> None:
        self.inventory._log_transaction(f"Sistem: {message}")

    def register_customer(self, username: str, name: str, email: str, phone: str, address: str,
                          password: str) -> Customer:
        email = email.lower()
        if email in self.email_index:
            raise ValueError("Email zaten kayıtlı")
        if username in self.username_index:
            raise ValueError("Kullanıcı adı zaten alınmış")
        customer = Customer(str(uuid.uuid4()), username, name, email, phone, address,
                            hashlib.sha256(password.encode()).hexdigest())
        self.customers[customer.id] = customer
        self.email_index[email] = customer
        self.username_index[username] = customer
        self._log_action(f"Kullanıcı kaydedildi: {username}")
        self._save_to_json()
        return customer

    def login(self, email: str, password: str) -> Customer:
        # Kullanıcı girişini doğrular ve mevcut sipariş durumlarını günceller
        email = email.lower()
        customer = self.email_index.get(email)
        if customer and customer.authenticate(password):
            self.current_user = customer
            self._log_action(f"Kullanıcı giriş yaptı: {customer.username}")
            for order in customer.order_history:
                if order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED] or not order.shipping_method:
                    continue
                if order.remaining_delivery_days <= 0:
                    order.update_status(OrderStatus.DELIVERED, self)
                elif order.remaining_delivery_days <= int(order.initial_delivery_days * 0.25):
                    order.update_status(OrderStatus.DISPATCHED, self)
                elif order.remaining_delivery_days <= int(order.initial_delivery_days * 0.50):
                    order.update_status(OrderStatus.SHIPPED, self)
                elif order.remaining_delivery_days <= int(order.initial_delivery_days * 0.75):
                    order.update_status(OrderStatus.PREPARING, self)
            if customer.order_history:
                print("\nSiparişleriniz:")
                print(customer.view_order_history())
            elif customer.email != "admin@example.com":
                print("Önceki sipariş bulunamadı")
            return customer
        raise ValueError("Geçersiz email veya şifre")

    def logout(self) -> None:
        if self.current_user:
            self._log_action(f"Kullanıcı çıkış yaptı: {self.current_user.username}")
            self.current_user = None

    def add_product(self, name: str, price: float, stock: int, category: str, weight: float,
                    description: str) -> Product:
        if not self.current_user or self.current_user.username != "admin":
            raise ValueError("Sadece yönetici ürün ekleyebilir")
        product = Product(str(uuid.uuid4()), name, price, category, weight, description,
                          f"SKU-{random.randint(1000, 9999)}")
        self.inventory.add_product(product, stock)
        self._log_action(f"Ürün eklendi: {name}")
        return product

    def list_products(self, category: Optional[str] = None, min_price: Optional[float] = None,
                      max_price: Optional[float] = None, in_stock: bool = False) -> List[Product]:
        # Ürünleri filtreleyerek listeler
        products = list(self.inventory.inventory.values())
        if category:
            products = [p for p in products if p.category.lower() == category.lower()]
        if min_price is not None:
            products = [p for p in products if p.price >= min_price]
        if max_price is not None:
            products = [p for p in products if p.price <= max_price]
        if in_stock:
            products = [p for p in products if self.inventory.get_stock(p.id) > 0]
        return products

    def select_shipping_method(self, order: Order, priority: str = "cost") -> ShippingMethod:
        # Sipariş için uygun kargolama yöntemini seçer
        available_methods = [
            method for method in self.shipping_methods.values()
            if method.is_available(order.region, order.total_weight())
        ]
        if not available_methods:
            raise ValueError("Uygun kargolama yöntemi yok")
        if priority == "speed":
            return min(available_methods, key=lambda m: m.estimate_delivery_days(order.region))
        return min(available_methods, key=lambda m: m.calculate_cost(order, order.region))

    def create_order(self, product_quantities: Dict[str, int], note: str = "",
                     order_type: str = "standart", premium_services: List[str] = None) -> Order:
        # Yeni bir sipariş oluşturur ve gerekli bildirimleri gönderir
        if not self.current_user:
            raise ValueError("Sipariş oluşturmak için giriş yapmalısınız")
        if self.current_user.username == "admin":
            raise ValueError("Yönetici sipariş oluşturamaz")

        products = {}
        for product_id, quantity in product_quantities.items():
            product = self.inventory.get_product(product_id)
            if not product:
                raise ValueError(f"Ürün {product_id} bulunamadı")
            products[product] = quantity

        factory = self.order_factories.get(order_type, self.order_factories["standart"])
        order = factory.create_order(self.current_user, products, note, self)
        self.current_user.add_order(order)

        decorated_order: OrderDecorator = BaseOrder(order)
        premium_services = premium_services or []
        if "fragile" in premium_services:
            decorated_order = FragileShipping(decorated_order)
        if "insured" in premium_services:
            decorated_order = InsuredShipping(decorated_order)

        if order_type != "ekspres":
            order.set_shipping_method(self.select_shipping_method(order))

        # durumu PREPARING olarak algılar ve tek durum bildirimi gönderir
        order.update_status(OrderStatus.PREPARING, self)

        self._log_action(f"Sipariş oluşturuldu: {order.id} (Kullanıcı: {self.current_user.username})")
        self._save_to_json()
        print(f"Sipariş oluşturuldu, maliyet:💵 ${decorated_order.get_cost():.2f}")
        print(decorated_order.get_description())
        print(order.get_estimated_delivery(self))
        return order

    def cancel_order(self, order_id: str) -> None:
        if not self.current_user:
            raise ValueError("Sipariş iptal etmek için giriş yapmalısınız")
        order = next((o for o in self.current_user.order_history if o.id == order_id), None)
        if not order:
            raise ValueError("Sipariş bulunamadı veya kullanıcıya ait değil")
        order.cancel(self)
        self._log_action(f"Sipariş iptal edildi: {order_id}")

    def get_order_estimated_delivery(self, order_id: str) -> str:
        if not self.current_user:
            raise ValueError("Teslimat süresini kontrol etmek için giriş yapmalısınız")
        order = next((o for o in self.current_user.order_history if o.id == order_id), None)
        if not order:
            raise ValueError("Sipariş bulunamadı veya kullanıcıya ait değil")
        return order.get_estimated_delivery(self)

# CLI Interface
# Komut satırı arayüzünü çalıştıran fonksiyon
def run_cli():
    system = ECommerceSystem()

    # ASCII Art for Welcome Screen
    WELCOME_BANNER = """
    ╔══════════════════════════════════════╗
    ║   E-TİCARET SİSTEMİNE HOŞ GELDİNİZ   ║
    ╚══════════════════════════════════════╝
    """

    # ASCII Art for Logged-in User Menu
    USER_MENU_HEADER = """
    ╔══════════════════════════════════════╗
    ║           KULLANICI MENÜSÜ           ║
    ╚══════════════════════════════════════╝
    """

    # ASCII Art for Admin Menu
    ADMIN_MENU_HEADER = """
    ╔══════════════════════════════════════╗
    ║           YÖNETİCİ PANELİ            ║
    ╚══════════════════════════════════════╝
    """

    # Separator for cleaner output
    SEPARATOR = "════════════════════════════════════════"

    # Sistemde envanter yoksa varsayılan ürünleri ekler
    if "admin@example.com" in system.email_index and not system.inventory.inventory:
        try:
            system.login("admin@example.com", "admin123")
            system.add_product("Laptop", 999.99, 10, "Elektronik", 2.0, "Yüksek performanslı laptop")
            system.add_product("Kitap", 19.48, 50, "Kitap", 0.5, "Çok satan roman")
            system.add_product("Kolye", 99.60, 20, "Takı", 0.3, "İnci kolye")
            system.logout()
        except ValueError as e:
            print(f"Kurulum hatası: {e}")

    while True:
        print(WELCOME_BANNER)
        
        #herhangi bir kullanıcı giriş yapmışsa gelen arayüz 
        if system.current_user:
            print(f"👤Kullanıcı: {system.current_user.username} ({system.current_user.email})")
            print(SEPARATOR)
            print("1. Ürünleri Listele🛒")
            print("2. Sipariş Oluştur 📦")
            print("3. Sipariş Geçmişini Görüntüle📜")
            print("4. Sipariş İptal Et ❌")
            print("5. Tahmini Teslimat Süresini Kontrol Et ⏰")
            print("6. Ürün Stoğunu Yenile 🔄" if system.current_user.username == "admin" else "") 
            print("7. Ürün Ekle ➕" if system.current_user.username == "admin" else "6. Çıkış Yap 🚪")
            print("8. Çıkış Yap 🚪"if system.current_user.username == "admin" else "7. Uygulamadan Çık 🚀")
        
        #herhangi bir kullanıcı giriş yapmamışsa gelen arayüz
        else:
            print(SEPARATOR)
            print("1. Kayıt Ol 📝")
            print("2. Giriş Yap 🔑")
            print("3. Çıkış 🚀")

        choice = input("\nSeçenek: ")

        #herhangi bir kullanıcı giriş yapmamışsa seçime göre işlemler 
        if not system.current_user:
            if choice == "1":
                print(f"{SEPARATOR}")
                print("📝 Yeni Kullanıcı Kaydı")
                print(SEPARATOR)
                try:
                    username = input("Kullanıcı adı: ")
                    name = input("İsim: ")
                    email = input("Email: ")
                    phone = input("Telefon: ")
                    address = input("Adres (örn: 123 Sokak, local): ")
                    password = input("Şifre: ")
                    customer = system.register_customer(username, name, email, phone, address, password)
                    print(f"\n✅ {customer.username} olarak kayıt oldunuz")
                except ValueError as e:
                    print(f"❌ Hata: {e}")

            elif choice == "2":
                print(f"{SEPARATOR}")
                print("🔑 Kullanıcı Girişi")
                print(SEPARATOR)
                try:
                    email = input("Email: ")
                    password = input("Şifre: ")
                    customer = system.login(email, password)
                    print(f"\n✅ {customer.username} olarak giriş yapıldı")
                except ValueError as e:
                    print(f"❌ Hata: {e}")

            elif choice == "3":
                print(f"{SEPARATOR}")
                print("🚀 Güle güle!")
                print(SEPARATOR)
                break

            else:
                print("❌ Geçersiz seçenek")
        
        #herhangi bir kullanıcı giriş yapmışsa seçime göre işlemler 
        else:
            if choice == "1":
                print(f"{SEPARATOR}")
                print("🛒 Ürün Listesi")
                print(SEPARATOR)
                category = input("Kategori (tümü için Enter): ") or None
                min_price = input("Min fiyat (boş bırakabilirsiniz): ")
                max_price = input("Max fiyat (boş bırakabilirsiniz): ")
                in_stock = input("Sadece stokta olanlar? (e/h): ").lower() == "e"
                try:
                    min_price = float(min_price) if min_price else None
                    max_price = float(max_price) if max_price else None
                    products = system.list_products(category, min_price, max_price, in_stock)
                    if products:
                        for p in products:
                            print(f"📦 {p}, Stok: {system.inventory.get_stock(p.id)}")
                    else:
                        print("❌ Ürün bulunamadı")
                except ValueError:
                    print("❌ Geçersiz fiyat formatı")

            elif choice == "2":
                print(f"{SEPARATOR}")
                print("📦 Yeni Sipariş Oluştur")
                print(SEPARATOR)
                order_type = input("Sipariş türü (standart/ekspres): ").lower()
                if order_type not in ["standart", "ekspres"]:
                    print("❌ Geçersiz sipariş türü")
                    continue
                premium_services = []
                if input("Kırılacak eşya koruması? (e/h): ").lower() == "e":
                    premium_services.append("kırılgan")
                if input("Sigorta? (e/h): ").lower() == "e":
                    premium_services.append("sigortalı")
                products = system.list_products(in_stock=True)
                if not products:
                    print("❌ Stokta ürün yok")
                    continue
                print("Ürünler:")
                for i, p in enumerate(products, 1):
                    print(f"{i}. {p}, Stok: {system.inventory.get_stock(p.id)}")
                product_quantities = {}
                while True:
                    idx = input("Ürün no ('tamam' için t): ")
                    if idx.lower() == "t":
                        break
                    try:
                        idx = int(idx) - 1
                        if 0 <= idx < len(products):
                            qty = int(input(f"{products[idx].name} miktarı: "))
                            product_quantities[products[idx].id] = qty
                        else:
                            print("❌ Geçersiz ürün no")
                    except ValueError:
                        print("❌ Geçersiz giriş")
                note = input("Not (boş bırakabilirsiniz): ")
                try:
                    system.create_order(product_quantities, note, order_type, premium_services)
                except ValueError as e:
                    print(f"❌ Hata: {e}")

            elif choice == "3":
                print(f"{SEPARATOR}")
                print("📜 Sipariş Geçmişi")
                print(SEPARATOR)
                status = input(
                    "Durum (beklemede/hazırlanıyor/yolda/dağıtımda/teslim edildi/iptal edildi, veya Enter): ")
                status_map = {
                    "beklemede": OrderStatus.PENDING,
                    "hazırlanıyor": OrderStatus.PREPARING,
                    "yolda": OrderStatus.SHIPPED,
                    "dağıtımda": OrderStatus.DISPATCHED,
                    "teslim edildi": OrderStatus.DELIVERED,
                    "iptal edildi": OrderStatus.CANCELLED
                }
                status = status_map.get(status.lower()) if status else None
                start_date = input("Başlangıç tarihi (YYYY-MM-DD, veya Enter): ")
                try:
                    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
                    print(system.current_user.view_order_history(status, start_date))
                except ValueError:
                    print("❌ Geçersiz tarih formatı")

            elif choice == "4":
                print(SEPARATOR)
                print("Siparişleriniz:")
                print(f"{SEPARATOR}")
                for o in system.current_user.order_history:
                    print(f"📦 ID: {o.id}, Durum: {str(o.status)}")
                order_id = input("İptal edilecek sipariş ID: ")
                try:
                    system.cancel_order(order_id)
                    print(f"\n✅ Sipariş {order_id} iptal edildi")
                except ValueError as e:
                    print(f"Hata: {e}")

            elif choice == "5":
                print(f"{SEPARATOR}")
                print("⏰ Tahmini Teslimat Süresi")
                print(SEPARATOR)

                for o in system.current_user.order_history:
                    print(f"📦 ID: {o.id}, Durum: {str(o.status)}")
                order_id = input("Teslimat süresi için sipariş ID: ")
                try:
                    print(system.get_order_estimated_delivery(order_id))
                except ValueError as e:
                    print(f"❌ Hata: {e}")

            elif choice == "6" and system.current_user.username == "admin":
                """if system.current_user.username != "admin":
                    print("Hata: Sadece yönetici stok yenileyebilir")
                    continue"""
                print(f"{SEPARATOR}")
                print("🔄 Ürün Stoğunu Yenile")
                print(SEPARATOR)

                products = system.list_products()
                if not products:
                    print("❌ Ürün bulunamadı")
                    continue
                for i, p in enumerate(products, 1):
                    print(f"{i}. {p}, Stok: {system.inventory.get_stock(p.id)}")
                try:
                    idx = int(input("Stok yenilenecek ürün no: ")) - 1
                    if 0 <= idx < len(products):
                        qty = int(input("Miktar: "))
                        system.inventory.restock_product(products[idx].id, qty, is_admin=True)
                        print(f"\n✅ {products[idx].name} stoğu yenilendi")
                    else:
                        print("❌ Geçersiz ürün no")
                except ValueError:
                    print("❌ Geçersiz giriş")

            elif choice == "6" and system.current_user.username != "admin":
                system.logout()
                print(f"{SEPARATOR}")
                print("🚪 Çıkış yapıldı")
                print(SEPARATOR)

            elif choice == "7" and system.current_user.username == "admin":
                print(f"{SEPARATOR}")
                print("➕ Yeni Ürün Ekleme")
                print(SEPARATOR)
                try:
                    name = input("Ürün adı: ")
                    price = float(input("Fiyat: "))
                    stock = int(input("Stok: "))
                    category = input("Kategori: ")
                    weight = float(input("Ağırlık (kg): "))
                    description = input("Açıklama: ")
                    product = system.add_product(name, price, stock, category, weight, description)
                    print(f"✅ Ürün eklendi: {product}")
                except ValueError as e:
                    print(f"❌ Hata: {e}")

            elif choice == "7" and system.current_user.username != "admin":
                print(f"{SEPARATOR}")
                print("🚀 Güle güle!")
                print(SEPARATOR)
                break

            elif choice == "8" and system.current_user.username == "admin":
                system.logout()
                print(f"{SEPARATOR}")
                print("🚪 Çıkış yapıldı")
                print(SEPARATOR)

            else:
                print("\n❌ Geçersiz seçenek")

if __name__ == "__main__":
    run_cli()