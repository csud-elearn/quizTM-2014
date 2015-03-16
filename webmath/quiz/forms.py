from django import forms
    
class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        
        self.question = question
        
class CheckboxForm(QuestionForm):
    def __init__(self, queryset, *args, **kwargs):
        QuestionForm.__init__(self, *args, **kwargs)
        self.fields['answer'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=queryset, required=False)
    
    def get_type(self):
        return 0 #Indication pour le rendu dans le template

class RadioForm(QuestionForm):
    def __init__(self, queryset, *args, **kwargs):
        QuestionForm.__init__(self, *args, **kwargs)
        self.fields['answer'] = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=queryset, empty_label=None, required=False)
        
    def get_type(self):
        return 0 #Indication pour le rendu dans le template
    
class SelectForm(QuestionForm):
    def __init__(self, queryset, *args, **kwargs):
        QuestionForm.__init__(self, *args, **kwargs)
        self.fields['answer'] = forms.ModelChoiceField(widget=forms.Select(attrs={'class' : 'form-control'}), queryset=queryset, label="", required=False)
    
    def get_type(self):
        return 1 #Indication pour le rendu dans le template
    
class TextForm(QuestionForm):
    def __init__(self, *args, **kwargs):
        QuestionForm.__init__(self, *args, **kwargs)
        self.fields['answer'] = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), min_length=0, max_length=100, label="", required=False)
    
    def get_type(self):
        return 1 #Indication pour le rendu dans le template