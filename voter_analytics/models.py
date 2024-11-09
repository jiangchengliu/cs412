from django.db import models

# Create your models here.


class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"


def load_data():
    Voter.objects.all().delete() 
    file = open("voter_analytics/newton_voters.csv", "r")
    headers = file.readline() 
    
    for line in file:
        fields = [field.strip() for field in line.split(",")]
        v = Voter()
        v.last_name = fields[1]
        v.first_name = fields[2]
        v.street_number = fields[3]
        v.street_name = fields[4]
        v.apartment_number = fields[5]
        v.zip_code = fields[6]
        v.date_of_birth = fields[7]
        v.date_of_registration = fields[8]
        v.party_affiliation = fields[9] 
        v.precinct_number = fields[10]
        v.v20state = fields[11].lower() == 'true' 
        v.v21town = fields[12].lower() == 'true'
        v.v21primary = fields[13].lower() == 'true'
        v.v22general = fields[14].lower() == 'true'
        v.v23town = fields[15].lower() == 'true'
        v.voter_score = int(fields[16]) 
        v.save()

    print("Data loaded successfully")