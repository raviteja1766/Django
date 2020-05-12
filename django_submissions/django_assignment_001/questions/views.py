
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from questions.models import Question

def get_list_of_questions(request):
    string = request.GET.get('sort_by')
    list_of_questions=Question.objects.all()
    if string == 'asc':
        list_of_questions=Question.objects.order_by('text')
    elif string == 'desc':
        list_of_questions=Question.objects.order_by('-text')
    context={'list_of_questions':list_of_questions}
    return render(request,'get_list_of_questions.html',context)

def create_question(request):
    if request.method == 'GET':
        return render(request,'create_question_form.html')
    elif request.method == 'POST':
        question_text=request.POST.get('question')
        question_answer=request.POST.get('answer')
        if  len(question_text.strip()) and len(question_answer.strip()):
            question_obj=Question.objects.create(text=question_text,answer=question_answer)
            return render(request,'create_question_success.html')
        else:
            return render(request,'create_question_failure.html')

def get_question(request,question_id):
    question=Question.objects.get(id=question_id)
    return render(request,'each_question_form.html',{'question':question})
    
def update_question(request,question_id):
    if request.method == 'POST':
        question_text=request.POST.get('question')
        question_answer=request.POST.get('answer')
        if  len(question_text.strip())and len(question_answer.strip()):
            question_obj = Question.objects.get(id = question_id)
            question_obj.text=question_text
            question_obj.answer=question_answer
            question_obj.save()
            return render(request,'update_question_success.html')
        else:
            return render(request,'update_question_failure.html')
    
def delete_question(request,question_id):
        try:
            question=Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return render(request,'delete_question_failure.html')    
        question.delete()
        return render(request,'delete_question_success.html')
        

