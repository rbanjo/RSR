# -*- coding: utf-8 -*-
from .models import *
#import docx2txt

# Create your views here.
#=======
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from django.template import loader

from .models import *
from .models import Document
from .forms import DocumentForm
from .filters import PersonFilter
from django.db.models import Q
from django.views.generic.edit import FormView

from django.forms import ModelForm

from .models import *
from .forms import DocumentForm

from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .filters import *
###Search #
from django.db.models import Q

###TESTING OCR
from PIL import Image
from wand.image import Image as IMG
import pytesseract
from django.template.context_processors import request
import re
# import textract
###

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def main(request):
    return render(request, 'main.html')

def get_string(name):
    img=Image.open(name)
    utf8_text = pytesseract.image_to_string(img)
    utf8_text = str(utf8_text.encode('ascii', 'ignore'))
    return utf8_text


class DocFileView(FormView):
    form_class = DocumentForm
    template_name = 'index.HTML'
    success_url = reverse_lazy('RSR:uploaddoc')

    def post(self, request, *args, **kwargs):
        form_class=self.form_class
        form=self.get_form(form_class)
        files=request.FILES.getlist('docfile')
        if form.is_valid():
            for counter in range(len(files)):
                temp_doc=Document(docfile=files[counter])
                temp_doc.firstname = request.POST.getlist('firstname')[counter]
                temp_doc.lastname = request.POST.getlist('lastname')[counter]
                temp_doc.type = request.POST.getlist('type')[counter]

                temp_doc.save()
                if ".doc" in temp_doc.docfile.path:
                    print('')
                    #print (temp_doc.docfile.path)
                    #temp_doc.docfile.wordstr = parse_word_file(temp_doc.docfile.path)
                    #print (temp_doc.docfile.wordstr)
                    #temp_doc.save(update_fields=['wordstr'])
                else:

                    # temp_doc.docfile.wordstr = textract.process(temp_doc.docfile.path)
                    path = os.path.join(settings.MEDIA_ROOT, temp_doc.docfile.name)
                    # if len(temp_doc.docfile.wordstr) < 50:
                    img = IMG(filename=path, resolution=200)
                    # save in temp folder
                    temp_path = os.path.join(settings.MEDIA_ROOT, 'temp/temp')
                    images = img.sequence
                    utf8_text = str
                    for i in range(len(images)):
                        IMG(images[i]).save(filename=temp_path + str(i) + ".jpg")
                    for i in range(len(images)):
                        if i == 0:
                            utf8_text = get_string(os.path.normpath(temp_path + str(i) + '.jpg'))
                            # delete from temp folder
                            os.remove(temp_path + str(i) + '.jpg')
                        else:
                            utf8_text += "\n\n"
                            utf8_text += get_string(os.path.normpath(temp_path + str(i) + '.jpg'))
                            # delete from temp folder
                            os.remove(temp_path + str(i) + '.jpg')

                    temp_doc.docfile.wordstr = utf8_text
                    # endif - do not uncomment
                    Document.objects.filter(pk=temp_doc.id).update(wordstr=utf8_text)
                    #print (Document.objects.get(pk=temp_doc.id).wordstr)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

''''@login_required
def uploaddoc(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            temp_doc = Document(docfile=request.FILES.getlist('docfile'))

            #temp_doc.firstname = Document(docfile=request.POST.get('firstname'))
            #temp_doc.lastname = Document(docfile=request.POST.get('lastname'))
            #temp_doc.type = Document(docfile=request.POST.get('type'))
            temp_doc.firstname = request.POST['firstname']
            temp_doc.lastname = request.POST['lastname']
            temp_doc.type = request.POST['type']

            temp_doc.save()

            if ".doc" in temp_doc.docfile.path:
                print (temp_doc.docfile.path)
                temp_doc.docfile.wordstr = parse_word_file(temp_doc.docfile.path)
                print (temp_doc.docfile.wordstr)
                temp_doc.save(update_fields=['wordstr'])
            else:

                # temp_doc.docfile.wordstr = textract.process(temp_doc.docfile.path)
                path = os.path.join(settings.MEDIA_ROOT, temp_doc.docfile.name)
                # if len(temp_doc.docfile.wordstr) < 50:
                img=IMG(filename=path,resolution=200)
                # save in temp folder
                temp_path = os.path.join(settings.MEDIA_ROOT,'temp/temp')
                images=img.sequence
                utf8_text = str
                for i in range(len(images)):
                    IMG(images[i]).save(filename=temp_path+str(i)+".jpg")
                for i in range(len(images)):
                    if i==0:
                        utf8_text = get_string(os.path.normpath(temp_path+str(i)+'.jpg'))
                        # delete from temp folder
                        os.remove(temp_path + str(i) + '.jpg')
                    else:
                        utf8_text+="\n\n"
                        utf8_text+=get_string(os.path.normpath(temp_path+str(i)+'.jpg'))
                        # delete from temp folder
                        os.remove(temp_path+str(i)+'.jpg')

                temp_doc.docfile.wordstr = utf8_text
                #endif - do not uncomment
                Document.objects.filter(pk=temp_doc.id).update(wordstr=utf8_text)
                print (Document.objects.get(pk=temp_doc.id).wordstr)
            return HttpResponseRedirect(reverse('RSR:uploaddoc'))
    else:
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request,'index.html',{'documents': documents, 'form': form})'''



def user_acc_cont(request):
    return render(request, 'acc_cont.html')


def uploadlist(request):
    documents = Document.objects.all()

    context = {'documents': documents}
    return render(request, 'uploadlist.html', context)


def listdelete(request, template_name='uploadlist.html'):
    docId = request.POST.get('docfile', None)
    documents = get_object_or_404(Document, pk=docId)
    if request.method == 'POST':
        documents.delete()
        return HttpResponseRedirect(reverse('uploadlist'))

    return render(request, template_name, {'object': documents})


# OCR TEAM

@login_required
def ocr (request):
    docID=request.POST.get('docfileID', None)
    documents=get_object_or_404(Document,pk=docID)
    var=str
    if documents.wordstr in [None,""]:
        if os.path.exists(str(settings.MEDIA_ROOT)+str(documents)):
            status=True
            file_path=str(settings.MEDIA_ROOT)+str(documents)
            img=IMG(filename=file_path,resolution=200)
            images=img.sequence
            for i in range(len(images)):
                IMG(images[i]).save(filename=str(settings.MEDIA_ROOT)+'/temp/'+str(i)+'.jpg')
            for i in range(len(images)):
                if i == 0:
                    var=get_string(str(settings.MEDIA_ROOT)+'/temp/'+str(i)+'.jpg')
                    os.remove(str(settings.MEDIA_ROOT)+'/temp/'+str(i)+'.jpg')
                else:
                    var+="\n\n"
                    var+=get_string(str(settings.MEDIA_ROOT)+'/temp/'+str(i)+'.jpg')
                    os.remove(str(settings.MEDIA_ROOT)+'/temp/'+str(i)+'.jpg')
            Document.objects.filter(pk=docID).update(wordstr=var)

        else:
            status=False
    else:
        status=True
        var=str(documents.wordstr)
    context={'var':var, 'status':status}
    return render(request, 'ocr.html',context)

@login_required
def parsing(request):
    return render(request, 'parsing.html')

@login_required
def search(request):
    query_set = Person.objects.all()
    query = request.GET.get("q")
    num = 0
    if query:
        query_set=query_set.filter(Name__icontains=query)
    # The filtered query_set is then put through more filters from django
    personFilter = PersonFilter(request.GET, query_set)
    return render(request, 'SearchExport/search.html', {'personFilter': personFilter, 'num':num})

#gets the name of the person from the text extracted: Abhishek Shrinivasan 07/20/17
def getName(string):
    lines=string.split('\n')
    keywords=['skills','technical','experience','personal','objective','manager']
    i=1
    for line in lines:
        words=line.split(' ')
        pointer=True
        if(len(words)>1 and len(words)<=5):
            for word in words:
                if str(word).lower() in keywords:
                   pointer=False
                   break
                elif word=='' or word.find("@")>-1 :
                    pointer=False
                    break
                elif any(i.isdigit() for i in word):
                    pointer = False
                    break
            if pointer==True:
                name=""
                for word in words:
                    name+=word
                    name+=" "
                return name
        else:
            pointer=False
        if pointer==True:
            break
        i+=1
        if i>50:
            return None

def getEmail(string):

    #print(str(string))
    match = re.search('([\w.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', str(string))

    if match is None:
        return 'No Email provided.'
    else:
        return match.group(0)
    # lines=string.split("\n")
    # email_suffix=['.com','.edu','.net']
    # for line in lines:
    #     words=line.split(' ')
    #     for word in words:
    #         if word.find('@')!=-1:
    #             return word
    #         for suffix in email_suffix:
    #             if word.find(suffix)!=-1:
    #                 return word

def getPhoneNumber(string):
    if re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[\-\.\s]??\d{4})', string):
        phones=re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[\-\.\s]??\d{4})', string)
    elif re.findall(r'.[\d]{1,3}\s[\d]{3}-[\d]{3}-[\d]{4}', string):
        phones=re.findall(r'.[\d]{1,3}\s[\d]{3}-[\d]{3}-[\d]{4}', string)
    elif re.findall(r'.[\d]{1,3}\s[\d]{3}\s[\d]{3}\s[\d]{4}', string):
        phones=re.findall(r'.[\d]{1,3}\s[\d]{3}\s[\d]{3}\s[\d]{4}', string)
    elif re.findall(r'.[\d]{1,3}\s[\d]{3}\.[\d]{3}\.[\d]{4}', string):
        phones = re.findall(r'.[\d]{1,3}\s[\d]{3}\.[\d]{3}\.[\d]{4}', string)
    elif re.findall(r'.[\d]{1,3}\s[(][\d]{3}[)]\s[\d]{3}\.[\d]{4}', string):
        phones=re.findall(r'.[\d]{1,3}\s[(][\d]{3}[)]\s[\d]{3}\.[\d]{4}', string)
    elif re.findall(r'.[\d]{1,3}\s[(][\d]{3}[)]\s[\d]{3}\s[\d]{4}', string):
        phones=re.findall(r'.[\d]{1,3}\s[(][\d]{3}[)]\s[\d]{3}\s[\d]{4}', string)
    elif re.findall(r'.[\d]{1,3}\s[(][\d]{3}[)]\s[\d]{3}-[\d]{4}', string):
        phones=re.findall(r'.[\d]{1,3}\s[(][\d]{3}[)]\s[\d]{3}-[\d]{4}', string)
    elif re.findall(r'.[\d]{1,3}[\d]{3}[\d]{3}[\d]{4}', string):
        phones=re.findall(r'.[\d]{1,3}[\d]{3}[\d]{3}[\d]{4}', string)
    else:
        phones=""
    if phones:
        for phonenumber in phones:
            print phonenumber







@login_required
def OCRSearch(request):
    doc_objects=Document.objects.all()
    search_item=str(request.GET.get('search'))
    print(search_item)
    result_location=[]
    names = {}
    for document in doc_objects:
        doc_string=str(document.wordstr)
        if search_item.lower() in doc_string.lower():
            result_location.append(document)
            print(document.docfile.name) # docfile.name?
            name=getName(doc_string)
            email=getEmail(doc_string)
            getPhoneNumber(doc_string)
            print(email)
            if name is not None:
                name=name.lower().title()
                names[name]=email
    context={'results': result_location,'names':names}

    return render(request, 'OCRSearch.html',context)

@login_required
def detail(request,pk):
    # Get the current person object using pk or id
    person = get_object_or_404(Person,pk=pk)
    related_obj_list=[]
    # This is the related_set names, I add the personto and _set part to it later on for preference purposes only
    relatedNames = ['school','course', 'certificate', 'side', 'skills', 'language'
        , 'clearence', 'company', 'awards', 'clubshobbies', 'volunteering']
    # This is the foreign key reference to the models
    modelReferences = ['SchoolID', 'CourseID', 'CertID', 'SideID', 'SkillsID', 'LangID', 'ClearenceLevel',
                       'CompanyName', 'AwardName', 'CHName', 'VolunName']
    # Im adding major beforehand to the list since it's a special case
    for major in person.persontoschool_set.all():
        related_obj_list.append('Major: '+ str(major.MajorID))
    # Loops through every model
    position=0
    for related in relatedNames:
        # Get the related set of each model
        # The default related set is the name of intermediary table, lowercased + _set
        # The related set is used to reverse foreign keys and you access it by currentmodel.related_set where
        # the related_set is where the foreign key to current model stems from
        string = 'personto'+related+'_set'
        related_obj = eval('person.'+string)
        # Related_obj cannot be iterated unless put in a query set so I put in a query set using all()
        related_obj = related_obj.all()
        # There should only be 1 object in this query set
        for item in related_obj:
            # I want to do something grab the exact field of the item so I use getattr
            item=getattr(item,modelReferences[position])
            # Finally I add the string I want to be displayed into related_obj_list which I will iterate through in
            # details template
            related_obj_list.append(related.capitalize()+': ' +str(item))
        position+=1
    return render(request, 'SearchExport/detail.html', {'person':person, 'list':related_obj_list})



@login_required
def user_acc_cont (request):
    return render(request, 'acc_cont.html')

@login_required
def export(request):
    return render (request, 'export.html')

@login_required
def linkanalysis(request):
    return render(request, 'linkanalysis.html')

@login_required
def uploadlist (request):
   # documents = Document.objects.filter(firstname = Document.firstname).filter(lastname = Document.lastname).filter(type = Document.type).filter(docfile = Document.docfile)
    documents = UploadListFilter(request.GET,queryset = Document.objects.all())
    #documents = Document.objects.all()
    context ={'documents':documents}
    return render(request,'uploadlist.html',context)

def listdelete(request, template_name='uploadlist.html'):
    docId = request.POST.get('docfile', None)
    documents = get_object_or_404(Document, pk=docId)
    if request.method == 'POST':
        documents.delete()
        return HttpResponseRedirect(reverse('RSR:uploadlist'))

    return render(request, template_name, {'object': documents})


'''def parse_word_file(filepath):
	parsed_string = docx2txt.process(filepath)
	return parsed_string'''
