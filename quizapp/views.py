from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_naive
from django.db.models import Avg, F, Sum
from aptiquiz import settings
from site_admin.views import *
from .models import *
from .forms import *
import re

# send mail requirements
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import generate_token

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):
    page = 'login'
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        
        user = authenticate(username=uname, password=password)
        if user is not None:
            if user.is_superuser == True:
                auth.login(request, user)
                return redirect('admin_dash')
            else:
                auth.login(request, user)
                request.session['uid'] = user.id
                return redirect('user_dash')
        else:
            messages.error(request, "Invalid username or password !")
            return redirect('login')
    return render(request, 'login.html', {'page':page})

def signup(request):
    page = 'register'
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        cpassword = request.POST.get('cpass')
        
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-])[A-Za-z\d!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]{8,}$"

        if not re.match(pattern, password):
            messages.error(request, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character !")
            return redirect('signup')
        elif cpassword != password:
            messages.error(request, "Passwords are not matching !!")
            return redirect('signup')
        else:
            try:
                User.objects.get(username=uname)
                messages.error(request, "Username already exists ! Try another one.")
                return redirect('signup')
            except User.DoesNotExist:
                try:
                    User.objects.get(email=email)
                    messages.error(request, "Email id already associated with an account ! Try another one.")
                    return redirect('signup')
                except User.DoesNotExist:
                    user = User.objects.create_user(username=uname, password=cpassword)
                    user.first_name = fname
                    user.last_name = lname
                    user.email = email
                    user.save()
                    messages.success(request, "You've successfully signed up. Try Login.")
                    return redirect('login')
    return render(request, 'login.html', {'page':page})

def forgot_pass(request):
    page = 'forgot'
    if request.method == 'POST':
        uname = request.POST.get('uname')
        try:
            user = User.objects.get(username=uname)
            # Reset mail
            current_site = get_current_site(request)
            email_sub = "Reset Password"
            message = render_to_string("reset_pass_mail.html",{
                'user' : user.first_name,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : generate_token.make_token(user),
            })
            email = EmailMessage(
                email_sub,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently=True
            email.send()
            messages.success(request, "Password reset link has been sent. Please check your mail")
            return redirect('forgot_pass')
        except User.DoesNotExist:
            messages.error(request, "Invalid Username ! Try again.")
            return redirect('forgot_pass')
    return render(request, 'forgot_pass.html', {'page':page})

def reset_password(request, id, token):
    page = 'reset_pass'
    uid =force_str(urlsafe_base64_decode(id))
    if request.method == 'POST':
        if 'uid' in request.session:
            del request.session['uid']
            logout(request)
        
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-])[A-Za-z\d!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]{8,}$"

        if not re.match(pattern, password):
            messages.error(request, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character !")
            return redirect('reset_password', id, token)
        elif password != cpassword:
            messages.error(request, "Passwords not matching !!")
            return redirect('reset_password', id, token)
        else:
            user = User.objects.get(pk=uid)
            user.set_password(cpassword)
            user.save()
            messages.success(request, "Password changed successfully, Try login.")
            return redirect('login')
    else:
        try:
            myuser = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None
        
        if myuser is not None and generate_token.check_token(myuser, token):
            return render(request, 'forgot_pass.html', {'page': page, 'id': id, 'token': token})
        else:
            return HttpResponse("Token Doesn't Match !!")

def signout(request):
    logout(request)
    if 'uid' in request.session:
        del request.session['uid']
    messages.success(request, "Logged out successfully.")
    return redirect('login')

@login_required(login_url='login')
def user_dash(request):
    user = User.objects.get(pk=request.session['uid'])
    try:
        dp = UserImages.objects.get(user=user)
    except UserImages.DoesNotExist:
        dp = None
    
    categories = ['qa', 'lr', 'vb']

    category_data = []
    for category in categories:
        total_possible_score = Quizzes.objects.filter(category=category).aggregate(total_score=Sum(F('marks_for_each') * F('total_questions')))['total_score'] or 0

        tot_score = QuizSession.objects.filter(user=user, quiz__category=category).aggregate(score = Sum('score'))['score'] or 0
        
        if total_possible_score != 0:
            avg_score = (tot_score/total_possible_score)* 5
            avg_score_in_10 = (tot_score/total_possible_score)* 10
        else:
            avg_score = 0
            avg_score_in_10 = 0

        category_data.append({
            'category': category,
            'avg_score': avg_score,
            'avg_score_in_10': avg_score_in_10,
        })
    
    return render(request, "user/user_dash.html", {'user': user, 'dp': dp, 'category_data': category_data})

@login_required(login_url='login')
def view_quizzes(request, cat):
    category = cat
    quizzes = Quizzes.objects.all().filter(category=category).exclude(attendees=request.user)
    return render(request, "user/view_quizzes.html", {'cat':category, 'quizzes': quizzes})

@login_required(login_url='login')
def navigate_question(request, quiz_id, question_number):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    questions = Questions.objects.filter(quiz=quiz)

    if 1 <= question_number <= len(questions):
        # Set the current question based on the selected question number
        request.session['current_question'] = question_number - 1

    return redirect('attend_quiz', quiz_id=quiz_id, mode='attend')

@login_required(login_url='login')
def attend_quiz(request, quiz_id, mode):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    if mode == 'start':
        if quiz.attendees.filter(pk=request.user.pk).exists():
            messages.error(request, "You've already attended that quiz. Try another one.")
            return redirect('user_dash')
        else:
            request.session['attending_quiz'] = quiz_id
            start_time = timezone.now()
            request.session['quiz_start_time'] = start_time.isoformat()
    if 'attending_quiz' in request.session:
        questions = Questions.objects.filter(quiz=quiz)
        answered_questions = UserResponse.objects.filter(user=request.user, quiz=quiz)
        
        question_ids = [question.id for question in questions]
        answered_question_ids = [response.question.id for response in answered_questions]
        
        answered_indexes = [question_ids.index(answer_id)+1 for answer_id in answered_question_ids]
        
        if mode != 'submission':
            if 'current_question' not in request.session:
                # Set the initial question to the first question in the quiz
                request.session['current_question'] = 0
                
                # Calculate and store the end time of the quiz in the session
                end_time = timezone.now() + timedelta(minutes=int(quiz.time_limit))
                request.session['quiz_end_time'] = end_time.isoformat()  # Store as string for serialization

            current_question_index = request.session['current_question']
            current_question = questions[current_question_index]
            
            if current_question.id in answered_question_ids:
                question = get_object_or_404(Questions, pk=current_question.id)
                submitted_answer = UserResponse.objects.get(quiz=quiz, question=question)
            else:
                submitted_answer = None

            form = QuizForm(request.POST or None)

            if request.method == 'POST':
                if form.is_valid():
                    selected_option = form.cleaned_data['selected_option'] or None

                    if selected_option != None:
                        # Check if user response for the question exists or not
                        try:
                            response = UserResponse.objects.get(user=request.user, quiz=quiz, question=current_question)
                            response.selected_option = selected_option
                            response.save()
                        except UserResponse.DoesNotExist:
                            # Store user response in the database
                            user_response = UserResponse(user=request.user, quiz=quiz, question=current_question, selected_option=selected_option)
                            user_response.save()

                    # Move to the next question
                    request.session['current_question'] += 1

                    # If all questions have been answered, redirect to a completion page
                    if request.session['current_question'] >= len(questions):
                        del request.session['current_question']
                        return redirect('attend_quiz', quiz_id=quiz_id, mode='submission')

                    # Redirect to the same page to load the next question
                    return redirect('attend_quiz', quiz_id=quiz_id, mode='attend')
        
        # Retrieve the end time from the session
        end_time_str = request.session['quiz_end_time']
        end_time = datetime.fromisoformat(end_time_str)
        
        if isinstance(end_time, timedelta):
            end_time = datetime.now(timezone.utc) + end_time

        if end_time.tzinfo != timezone.utc:
            end_time = end_time.astimezone(timezone.utc)

        remaining_time = end_time - timezone.now()
        remaining_seconds = max(remaining_time.total_seconds(), 0)
        
        if mode != 'submission':
            data = {
                'quiz': quiz,
                'questions': questions,
                'current_question': current_question,
                'current_question_number': current_question_index + 1,
                'answer': submitted_answer,
                'answered_questions': answered_indexes,
                'form': form,
                'remaining_time': remaining_seconds,  # Pass remaining time to the template
                'mode': mode,
            }
        else:
            data = {
                'quiz': quiz,
                'questions': questions,
                'answered_questions': answered_indexes,
                'remaining_time': remaining_seconds,
                'mode': mode,
            }
        
        return render(request, "user/quiz.html", data)
    else:
        return redirect('user_dash')

@login_required(login_url='login')
def finish_quiz(request, quiz_id):
    if 'attending_quiz' in request.session:
        del request.session['attending_quiz']
    if 'current_question' in request.session:
        del request.session['current_question']
    if 'quiz_start_time' in request.session:
        quiz = get_object_or_404(Quizzes, pk=quiz_id)
        quiz_start_time_str = request.session['quiz_start_time']
        quiz_start_time = make_naive(datetime.fromisoformat(quiz_start_time_str))
        end_time = make_naive(timezone.now())

        # Create a QuizSession object for the user's participation
        quiz_session = QuizSession(user=request.user, quiz=quiz, start_time=quiz_start_time, end_time=end_time)
        quiz_session.save()

        del request.session['quiz_start_time']
    if 'quiz_end_time' in request.session:
        del request.session['quiz_end_time']
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    quiz.attendees.add(request.user)
    hashed_id = urlsafe_base64_encode(force_bytes(quiz_id))
    hashed_user_id = urlsafe_base64_encode(force_bytes(request.user.id))
    return redirect('view_result', hashed_id, hashed_user_id)

@login_required(login_url='login')
def view_result(request, quiz_id, user_id):
    id = force_str(urlsafe_base64_decode(quiz_id))
    uid = force_str(urlsafe_base64_decode(user_id))
    quiz = get_object_or_404(Quizzes, pk=id)
    user = get_object_or_404(User, pk=uid)
    
    questions = Questions.objects.filter(quiz=quiz)
    score = 0
    total_score = quiz.total_questions * quiz.marks_for_each
    
    for question in questions:
        user_response = UserResponse.objects.filter(user=user, quiz=quiz, question=question).first()
        if user_response:
            if user_response.selected_option == question.answer:
                score += quiz.marks_for_each
    
    score_percent = (score/total_score)*100
    if score_percent >= 35:
        result = 'Passed'
    else:
        result = 'Failed'
    
    user_responses = UserResponse.objects.filter(user=user, quiz=quiz)
    quiz_session = QuizSession.objects.get(user=user, quiz=quiz)
    
    if not quiz_session.score:
        quiz_session.score = score
        quiz_session.save()
    
    if request.user.is_superuser == True:
        requester = 'admin'
    else:
        requester = 'user'
    
    data = {
        'quiz': quiz,
        'user': user,
        'total_score': total_score,
        'score': score,
        'score_percent': score_percent,
        'result': result,
        'questions': questions,
        'user_responses': user_responses,
        'session': quiz_session,
        'requester': requester,
    }
    return render(request, "user/quiz_result.html", data)

@login_required(login_url='login')
def profile(request):
    page = 'profile'
    user = User.objects.get(pk=request.session['uid'])
    
    if request.method == 'POST':        
        form_type = request.POST.get('form_type')
        
        if form_type == 'dp_update':
            user_object = get_object_or_404(User, pk=request.session['uid'])
            try:
                UserImages.objects.get(user=user_object)
                image_instance = get_object_or_404(UserImages, user=user_object)
                form = DP_Form(request.POST, request.FILES, instance=image_instance)
            
                if form.is_valid():
                    try:
                        form.save()
                        return redirect('profile')
                    except Exception as e:
                        messages.error(request, f"{e}")
                        return redirect('profile')
                else:
                    messages.error(request, "Something went wrong ! Please try again.")
                    return redirect('profile')
            except UserImages.DoesNotExist:
                image = request.FILES.get('image')
                user_image = UserImages(user=user_object, image=image)
                user_image.save()
                return redirect('profile')
        
        elif form_type == 'edit_profile':
            username = request.POST.get('username')
            email = request.POST.get('email')
            is_exist = User.objects.exclude(pk=request.session['uid']).filter(username=username)
            is_email_exist = User.objects.exclude(pk=request.session['uid']).filter(email=email)
            
            if is_exist:
                messages.error(request, "Username already taken ! Try another one.")
                return redirect('profile')
            elif is_email_exist:
                messages.error(request, "Email id already exists ! Try another one.")
                return redirect('profile')
            else:
                form = UserEditProfileForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Profile updated successfully.")
                    return redirect('profile')
                else:
                    messages.error(request, "Something went wrong ! Please try again.")
                    return redirect('profile')
        elif form_type == 'pass_update':
            password = request.POST.get('password')
            pass_check = authenticate(username=user.username, password=password)
            
            if pass_check is not None:
                hashed_id = urlsafe_base64_encode(force_bytes(user.pk)),
                token = generate_token.make_token(user)
                return redirect('reset_password', hashed_id, token)
            else:
                messages.error(request, "Wrong password !!")
                return redirect('profile')                
        else:
            return HttpResponse("Wrong POST request !!")
    else:
        try:
            dp = UserImages.objects.get(user=user)
        except UserImages.DoesNotExist:
            dp = None
        return render(request, 'user/profile.html', {'page': page, 'user': user, 'dp':dp})
