from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import User, Profile, Review, Listing, Message, PurchaseHistory, SellerLike, Server
from schemas import (
    UserCreate, UserLogin, UserResponse, Token, UserLanguageUpdate,
    ProfileCreate, ProfileUpdate, ProfileResponse,
    ReviewCreate, ReviewResponse,
    ListingCreate, ListingUpdate, ListingResponse,
    MessageCreate, MessageResponse,
    PurchaseHistoryResponse, SellerLikeCreate, SellerLikeResponse,
    ServerCreate, ServerResponse, ServerActivityResponse
)
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from datetime import timedelta, datetime
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="L2 Adena Marketplace API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Security middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

security = HTTPBearer()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: str, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

manager = ConnectionManager()

def get_current_user_ws(token: str = Query(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello from L2 Adena Backend!"}

# Auth endpoints
@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout():
    # For JWT, logout is handled client-side by discarding the token
    return {"message": "Logged out successfully"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/users/me/language", response_model=UserResponse)
async def update_user_language(language_update: UserLanguageUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.language = language_update.language
    db.commit()
    db.refresh(current_user)
    return current_user

# Users CRUD
@app.get("/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = user_update.email
    user.username = user_update.username
    if user_update.password:
        user.password_hash = get_password_hash(user_update.password)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

# Profiles CRUD
@app.post("/profiles", response_model=ProfileResponse)
async def create_profile(profile: ProfileCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    db_profile = Profile(**profile.dict(), user_id=current_user.id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.get("/profiles/me", response_model=ProfileResponse)
async def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return current_user.profile

@app.put("/profiles/me", response_model=ProfileResponse)
async def update_profile(profile_update: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in profile_update.dict(exclude_unset=True).items():
        setattr(current_user.profile, key, value)
    db.commit()
    db.refresh(current_user.profile)
    return current_user.profile

@app.delete("/profiles/me")
async def delete_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(current_user.profile)
    db.commit()
    return {"message": "Profile deleted"}

# Servers CRUD
@app.post("/servers", response_model=ServerResponse)
async def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    db_server = Server(**server.dict())
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

@app.get("/servers", response_model=List[ServerResponse])
async def get_servers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    servers = db.query(Server).offset(skip).limit(limit).all()
    return servers

@app.get("/servers/{server_id}", response_model=ServerResponse)
async def get_server(server_id: int, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@app.put("/servers/{server_id}", response_model=ServerResponse)
async def update_server(server_id: int, server_update: ServerCreate, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    for key, value in server_update.dict(exclude_unset=True).items():
        setattr(server, key, value)
    db.commit()
    db.refresh(server)
    return server

@app.delete("/servers/{server_id}")
async def delete_server(server_id: int, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    db.delete(server)
    db.commit()
    return {"message": "Server deleted"}

@app.get("/servers/activity", response_model=List[ServerActivityResponse])
async def get_servers_activity(db: Session = Depends(get_db)):
    query = db.query(
        Server.id,
        Server.name,
        Server.chronicle,
        func.count(Listing.id).label('active_listings'),
        func.count(PurchaseHistory.id).label('total_transactions'),
        func.count(func.distinct(User.id)).label('total_sellers')
    ).join(Listing, Server.id == Listing.server_id)\
     .join(User, Listing.seller_id == User.id)\
     .outerjoin(PurchaseHistory, Listing.id == PurchaseHistory.listing_id)\
     .filter(Listing.status == "ACTIVE")\
     .filter(User.is_verified == True)\
     .group_by(Server.id, Server.name, Server.chronicle)\
     .order_by((func.count(Listing.id) + func.count(PurchaseHistory.id)).desc())

    results = query.all()
    return results

# Reviews CRUD
@app.post("/reviews", response_model=ReviewResponse)
async def create_review(review: ReviewCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_review = Review(**review.dict(), reviewer_id=current_user.id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/reviews", response_model=List[ReviewResponse])
async def get_reviews(listing_id: Optional[int] = None, reviewer_id: Optional[int] = None, reviewee_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Review)
    if listing_id:
        query = query.filter(Review.listing_id == listing_id)
    if reviewer_id:
        query = query.filter(Review.reviewer_id == reviewer_id)
    if reviewee_id:
        query = query.filter(Review.reviewee_id == reviewee_id)
    reviews = query.offset(skip).limit(limit).all()
    return reviews

@app.get("/reviews/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@app.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(review_id: int, review_update: ReviewCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.reviewer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for key, value in review_update.dict(exclude_unset=True).items():
        setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return review

@app.delete("/reviews/{review_id}")
async def delete_review(review_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.reviewer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}

# Listings (Ads) CRUD
@app.post("/listings", response_model=ListingResponse)
async def create_listing(listing: ListingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_verified:
        raise HTTPException(status_code=403, detail="Only verified sellers can create listings")
    db_listing = Listing(**listing.dict(), seller_id=current_user.id)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@app.get("/listings", response_model=List[ListingResponse])
async def get_listings(
    seller_id: Optional[int] = None,
    server_id: Optional[int] = None,
    chronicle: Optional[str] = None,
    type: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    quantity_min: Optional[int] = None,
    quantity_max: Optional[int] = None,
    description_search: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Listing).filter(Listing.status == "ACTIVE")
    if seller_id:
        query = query.filter(Listing.seller_id == seller_id)
    if server_id:
        query = query.filter(Listing.server_id == server_id)
    if chronicle:
        query = query.filter(Listing.chronicle.ilike(f"%{chronicle}%"))
    if type:
        query = query.filter(Listing.type == type)
    if price_min is not None:
        query = query.filter(Listing.price >= price_min)
    if price_max is not None:
        query = query.filter(Listing.price <= price_max)
    if quantity_min is not None:
        query = query.filter(Listing.quantity >= quantity_min)
    if quantity_max is not None:
        query = query.filter(Listing.quantity <= quantity_max)
    if description_search:
        query = query.filter(Listing.description.ilike(f"%{description_search}%"))
    # Sort by featured first, then by created_at desc
    query = query.order_by(Listing.is_featured.desc(), Listing.created_at.desc())
    listings = query.offset(skip).limit(limit).all()
    return listings

@app.get("/listings/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@app.put("/listings/{listing_id}", response_model=ListingResponse)
async def update_listing(listing_id: int, listing_update: ListingUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for key, value in listing_update.dict(exclude_unset=True).items():
        setattr(listing, key, value)
    db.commit()
    db.refresh(listing)
    return listing

@app.delete("/listings/{listing_id}")
async def delete_listing(listing_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted"}

# Messages CRUD
@app.post("/messages", response_model=MessageResponse)
async def create_message(message: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_message = Message(**message.dict(), sender_id=current_user.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages", response_model=List[MessageResponse])
async def get_messages(room_id: Optional[str] = None, sender_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Message)
    if room_id:
        query = query.filter(Message.room_id == room_id)
    if sender_id:
        query = query.filter(Message.sender_id == sender_id)
    messages = query.offset(skip).limit(limit).all()
    return messages

@app.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.put("/messages/{message_id}", response_model=MessageResponse)
async def update_message(message_id: int, message_update: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for key, value in message_update.dict(exclude_unset=True).items():
        setattr(message, key, value)
    db.commit()
    db.refresh(message)
    return message

@app.delete("/messages/{message_id}")
async def delete_message(message_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(message)
    db.commit()
    return {"message": "Message deleted"}

# Chat endpoints
@app.post("/chat/start")
async def start_chat(listing_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    seller_id = listing.seller_id
    buyer_id = current_user.id
    room_id = f"{listing_id}_{buyer_id}_{seller_id}"
    # Check if room already has messages, but for now, just return room_id
    return {"room_id": room_id}

@app.get("/chat/rooms")
async def get_chat_rooms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get all messages where user is sender or in room_id
    messages = db.query(Message).filter(
        (Message.sender_id == current_user.id) |
        (Message.room_id.like(f"%_{current_user.id}_%")) |
        (Message.room_id.like(f"%_{current_user.id}"))
    ).order_by(Message.created_at.desc()).all()
    rooms = {}
    for msg in messages:
        if msg.room_id not in rooms:
            # Parse other user
            parts = msg.room_id.split('_')
            listing_id = int(parts[0])
            buyer_id = int(parts[1])
            seller_id = int(parts[2])
            other_user_id = seller_id if current_user.id == buyer_id else buyer_id
            other_user = db.query(User).filter(User.id == other_user_id).first()
            rooms[msg.room_id] = {
                "room_id": msg.room_id,
                "other_user": other_user.username if other_user else "Unknown",
                "last_message": msg.content,
                "last_message_time": msg.created_at.isoformat()
            }
    return list(rooms.values())

@app.websocket("/ws/chat/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str, token: str = Query(...), db: Session = Depends(get_db)):
    user = get_current_user_ws(token, db)
    # Check access
    if not user.is_admin:
        # Parse room_id: listing_id_buyer_id_seller_id
        try:
            parts = room_id.split('_')
            listing_id = int(parts[0])
            buyer_id = int(parts[1])
            seller_id = int(parts[2])
            if user.id not in [buyer_id, seller_id]:
                await websocket.close(code=1008)
                return
        except:
            await websocket.close(code=1008)
            return
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            content = message_data.get("content")
            if content:
                # Save to DB
                db_message = Message(room_id=room_id, sender_id=user.id, content=content)
                db.add(db_message)
                db.commit()
                db.refresh(db_message)
                # Broadcast
                await manager.broadcast(json.dumps({
                    "id": db_message.id,
                    "room_id": room_id,
                    "sender_id": user.id,
                    "sender_username": user.username,
                    "content": content,
                    "created_at": db_message.created_at.isoformat()
                }), room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

# Purchase History CRUD
@app.post("/purchase-history", response_model=PurchaseHistoryResponse)
async def create_purchase_history(purchase: PurchaseHistoryResponse, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Assuming purchase is created when a transaction happens, but for now, allow manual creation
    db_purchase = PurchaseHistory(**purchase.dict(), buyer_id=current_user.id)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@app.get("/purchase-history/me", response_model=List[PurchaseHistoryResponse])
async def get_my_purchase_history(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    purchases = db.query(PurchaseHistory).filter(PurchaseHistory.buyer_id == current_user.id).offset(skip).limit(limit).all()
    return purchases

@app.get("/purchase-history/{purchase_id}", response_model=PurchaseHistoryResponse)
async def get_purchase_history(purchase_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    purchase = db.query(PurchaseHistory).filter(PurchaseHistory.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    if purchase.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return purchase

# Seller Likes CRUD
@app.post("/likes", response_model=SellerLikeResponse)
async def like_seller(like: SellerLikeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if already liked
    existing_like = db.query(SellerLike).filter(SellerLike.buyer_id == current_user.id, SellerLike.seller_id == like.seller_id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")
    db_like = SellerLike(buyer_id=current_user.id, seller_id=like.seller_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

@app.delete("/likes/{seller_id}")
async def unlike_seller(seller_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    like = db.query(SellerLike).filter(SellerLike.buyer_id == current_user.id, SellerLike.seller_id == seller_id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(like)
    db.commit()
    return {"message": "Unliked"}

@app.get("/likes/me", response_model=List[SellerLikeResponse])
async def get_my_likes(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    likes = db.query(SellerLike).filter(SellerLike.buyer_id == current_user.id).offset(skip).limit(limit).all()
    return likes

@app.get("/users/{user_id}/likes-count")
async def get_user_likes_count(user_id: int, db: Session = Depends(get_db)):
    count = db.query(SellerLike).filter(SellerLike.seller_id == user_id).count()
    return {"likes_count": count}

@app.get("/users/{user_id}/reputation")
async def get_user_reputation(user_id: int, db: Session = Depends(get_db)):
    from sqlalchemy import func
    result = db.query(func.avg(Review.rating)).filter(Review.reviewee_id == user_id).scalar()
    average_rating = float(result) if result else 0.0
    review_count = db.query(Review).filter(Review.reviewee_id == user_id).count()
    return {"average_rating": average_rating, "review_count": review_count}

# Admin endpoints
@app.post("/admin/expire-featured")
async def expire_featured_listings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.utcnow()
    expired_listings = db.query(Listing).filter(Listing.is_featured == True, Listing.featured_expires_at < now).all()
    count = 0
    for listing in expired_listings:
        listing.is_featured = False
        listing.featured_expires_at = None
        count += 1
    db.commit()
    return {"message": f"Expired {count} featured listings"}

# Stripe placeholders for future integration
@app.post("/stripe/create-payment-intent")
async def create_payment_intent():
    # TODO: Implement Stripe payment intent creation
    # This will handle payments for premium features
    return {"message": "Stripe integration not yet implemented"}

@app.post("/stripe/webhook")
async def stripe_webhook():
    # TODO: Implement Stripe webhook handling
    # This will handle payment confirmations and updates
    return {"message": "Stripe webhook not yet implemented"}

@app.post("/premium/feature-listing")
async def feature_listing():
    # TODO: Implement featuring listing with payment
    # This will set is_featured=True and featured_expires_at
    return {"message": "Premium feature not yet implemented"}

@app.post("/premium/verify-seller")
async def verify_seller():
    # TODO: Implement seller verification with payment
    # This will set is_verified=True
    return {"message": "Seller verification not yet implemented"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)