from django.db import models

class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.breed}"

class Mission(models.Model):
    cat = models.OneToOneField(SpyCat, on_delete=models.PROTECT, null=True, related_name='mission')
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission for {self.cat.name}"

class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Target {self.name} in {self.country} for {self.mission.cat.name}"