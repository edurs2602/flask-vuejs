import os
import sys
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from db.models import User as MongoUser, UserPreferences as MongoUserPreferences

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_DIR = os.path.join(ROOT_DIR, "server")
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

@dataclass
class UserPreferencesData:
    timezone: str

@dataclass
class UserData:
    username: str
    password: str
    roles: list
    preferences: UserPreferencesData
    active: bool = True
    created_ts: float = 0.0

def parse_timestamp(timestamp_str: str) -> float:
    dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.timestamp()

def build_roles(record: dict) -> list:
    roles = []
    if record.get("is_user_admin"):
        roles.append("admin")
    if record.get("is_user_manager"):
        roles.append("manager")
    if record.get("is_user_tester"):
        roles.append("tester")
    return roles

def import_users():
    json_path = os.path.join(ROOT_DIR, "udata.json")
    print(f"[DEBUG] Looking for JSON file at: {json_path}")
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        print("[DEBUG] JSON file loaded successfully.")
    except Exception as e:
        error_msg = f"Error reading JSON file: {e}"
        print(f"[ERROR] {error_msg}")
        return error_msg

    users = data.get("users", [])
    print(f"[DEBUG] Found {len(users)} user records in the JSON.")
    inserted = 0
    for idx, record in enumerate(users, start=1):
        print(f"[DEBUG] Processing record #{idx}: {record}")
        try:
            user_data = UserData(
                username=record["user"],
                password=record["password"],
                roles=build_roles(record),
                preferences=UserPreferencesData(timezone=record["user_timezone"]),
                active=record.get("is_user_active", True),
                created_ts=parse_timestamp(record["created_at"])
            )
            print(f"[DEBUG] Parsed user data: {asdict(user_data)}")
        except Exception as e:
            print(f"[ERROR] Error parsing record #{idx}: {e}")
            continue

        user_dict = asdict(user_data)
        try:
            mongo_user = MongoUser(
                username=user_dict["username"],
                password=user_dict["password"],
                roles=user_dict["roles"],
                preferences=MongoUserPreferences(**user_dict["preferences"]),
                active=user_dict["active"],
                created_ts=user_dict["created_ts"]
            )
            mongo_user.save()
            print(f"[DEBUG] Inserted user: {user_dict['username']}")
            inserted += 1
        except Exception as e:
            print(f"[ERROR] Error inserting user {user_dict['username']}: {e}")
            continue

    result_msg = f"Inserted {inserted} users."
    print(f"[DEBUG] {result_msg}")
    return result_msg

if __name__ == "__main__":
    print("Task result:", import_users())
