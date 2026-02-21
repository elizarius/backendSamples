from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    """Sample model for demonstration"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    #  Make created_by optional
    #  TBD AELZ: For demo purposes, allow NULL and blank. In production, consider if this should be required. 
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    # TBD AELZ: remove user key form DB, generaly say, it have to be token based, but not user
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='items',
        null=True,      #   Allow NULL in database
        blank=True      # Allow empty in forms
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
