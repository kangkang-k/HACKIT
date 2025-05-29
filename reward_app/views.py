import json
from .forms import *
from django.shortcuts import get_object_or_404
from .models import Reward, Category, RewardApplication
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CreateCategoryAPIView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return JsonResponse({
                'success': True,
                'category': model_to_dict(category)
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)


class UpdateCategoryAPIView(SuperuserRequiredMixin, View):
    def post(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return JsonResponse({
                'success': True,
                'category': model_to_dict(category)
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)


class ListCategoriesAPIView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        categories_list = [model_to_dict(category) for category in categories]
        return JsonResponse({
            'success': True,
            'categories': categories_list
        }, status=200)


class DeleteCategoryAPIView(SuperuserRequiredMixin, View):
    def delete(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return JsonResponse({'success': True, 'message': 'Category deleted successfully'}, status=200)


class CreateRewardAPIView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = RewardForm(request.POST)
        if form.is_valid():
            reward = form.save(commit=False)
            reward.creator = request.user
            reward.save()
            return JsonResponse({
                'success': True,
                'reward': model_to_dict(reward)
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)


class DeleteRewardAPIView(LoginRequiredMixin, View):
    def delete(self, request, reward_id, *args, **kwargs):
        try:
            reward = Reward.objects.get(id=reward_id, creator=request.user)
            reward.delete()
            return JsonResponse({'success': True, 'message': 'Reward deleted successfully.'}, status=200)
        except Reward.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reward not found or not authorized.'}, status=404)


class UpdateRewardAPIView(LoginRequiredMixin, View):
    def post(self, request, reward_id, *args, **kwargs):
        try:
            reward = Reward.objects.get(id=reward_id, creator=request.user)
        except Reward.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reward not found or not authorized.'}, status=404)

        if reward.status != 'pending':
            return JsonResponse({'success': False, 'message': 'Only rewards with status "Pending" can be modified.'},
                                status=403)

        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            updated_reward = form.save()
            return JsonResponse({
                'success': True,
                'reward': model_to_dict(updated_reward)
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)


class ListRewardsAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        rewards = Reward.objects.filter(creator=request.user)
        rewards_list = [model_to_dict(reward) for reward in rewards]
        return JsonResponse({'success': True, 'rewards': rewards_list}, status=200)


class RewardApplicationCreateAPIView(View):
    def post(self, request, *args, **kwargs):
        form = RewardApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            return JsonResponse({'id': application.id, 'message': 'RewardApplication created successfully'}, status=201)
        return JsonResponse(form.errors, status=400)


class RewardApplicationDeleteAPIView(View):
    def delete(self, request, application_id, *args, **kwargs):
        # 获取要删除的对象
        application = get_object_or_404(RewardApplication, id=application_id)

        # 删除对象
        application.delete()

        # 返回成功响应
        return JsonResponse({'message': 'RewardApplication deleted successfully'}, status=204)


class RewardApplicationAcceptAPIView(LoginRequiredMixin, View):
    def patch(self, request, application_id, *args, **kwargs):
        application = get_object_or_404(RewardApplication, id=application_id)

        reward = get_object_or_404(Reward, id=application.reward_id)
        if reward.creator != request.user:
            return JsonResponse({'message': 'You are not allowed to modify this application.'}, status=403)

        application.is_accepted = True
        reward.status = 'accepted'

        application.save()
        reward.save()

        return JsonResponse({'message': 'RewardApplication updated successfully'}, status=200)


class RewardApplicationRejectAPIView(LoginRequiredMixin, View):
    def patch(self, request, application_id, *args, **kwargs):
        application = get_object_or_404(RewardApplication, id=application_id)

        reward = get_object_or_404(Reward, id=application.reward_id)
        if reward.creator != request.user:
            return JsonResponse({'message': 'You are not allowed to modify this application.'}, status=403)

        application.is_accepted = False

        application.save()

        return JsonResponse({'message': 'RewardApplication updated successfully'}, status=200)


class UpdateRewardStatusAPIView(LoginRequiredMixin, View):
    def patch(self, request, reward_id, *args, **kwargs):
        try:
            application = RewardApplication.objects.get(reward_id=reward_id, applicant=request.user, is_accepted=True)
            reward = application.reward

            try:
                data = json.loads(request.body)
                new_status = data.get('status')
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid JSON data'
                }, status=400)

            if new_status not in dict(Reward.STATUS_CHOICES).keys():
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid status value'
                }, status=400)

            reward.status = new_status
            reward.save()

            return JsonResponse({
                'success': True,
                'reward': model_to_dict(reward)
            }, status=200)

        except RewardApplication.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'You have not applied for this reward or it was not accepted'
            }, status=404)
