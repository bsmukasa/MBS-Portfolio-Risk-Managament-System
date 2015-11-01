import os
import django
from random import uniform

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Factory
from risk_management.models import AssumptionProfile

fake = Factory.create()


if __name__ == '__main__':
    print("Starting seed script...")
    print("Seeding complete...")
