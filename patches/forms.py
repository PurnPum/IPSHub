import json

from django import forms
from .models import POField, PatchData

class DynamicPatchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        patch_options = kwargs.pop('patch_options', [])
        patch = kwargs.pop('patch', [])
        super(DynamicPatchForm, self).__init__(*args, **kwargs)
        
        field_types = {
            'Boolean': forms.BooleanField,
            'Text': forms.CharField,
            'Integer': forms.IntegerField,
            'Selection': forms.ChoiceField
            }
        
        for patch_option in patch_options:
            default=None
            fields = POField.objects.filter(patch_option=patch_option)
            if patch is not None:
                patchDatas = PatchData.objects.filter(patch=patch)
            for field in fields:
                initial_json_data = json.loads(field.initial_data)
                field_name = f'field_{field.id}'
                if patch is not None:
                    try:
                        default = patchDatas.get(field=field).data
                    except:
                        default = None
                if 'data' in initial_json_data:
                    if isinstance(initial_json_data['data'], list):
                        choices = [(choice, choice) for choice in initial_json_data['data']]
                        if default is None:
                            default_data_json = json.loads(field.default_data)
                            if 'data' in default_data_json:
                                default=default_data_json['data']
                            else:
                                default=''
                        self.fields[field_name] = field_types['Selection'](
                            label=field.name,
                            choices=choices,
                            required=False,
                            initial=default
                        )
                else:
                    self.fields[field_name] = field_types[field.field_type](
                        label=field.name,
                        required=False,
                        initial=''
                    )

    def save(self, patch, commit=True):
        saved_objects = []
        
        for field_name, field_value in self.cleaned_data.items():
            if field_name.startswith('field_'):
                field_id = field_name.split('_')[1]
                po_field = POField.objects.get(id=field_id)
                if field_value != json.loads(po_field.default_data)['data']: # If the value is the same as the default value, dont save it.
                    patch_data = PatchData(
                        patch=patch,
                        field=po_field,
                        data=field_value
                    )
                    saved_objects.append(patch_data)
        
        if len(saved_objects) == 0:
            raise(forms.ValidationError('All fields have their default value'))
        
        if commit:
            for obj in saved_objects:
                obj.save()
        
        return saved_objects

    def patchless(self):
        return self.save(None,commit=False)
    
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for something...',
            }
        )
    )