import threading, time, random
from datetime import datetime
from .db import SessionLocal
from .crud import ensure_product, record_event

# 模拟的数据源循环：仅用于演示
def mock_data_source_loop(interval_seconds: int = 30):
    def loop():
        db = SessionLocal()
        try:
            while True:
                # 这里可从真实授权的 API 获取商品状态；当前为随机模拟
                products = ["maotai-001"]
                for pid in products:
                    p = ensure_product(db, pid)
                    prev = p.last_in_stock
                    # 随机更改（更偏向无货）
                    new_state = random.choice([False, False, True])
                    if prev != new_state and (not prev and new_state):
                        # restock event
                        payload = {"from": prev, "to": new_state, "price": float(p.last_price)}
                        record_event(db, pid, "restock", payload)
                        print(f"[{datetime.utcnow().isoformat()}] EVENT restock {pid} -> {payload}")
                    # update product record
                    p.last_in_stock = new_state
                    p.last_checked_at = datetime.utcnow()
                    db.add(p)
                    db.commit()
                time.sleep(interval_seconds)
        finally:
            db.close()

    t = threading.Thread(target=loop, daemon=True)
    t.start()
