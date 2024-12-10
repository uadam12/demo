from django.core.management.base import BaseCommand
from ..data.institutions import institutions_by_type
from ..data.programs import programs
from ..data.banks import banks
from ..data.lgas import lgas
from ..data.faqs import faqs

from board.models import Bank, LGA
from main.models import Article, FAQ
from academic.models import InstitutionType, Institution, Course, Program, Level


class Command(BaseCommand):
    help = 'Populate data base with some data'
    
    def handle(self, *_, **__):
        # Frequently Asked Questions
        questions = [q.question for q in FAQ.objects.all()]
        faq_models = [FAQ(**faq) for faq in faqs if not faq['question'] in questions]
        FAQ.objects.bulk_create(faq_models)

        # Add bank models
        available_banks = Bank.objects.all()
        available_bank_codes = [bank.code for bank in available_banks]
        bank_models = [Bank(**bank) for bank in banks if not bank['code'] in available_bank_codes]        
        Bank.objects.bulk_create(bank_models)

        # Add LGA models
        available_lgas = [lga.code for lga in LGA.objects.all()]
        lga_models = [LGA(code=code, name=name) for code, name in lgas.items() if not code in available_lgas]
        LGA.objects.bulk_create(lga_models)

        # Add programs and their levels
        program_names = [program.name for program in Program.objects.all()]
        for name in programs:
            if name in program_names: continue
            program = Program.objects.create(name=name)

            levels = programs[name]['levels']
            for level in levels:
                Level.objects.create(program=program, **level)
        
            courses = programs[name]['courses']
            for course in courses:
                try:
                    Course.objects.get_or_create(title=course, program=program)
                except Exception as e:
                    print(e)
                    
        # Add LGA models
        available_inst_types = [inst_type.name for inst_type in InstitutionType.objects.all()]
        for ins_type in institutions_by_type:
            if ins_type in available_inst_types: continue
            i_type = InstitutionType.objects.create(name=ins_type)
            
            for inst in institutions_by_type[ins_type]:
                try:
                    Institution.objects.create(institution_type=i_type, name=inst)
                except Exception as e:
                    print(e)

        print('Database populated successfully!!!')