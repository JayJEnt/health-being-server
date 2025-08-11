"""/vitamins router"""
from fastapi import APIRouter, Depends

from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from api.schemas.vitamin import VitaminCreate, Vitamin
from config import settings


router = APIRouter(prefix="/vitamins", tags=["vitamins"])