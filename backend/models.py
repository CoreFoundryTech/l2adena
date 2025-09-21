from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    language = Column(String, default='en')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False)
    listings = relationship("Listing", back_populates="seller")
    reviews_given = relationship("Review", foreign_keys="Review.reviewer_id", back_populates="reviewer")
    reviews_received = relationship("Review", foreign_keys="Review.reviewee_id", back_populates="reviewee")
    messages = relationship("Message", back_populates="sender")
    purchase_history = relationship("PurchaseHistory", back_populates="buyer")
    seller_likes_given = relationship("SellerLike", foreign_keys="SellerLike.buyer_id", back_populates="buyer")
    seller_likes_received = relationship("SellerLike", foreign_keys="SellerLike.seller_id", back_populates="seller")

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    chronicle = Column(String, nullable=False)  # e.g., "Interlude", "High Five"

    listings = relationship("Listing", back_populates="server")

class Profile(Base):
    __tablename__ = "profiles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    description = Column(Text)
    server_list = Column(Text)  # Could be JSON or comma-separated

    user = relationship("User", back_populates="profile")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    reviewee_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    listing = relationship("Listing", back_populates="reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
    reviewee = relationship("User", foreign_keys=[reviewee_id], back_populates="reviews_received")

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"))
    server_id = Column(Integer, ForeignKey("servers.id"))
    chronicle = Column(String, nullable=False)
    type = Column(String, nullable=False)  # BUY or SELL
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    status = Column(String, default="ACTIVE")  # ACTIVE or CLOSED
    is_featured = Column(Boolean, default=False)
    featured_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    seller = relationship("User", back_populates="listings")
    server = relationship("Server", back_populates="listings")
    reviews = relationship("Review", back_populates="listing")
    purchase_history = relationship("PurchaseHistory", back_populates="listing")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String, nullable=False)  # Unique room per transaction
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    sender = relationship("User", back_populates="messages")

class PurchaseHistory(Base):
    __tablename__ = "purchase_history"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"))
    listing_id = Column(Integer, ForeignKey("listings.id"))
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, nullable=False)  # e.g., COMPLETED, PENDING

    buyer = relationship("User", back_populates="purchase_history")
    listing = relationship("Listing", back_populates="purchase_history")

class SellerLike(Base):
    __tablename__ = "seller_likes"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="seller_likes_given")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="seller_likes_received")