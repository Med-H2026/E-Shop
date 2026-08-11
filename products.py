from app import app, db, Product

with app.app_context():
    db.create_all()
    # Add sample data
    p1 = Product(name="Wireless Headphones", price=79, category="Electronics", image="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300")
    p2 = Product(name="Running Shoes", price=120, category="Fashion", image="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300")
    db.session.add_all([p1,p2])
    db.session.commit()
    print("Products added!")