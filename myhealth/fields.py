from .models import Consultation, Medication
from django import forms

class HealthForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Consultation
        fields = ['date','title','doctor', 'location','specialism','upsurge','description']
		
def get_absolute_url(self):
        return reverse('consultatie_detail', kwargs={'pk': self.pk})
		
class MedicationForm(forms.ModelForm):

    class Meta:
        model = Medication
        fields = ['start_date','end_date','medicatie','aantal_ochtend', 'aantal_avond','pijn','opmerking','rechtervoet','linkervoet','rechterhand','linkerhand','rug']
		