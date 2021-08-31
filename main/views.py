from django.views.generic import TemplateView, ListView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 

from .forms import *
from .filters import *


class ChangeLanguageView(TemplateView):
	template_name = 'main/change_language.html'


#######################################
def check_empty(value, dtype=None): 
	if value:
		if dtype:
			value = dtype(value)
	else:
		value = ''
	return value

class StoragePageView(ListView):
	template_name = 'main/storage.html'

	def get(self, request, *args, **kwargs):

		storage_name = check_empty(request.GET.get('storage_name'))

		storages = Storage.objects.filter(
			Q(storage_name__icontains=storage_name)).all()
		
		form  = StorageForm()
		data = {'form': form, 'storages': storages}
		return render(request, self.template_name, data)


	def post(self, request, *args, **kwargs):
		
		if 'pk' in request.POST:
			# delete
			pk = request.POST.get('pk')
			# print(f"\n\n {pk} \n\n")
			storage = Storage.objects.get(id=pk)
			if storage:
				storage.delete()
		else:
			# create
			form = StorageForm(request.POST)
			if form.is_valid():
				form.save()

		return HttpResponseRedirect(reverse('storages'))
		# return HttpResponse(str(form.is_valid()))


class DocPageView(TemplateView):
	template_name = 'main/document.html'

	def get(self, request, *args, **kwargs):
		doc_name = check_empty(request.GET.get('doc_name'))
		docs = Document.objects.filter(
			Q(doc_name__icontains=doc_name)).all()

		for doc in docs:
			in_use_instances = []
			free_instances = []

			docs_instances = DocsInstance.objects.filter(document=doc).all()
			for instance in docs_instances:
				in_use_instance = DocsInUse.objects.filter(doc_instance=instance).all()
				print(f"\n\n {instance} {in_use_instance}\n\n")
				if in_use_instance:
					in_use_instances += [inst for inst in in_use_instance]
				else:
					free_instances.append(instance)

			doc.instances = free_instances
			doc.instance_count = len(docs_instances)
			doc.in_use_count = len(in_use_instances)
			doc.docs_in_use = in_use_instances
			# print(f"\n\n [In use]: {doc} = {type(doc.in_use)} \n\n")
		# print(f"\n\n user_code = {} \n\n")
		form  = DocForm()
		data = {'form': form, 'docs': docs}
		return render(request, self.template_name, data)
	
	def post(self, request, *args, **kwargs):

		if 'deletedoc' in request.POST:
			pk = request.POST.get('pk')
			doc = Document.objects.get(id=pk)
			if doc:
				doc.delete()
		elif 'adddoc' in request.POST:
			doc_instances_storage = check_empty(request.POST.get('doc-instances-storage'))
			doc_instances_storage = doc_instances_storage.split(',')
			doc_name = check_empty(request.POST.get('doc_name'))
			cell_row = check_empty(request.POST.get('cell_row'), dtype=int)
			cell_column = check_empty(request.POST.get('cell_column'), dtype=int)
			storage_id = check_empty(request.POST.get('storage'))
			storage = Storage.objects.filter(id=storage_id).first()
			doc = Document(doc_name=doc_name, storage=storage, cell_row=cell_row, cell_column=cell_column)
			if doc:
				doc.save()
			for doc_instance_number in doc_instances_storage:
				docs_instance = DocsInstance(document=doc, unique_number=doc_instance_number)
				if docs_instance:
					docs_instance.save()
		elif 'switchdocinuse' in request.POST:
			instance_id = check_empty(request.POST.get('instance_id'))
			doc_description = check_empty(request.POST.get('doc_description'))
			doc_instance = DocsInstance.objects.filter(id=instance_id).first()
			doc_in_use = DocsInUse(doc_instance=doc_instance, who_use=doc_description)
			if doc_in_use:
				doc_in_use.save()
		elif 'takedocinuse' in request.POST:
			doc_in_use_id = check_empty(request.POST.get('doc_in_use_id'))
			docs_in_use = DocsInUse.objects.filter(id=doc_in_use_id).first()
			if docs_in_use:
				docs_in_use.delete()
			print(f"\n\n [takedocinuse]: {doc_in_use_id} {docs_in_use} \n\n")

		return HttpResponseRedirect(reverse('docs'))


class IndexPageView(TemplateView):
	template_name = 'main/index.html'

class AboutPageView(TemplateView):
	template_name = 'main/about.html'

#######################################
