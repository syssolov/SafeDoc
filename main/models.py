from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class Storage(models.Model):
	storage_name = models.CharField(max_length=500, null=False, unique=True)
	cells_columns_count = models.IntegerField()
	cells_rows_count = models.IntegerField()

	def __str__(self):
		return f"{self.storage_name}"


class Document(models.Model):
	doc_name = models.CharField(max_length=500, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	storage = models.ForeignKey(Storage, null=True, on_delete=models.CASCADE)
	cell_row = models.IntegerField()
	cell_column = models.IntegerField()

	# number = models.IntegerField()

	def __str__(self):
		return f"{self.doc_name}"

	def save(self, *args, **kwargs):
		# if not self.number>0:
		# 	# raise ValidationError(('Количество экземпляров документа должно быть больше нуля!'))
		# 	return 
		if not (self.cell_column>0 and self.cell_column<=self.storage.cells_columns_count):
			# raise ValidationError(('Ошибочка! self.cell_column<=self.storage.cells_columns_count)'))
			return 
		if not (self.cell_row>0 and self.cell_row<=self.storage.cells_rows_count):
			# raise ValidationError(('Ошибочка! not (self.cell_row>0 and self.cell_column<=self.storage.cells_rows_count)'))
			return 

		super(Document, self).save(*args, **kwargs)


class DocsInstance(models.Model):
	document = models.ForeignKey(Document, on_delete=models.CASCADE, )
	unique_number = models.CharField(max_length=500, null=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.unique_number}"


class DocsInUse(models.Model):
	doc_instance = models.ForeignKey(DocsInstance, default=None, on_delete=models.CASCADE, )
	who_use = models.CharField(max_length=500, null=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.doc_instance}"

	# def save(self, *args, **kwargs):
	# 	print("\n\n")
	# 	print("---->", self.document.number, DocsInUse.objects.filter(document=self.document).count())
	# 	print("\n\n")
	# 	if (DocsInUse.objects.filter(document=self.document).count() == self.document.number):
	# 		# return 
	# 		raise ValidationError("Больше не осталось экземпляров этого документа!")
	# 	# if not (self.cell_column>0 and self.cell_column<=self.storage.cells_columns_count):
	# 	# 	raise ValidationError(('Ошибочка! self.cell_column<=self.storage.cells_columns_count)'))
	# 	# if not (self.cell_row>0 and self.cell_row<=self.storage.cells_rows_count):
	# 	# 	raise ValidationError(('Ошибочка! not (self.cell_row>0 and self.cell_column<=self.storage.cells_rows_count)'))

	# 	super(DocsInUse, self).save(*args, **kwargs)

from django.utils import timezone

def defaul_time():
	return timezone.now() + timezone.timedelta(hours=6)

class History(models.Model):
	ACTIONS = [
		(1, ("Создан")),
		(2, ("Удален")),
		(3, ("Изменен")),
		(4, ("Выдан")),
		(5, ("Принят")),
	]

	action = models.IntegerField(choices=ACTIONS)
	doc_name = models.CharField(max_length=500, null=False)
	doc_id = models.IntegerField(null=False)
	doc_instance_unique_number = models.CharField(max_length=500, null=True, blank=True)
	who_use = models.CharField(max_length=500, null=True, blank=True)
	description = models.CharField(max_length=1200, null=True, blank=True)
	created_at = models.DateTimeField(default=defaul_time)

	def __str__(self):
		return f"{self.doc_name}"

	class Meta:
		ordering = ('-doc_id', )

