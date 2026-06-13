from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="employee")
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    department = db.Column(db.String(60))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    added_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_label(self):
        labels = {"admin": "مدير عام", "manager": "مدير", "supervisor": "مشرف", "employee": "موظف"}
        return labels.get(self.role, self.role)

    @property
    def role_icon(self):
        icons = {"admin": "🛡️", "manager": "👨‍💼", "supervisor": "👨‍💻", "employee": "👤"}
        return icons.get(self.role, "👤")


class QuoteRequest(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(120), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(60), nullable=False)
    details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending")
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    responded_at = db.Column(db.DateTime)

    @property
    def status_label(self):
        labels = {"pending": "قيد الانتظار", "approved": "تمت الموافقة", "rejected": "مرفوض", "done": "تم"}
        return labels.get(self.status, self.status)

    @property
    def status_color(self):
        colors = {"pending": "warning", "approved": "success", "rejected": "danger", "done": "info"}
        return colors.get(self.status, "secondary")


class Giveaway(db.Model):
    __tablename__ = "giveaways"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(256))
    prize_value = db.Column(db.String(60))
    winner_count = db.Column(db.Integer, default=1)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="active")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def status_label(self):
        return {"active": "نشط", "ended": "منتهي", "upcoming": "قادم"}.get(self.status, self.status)


class ApprovalRequest(db.Model):
    __tablename__ = "approvals"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(60), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    requester = db.relationship("User", backref="approvals")
    details = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    responded_at = db.Column(db.DateTime)


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    customer_type = db.Column(db.String(20), default="individual")
    source = db.Column(db.String(60))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_by = db.relationship("User", backref="customers")

    def to_dict(self):
        return {
            "id": self.id, "code": self.code, "name": self.name,
            "phone": self.phone or "", "email": self.email or "",
            "customer_type": self.customer_type or "individual",
            "source": self.source or "",
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by.name if self.created_by else "",
        }


class Invoice(db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.Integer, unique=True)
    customer_name = db.Column(db.String(120), default="—")
    customer_phone = db.Column(db.String(20), default="")
    items_json = db.Column(db.Text, default="[]")
    disc_pct = db.Column(db.Float, default=0)
    disc_amt = db.Column(db.Float, default=0)
    grand_total = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="active")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_by = db.relationship("User", backref="invoices")

    @property
    def items(self):
        try: return json.loads(self.items_json)
        except: return []

    @items.setter
    def items(self, val):
        self.items_json = json.dumps(val)

    def to_dict(self):
        return {
            "id": self.id, "serial": self.serial,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "items": self.items,
            "disc_pct": self.disc_pct, "disc_amt": self.disc_amt,
            "grand_total": self.grand_total,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Visitor(db.Model):
    __tablename__ = "visitors"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    browser = db.Column(db.String(60))
    browser_version = db.Column(db.String(20))
    os = db.Column(db.String(60))
    device = db.Column(db.String(30))
    screen_size = db.Column(db.String(20))
    language = db.Column(db.String(20))
    referrer = db.Column(db.String(256))
    page_visited = db.Column(db.String(256))
    country = db.Column(db.String(60))
    city = db.Column(db.String(60))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    page_url = db.Column(db.String(512))
    visited_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class EmployeeRequest(db.Model):
    __tablename__ = "employee_requests"
    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(60), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    requester = db.relationship("User", backref="requests", foreign_keys=[requester_id])
    details_json = db.Column(db.Text, default="{}")
    target_model = db.Column(db.String(60))
    target_id = db.Column(db.Integer)
    status = db.Column(db.String(20), default="pending")
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    responded_at = db.Column(db.DateTime)
    responded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    responded_by = db.relationship("User", foreign_keys=[responded_by_id])

    @property
    def details(self):
        try: return json.loads(self.details_json)
        except: return {}

    @details.setter
    def details(self, val):
        self.details_json = json.dumps(val)

    @property
    def action_label(self):
        labels = {
            "delete_customer": "حذف عميل",
            "edit_customer": "تعديل بيانات عميل",
            "delete_invoice": "حذف فاتورة",
            "edit_invoice": "تعديل فاتورة",
        }
        return labels.get(self.action_type, self.action_type)

    @property
    def status_label(self):
        return {"pending": "قيد الانتظار", "approved": "تمت الموافقة", "rejected": "مرفوض"}.get(self.status, self.status)
