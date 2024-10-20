import os
from django.conf import settings
from .helpers import PDFDoc, Header, Row, Text, Grid, Signature


def get_image(name):
    return os.path.join(
        settings.MEDIA_ROOT,
        name
    )

def generate_application_form(application, request):
    #doc = PDFDoc(f"{application.application_id} Application Form.pdf")
    applicant = application.applicant
    info = applicant.personal_info
    
    try:
        applicant_img = get_image(applicant.picture.name)
    except:
        applicant_img = get_image('applicant.jpg')

    doc = PDFDoc('demo.pdf')
    doc.add(Header(
        get_image('logo.png'), 
        str(application.scholarship),
        application.application_id,
        applicant_img
    ))

    # Personal Information
    doc.add_header("Personal Information")
    doc.add(Row(
        ('Firstname', applicant.first_name),
        ('Lastname', applicant.last_name),
        ('Guardian fullname', info.guardian_name),
        ('Gender', info.gender),
        ('Date of Birth', str(info.date_of_birth))
    ))
    doc.add(Row(
        ('Email address', applicant.email),
        ('Phone Number', info.phone_number),
        ('National Identification Number', info.nin),
        ('Bank Verification Number', info.bvn)
    ))
    doc.add(Row(
        ('Place of birth', info.place_of_birth),
        ('Local Government Area', str(info.local_government_area)),
        ('Residential Address', info.residential_address)
    ))
    
    # Academic Information
    doc.add_header("Academic Information")
    doc.add(Row(
        ('Institution', str(application.instituion)),
        ('Program', str(application.program)),
        ('Course Of Study', str(application.course_of_study))
    ))
    doc.add(Row(
        ('Current Level', str(application.level)),
        ('ID Number', application.id_number),
        ('Admission Year', str(application.admission_year)),
        ('Graduation Year', str(application.graduation_year))
    ))
    
    # Account details
    doc.add_header('Account Details')
    doc.add(Row(
        ('Account Bank', str(application.account_bank)),
        ('Account Name', application.account_name),
        ('Account Number', application.account_number)
    ))
    
    
    # School attended
    doc.add_header('School Attended')
    doc.add(Grid(
        application.schools_attended
    ))
    # Referee Details
    doc.add_header('Referee')
    doc.add(Row(
        ('Fullname', application.referee_name),
        ('Phone number', application.referee_phone_number),
        ('Occupation', application.referee_occupation)
    ))

    doc.add_header('Decleration')
    for text in application.declerations:
        doc.add(Text(text))
    
    doc.add_space(60)
    doc.add(Signature(
        application.applied_on
    ))

    return doc.generate_pdf()

