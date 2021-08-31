from .models import *
from django.forms import ModelForm, TextInput, NumberInput, Select


class StorageForm(ModelForm):
	class Meta:
		model = Storage
		fields = ('storage_name', 'cells_columns_count', 'cells_rows_count', )

		widgets = {
			"storage_name": TextInput(attrs={
				"class": "form-control",
				"placeholder": "Наименование хранилища"
			}),
			"cells_rows_count": NumberInput(attrs={
				"class": "form-control",
				"placeholder": "Количество полок"
			}),
			"cells_columns_count": NumberInput(attrs={
				"class": "form-control",
				"placeholder": "Количество сейфов на полке"
			})
		}

class DocForm(ModelForm):
	class Meta:
		model = Document
		fields = ('doc_name', 'storage', 'cell_row', 'cell_column', )


		# storage.widget.attrs.update({'class': 'form-control'})

		widgets = {
			"doc_name": TextInput(attrs={
				"class": "form-control",
				"placeholder": "Название документа"
			}),
			"storage": Select(attrs={
				"class": "form-control",
				"placeholder": "Наименование хранилища"
			}),
			"cell_row": NumberInput(attrs={
				"class": "form-control",
				"placeholder": "Номер полки"
			}),
			"cell_column": NumberInput(attrs={
				"class": "form-control",
				"placeholder": "Номер сейфа"
			}),
		}

