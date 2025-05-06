from django.db import models
from django.contrib.auth.models import User
import numpy as np

# 🛍️ Item Model (Existing)
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# 🔒 FaceProfile Model (New) → Stores Face Data for Authentication
class FaceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_encoding = models.BinaryField()  # Stores face encoding as binary data

    def set_encoding(self, encoding):
        """Store face encoding as a binary NumPy array"""
        self.face_encoding = np.array(encoding, dtype=np.float64).tobytes()

    def get_encoding(self):
        """Retrieve face encoding as a NumPy array"""
        return np.frombuffer(self.face_encoding, dtype=np.float64)