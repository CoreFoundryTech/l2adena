from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ListingType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

# Server schemas
class ServerBase(BaseModel):
    name: str
    chronicle: str

class ServerCreate(ServerBase):
    pass

class ServerResponse(ServerBase):
    id: int

    class Config:
        from_attributes = True

class ServerActivityResponse(BaseModel):
    id: int
    name: str
    chronicle: str
    active_listings: int
    total_transactions: int
    total_sellers: int

    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_verified: bool
    language: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLanguageUpdate(BaseModel):
    language: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Profile schemas
class ProfileBase(BaseModel):
    description: Optional[str] = None
    server_list: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    user_id: int

    class Config:
        from_attributes = True

# Review schemas
class ReviewBase(BaseModel):
    listing_id: int
    reviewee_id: int
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    reviewer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Listing (Ads) schemas
class ListingBase(BaseModel):
    server_id: int
    chronicle: str
    type: ListingType
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    description: Optional[str] = None

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        return v

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

class ListingCreate(ListingBase):
    is_featured: Optional[bool] = False

class ListingUpdate(ListingBase):
    status: Optional[str] = None
    is_featured: Optional[bool] = None

class ListingResponse(ListingBase):
    id: int
    seller_id: int
    status: str
    is_featured: bool
    featured_expires_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    room_id: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Purchase History schemas (if needed)
class PurchaseHistoryBase(BaseModel):
    buyer_id: int
    listing_id: int
    status: str

class PurchaseHistoryResponse(PurchaseHistoryBase):
    id: int
    transaction_date: datetime

    class Config:
        from_attributes = True

# Seller Like schemas
class SellerLikeBase(BaseModel):
    seller_id: int

class SellerLikeCreate(SellerLikeBase):
    pass

class SellerLikeResponse(SellerLikeBase):
    id: int
    buyer_id: int
    created_at: datetime

    class Config:
        from_attributes = True