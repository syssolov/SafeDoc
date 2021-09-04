from django.views.generic import TemplateView, ListView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 
from copy import deepcopy

from .forms import *
from .filters import *

import json


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
				# print(f"\n\n {instance} {in_use_instance}\n\n")
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
				doc_instances = DocsInstance.objects.filter(document=doc).all()
				logs = []
				for doc_instance in doc_instances:
					log = History(
						action = 2,
						doc_name = doc_instance.document.doc_name,
						doc_id = doc_instance.document.id,
						doc_instance_unique_number = doc_instance.unique_number
					)
					logs.append(log)
				try:
					doc.delete()
					# <logging>
					for log in logs:
						log.save()
					# </logging>
				except Exception as exc:
					print(f"{exc}")

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
						# <logging>
						log = History(
							action = 1,
							doc_name = doc.doc_name,
							doc_id = doc.id,
							doc_instance_unique_number = docs_instance.unique_number
						)
						log.save()
						# </logging>

		elif 'switchdocinuse' in request.POST:
			instance_id = check_empty(request.POST.get('instance_id'))
			doc_description = check_empty(request.POST.get('doc_description'))
			doc_instance = DocsInstance.objects.filter(id=instance_id).first()
			doc_in_use = DocsInUse(doc_instance=doc_instance, who_use=doc_description)
			if doc_in_use:
				doc_in_use.save()

				# <logging>
				log = History(
					action = 4,
					doc_name = doc_instance.document.doc_name,
					doc_id = doc_instance.document.id,
					doc_instance_unique_number = doc_instance.unique_number,
					who_use = doc_in_use.who_use
				)
				log.save()
				# </logging>

		elif 'takedocinuse' in request.POST:
			doc_in_use_id = check_empty(request.POST.get('doc_in_use_id'))
			doc_in_use = DocsInUse.objects.filter(id=doc_in_use_id).first()
			if doc_in_use:
				doc_in_use_copy = deepcopy(doc_in_use) # запись текущего состояния
				doc_instance = doc_in_use_copy.doc_instance # 	           объекта

				doc_in_use.delete()

				# <logging>
				log = History(
					action = 5,
					doc_name = doc_instance.document.doc_name,
					doc_id = doc_instance.document.id,
					doc_instance_unique_number = doc_instance.unique_number,
					who_use = doc_in_use_copy.who_use
				)
				log.save()
				# </logging>

		return HttpResponseRedirect(reverse('docs'))


class IndexPageView(TemplateView):
	template_name = 'main/index.html'


class AboutPageView(TemplateView):
	template_name = 'main/about.html'


class HistoryPageView(TemplateView):
	template_name = 'main/history.html'

	def post(self, request, *args, **kwargs):
		search_query = check_empty(request.POST.get('search_query'))
		print(f"\n\n request.POST={request.POST} \n\n")
		# search_query = '5668468'
		history = History.objects.filter(
			Q(doc_name__icontains=search_query) |\
			Q(doc_instance_unique_number__icontains=search_query)).all()

		
		data = {}
		for log in history:
			if log.doc_id not in data:
				data[log.doc_id] = {'doc_name': log.doc_name, 'instances': {}}
			if log.doc_instance_unique_number not in data[log.doc_id]['instances']:
				data[log.doc_id]['instances'][log.doc_instance_unique_number] = []
			data[log.doc_id]['instances'][log.doc_instance_unique_number].append(
				{
					'doc_id': log.doc_id,
					'doc_name': log.doc_name,
					'action': log.action,
					'who_use': log.who_use,
					'created_at': log.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
					'description': log.description,
				}
			)

		print(f"\n\n{data}\n\n")

		return HttpResponse( json.dumps(data, ensure_ascii=False) )

		# return HttpResponse( json.dumps( data ) )
#######################################
