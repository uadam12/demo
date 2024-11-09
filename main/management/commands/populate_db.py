from django.core.management.base import BaseCommand
from ..data.institutions import inst_types
from ..data.programs import programs
from ..data.banks import banks
from ..data.lgas import lgas
from ..data.articles import articles
from ..data.criteria import criteria, requirements
from ..data.field_of_study import field_of_study

from board.models import Bank, LGA, Requirement, Criterion
from main.models import Article
from academic.models import (
    InstitutionType, Institution,
    CourseType, Course, 
    Program, Level,    
)


class Command(BaseCommand):
    help = 'Populate data base with some data'
    
    def handle(self, *args, **options):
        # Articles
        available_articles = Article.objects.all()
        available_headlines = [article.headline for article in available_articles]
        article_models = [Article(**article) for article in articles if not article['headline'] in available_headlines]
        Article.objects.bulk_create(article_models)

        # Requirements
        available_requirements = Requirement.objects.all()
        available_requirement_texts = [r.text for r in available_requirements]
        r_models = [Requirement(**r) for r in requirements if not r['text'] in available_requirement_texts]
        Requirement.objects.bulk_create(r_models)

        # Criteria
        available_criteria = Criterion.objects.all()
        available_criteria_text = [c.text for c in available_criteria]
        c_models = [Criterion(text=c) for c in criteria if not c in available_criteria_text]        
        Criterion.objects.bulk_create(c_models)

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
            levels = programs[name]

            for level in levels:
                Level.objects.create(program=program, **level)


        # Add Course type and courses
        for course_type in field_of_study:
            c_type, _ = CourseType.objects.get_or_create(title=course_type)
            
            for title in field_of_study[course_type]:
                try:
                    Course.objects.get_or_create(title=title, course_type=c_type)
                except Exception as e:
                    print(e)

                
        for ins_type in inst_types:
            i_type = InstitutionType.objects.create(name=ins_type)
            
            for inst in inst_types[ins_type]:
                Institution.objects.create(institution_type=i_type, name=inst)

        print('Database populated successfully!!!')