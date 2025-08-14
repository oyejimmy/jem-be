# seed_data.py
from app.database.db import SessionLocal, init_db
from app.models.products import Product, Anklet, Bangle, Bracelet, Combo, EarStud, Earing, Hoop, Pendant, Ring, WallFrame

def create_sample_data(model_class, category_name, is_product=False):
    """Generate 10 sample rows for a given model."""
    return [
        model_class(
            name=f"{category_name} Item {i+1}",
            full_name=f"Full {category_name} Item {i+1}",
            retail_price=100.0 + i * 10,
            offer_price=90.0 + i * 5,
            currency="USD",
            description=f"This is a description for {category_name} item {i+1}.",
            delivery_charges=5.0,
            stock=50 - i,
            images=f"image_{i+1}.jpg",
            available=1,
            sold=0,
            status="available",
            **({"type": category_name} if is_product else {})  # Only for Product table
        )
        for i in range(10)
    ]

def seed_all_tables():
    init_db()
    db = SessionLocal()

    model_map = {
        Product: "Product",
        Anklet: "Anklet",
        Bangle: "Bangle",
        Bracelet: "Bracelet",
        Combo: "Combo",
        EarStud: "Ear Stud",
        Earing: "Earing",
        Hoop: "Hoop",
        Pendant: "Pendant",
        Ring: "Ring",
        WallFrame: "Wall Frame"
    }

    for model_class, category_name in model_map.items():
        if db.query(model_class).count() == 0:
            sample_data = create_sample_data(
                model_class,
                category_name,
                is_product=(model_class == Product)
            )
            db.add_all(sample_data)
            print(f"✅ Inserted 10 rows into {category_name} table.")
        else:
            print(f"⚠️ {category_name} table already has data. Skipping...")

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_all_tables()
    print("✅ Database seeded with sample data successfully.")
    print("You can now run your application.")
