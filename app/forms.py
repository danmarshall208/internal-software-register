from django import forms
from .models import Tool, DependencyTag, BusinessTag, Feedback
from django.core.validators import MaxValueValidator, MinValueValidator

TRUE_FALSE_CHOICES = (
    (True, "Yes"),
    (False, "No")
)

YEAR_CHOICES = []
for year in range(2000, 2019):
    YEAR_CHOICES.append((year, year))


class ToolForm(forms.ModelForm):
    active = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, initial=True)
    restricted_access = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, initial=False)
    year_created = forms.IntegerField(validators=[MaxValueValidator(3000), MinValueValidator(1)])

    class Meta:
        model = Tool
        exclude = ['owner', 'created_by']
        labels = {
            'location': 'Tool location',
            'restricted_access': 'Restricted access?',
            'dependency_tags': 'Dependencies',
            'business_tags': 'Tags',
            'active': 'Is being actively used right now?',
            'future_plans': 'Future plans for tool',
        }
        field_classes = {
            'active': forms.ChoiceField,
        }


class SearchForm(forms.Form):
    text_search = forms.CharField(required=False, validators=[])
    tag_search = forms.CharField(required=False, validators=[])

    def clean_tag_search(self):
        data = self.cleaned_data['tag_search']
        print(data)
        tags = list(filter(None, self.cleaned_data['tag_search'].split(',')))
        tag_list = BusinessTag.objects.all()
        tag_names = [tag.name for tag in tag_list]
        for tag in tags:
            print(tag)
            if tag not in tag_names:
                print(tag)
                raise forms.ValidationError("Tag does not exist")

        return self.data['tag_search']


class DependencyTagForm(forms.ModelForm):
    class Meta:
        model = DependencyTag
        exclude = []
        labels = {
            'name': 'Dependency Tag'
        }


class BusinessTagForm(forms.ModelForm):
    class Meta:
        model = BusinessTag
        exclude = []
        labels = {
            'name': 'Tag'
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['sesa']
        labels = {
            'text': 'Feedback'
        }
