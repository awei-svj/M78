from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from . import db, crud, schemas, tasks
from .db import SessionLocal, init_db

app = FastAPI(title="i茅台 合规监测 模板（后端）")

# 初始化 DB（创建表）
init_db()

# 启动模拟任务（仅演示）
tasks.mock_data_source_loop(interval_seconds=30)

def get_db():
    db_sess = SessionLocal()
    try:
        yield db_sess
    finally:
        db_sess.close()

@app.post("/users", summary="创建用户（演示）", response_model=dict)
def create_user(u: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, u.phone, u.email)

@app.post("/addresses", summary="保存地址（演示)")
def save_address(a: schemas.AddressCreate, db: Session = Depends(get_db)):
    # 简化示例
    from uuid import uuid4
    addr = crud.create_address(db, a.user_id, a.name, a.phone, a.full_address, a.is_default)
    return addr

@app.post("/subscribe", summary="订阅商品到货（演示）")
def subscribe(s: schemas.SubscribeReq, db: Session = Depends(get_db)):
    # Ensure product exists
    crud.ensure_product(db, s.product_id)
    return crud.create_subscription(db, s.user_id, s.product_id)

@app.get("/products/{product_id}", response_model=schemas.ProductOut, summary="查看商品状态")
def get_product(product_id: str, db: Session = Depends(get_db)):
    p = crud.get_product(db, product_id)
    if not p:
        raise HTTPException(404, "product missing")
    return p

@app.get("/events", response_model=list[schemas.EventOut], summary="事件历史")
def list_events(limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_events(db, limit)

@app.post("/refresh/{product_id}", summary="手动触发查询（演示）")
def manual_refresh(product_id: str, db: Session = Depends(get_db)):
    # 在合规环境中：这里应调用已授权数据源的接口并更新数据库
    # 当前示例：随机更新状态一次以模拟“手动查询”
    from .crud import ensure_product, record_event
    import random
    p = ensure_product(db, product_id)
    prev = p.last_in_stock
    new_state = random.choice([False, True])
    p.last_in_stock = new_state
    db.add(p); db.commit()
    if not prev and new_state:
        ev = record_event(db, product_id, "restock_manual", {"from": prev, "to": new_state, "price": float(p.last_price)})
        return {"ok": True, "event": ev.id}
    return {"ok": True, "status": "no_change"}
