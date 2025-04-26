from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import User
import json


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            required_fields = ['username', 'password', 'email']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False,
                        'message': f'缺少必填字段: {field}'
                    }, status=400)

            if User.objects.filter(username=data['username']).exists():
                return JsonResponse({
                    'success': False,
                    'message': '用户名已存在'
                }, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({
                    'success': False,
                    'message': '邮箱已被注册'
                }, status=400)

            user = User(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                phone_number=data.get('phone_number'),
                gender=data.get('gender'),
                age=data.get('age'),
                code_age=data.get('code_age', 0)
            )
            user.save()

            return JsonResponse({
                'success': True,
                'message': '注册成功',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': '无效的JSON数据'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'注册失败: {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': '只支持POST请求'
    }, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            required_fields = ['username', 'password']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False,
                        'message': f'缺少必填字段: {field}'
                    }, status=400)

            try:
                user = User.objects.get(username=data['username'])
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': '用户名或密码错误'
                }, status=400)

            if not check_password(data['password'], user.password):
                return JsonResponse({
                    'success': False,
                    'message': '用户名或密码错误'
                }, status=400)
            auth_login(request, user)
            return JsonResponse({
                'success': True,
                'message': '登录成功',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'gender': user.gender,
                    'age': user.age,
                    'code_age': user.code_age,
                    'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': '无效的JSON数据'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'登录失败: {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': '只支持POST请求'
    }, status=405)
