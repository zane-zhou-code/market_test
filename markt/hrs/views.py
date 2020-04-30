from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse

from django.db.models import Avg
from urllib.parse import quote
from io import BytesIO
import os, xlwt, requests, json

from .captcha import Captcha
from .forms import RegisterForm, LoginForm, TEL_PATTERN
from .models import Subject, Teacher, User
from .utils import generate_captcha_code, generate_mobile_code



depts_list = [
    {'no': 10, 'name': '财务部', 'location': '北京'},
    {'no': 20, 'name': '研发部', 'location': '成都'},
    {'no': 30, 'name': '销售部', 'location': '上海'},
]


def index(request):
    return render(request, 'index.html', {'depts_list':depts_list})

def get_subjects_data(request):
    queryset = Teacher.objects.values('subject__name').annotate(
        good=Avg('good_count'), bad=Avg('bad_count'))
    names = [result['subject__name'] for result in queryset]
    good = [result['good'] for result in queryset]
    bad = [result['bad'] for result in queryset]
    return JsonResponse({'names': names, 'good': good, 'bad': bad})
def get_teachers_data(request):
    """获取老师评价数据"""
    # only() - 指定要查询对象的哪些属性（SQL投影操作）
    # defer() - 指定暂时不查询对象的哪些属性
    queryset = Teacher.objects.all().only('name', 'good_count', 'bad_count')
    names = [teacher.name for teacher in queryset]
    good = [teacher.good_count for teacher in queryset]
    bad = [teacher.bad_count for teacher in queryset]
    return JsonResponse({'names': names, 'good': good, 'bad': bad})
def show_bar(request, no):
    """显示柱状图"""
    return render(request, f'bar{no}.html')
def export_pdf(request):
    """导出PDF文档"""
    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'resources/Python全栈+人工智能.pdf')
    file_stream = open(filename, 'rb')
    file_iter = iter(lambda: file_stream.read(1024), b'')
    resp = StreamingHttpResponse(file_iter, content_type='application/pdf')
    filename = quote('Python全栈+人工智能.pdf')
    resp['content-disposition'] = f'inline; filename="{filename}"'
    return resp
def export_teachers_excel(request):
    """导出Excel报表"""
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('老师信息表')
    # 多对一：select_related('关联属性')
    # 多对多：prefetch_related('关联属性')
    queryset = Teacher.objects.all().select_related('subject')
    colnames = ('姓名', '介绍', '好评数', '差评数', '学科')
    for index, name in enumerate(colnames):
        sheet.write(0, index, name)
    props = ('name', 'detail', 'good_count', 'bad_count', 'subject')
    for row, teacher in enumerate(queryset):
        for col, prop in enumerate(props):
            value = getattr(teacher, prop, '')
            if isinstance(value, Subject):
                value = value.name
            sheet.write(row + 1, col, value)
    buffer = BytesIO()
    wb.save(buffer)
    # 将二进制数据写入响应的消息体中并设置MIME类型
    resp = HttpResponse(buffer.getvalue(), content_type='application/vnd.ms-excel')
    # 中文文件名需要处理成百分号编码
    filename = quote('老师.xls')
    # 通过响应头告知浏览器下载该文件以及对应的文件名
    resp['content-disposition'] = f'attachment; filename="{filename}"'
    return resp
def get_mobile_code(request):
    """获得手机验证码"""
    tel = request.GET.get('tel')
    if TEL_PATTERN.fullmatch(tel):
        code = generate_mobile_code()
        request.session['mobile_code'] = code
        resp = requests.post(
            url='http://sms-api.luosimao.com/v1/send.json',
            auth=('api', 'key-6d2417156fefbd9c0e78fae069a34580'),
            data={
                'mobile': tel,
                'message': f'您的短信验证码是{code}，打死也不能告诉别人。【Python小课】',
            },
            timeout=3,
            verify=False
        )
        if json.loads(resp.text)['error'] == 0:
            code, hint = 20001, '短信验证码发送成功'
        else:
            code, hint = 20002, '短信验证码发送失败，请稍后重试'
    else:
        code, hint = 20003, '请输入有效的手机号码'
def get_captcha(request):
    """生成图片验证码"""
    code  = generate_captcha_code()
    request.session['captcha'] = code
    image = Captcha.instance().generate(code, fmt='PNG')
    return HttpResponse(image, content_type='image/png')
def logout(request):
    """用户注销"""
    request.session.flush()
    return redirect('/')
def login(request):
    """用户登录"""
    hint = ''
    backurl = request.GET.get('backurl', '/')
    if request.method == 'POST':
        backurl = request.POST['backurl']
        form = LoginForm(request.POST)
        if form.is_valid():
            # 对验证码的正确性进行验证
            captcha_from_user = form.cleaned_data['captcha']
            captcha_from_sess = request.session.get('captcha', '')
            if captcha_from_sess.lower() != captcha_from_user.lower():
                hint = '请输入正确的验证码'
            else:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.filter(username=username, password=password).first()
                if user:
                    # 登录成功后将用户编号和用户名保存在session中
                    request.session['userid'] = user.no
                    request.session['username'] = user.username
                    return redirect(backurl)
                else:
                    hint = '用户名或密码错误'
        else:
            hint = '请输入有效的登录信息'
    return render(request, 'login.html', {'hint': hint, 'backurl': backurl})
def register(request):
    """用户注册"""
    hint = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            code_from_session = request.session.get('mobile_code')
            code_from_user = form.cleaned_data['code']
            if code_from_session == code_from_user:
                form.save()
                hint = '注册成功，请登录'
                return render(request, 'login.html', {'hint': hint})
            else:
                hint = '请输入正确的手机验证码'
        else:
            hint = '请输入有效的注册信息'
    return render(request, 'register.html', {'hint': hint})
def show_subjects(request):
    """查看所有学科"""
    subjects = Subject.objects.all()
    return render(request, 'subject.html', {'subjects': subjects})
def show_teachers(request):
    """显示指定学科的老师"""
    try:
        sno = int(request.GET['sno'])
        subject = Subject.objects.get(no=sno)
        teachers = subject.teacher_set.all()
        return render(request, 'teachers.html', {'subject': subject, 'teachers': teachers})
    except (KeyError, ValueError, Subject.DoesNotExist):
        return redirect('index')
def praise_or_criticize(request):
    """给老师点好评或者差评"""
    code, hint = 10002, '无效的老师编号'
    try:
        tno = int(request.GET['tno'])
        teacher = Teacher.objects.filter(no=tno).first()
        if teacher:
            if request.path.startswith('/praise/'):
                teacher.good_count += 1
            else:
                teacher.bad_count += 1
            teacher.save()
            code, hint = 10001, '投票操作成功'
    except (KeyError, ValueError):
        pass
    return JsonResponse({'code': code, 'hint': hint})

















