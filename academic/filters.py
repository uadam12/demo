import django_filters as df
from django import forms
from crispy_forms.layout import Layout
from app.filter import FilterDataSet
from .models import Course, CourseType, Program, Level, Institution, InstitutionType


class SearchFilter(FilterDataSet):
    name = df.CharFilter(
        'name', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search by Name'
        })
    )

    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(self.search_field_with_btn('name'))
        return form

class InstitutionTypeFilter(SearchFilter):
    class Mete:
        model = InstitutionType
        fields = ['name']

class CourseTypeFilter(SearchFilter):
    name = df.CharFilter(
        'title', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search by Name'
        })
    )

    class Mete:
        model = CourseType
        fields = []

class ProgramFilter(SearchFilter):
    class Mete:
        model = Program
        fields = ['name']


class InstitutionFilter(FilterDataSet):
    class Mete:
        model = Institution
        fields = ('institution_type', 'name')

    name = df.CharFilter(
        'name', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search Institution'
        })
    )
    institution_type = df.ModelMultipleChoiceFilter(
        field_name = 'institution_type',
        queryset = InstitutionType.objects.all(),
        label = '', widget = forms.CheckboxSelectMultiple(attrs={
            'placeholder': 'Search Institution'
        })
    )
    
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'institution_type', 
            self.search_field_with_btn('name')
        )
        
        return form
    
class LevelFilter(FilterDataSet):
    class Mete:
        model = Level
        fields = ['name']
    
    name = df.CharFilter(
        'name', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search Institution'
        })
    )

    program = df.ModelMultipleChoiceFilter(
        field_name = 'program',
        queryset = Program.objects.all(),
        label = '', widget = forms.CheckboxSelectMultiple(attrs={
            'placeholder': 'Search Program'
        })
    )
    
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'program', 
            self.search_field_with_btn('name')
        )
        
        return form

class CourseFilter(CourseTypeFilter):
    class Mete:
        model = Course
        fields = []

    course_type = df.ModelMultipleChoiceFilter(
        field_name = 'course_type',
        queryset = CourseType.objects.all(),
        label = '', widget = forms.CheckboxSelectMultiple(attrs={
            'placeholder': 'Search Institution'
        })
    )
    
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'course_type', self.search_field_with_btn('name')
        )
        
        return form