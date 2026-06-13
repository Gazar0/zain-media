import os
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from functools import wraps

from flask import (Flask, request, jsonify, render_template,
                   redirect, url_for, flash, send_from_directory, session)
from flask_cors import CORS
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from dotenv import load_dotenv
from models import db, User, QuoteRequest, Giveaway, ApprovalRequest, Customer, Invoice, EmployeeRequest, Visitor

load_dotenv()

app = Flask(__name__, template_folder="admin", static_folder="../static")
app.secret_key = os.getenv("SECRET_KEY", "zain-media-secret-key-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "zainmedia.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin_login"

@app.context_processor
def inject_globals():
    return dict(site_url="https://zainmedia.loca.lt")

# ─── SMTP Config ────────────────────────────
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "memogazar049@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", SMTP_EMAIL)

# ─── Admin credentials ──────────────────────
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "zain@2026")


# ─── Helpers ────────────────────────────────
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("ليس لديك صلاحية الوصول لهذه الصفحة", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def admin_or_manager_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ("admin", "manager"):
            flash("ليس لديك صلاحية الوصول لهذه الصفحة", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def any_staff_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("يجب تسجيل الدخول أولاً", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def send_email(to_email, subject, html_body):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def trigger_gdrive_backup():
    try:
        import subprocess
        subprocess.Popen(["python3", os.path.join(os.path.dirname(__file__), "gdrive_backup.py")])
    except Exception as e:
        print(f"Backup trigger error: {e}")


# ─── Tracking API ────────────────────────────
@app.route("/api/track", methods=["POST"])
def api_track():
    data = request.get_json() or {}
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()
    ua = request.headers.get("User-Agent", data.get("user_agent", ""))
    browser = data.get("browser", "")
    browser_ver = data.get("browser_version", "")
    os_name = data.get("os", "")
    device = data.get("device", "")
    screen = data.get("screen_size", "")
    lang = data.get("language", request.headers.get("Accept-Language", ""))
    ref = data.get("referrer", request.headers.get("Referer", ""))
    page = data.get("page_visited", request.headers.get("Referer", ""))
    country = data.get("country", "")
    city = data.get("city", "")
    lat = data.get("lat")
    lng = data.get("lng")
    v = Visitor(
        ip=ip, user_agent=ua,
        browser=browser, browser_version=browser_ver,
        os=os_name, device=device,
        screen_size=screen, language=lang,
        referrer=ref, page_visited=page,
        country=country, city=city,
        lat=lat, lng=lng,
    )
    db.session.add(v)
    db.session.commit()
    return jsonify({"ok": True}), 200


@app.route("/api/visitors")
@login_required
def api_visitors():
    visitors = Visitor.query.order_by(Visitor.visited_at.desc()).limit(200).all()
    return jsonify([{
        "id": v.id, "ip": v.ip, "browser": v.browser,
        "os": v.os, "device": v.device,
        "screen_size": v.screen_size,
        "country": v.country, "city": v.city,
        "lat": v.lat, "lng": v.lng,
        "page_visited": v.page_visited,
        "referrer": v.referrer,
        "language": v.language,
        "visited_at": v.visited_at.isoformat() if v.visited_at else None,
    } for v in visitors])


@app.route("/admin/visitors")
@login_required
@admin_required
def admin_visitors():
    visitors = Visitor.query.order_by(Visitor.visited_at.desc()).limit(100).all()
    total = Visitor.query.count()
    today = Visitor.query.filter(
        db.func.date(Visitor.visited_at) == db.func.date("now")
    ).count()
    return render_template("admin_visitors.html", visitors=visitors,
                          total=total, today=today)


# ─── Create default admin ───────────────────
def init_db():
    db.create_all()
    # ── Migration: add new columns if missing ──
    from sqlalchemy import text as sa_text
    with db.engine.connect() as conn:
        for col, typ in [("customer_type", "VARCHAR(20) DEFAULT 'individual'"), ("source", "VARCHAR(60)")]:
            try:
                conn.execute(sa_text(f"ALTER TABLE customers ADD COLUMN {col} {typ}"))
                conn.commit()
            except Exception:
                conn.rollback()
    # ── Visitors table (auto-created by db.create_all) ──
    # ── Default admin ──
    if not User.query.filter_by(username=ADMIN_USERNAME).first():
        admin = User(
            username=ADMIN_USERNAME,
            name="مدير النظام",
            email=SMTP_EMAIL,
            role="admin",
            phone="201002711494",
        )
        admin.set_password(ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()


# ─── API Routes (Public) ────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/giveaways")
def api_giveaways():
    giveaways = Giveaway.query.filter_by(status="active").order_by(Giveaway.created_at.desc()).all()
    return jsonify([{
        "id": g.id, "title": g.title, "description": g.description,
        "image_url": g.image_url, "prize_value": g.prize_value,
        "winner_count": g.winner_count,
        "end_date": g.end_date.isoformat() if g.end_date else None,
    } for g in giveaways])


@app.route("/api/quotes", methods=["POST"])
def api_create_quote():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    service = data.get("service", "").strip()
    details = data.get("details", "").strip()

    if not name or not email or not phone or not service or not details:
        return jsonify({"error": "جميع الحقول المطلوبة يجب ملؤها"}), 400

    quote = QuoteRequest(
        client_name=name, client_email=email,
        client_phone=phone, service=service, details=details,
        status="pending"
    )
    db.session.add(quote)
    db.session.commit()

    # Send email to admin
    admin_email_body = f"""
    <div dir="rtl" style="font-family:Arial;max-width:600px;margin:auto;padding:20px;">
        <h2 style="color:#7C3AED;">طلب عرض سعر جديد</h2>
        <table style="width:100%;border-collapse:collapse;">
            <tr><td style="padding:8px;font-weight:bold;color:#7C3AED;">العميل:</td><td>{name}</td></tr>
            <tr style="background:#f9f9f9;"><td style="padding:8px;font-weight:bold;color:#7C3AED;">البريد:</td><td>{email}</td></tr>
            <tr><td style="padding:8px;font-weight:bold;color:#7C3AED;">الهاتف:</td><td>{phone}</td></tr>
            <tr style="background:#f9f9f9;"><td style="padding:8px;font-weight:bold;color:#7C3AED;">الخدمة:</td><td>{service}</td></tr>
        </table>
        <div style="margin-top:16px;padding:16px;background:#f5f3ff;border-radius:8px;">
            <h4 style="color:#7C3AED;margin:0 0 8px;">التفاصيل:</h4>
            <p style="margin:0;line-height:1.7;">{details}</p>
        </div>
        <a href="http://localhost:5000/admin/quotes" style="display:inline-block;margin-top:16px;padding:10px 24px;background:#7C3AED;color:white;border-radius:8px;text-decoration:none;">عرض في لوحة التحكم</a>
    </div>"""

    sent_to_admin = send_email(RECEIVER_EMAIL, f"طلب عرض سعر جديد من {name}", admin_email_body)

    # Send confirmation to client
    client_email_body = f"""
    <div dir="rtl" style="font-family:Arial;max-width:600px;margin:auto;padding:20px;">
        <h2 style="color:#7C3AED;">شكراً لتواصلك مع Zain Media</h2>
        <p>عزيزي {name}،</p>
        <p>تم استلام طلب عرض السعر الخاص بك بنجاح. سنقوم بمراجعته والرد عليك في أقرب وقت ممكن.</p>
        <div style="padding:16px;background:#f5f3ff;border-radius:8px;margin:16px 0;">
            <p style="margin:0;color:#555;"><strong>الخدمة المطلوبة:</strong> {service}</p>
        </div>
        <p>مع تحيات،<br>فريق Zain Media</p>
    </div>"""

    send_email(email, "تم استلام طلبك — Zain Media", client_email_body)

    trigger_gdrive_backup()

    return jsonify({
        "success": True,
        "message": "تم إرسال طلب عرض السعر بنجاح. سيتم التواصل معك قريباً."
    }), 200


@app.route("/api/portfolios")
def api_portfolios():
    return jsonify(PORTFOLIO_DATA)


@app.route("/api/services")
def api_services():
    return jsonify(SERVICES_DATA)


@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    message = data.get("message", "").strip()
    if not name or not email or not message:
        return jsonify({"error": "الاسم، البريد، والرسالة مطلوبون"}), 400

    body = f"""
    <div dir="rtl" style="font-family:Arial;max-width:600px;margin:auto;padding:20px;">
        <h2 style="color:#7C3AED;">رسالة جديدة من موقع Zain Media</h2>
        <table style="width:100%;border-collapse:collapse;">
            <tr><td style="padding:8px;font-weight:bold;color:#7C3AED;">الاسم:</td><td>{name}</td></tr>
            <tr style="background:#f9f9f9;"><td style="padding:8px;font-weight:bold;color:#7C3AED;">البريد:</td><td>{email}</td></tr>
            <tr><td style="padding:8px;font-weight:bold;color:#7C3AED;">الهاتف:</td><td>{phone or '—'}</td></tr>
        </table>
        <div style="margin-top:16px;padding:16px;background:#f5f3ff;border-radius:8px;">
            <h4 style="color:#7C3AED;margin:0 0 8px;">الرسالة:</h4>
            <p style="margin:0;line-height:1.7;">{message}</p>
        </div>
    </div>"""
    sent = send_email(RECEIVER_EMAIL, f"رسالة جديدة من {name} — Zain Media", body)
    if sent:
        return jsonify({"success": True, "message": "تم إرسال الرسالة بنجاح"}), 200
    return jsonify({"error": "فشل إرسال البريد"}), 500


@app.route("/api/stats")
def api_stats():
    quotes_count = QuoteRequest.query.count()
    giveaways_count = Giveaway.query.filter_by(status="active").count()
    employees_count = User.query.count()
    return jsonify({
        "quotes": quotes_count,
        "giveaways": giveaways_count,
        "employees": employees_count,
    })


# ─── Customer API ────────────────────────────
@app.route("/api/customers", methods=["GET"])
@login_required
def api_customers_list():
    search_type = request.args.get("type", "")
    search_query = request.args.get("q", "").strip()
    query = Customer.query
    if search_type == "code" and search_query:
        query = query.filter(Customer.code.like(f"%{search_query}%"))
    elif search_query:
        query = query.filter(
            db.or_(Customer.name.like(f"%{search_query}%"),
                   Customer.phone.like(f"%{search_query}%"))
        )
    customers = query.order_by(Customer.created_at.desc()).all()
    return jsonify([c.to_dict() for c in customers])


@app.route("/api/customers", methods=["POST"])
@login_required
def api_customers_add():
    data = request.get_json()
    if not data or not data.get("name", "").strip():
        return jsonify({"error": "اسم العميل مطلوب"}), 400
    name = data["name"].strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    customer_type = data.get("customer_type", "individual")
    source = data.get("source", "")
    last_cust = Customer.query.order_by(Customer.id.desc()).first()
    next_code = str((last_cust.id + 1) if last_cust else 1).zfill(6)
    cust = Customer(code=next_code, name=name, phone=phone, email=email,
                    customer_type=customer_type, source=source,
                    created_by_id=current_user.id)
    db.session.add(cust)
    db.session.commit()
    return jsonify(cust.to_dict()), 201


@app.route("/api/customers/<int:cust_id>", methods=["PUT"])
@login_required
def api_customers_update(cust_id):
    if current_user.role not in ("admin", "manager"):
        return jsonify({"error": "ليس لديك صلاحية"}), 403
    cust = db.session.get(Customer, cust_id)
    if not cust:
        return jsonify({"error": "العميل غير موجود"}), 404
    data = request.get_json()
    if data.get("name", "").strip():
        cust.name = data["name"].strip()
    if "phone" in data:
        cust.phone = data.get("phone", "").strip()
    if "email" in data:
        cust.email = data.get("email", "").strip()
    db.session.commit()
    return jsonify(cust.to_dict())


@app.route("/api/customers/<int:cust_id>", methods=["DELETE"])
@login_required
def api_customers_delete(cust_id):
    if current_user.role not in ("admin", "manager"):
        # Create employee request instead
        cust = db.session.get(Customer, cust_id)
        if cust:
            req = EmployeeRequest(
                action_type="delete_customer",
                requester_id=current_user.id,
                target_model="customer",
                target_id=cust_id,
                details={"customer_name": cust.name, "customer_code": cust.code}
            )
            db.session.add(req)
            db.session.commit()
            return jsonify({"message": "تم إرسال طلب الحذف للمشرف", "request_id": req.id}), 202
        return jsonify({"error": "العميل غير موجود"}), 404
    cust = db.session.get(Customer, cust_id)
    if not cust:
        return jsonify({"error": "العميل غير موجود"}), 404
    db.session.delete(cust)
    db.session.commit()
    return jsonify({"message": "تم حذف العميل"}), 200


# ─── Invoice API ─────────────────────────────
@app.route("/api/invoices", methods=["GET"])
@login_required
def api_invoices_list():
    status = request.args.get("status", "active")
    query = Invoice.query
    if status != "all":
        query = query.filter_by(status=status)
    invoices = query.order_by(Invoice.created_at.desc()).all()
    return jsonify([inv.to_dict() for inv in invoices])


@app.route("/api/invoices", methods=["POST"])
@login_required
def api_invoices_create():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    items = data.get("items", [])
    if not items:
        return jsonify({"error": "الفارغة فارغة"}), 400
    last_inv = Invoice.query.order_by(Invoice.serial.desc()).first()
    next_serial = (last_inv.serial + 1) if last_inv else 1
    disc_pct = float(data.get("disc_pct", 0))
    disc_amt = float(data.get("disc_amt", 0))
    grand_total = float(data.get("grand_total", 0))
    inv = Invoice(
        serial=next_serial,
        customer_name=data.get("customer_name", "—"),
        customer_phone=data.get("customer_phone", ""),
        disc_pct=disc_pct,
        disc_amt=disc_amt,
        grand_total=grand_total,
        status="active",
        created_by_id=current_user.id,
    )
    inv.items = items
    db.session.add(inv)
    db.session.commit()
    return jsonify(inv.to_dict()), 201


@app.route("/api/invoices/<int:inv_id>", methods=["DELETE"])
@login_required
def api_invoices_delete(inv_id):
    if current_user.role not in ("admin", "manager"):
        inv = db.session.get(Invoice, inv_id)
        if inv:
            req = EmployeeRequest(
                action_type="delete_invoice",
                requester_id=current_user.id,
                target_model="invoice",
                target_id=inv_id,
                details={"invoice_serial": inv.serial, "customer_name": inv.customer_name}
            )
            db.session.add(req)
            db.session.commit()
            return jsonify({"message": "تم إرسال طلب الحذف للمشرف", "request_id": req.id}), 202
        return jsonify({"error": "الفاتورة غير موجودة"}), 404
    inv = db.session.get(Invoice, inv_id)
    if not inv:
        return jsonify({"error": "الفاتورة غير موجودة"}), 404
    inv.status = "deleted"
    inv.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({"message": "تم حذف الفاتورة"}), 200


@app.route("/api/invoices/<int:inv_id>", methods=["PUT"])
@login_required
def api_invoices_update(inv_id):
    if current_user.role not in ("admin", "manager"):
        return jsonify({"error": "ليس لديك صلاحية"}), 403
    inv = db.session.get(Invoice, inv_id)
    if not inv:
        return jsonify({"error": "الفاتورة غير موجودة"}), 404
    data = request.get_json()
    if "customer_name" in data:
        inv.customer_name = data["customer_name"]
    if "customer_phone" in data:
        inv.customer_phone = data["customer_phone"]
    if "items" in data:
        inv.items = data["items"]
    if "disc_pct" in data:
        inv.disc_pct = float(data["disc_pct"])
    if "disc_amt" in data:
        inv.disc_amt = float(data["disc_amt"])
    if "grand_total" in data:
        inv.grand_total = float(data["grand_total"])
    db.session.commit()
    return jsonify(inv.to_dict())


@app.route("/api/invoices/<int:inv_id>/restore", methods=["POST"])
@login_required
def api_invoices_restore(inv_id):
    if current_user.role not in ("admin", "manager"):
        return jsonify({"error": "ليس لديك صلاحية"}), 403
    inv = db.session.get(Invoice, inv_id)
    if not inv:
        return jsonify({"error": "الفاتورة غير موجودة"}), 404
    inv.status = "active"
    inv.deleted_at = None
    db.session.commit()
    return jsonify(inv.to_dict())


# ─── Employee Requests API ───────────────────
@app.route("/api/requests", methods=["GET"])
@login_required
def api_requests_list():
    if current_user.role not in ("admin", "manager"):
        return jsonify({"error": "ليس لديك صلاحية"}), 403
    status = request.args.get("status", "pending")
    query = EmployeeRequest.query
    if status != "all":
        query = query.filter_by(status=status)
    reqs = query.order_by(EmployeeRequest.created_at.desc()).all()
    result = []
    for r in reqs:
        d = {
            "id": r.id,
            "action_type": r.action_type,
            "action_label": r.action_label,
            "requester_name": r.requester.name if r.requester else "—",
            "target_model": r.target_model,
            "target_id": r.target_id,
            "details": r.details,
            "status": r.status,
            "status_label": r.status_label,
            "admin_notes": r.admin_notes or "",
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "responded_at": r.responded_at.isoformat() if r.responded_at else None,
        }
        result.append(d)
    return jsonify(result)


@app.route("/api/requests/<int:req_id>/respond", methods=["POST"])
@login_required
def api_requests_respond(req_id):
    if current_user.role not in ("admin", "manager"):
        return jsonify({"error": "ليس لديك صلاحية"}), 403
    req = db.session.get(EmployeeRequest, req_id)
    if not req:
        return jsonify({"error": "الطلب غير موجود"}), 404
    data = request.get_json()
    new_status = data.get("status", "approved")
    notes = data.get("notes", "").strip()
    if new_status not in ("approved", "rejected"):
        return jsonify({"error": "حالة غير صالحة"}), 400
    req.status = new_status
    req.admin_notes = notes
    req.responded_at = datetime.now(timezone.utc)
    req.responded_by_id = current_user.id

    # If approved, execute the action
    if new_status == "approved" and req.target_model == "customer" and req.action_type == "delete_customer":
        cust = db.session.get(Customer, req.target_id)
        if cust:
            db.session.delete(cust)
    elif new_status == "approved" and req.target_model == "invoice" and req.action_type == "delete_invoice":
        inv = db.session.get(Invoice, req.target_id)
        if inv:
            inv.status = "deleted"
            inv.deleted_at = datetime.now(timezone.utc)

    db.session.commit()
    return jsonify({"message": "تم تحديث الطلب"})


# ─── Admin Routes ───────────────────────────
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("admin_staff"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("admin_staff"))
        flash("اسم المستخدم أو كلمة المرور غير صحيحة", "danger")
    return render_template("login.html")


@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    quotes_count = QuoteRequest.query.count()
    pending_quotes = QuoteRequest.query.filter_by(status="pending").count()
    employees_count = User.query.count()
    giveaways_count = Giveaway.query.filter_by(status="active").count()
    customers_count = Customer.query.count()
    invoices_count = Invoice.query.filter_by(status="active").count()
    pending_requests = EmployeeRequest.query.filter_by(status="pending").count()
    visitors_count = Visitor.query.count()
    visitors_today = Visitor.query.filter(
        db.func.date(Visitor.visited_at) == db.func.date("now")
    ).count()
    recent_visitors = Visitor.query.order_by(Visitor.visited_at.desc()).limit(5).all()
    recent_quotes = QuoteRequest.query.order_by(QuoteRequest.created_at.desc()).limit(5).all()
    return render_template("dashboard.html",
        quotes_count=quotes_count, pending_quotes=pending_quotes,
        employees_count=employees_count, giveaways_count=giveaways_count,
        customers_count=customers_count, invoices_count=invoices_count,
        pending_requests=pending_requests,
        visitors_count=visitors_count, visitors_today=visitors_today,
        recent_visitors=recent_visitors, recent_quotes=recent_quotes)


@app.route("/admin/employees", methods=["GET", "POST"])
@login_required
def admin_employees():
    if request.method == "POST":
        if current_user.role != "admin":
            flash("ليس لديك صلاحية لإضافة موظفين", "danger")
            return redirect(url_for("admin_employees"))
        username = request.form.get("username", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        role = request.form.get("role", "employee")
        department = request.form.get("department", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password or not name:
            flash("اسم المستخدم، كلمة المرور، والاسم مطلوبون", "danger")
            return redirect(url_for("admin_employees"))
        if User.query.filter_by(username=username).first():
            flash("اسم المستخدم موجود بالفعل", "danger")
            return redirect(url_for("admin_employees"))
        emp = User(
            username=username, name=name, email=email, phone=phone,
            role=role, department=department, added_by=current_user.id,
        )
        emp.set_password(password)
        db.session.add(emp)
        db.session.commit()
        trigger_gdrive_backup()
        flash("تم إضافة الموظف بنجاح", "success")
        return redirect(url_for("admin_employees"))

    employees = User.query.order_by(User.created_at.desc()).all()
    employees_json = [{
        "id": e.id, "username": e.username, "name": e.name or "",
        "email": e.email or "", "phone": e.phone or "",
        "role": e.role, "role_label": e.role_label,
        "role_icon": e.role_icon, "department": e.department or "",
        "is_active": e.is_active,
        "created_at": e.created_at.isoformat() if e.created_at else None,
    } for e in employees]
    return render_template("employees.html", employees=employees, employees_json=employees_json)


@app.route("/admin/employees/<int:emp_id>/delete", methods=["POST"])
@login_required
@admin_required
def admin_delete_employee(emp_id):
    emp = db.session.get(User, emp_id)
    if emp and emp.id != current_user.id:
        db.session.delete(emp)
        db.session.commit()
        trigger_gdrive_backup()
        flash("تم حذف الموظف", "success")
    return redirect(url_for("admin_employees"))


@app.route("/admin/employees/<int:emp_id>/toggle", methods=["POST"])
@login_required
@admin_required
def admin_toggle_employee(emp_id):
    emp = db.session.get(User, emp_id)
    if emp and emp.id != current_user.id:
        emp.is_active = not emp.is_active
        db.session.commit()
        trigger_gdrive_backup()
    return redirect(url_for("admin_employees"))


@app.route("/admin/quotes")
@login_required
def admin_quotes():
    status_filter = request.args.get("status", "all")
    query = QuoteRequest.query
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
    quotes = query.order_by(QuoteRequest.created_at.desc()).all()
    return render_template("quotes.html", quotes=quotes, current_filter=status_filter)


@app.route("/admin/quotes/<int:qid>/respond", methods=["POST"])
@login_required
def admin_respond_quote(qid):
    quote = db.session.get(QuoteRequest, qid)
    if not quote:
        flash("طلب غير موجود", "danger")
        return redirect(url_for("admin_quotes"))
    status = request.form.get("status")
    notes = request.form.get("notes", "").strip()
    if status in ("approved", "rejected", "done"):
        quote.status = status
        quote.admin_notes = notes
        quote.responded_at = datetime.now(timezone.utc)
        db.session.commit()
        trigger_gdrive_backup()

        # Notify client
        status_msg = {"approved": "تمت الموافقة على طلبك", "rejected": "نأسف، لم يتم الموافقة على طلبك", "done": "تم إنجاز طلبك"}
        client_body = f"""
        <div dir="rtl" style="font-family:Arial;max-width:600px;margin:auto;padding:20px;">
            <h2 style="color:#7C3AED;">{status_msg[status]}</h2>
            <p>عزيزي {quote.client_name}،</p>
            <p>بخصوص طلب عرض السعر الخاص بخدمة <strong>{quote.service}</strong></p>
            {'<p>ملاحظات: ' + notes + '</p>' if notes else ''}
            <p>مع تحيات،<br>فريق Zain Media</p>
        </div>"""
        send_email(quote.client_email, f"{status_msg[status]} — Zain Media", client_body)

        flash("تم تحديث حالة الطلب وإرسال إشعار للعميل", "success")
    return redirect(url_for("admin_quotes"))


@app.route("/admin/giveaway", methods=["GET", "POST"])
@login_required
def admin_giveaway():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        image_url = request.form.get("image_url", "").strip()
        prize_value = request.form.get("prize_value", "").strip()
        winner_count = int(request.form.get("winner_count", 1))
        g = Giveaway(title=title, description=description, image_url=image_url,
                     prize_value=prize_value, winner_count=winner_count)
        db.session.add(g)
        db.session.commit()
        trigger_gdrive_backup()
        flash("تم إضافة المسابقة", "success")
        return redirect(url_for("admin_giveaway"))
    giveaways = Giveaway.query.order_by(Giveaway.created_at.desc()).all()
    return render_template("giveaway.html", giveaways=giveaways)


@app.route("/admin/giveaway/<int:gid>/delete", methods=["POST"])
@login_required
@admin_required
def admin_delete_giveaway(gid):
    g = db.session.get(Giveaway, gid)
    if g:
        db.session.delete(g)
        db.session.commit()
        trigger_gdrive_backup()
        flash("تم حذف المسابقة", "success")
    return redirect(url_for("admin_giveaway"))


@app.route("/admin/settings", methods=["GET", "POST"])
@login_required
@admin_required
def admin_settings():
    if request.method == "POST":
        current_password = request.form.get("current_password", "").strip()
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        if not current_password:
            flash("يجب إدخال كلمة المرور الحالية", "danger")
            return redirect(url_for("admin_settings"))
        if not current_user.check_password(current_password):
            flash("كلمة المرور الحالية غير صحيحة", "danger")
            return redirect(url_for("admin_settings"))
        if not new_password:
            flash("يجب إدخال كلمة المرور الجديدة", "danger")
            return redirect(url_for("admin_settings"))
        if len(new_password) < 6:
            flash("كلمة المرور الجديدة يجب أن تكون 6 أحرف على الأقل", "danger")
            return redirect(url_for("admin_settings"))
        if new_password != confirm_password:
            flash("كلمة المرور الجديدة وتأكيدها غير متطابقين", "danger")
            return redirect(url_for("admin_settings"))
        current_user.set_password(new_password)
        db.session.commit()
        flash("تم تغيير كلمة المرور بنجاح", "success")
        return redirect(url_for("admin_settings"))
    return render_template("settings.html")


@app.route("/admin/staff")
@login_required
def admin_staff():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    invoices = Invoice.query.filter_by(status="active").order_by(Invoice.created_at.desc()).limit(10).all()
    return render_template("staff_portal.html", customers=customers, invoices=invoices)


@app.route("/admin/customers", methods=["GET", "POST"])
@login_required
def admin_customers():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        customer_type = request.form.get("customer_type", "individual")
        source = request.form.get("source", "")
        if not name:
            flash("اسم العميل مطلوب", "danger")
            return redirect(url_for("admin_customers"))
        last_cust = Customer.query.order_by(Customer.id.desc()).first()
        next_code = str((last_cust.id + 1) if last_cust else 1).zfill(6)
        cust = Customer(code=next_code, name=name, phone=phone, email=email,
                        customer_type=customer_type, source=source,
                        created_by_id=current_user.id)
        db.session.add(cust)
        db.session.commit()
        flash(f"تم إضافة العميل {name} بكود {next_code}", "success")
        return redirect(url_for("admin_customers"))
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template("admin_customers.html", customers=customers)


@app.route("/admin/customers/<int:cid>/delete", methods=["POST"])
@login_required
def admin_customers_delete(cid):
    cust = db.session.get(Customer, cid)
    if not cust:
        flash("العميل غير موجود", "danger")
        return redirect(url_for("admin_customers"))
    if current_user.role not in ("admin", "manager"):
        req = EmployeeRequest(
            action_type="delete_customer",
            requester_id=current_user.id,
            target_model="customer",
            target_id=cid,
            details={"customer_name": cust.name, "customer_code": cust.code}
        )
        db.session.add(req)
        db.session.commit()
        flash("تم إرسال طلب الحذف للمشرف", "warning")
    else:
        db.session.delete(cust)
        db.session.commit()
        flash("تم حذف العميل", "success")
    return redirect(url_for("admin_customers"))


@app.route("/admin/invoices", methods=["GET"])
@login_required
def admin_invoices():
    status = request.args.get("status", "active")
    query = Invoice.query
    if status != "all":
        query = query.filter_by(status=status)
    invoices = query.order_by(Invoice.created_at.desc()).all()
    return render_template("admin_invoices.html", invoices=invoices, current_filter=status)


@app.route("/admin/invoices/<int:iid>/delete", methods=["POST"])
@login_required
def admin_invoice_delete(iid):
    inv = db.session.get(Invoice, iid)
    if not inv:
        flash("الفاتورة غير موجودة", "danger")
        return redirect(url_for("admin_invoices"))
    if current_user.role not in ("admin", "manager"):
        req = EmployeeRequest(
            action_type="delete_invoice",
            requester_id=current_user.id,
            target_model="invoice",
            target_id=iid,
            details={"invoice_serial": inv.serial, "customer_name": inv.customer_name}
        )
        db.session.add(req)
        db.session.commit()
        flash("تم إرسال طلب الحذف للمشرف", "warning")
    else:
        inv.status = "deleted"
        inv.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
        flash("تم حذف الفاتورة", "success")
    return redirect(url_for("admin_invoices"))


@app.route("/admin/invoices/<int:iid>/restore", methods=["POST"])
@login_required
def admin_invoice_restore(iid):
    inv = db.session.get(Invoice, iid)
    if not inv:
        flash("الفاتورة غير موجودة", "danger")
        return redirect(url_for("admin_invoices"))
    if current_user.role not in ("admin", "manager"):
        flash("ليس لديك صلاحية", "danger")
        return redirect(url_for("admin_invoices"))
    inv.status = "active"
    inv.deleted_at = None
    db.session.commit()
    flash("تم استعادة الفاتورة", "success")
    return redirect(url_for("admin_invoices"))


@app.route("/admin/employee-requests")
@login_required
def admin_employee_requests():
    if current_user.role not in ("admin", "manager"):
        flash("ليس لديك صلاحية", "danger")
        return redirect(url_for("admin_dashboard"))
    status = request.args.get("status", "pending")
    query = EmployeeRequest.query
    if status != "all":
        query = query.filter_by(status=status)
    reqs = query.order_by(EmployeeRequest.created_at.desc()).all()
    return render_template("admin_requests.html", requests=reqs, current_filter=status)


@app.route("/admin/employee-requests/<int:rid>/respond", methods=["POST"])
@login_required
def admin_respond_request(rid):
    if current_user.role not in ("admin", "manager"):
        flash("ليس لديك صلاحية", "danger")
        return redirect(url_for("admin_employee_requests"))
    req = db.session.get(EmployeeRequest, rid)
    if not req:
        flash("الطلب غير موجود", "danger")
        return redirect(url_for("admin_employee_requests"))
    new_status = request.form.get("status", "approved")
    notes = request.form.get("notes", "").strip()
    if new_status not in ("approved", "rejected"):
        flash("حالة غير صالحة", "danger")
        return redirect(url_for("admin_employee_requests"))
    req.status = new_status
    req.admin_notes = notes
    req.responded_at = datetime.now(timezone.utc)
    req.responded_by_id = current_user.id
    if new_status == "approved" and req.target_model == "customer" and req.action_type == "delete_customer":
        cust = db.session.get(Customer, req.target_id)
        if cust:
            db.session.delete(cust)
    elif new_status == "approved" and req.target_model == "invoice" and req.action_type == "delete_invoice":
        inv = db.session.get(Invoice, req.target_id)
        if inv:
            inv.status = "deleted"
            inv.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(f"تم {'الموافقة على' if new_status == 'approved' else 'رفض'} الطلب", "success")
    return redirect(url_for("admin_employee_requests"))


@app.route("/admin/employees/<int:emp_id>/role", methods=["POST"])
@login_required
@admin_required
def admin_employee_role(emp_id):
    emp = db.session.get(User, emp_id)
    if not emp or emp.id == current_user.id:
        flash("لا يمكن تعديل دور نفسك", "danger")
        return redirect(url_for("admin_employees"))
    new_role = request.form.get("role", "").strip()
    if new_role not in ("admin", "manager", "supervisor", "employee"):
        flash("دور غير صالح", "danger")
        return redirect(url_for("admin_employees"))
    emp.role = new_role
    db.session.commit()
    flash(f"تم تغيير دور {emp.name} إلى {emp.role_label}", "success")
    return redirect(url_for("admin_employees"))


@app.route("/admin/employees/<int:emp_id>/edit", methods=["POST"])
@login_required
@admin_required
def admin_employee_edit(emp_id):
    emp = db.session.get(User, emp_id)
    if not emp:
        flash("الموظف غير موجود", "danger")
        return redirect(url_for("admin_employees"))
    emp.name = request.form.get("name", emp.name).strip()
    emp.email = request.form.get("email", emp.email).strip()
    emp.phone = request.form.get("phone", emp.phone).strip()
    emp.department = request.form.get("department", emp.department).strip()
    password = request.form.get("password", "").strip()
    if password:
        if len(password) < 6:
            flash("كلمة المرور يجب أن تكون 6 أحرف على الأقل", "danger")
            return redirect(url_for("admin_employees"))
        emp.set_password(password)
    db.session.commit()
    flash("تم تحديث بيانات الموظف", "success")
    return redirect(url_for("admin_employees"))


# ─── Portfolio & Services Static Data ──────
PORTFOLIO_DATA = [
    {"id": 1, "title": "الهوية البصرية — تكافل", "category": "design", "client": "شركة تكافل للتأمين",
     "description": "هوية بصرية متكاملة تشمل الشعار، كتيب العلامة، والمطبوعات", "image": "design-1.jpg"},
    {"id": 2, "title": "حملة إعلانية — مذاق", "category": "design", "client": "مطعم مذاق",
     "description": "تصاميم إعلانية متكاملة لموسم رمضان (بنرات، منيو، بوسترات)", "image": "design-2.jpg"},
    {"id": 3, "title": "تصميم متجر إلكتروني", "category": "design", "client": "متجر أزياء",
     "description": "تصميم واجهة متجر إلكتروني متكامل بهوية بصرية مميزة", "image": "design-3.jpg"},
    {"id": 4, "title": "فيديو افتتاحي — المنارة", "category": "video", "client": "شركة المنارة العقارية",
     "description": "فيديو افتتاحي بمونتاج احترافي وموشن جرافيك", "image": "video-1.jpg"},
    {"id": 5, "title": "سلسلة فيديوهات توعوية", "category": "video", "client": "منظمة بصيرة",
     "description": "10 فيديوهات توعوية مع رسومات متحركة ومؤثرات بصرية", "image": "video-2.jpg"},
    {"id": 6, "title": "إعلان متحرك — منتج جديد", "category": "video", "client": "شركة تقنية",
     "description": "إعلان متحرك 30 ثانية بموشن جرافيك ثنائي الأبعاد", "image": "video-3.jpg"},
    {"id": 7, "title": "إدارة حسابات — متجر", "category": "social", "client": "متجر إلكتروني",
     "description": "إدارة كاملة +250% متابعين و +180% تفاعل في 6 أشهر", "image": "social-1.jpg"},
    {"id": 8, "title": "حملة تسويقية — مهرجان", "category": "social", "client": "مهرجان ثقافي",
     "description": "حملة تسويق متكاملة عبر منصات التواصل الاجتماعي", "image": "social-2.jpg"},
    {"id": 9, "title": "إطلاق علامة تجارية", "category": "social", "client": "علامة تجارية جديدة",
     "description": "استراتيجية إطلاق متكاملة عبر السوشيال ميديا", "image": "social-3.jpg"},
    {"id": 10, "title": "حملة إعلانات ممولة", "category": "marketing", "client": "شركة عقارات",
     "description": "حملة إعلانات ممولة حققت ROI 400% في شهرين", "image": "marketing-1.jpg"},
    {"id": 11, "title": "تحسين محركات البحث", "category": "marketing", "client": "متجر أونلاين",
     "description": "ظهور في الصفحة الأولى لمحركات البحث لأهم الكلمات", "image": "marketing-2.jpg"},
    {"id": 12, "title": "حملة إعلانات مطبوعة", "category": "ads", "client": "مركز تجاري",
     "description": "تصميم وطباعة إعلانات للوحات الطرق والمجلات", "image": "ads-1.jpg"},
    {"id": 13, "title": "لوحات إعلانية رقمية", "category": "ads", "client": "شركة اتصالات",
     "description": "تصاميم لوحات إعلانية رقمية لمناطق حيوية في المدينة", "image": "ads-2.jpg"},
    {"id": 14, "title": "حملة إعلانية متكاملة", "category": "ads", "client": "مطعم",
     "description": "حملة إعلانية متكاملة تشمل مطبوعات، لوحات، وإعلانات رقمية", "image": "ads-3.jpg"},
    {"id": 15, "title": "كتيب شركة — بروشور", "category": "print", "client": "شركة استشارات",
     "description": "تصميم وطباعة كتيب بروشور 24 صفحة بمقاس A4", "image": "print-1.jpg"},
    {"id": 16, "title": "هوية مطبوعة — كروت", "category": "print", "client": "بنك",
     "description": "تصميم وطباعة كروت شخصية، أظرف، ورق رسمي", "image": "print-2.jpg"},
    {"id": 17, "title": "كتاب فني — مجلد", "category": "print", "client": "دار نشر",
     "description": "إخراج وطباعة كتاب فني بغلاف مقوى وتجليد فاخر", "image": "print-3.jpg"},
    {"id": 18, "title": "تصميم جرافيك — متجر", "category": "design", "client": "متجر مجوهرات",
     "description": "تصميم صور منتجات وبنرات إعلانية للمتجر", "image": "design-4.jpg"},
    {"id": 19, "title": "فيديو موشن — منتج", "category": "video", "client": "شركة أغذية",
     "description": "فيديو موشن جرافيك 45 ثانية يشرح منتج جديد", "image": "video-4.jpg"},
    {"id": 20, "title": "حملة سوشيال — موسم", "category": "social", "client": "فندق سياحي",
     "description": "حملة سوشيال ميديا متكاملة للموسم الصيفي", "image": "social-4.jpg"},
    {"id": 21, "title": "تصميم إعلان — صحيفة", "category": "ads", "client": "شركة سيارات",
     "description": "تصميم إعلان صحفي كامل الصفحة لموديل جديد", "image": "ads-4.jpg"},
    {"id": 22, "title": "طباعة أوفسيت — مجلة", "category": "print", "client": "مجلة شهرية",
     "description": "طباعة أوفسيت لمجلة شهرية 64 صفحة بكمية 10000 نسخة", "image": "print-4.jpg"},
]


SERVICES_DATA = [
    {"id": 1, "icon": "palette", "color": "#A78BFA", "title": "التصميم الجرافيكي",
     "desc": "تصميم الشعارات، الهويات البصرية، البنرات، الإعلانات، والمطبوعات بأعلى جودة إبداعية."},
    {"id": 2, "icon": "video", "color": "#F59E0B", "title": "مونتاج الفيديو",
     "desc": "مونتاج احترافي، موشن جرافيك، أنيميشن، وفيديوهات دعائية لعلامتك التجارية."},
    {"id": 3, "icon": "chart-line", "color": "#A78BFA", "title": "إدارة السوشيال ميديا",
     "desc": "إدارة حساباتك، إنشاء المحتوى، جدولة المنشورات، وزيادة التفاعل والمتابعين."},
    {"id": 4, "icon": "bullhorn", "color": "#F59E0B", "title": "التسويق الرقمي",
     "desc": "حملات إعلانية مدفوعة، تحسين محركات البحث، واستراتيجيات تسويق متكاملة."},
    {"id": 5, "icon": "ad", "color": "#A78BFA", "title": "الدعاية والإعلان",
     "desc": "تصميم وإنتاج محتوى دعائي وإعلاني للمطبوعات، اللوحات، والمنصات الرقمية."},
    {"id": 6, "icon": "print", "color": "#F59E0B", "title": "الطباعة الديجيتال والأوفسيت",
     "desc": "طباعة ديجيتال وأوفسيت بجودة عالية للبروشورات، الكروت، البنرات، الكتب، والمجلات."},
]


# ─── Serve the main site ────────────────────
@app.route("/")
def serve_index():
    return send_from_directory("../static", "index.html")


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory("../static/assets", filename)


@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory("../static/images", filename)


# ─── Start ──────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        init_db()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
