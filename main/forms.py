from django import forms
from .models import Preference, Company, User


class PreferenceCreationForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['company']

    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.none()
        all_companies = Company.objects.values_list('name', 'id')
        selected_companies = Preference.objects.values_list('user', 'company').filter(user=user_id)
        companies = []
        for a_company in all_companies:
            found = False
            for s_company in selected_companies:
                s_id = s_company[1]
                a_id = a_company[1]
                if s_id == a_id:
                    found = True
                    break
                
            if not found:
                a_name = a_company[0]
                companies.append(a_name)
        query_comp = Company.objects.filter(name__in=companies)
        if query_comp:
            self.fields['company'].queryset = query_comp

