from django.core.management import BaseCommand
from users.models import User
from applicant.models import PersonalInformation, AcademicInformation, AccountBank, Referee
from board.models import LGA, Bank
from academic.models import InstitutionType, Program, CourseType
from ..data.users import applicants
import random


def create_applicant(data):
    user = User(
        first_name=data['first_name'], 
        last_name=data['last_name'],
        email=data['email']
    )
    user.set_password('bssb@123')
    user.save()
        
    lga = random.choice(LGA.objects.all())
    pdata = data['personal_information']
    PersonalInformation(
        guardian_name=pdata['gurdian_fullname'],
        phone_number=pdata['phone_number'],
        date_of_birth=pdata['date_of_birth'],
        place_of_birth=pdata['place_of_birth'],
        nin=pdata['nin'], bvn=pdata['bvn'],
        local_government_area=lga, user=user,
        residential_address=pdata['residential_address'],
    ).save()
        
        
    institution_type = random.choice(InstitutionType.objects.all())
    institution = random.choice(institution_type.institutions.all())
    course_type = random.choice(CourseType.objects.all())
    course = random.choice(course_type.courses.all())
    program = random.choice(Program.objects.all())
    level = random.choice(program.levels.all())
    adata = data['academic_information']
    AcademicInformation(
        year_of_admission=adata['year_of_admission'],
        year_of_graduation=adata['year_of_graduation'],
        id_number=adata['id_number'],
        institution_type = institution_type,
        institution = institution,
        program = program,
        course_type = course_type,
        course_of_study = course,
        current_level = level,
        user = user
    ).save()
        
    AccountBank(
        account_name = user.first_name + ' ' + user.last_name,
        account_number = data['account_infomation']['number'],
        bank = random.choice(Bank.objects.all()),
        user = user
    ).save()
        
    referee = data['referee']
    Referee(
        user = user,
        fullname = referee['fullname'],
        occupation = referee['occupation'],
        phone_number = referee['phone_number'],
    ).save()


class Command(BaseCommand):
    help = 'Add fake applicants'
    
    def handle(self, *args, **options):
        for data in applicants:
            email = data['email']
            applicant_exists = User.objects.filter(email=email).exists()

            if applicant_exists: continue
            
            try:
                create_applicant(data)
            except Exception as e:
                print(e)
        
        print('Fake Applicants added successfully!!!')