from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from quizapp.views import *
from quizapp.models import *
from quizapp.forms import AddQuizForm, AddQuestionForm, EditQuestionForm

# Create your views here.

@login_required(login_url='login')
def admin_dash(request):
    quizzes = Quizzes.objects.all().order_by('-id')
    return render(request, 'admin/admin_dashboard.html', {'quizzes': quizzes})

@login_required(login_url='login')
def add_quiz(request):
    if request.method == 'POST':
        form = AddQuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz added successfully.')
            return redirect('admin_dash')
    else:
        form = AddQuizForm()
    return render(request, 'admin/add_quiz.html', {'form': form})

@login_required(login_url='login')
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)

    if request.method == 'POST':
        form = AddQuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, f'{quiz.name} has been successfully updated.')
            return redirect('admin_dash')  
    else:
        form = AddQuizForm(instance=quiz)

    return render(request, 'admin/edit_quiz.html', {'form': form, 'quiz': quiz})

@login_required(login_url='login')
def delete_quiz(request, quiz_id):
    try:
        quiz = get_object_or_404(Quizzes, pk=quiz_id)
        name = quiz.name
        quiz.delete()
        messages.success(request, f'{name} deleted successfully.')
        return redirect('admin_dash')
    except:
        messages.error(request, 'Something went wrong ! Try again.')
        return redirect('admin_dash')

@login_required(login_url='login')
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    total_questions = quiz.total_questions

    if request.method == 'POST':
        # Handle form submissions
        forms = [AddQuestionForm(request.POST, request.FILES, prefix=str(i)) for i in range(total_questions)]
        if all(form.is_valid() for form in forms):
            # Save each form
            for form in forms:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()
            messages.success(request, f'{total_questions} questions were successfully added to {quiz.name}.')
            return redirect('admin_dash')
    else:
        # Display forms for adding questions
        forms = [AddQuestionForm(prefix=str(i)) for i in range(total_questions)]
    
    return render(request, 'admin/add_questions.html', {'quiz': quiz, 'forms': forms})

@login_required(login_url='login')
def edit_questions(request, quiz_id):
    questions = Questions.objects.filter(quiz_id=quiz_id)
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    
    if request.method == 'POST':
        forms = [EditQuestionForm(request.POST, instance=question, prefix=str(question.id)) for question in questions]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            messages.success(request, f'{quiz.name} questions were successfully modified.')
            return redirect('admin_dash')
    else:
        forms = [EditQuestionForm(instance=question, prefix=str(question.id)) for question in questions]

    data = {
        'forms': forms,
        'quiz': quiz,
    }

    return render(request, 'admin/edit_questions.html', data)

@login_required(login_url='login')
def view_users(request):
    users = User.objects.filter(is_superuser=False).order_by('-id')
    return render(request, 'admin/view_users.html', {'users': users})

@login_required(login_url='login')
def remove_user(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        name = user.first_name
        user.delete()
        messages.success(request, f'{name} was successfully removed.')
        return redirect('view_users')
    except:
        messages.error(request, 'Something went wrong ! Try again.')
        return redirect('view_users')

@login_required(login_url='login')
def view_results(request):
    quiz_sessions = QuizSession.objects.all().order_by('-id')
    return render(request, 'admin/view_results.html', {'quiz_sessions': quiz_sessions, })
