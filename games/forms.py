from django import forms

class CreateGameForm(forms.Form):
    opponent_username = forms.CharField(label='Opponent', max_length=100)

    def __init__(self, *args, **kwargs):
        super(CreateGameForm, self).__init__(*args, **kwargs)
        self.fields['opponent_username'].widget.attrs = {
            'class': 'form-control'
        }


class AttackForm(forms.Form):
    X_CHOICES = (
        (x, chr(x + ord('A'))) 
        for x in range(0,10)
    )
    Y_CHOICES = (
        (y, str(y)) 
        for y in range(0,10)
    )
    target_x = forms.ChoiceField(choices=X_CHOICES)
    target_y = forms.ChoiceField(choices=Y_CHOICES)
    game_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(AttackForm, self).__init__(*args, **kwargs)
        self.fields['target_x'].widget.attrs = {
            'class': 'form-control col-md-1'
        }
        self.fields['target_y'].widget.attrs = {
            'class': 'form-control col-md-1'
        }