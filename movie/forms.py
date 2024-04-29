from django import forms
from .models import Movies, Main_Actor, Director, Ranked

class CreateAndRateMovieForm(forms.ModelForm):
    rating = forms.IntegerField(label='Rating', min_value=0, max_value=10)

    class Meta:
        model = Movies
        fields = ['title', 'release_year', 'duration', 'main_actor', 'director']


class EditMovieForm(forms.Form):
    def __init__(self, *args, **kwargs):
        movies = kwargs.pop('movies')
        super(EditMovieForm, self).__init__(*args, **kwargs)
        self.fields['movie'] = forms.ModelChoiceField(queryset=movies, empty_label="")
        self.fields['title'] = forms.CharField(max_length=255)
        self.fields['release_year'] = forms.IntegerField()
        self.fields['duration'] = forms.IntegerField()
        self.fields['main_actor'] = forms.ModelChoiceField(queryset=Main_Actor.objects.all())
        self.fields['director'] = forms.ModelChoiceField(queryset=Director.objects.all())
        self.fields['rating'] = forms.IntegerField()
