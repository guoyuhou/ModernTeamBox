from app import app, db
from app.models import User, Room, Booking

with app.app_context():
    db.drop_all()  # 注意：这会删除所有现有数据
    db.create_all()

    # 添加一些示例房间
    rooms = [
        Room(name='海景大床房', description='宽敞的房间，配有king size大床和无敌海景', price=888, capacity=2),
        Room(name='山景双床房', description='舒适的双床房，可欣赏美丽的山景', price=666, capacity=2),
        Room(name='家庭套房', description='适合家庭入住的大套房，设有独立的客厅和两间卧室', price=1288, capacity=4)
    ]

    for room in rooms:
        db.session.add(room)

    # 添加一个示例用户
    user = User(username='admin', email='admin@example.com')
    user.set_password('password')
    db.session.add(user)

    db.session.commit()

    print("数据库创建成功，并添加了示例房间和用户。")
