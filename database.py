import sqlite3

DB_NAME = "compliance.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            zone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            officer_id INTEGER NOT NULL,
            product_name TEXT,
            manufacturer_address TEXT,
            net_quantity TEXT,
            mfg_date TEXT,
            mrp TEXT,
            consumer_care TEXT,
            country_of_origin TEXT,
            unit_sale_price TEXT,
            font_legibility TEXT,
            status TEXT,
            was_edited BOOLEAN DEFAULT 0,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (officer_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    conn.close()

def save_record(record: dict) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO records (
            officer_id, product_name, manufacturer_address, net_quantity,
            mfg_date, mrp, consumer_care, country_of_origin,
            unit_sale_price, font_legibility, status, was_edited
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["officer_id"], record["product_name"], record["manufacturer_address"],
        record["net_quantity"], record["mfg_date"], record["mrp"],
        record["consumer_care"], record["country_of_origin"],
        record["unit_sale_price"], record["font_legibility"],
        record["status"], record.get("was_edited", False)
    ))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_records_by_officer(officer_id: int) -> list:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE officer_id = ?", (officer_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")
    test_record = {
        "officer_id": 1,
        "product_name": "Test Biscuit Packet",
        "manufacturer_address": "123 Factory Road, Pune",
        "net_quantity": "200g",
        "mfg_date": "01/2026",
        "mrp": "Rs. 50",
        "consumer_care": "1800-123-456",
        "country_of_origin": "India",
        "unit_sale_price": "Rs. 250/kg",
        "font_legibility": "Compliant",
        "status": "compliant"
    }

    new_id = save_record(test_record)
    print(f"Inserted record with ID: {new_id}")

    records = get_records_by_officer(1)
    print(f"Records for officer 1: {records}")