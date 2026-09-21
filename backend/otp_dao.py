import random
from datetime import datetime, timedelta


def generate_otp():
    return str(random.randint(100000, 999999))


def create_otp(connection, email):
    cursor = connection.cursor()
    # Clear any previous unverified codes for this email before issuing a new one
    cursor.execute("DELETE FROM otp_verifications WHERE email = %s AND is_verified = 0", (email,))
    otp_code = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=10)
    cursor.execute(
        "INSERT INTO otp_verifications (email, otp_code, is_verified, expires_at, created_at) "
        "VALUES (%s, %s, 0, %s, %s)",
        (email, otp_code, expires_at, datetime.now())
    )
    connection.commit()
    return otp_code


def verify_otp(connection, email, otp_code):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, expires_at FROM otp_verifications WHERE email = %s AND otp_code = %s AND is_verified = 0 "
        "ORDER BY id DESC LIMIT 1",
        (email, otp_code)
    )
    row = cursor.fetchone()
    if row is None:
        return False, "Incorrect code."

    otp_id, expires_at = row
    if datetime.now() > expires_at:
        return False, "This code has expired. Please request a new one."

    cursor.execute("UPDATE otp_verifications SET is_verified = 1 WHERE id = %s", (otp_id,))
    connection.commit()
    return True, None


def is_email_verified_recently(connection, email):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id FROM otp_verifications WHERE email = %s AND is_verified = 1 "
        "AND created_at > %s ORDER BY id DESC LIMIT 1",
        (email, datetime.now() - timedelta(minutes=30))
    )
    return cursor.fetchone() is not None


def clear_otp(connection, email):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM otp_verifications WHERE email = %s", (email,))
    connection.commit()