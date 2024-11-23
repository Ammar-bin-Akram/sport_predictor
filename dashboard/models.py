from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from sklearn.tree import DecisionTreeClassifier
import joblib

# Create your models here.

GENDER = (
    (0, 'Female'),
    (1, 'Male')
)

class Data(models.Model):
    name = models.CharField(max_length=100, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(13), MaxValueValidator(19)], null=True)
    height = models.PositiveIntegerField(null=True)
    sex = models.PositiveIntegerField(choices=GENDER, null=True)
    predictions = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        model = joblib.load('ml_model/sport_model.joblib')
        answer = model.predict([[self.age, self.height, self.sex]])
        if answer == [0]:
            self.predictions = 'Basketball'
        elif answer == [1]:
            self.predictions = 'Hockey'
        elif answer == [2]:
            self.predictions = 'Soccer'
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date'] # to get most recent on top

    def __str__(self):
        return self.name
    
