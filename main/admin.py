from django.contrib import admin
from .models import *


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
	list_display = ('storage_name', 'cells_columns_count', 'cells_rows_count')

	class Meta:
		verbose_name = 'Хранилище'
		verbose_name_plural = 'Хранилища'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('doc_name', 'storage', 'cell_column', 'cell_row', 'created_at', )
	list_filter = ('doc_name', 'storage')

	class Meta:
		verbose_name = 'Документ'
		verbose_name_plural = 'Документы'


@admin.register(DocsInUse)
class DocsInUseAdmin(admin.ModelAdmin):
	list_display = ('doc_instance', 'who_use', 'created_at', )
	list_filter = ('doc_instance', 'who_use', 'created_at')

	class Meta:
		verbose_name = 'Документ на руках'
		verbose_name_plural = 'Документы на руках'

@admin.register(DocsInstance)
class DocsInstanceAdmin(admin.ModelAdmin):
	list_display = ('document', 'unique_number', 'created_at', )
	list_filter = ('document', 'unique_number', 'created_at')