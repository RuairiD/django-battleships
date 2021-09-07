from django import forms
from django.core.exceptions import ValidationError

class CreateGameForm(forms.Form):

    def __init__(self, *args, **kwargs):
        max_players = kwargs.pop('max_players')
        super(CreateGameForm, self).__init__(*args, **kwargs)
        for i in range(0, max_players):
            field_name = 'opponent_username_{}'.format(i)
            self.fields[field_name] = forms.CharField(
                label='Opponent {}'.format(i+1),
                max_length=100
            )
            self.fields[field_name].widget.attrs = {
                'class': 'form-control'
            }
            # Minimum of one player required
            self.fields[field_name].required = (i == 0)


class AttackForm(forms.Form):

    X_CHOICES = (
        (x, chr(x + ord('A')))
        for x in range(0, 10)
    )
    Y_CHOICES = (
        (y, str(y))
        for y in range(0, 10)
    )

    # Either target_x and target_y...
    target_x = forms.ChoiceField(choices=X_CHOICES,
            required=False)
    target_y = forms.ChoiceField(choices=Y_CHOICES,
            required=False)

    # ...or target.
    target = forms.CharField(max_length=2,
            required=False)


    def clean(self):

        super(AttackForm, self).clean()

        has_xy = 'target_x' and 'target_y' in self.cleaned_data
        has_target = 'target' in self.cleaned_data

        if has_xy != has_target:
            raise ValidationError("You must pass either target_x and target_y, "
                    "or target.")

        if has_target:
            target = self.cleaned_data['target'].upper()

            if len(target)!=2:
                raise ValidationError("target must be two characters long, "
                        "e.g. 'A1'.")

            self.cleaned_data['target_x'] = ord(target[0]) - ord('A')
            self.cleaned_data['target_y'] = ord(target[1]) - ord('0')


    def __init__(self, *args, **kwargs):
        other_teams = kwargs.pop('other_teams')
        super(AttackForm, self).__init__(*args, **kwargs)
        self.fields['target_x'].widget.attrs = {
            'class': 'form-control col-md-1'
        }
        self.fields['target_y'].widget.attrs = {
            'class': 'form-control col-md-1'
        }
        self.fields['target_team'] = forms.ChoiceField(
            choices=(
                (team.id, team.player.user.username)
                for team in other_teams
            )
        )
        self.fields['target_team'].widget.attrs = {
            'class': 'form-control'
        }
