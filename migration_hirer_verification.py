"""Thêm cột is_verified / verify_requested cho hirer_profile (idempotent, chạy được cho SQLite và Postgres)."""
from sqlalchemy import inspect, text

from app import app, db


def run():
    with app.app_context():
        cols = {c['name'] for c in inspect(db.engine).get_columns('hirer_profile')}
        for name in ('is_verified', 'verify_requested'):
            if name in cols:
                print(f'[SKIP] hirer_profile.{name} đã tồn tại')
                continue
            db.session.execute(text(
                f'ALTER TABLE hirer_profile ADD COLUMN {name} BOOLEAN NOT NULL DEFAULT FALSE'
            ))
            print(f'[OK] Đã thêm hirer_profile.{name}')
        db.session.commit()


if __name__ == '__main__':
    run()
