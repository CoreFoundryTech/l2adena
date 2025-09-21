from database import SessionLocal, engine
from models import User, Profile, Listing, Review, Message, PurchaseHistory, SellerLike, Server
from passlib.context import CryptContext
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def init_db():
    # Create tables
    from models import Base
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Create sample users
    user1 = User(email="user1@example.com", username="user1", password_hash=get_password_hash("password1"), is_verified=True)
    user2 = User(email="user2@example.com", username="user2", password_hash=get_password_hash("password2"), is_verified=False)

    db.add(user1)
    db.add(user2)
    db.commit()

    # Create servers
    server1 = Server(name="Adena", chronicle="Interlude")
    server2 = Server(name="Adena Classic", chronicle="Interlude")
    server3 = Server(name="Adena High Five", chronicle="High Five")

    db.add(server1)
    db.add(server2)
    db.add(server3)
    db.commit()

    # Create profiles
    profile1 = Profile(user_id=user1.id, description="Experienced seller", server_list="Adena, Adena Classic")
    profile2 = Profile(user_id=user2.id, description="New buyer", server_list="Adena")

    db.add(profile1)
    db.add(profile2)
    db.commit()

    # Create listings
    listing1 = Listing(seller_id=user1.id, server_id=server1.id, chronicle="Interlude", type="SELL", quantity=1000, price=1.5, description="High quality adena", status="ACTIVE")
    listing2 = Listing(seller_id=user1.id, server_id=server3.id, chronicle="High Five", type="BUY", quantity=500, price=1.2, description="Buying adena", status="ACTIVE")

    db.add(listing1)
    db.add(listing2)
    db.commit()

    # Create reviews
    review1 = Review(listing_id=listing1.id, reviewer_id=user2.id, reviewee_id=user1.id, rating=5, comment="Great seller!")

    db.add(review1)
    db.commit()

    # Create messages
    message1 = Message(room_id="room1", sender_id=user1.id, content="Hello, interested in your listing")

    db.add(message1)
    db.commit()

    # Create purchase history
    purchase1 = PurchaseHistory(buyer_id=user2.id, listing_id=listing1.id, status="COMPLETED")

    db.add(purchase1)
    db.commit()

    # Create seller likes
    like1 = SellerLike(buyer_id=user2.id, seller_id=user1.id)

    db.add(like1)
    db.commit()

    db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized with test data.")