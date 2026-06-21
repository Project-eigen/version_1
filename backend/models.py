from datetime import datetime
import json
from extensions import db


class Family(db.Model):
    __tablename__ = "families"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    family_code = db.Column(db.String(6), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    members = db.relationship("User", backref="family", lazy=True)
    join_requests = db.relationship("FamilyJoinRequest", backref="family", lazy=True)
    medicines = db.relationship("MedicineEntry", backref="family", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "family_code": self.family_code,
            "created_at": self.created_at.isoformat(),
        }


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    avatar_url = db.Column(db.String(512))
    family_id = db.Column(db.Integer, db.ForeignKey("families.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    medicines = db.relationship("MedicineEntry", backref="user", lazy=True)
    logs = db.relationship("MedicineLog", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "family_id": self.family_id,
        }


class FamilyJoinRequest(db.Model):
    __tablename__ = "family_join_requests"

    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey("families.id"), nullable=False)
    status = db.Column(
        db.String(16), default="pending"
    )  # pending | accepted | rejected
    responder_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    requester = db.relationship("User", foreign_keys=[requester_id])
    responder = db.relationship("User", foreign_keys=[responder_id])

    def to_dict(self):
        return {
            "id": self.id,
            "requester": self.requester.to_dict(),
            "family_id": self.family_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class MedicineEntry(db.Model):
    __tablename__ = "medicine_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey("families.id"), nullable=True)
    name = db.Column(db.String(256), nullable=False)
    dosage = db.Column(db.String(128))
    schedule_json = db.Column(db.Text)  # JSON: ["morning", "evening"] etc.
    scan_image_url = db.Column(db.String(512))  # image from scanner
    pack_image_url = db.Column(db.String(512))  # image of the physical pack
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    logs = db.relationship("MedicineLog", backref="medicine", lazy=True)

    @property
    def schedule(self):
        if self.schedule_json:
            return json.loads(self.schedule_json)
        return []

    @schedule.setter
    def schedule(self, value):
        self.schedule_json = json.dumps(value)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "family_id": self.family_id,
            "name": self.name,
            "dosage": self.dosage,
            "schedule": self.schedule,
            "scan_image_url": self.scan_image_url,
            "pack_image_url": self.pack_image_url,
            "created_at": self.created_at.isoformat(),
        }


class MedicineLog(db.Model):
    __tablename__ = "medicine_logs"

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("medicine_entries.id"), nullable=False)
    logged_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    time_slot = db.Column(db.String(16))  # morning | afternoon | evening | night
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "entry_id": self.entry_id,
            "logged_by_user_id": self.logged_by_user_id,
            "time_slot": self.time_slot,
            "logged_at": self.logged_at.isoformat(),
        }
