#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔐 SECRETS MANAGEMENT - مدیریت امن اطلاعات حساس
این فایل هرگز نباید به گیت‌هاب پوش شود!
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
import base64
import hashlib

class SecretsManager:
    """
    مدیریت امن توکن‌ها و کلیدها با رمزنگاری
    """
    
    def __init__(self, key_file: str = "config/.secrets.key"):
        self.key_file = Path(key_file)
        self.secrets_file = Path("config/secrets.json.enc")
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
        self.secrets = self._load_secrets()
    
    def _load_or_create_key(self) -> bytes:
        """بارگذاری یا ایجاد کلید رمزنگاری"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            self.key_file.parent.mkdir(exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _load_secrets(self) -> Dict:
        """بارگذاری و رمزگشایی secrets"""
        if not self.secrets_file.exists():
            return {}
        
        try:
            with open(self.secrets_file, 'rb') as f:
                encrypted = f.read()
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted)
        except:
            return {}
    
    def _save_secrets(self):
        """رمزنگاری و ذخیره secrets"""
        encrypted = self.cipher.encrypt(json.dumps(self.secrets).encode())
        with open(self.secrets_file, 'wb') as f:
            f.write(encrypted)
    
    def get(self, key: str, default: Any = None) -> Any:
        """دریافت یک secret"""
        return self.secrets.get(key, default)
    
    def set(self, key: str, value: Any):
        """تنظیم یک secret"""
        self.secrets[key] = value
        self._save_secrets()
    
    def get_telegram_token(self) -> Optional[str]:
        """دریافت توکن تلگرام"""
        return self.get('TELEGRAM_TOKEN', os.getenv('TELEGRAM_TOKEN'))
    
    def get_railway_token(self) -> Optional[str]:
        """دریافت توکن Railway"""
        return self.get('RAILWAY_TOKEN', os.getenv('RAILWAY_TOKEN'))
    
    def get_github_token(self) -> Optional[str]:
        """دریافت توکن گیت‌هاب"""
        return self.get('GITHUB_TOKEN', os.getenv('GITHUB_TOKEN'))
    
    def get_openai_key(self) -> Optional[str]:
        """دریافت کلید OpenAI (برای تکامل آینده)"""
        return self.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
    
    def get_user_api_key(self, user_id: int, api_name: str) -> Optional[str]:
        """دریافت API Key یک کاربر"""
        key = f"user_{user_id}_{api_name}"
        return self.get(key)
    
    def set_user_api_key(self, user_id: int, api_name: str, api_key: str):
        """ذخیره API Key یک کاربر"""
        key = f"user_{user_id}_{api_name}"
        self.set(key, api_key)
    
    def get_all_secrets(self) -> Dict:
        """دریافت همه secrets (فقط برای مدیریت)"""
        return self.secrets.copy()
    
    def rotate_key(self):
        """تغییر کلید رمزنگاری (برای امنیت بیشتر)"""
        new_key = Fernet.generate_key()
        new_cipher = Fernet(new_key)
        
        # رمزگشایی با کلید قدیم
        decrypted = json.dumps(self.secrets).encode()
        
        # رمزنگاری با کلید جدید
        encrypted = new_cipher.encrypt(decrypted)
        
        # ذخیره کلید جدید
        with open(self.key_file, 'wb') as f:
            f.write(new_key)
        
        # ذخیره secrets با کلید جدید
        with open(self.secrets_file, 'wb') as f:
            f.write(encrypted)
        
        self.key = new_key
        self.cipher = new_cipher

# نمونه‌سازی سراسری
secrets = SecretsManager()
