import json
from .models import Patch, PatchOption, POField, PatchData

from django import forms
from .models import POField, PatchData

class DynamicPatchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        patch_options = kwargs.pop('patch_options', [])
        super(DynamicPatchForm, self).__init__(*args, **kwargs)
        
        field_types = {'Boolean': forms.BooleanField, 'Text': forms.CharField, 'Integer': forms.IntegerField, 'Selection': forms.ChoiceField}
        
        for patch_option in patch_options:
            fields = POField.objects.filter(patch_option=patch_option)
            for field in fields:
                initial_json_data = json.loads(field.initial_data)
                field_name = f'field_{field.id}'
                if 'data' in initial_json_data:
                    if isinstance(initial_json_data['data'], list):
                        default_data_json = json.loads(field.default_data)
                        if 'data' in default_data_json:
                            default=default_data_json['data']
                        else:
                            default=''
                        choices = [(choice, choice) for choice in initial_json_data['data']]
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
                            initial=default
                        )
                else:
                    self.fields[field_name] = field_types[field.field_type](
                        label=field.name,
                        required=False,
                        initial=''
                    )

    def save(self, patch):
        for field_name, field_value in self.cleaned_data.items():
            if field_name.startswith('field_'):
                field_id = field_name.split('_')[1]
                po_field = POField.objects.get(id=field_id)
                PatchData.objects.update_or_create(
                    patch=patch,
                    field=po_field,
                    defaults={'data': field_value}
                )
