from django import forms

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border mt-4'

class RecommendationForm(forms.Form):
    titles = forms.CharField(label="Type your title here :", 
                                max_length=100, 
                                required=True, 
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': 'Dogville', 
                                        'class': INPUT_CLASSES}))
    
class InferenceForm(forms.Form):
    description = forms.CharField(label="Type the description of the movie you would want to watch :", 
                                max_length=128, 
                                required=True, 
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': 'Type your description here ...', 
                                        'class': INPUT_CLASSES}))