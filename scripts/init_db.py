import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.models import init_db

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized.")