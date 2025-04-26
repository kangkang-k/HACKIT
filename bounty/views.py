# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bounty, User
import json
from django.utils import timezone
from datetime import datetime


def check_auth(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': '请先登录'
            }, status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


@csrf_exempt
@check_auth
def create_bounty(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            required_fields = ['title', 'description', 'reward', 'bounty_type']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False,
                        'message': f'缺少必填字段: {field}'
                    }, status=400)

            try:
                reward = float(data['reward'])
                if reward <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return JsonResponse({
                    'success': False,
                    'message': '赏金必须是大于0的数字'
                }, status=400)

            deadline = None
            if 'deadline' in data and data['deadline']:
                try:
                    deadline = datetime.strptime(data['deadline'], '%Y-%m-%d %H:%M:%S')
                    if deadline <= timezone.now():
                        return JsonResponse({
                            'success': False,
                            'message': '截止时间必须晚于当前时间'
                        }, status=400)
                except ValueError:
                    return JsonResponse({
                        'success': False,
                        'message': '截止时间格式错误，请使用: YYYY-MM-DD HH:MM:SS'
                    }, status=400)

            bounty = Bounty.objects.create(
                title=data['title'],
                description=data['description'],
                reward=reward,
                bounty_type=data['bounty_type'],
                creator=request.user,
                deadline=deadline,
                tech_stack=data.get('tech_stack', ''),
                difficulty=data.get('difficulty', 1),
                status='open'
            )

            return JsonResponse({
                'success': True,
                'message': '悬赏发布成功',
                'data': {
                    'id': bounty.id,
                    'title': bounty.title,
                    'reward': float(bounty.reward),
                    'status': bounty.status,
                    'created_at': bounty.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'deadline': bounty.deadline.strftime('%Y-%m-%d %H:%M:%S') if bounty.deadline else None
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
                'message': f'发布悬赏失败: {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': '只支持POST请求'
    }, status=405)
