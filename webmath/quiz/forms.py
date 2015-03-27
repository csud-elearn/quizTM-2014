from django import forms
    
class QuestionForm(forms.Form):
    """
    Classe abstraite dont héritent tous les formulaires destinés à la résolution
    des quiz. Seul l'attribut ``question`` est défini. Il correspond à la référence
    de la question dans la base de données et permet d'afficher facilement des informations
    sur la question depuis le template.
    """
    def __init__(self, question, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        
        self.question = question
        
class CheckboxForm(QuestionForm):
    """
    Formulaire Django personnalisé correspondant à une question à choix multiples
    pouvant admettre plusieurs réponses correctes.
    
    Le type de champ de formulaire utilisé est un ``ModelMultipleChoiceField``. Ce champ permet
    de sélectionner plusieurs entrées d'une table de la base de données par l'intermédiaire
    de cases à cocher. Ici, il s'agit
    de la table :py:class`models.QcmChoice`.
    
    L'argument ``queryset`` permet de définir les choix qui seront affichés, il s'agit
    d'une liste d'entrées de la table :py:class`models.QcmChoice`.
    """
    def __init__(self, queryset, *args, **kwargs):
        QuestionForm.__init__(self, *args, **kwargs)
        self.fields['answer'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=queryset,
            required=False
        )
    
    def get_type(self):
        """
        Retourne ``1`` pour donner une indication sur la manière d'afficher 
        la question dans le template
        """
        return 1 #Indication pour le rendu dans le template

class RadioForm(QuestionForm):
    """
    Formulaire Django personnalisé correspondant à une question à choix multiples
    avec une seule réponse correcte.
    
    Ici, on utilise un champ de formulaire ``ModelChoiceField``. Il s'agit du même principe
    que pour :py:class:`CheckboxForm` sauf qu'un seul choix peut être sélectionné et
    que le formulaire est affiché en HTML sous forme de boutons radio.
    """
    def __init__(self, queryset, *args, **kwargs):
        QuestionForm.__init__(self, *args, **kwargs)
        self.fields['answer'] = forms.ModelChoiceField(
            widget=forms.RadioSelect,
            queryset=queryset,
            empty_label=None,
            required=False
        )
        
    def get_type(self):
        """
        Retourne ``1`` pour donner une indication sur la manière d'afficher 
        la question dans le template
        """
        return 1 #Indication pour le rendu dans le template
    
class TextForm(QuestionForm):
    """
    Formulaire Django personnalisé destiné à l'affichage des questions à réponse courte.
    
    Un ``CharField`` constitue l'unique champ de ce formulaire. Il s'agit simplement
    d'un champ de texte basique dans lequel l'étudiant peut écrire sa réponse.
    """
    def __init__(self, *args, **kwargs):
        QuestionForm.__init__(self, *args, **kwargs)
        self.fields['answer'] = forms.CharField(
            widget=forms.TextInput(attrs={'class' : 'form-control'}),
            min_length=0,
            max_length=100,
            label="",
            required=False
        )
    
    def get_type(self):
        """
        Retourne ``0`` pour donner une indication sur la manière d'afficher 
        la question dans le template
        """
        return 0 #Indication pour le rendu dans le template