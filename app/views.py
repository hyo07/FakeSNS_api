from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .forms import ArticleForm
from .models import Article, Profile
from libs import BlackList


# トップページ
def top(request):
    return render(request, "index.html")


# 一覧表示
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "index.html"
    model = Article
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.all().order_by("-created_at")

    # ブラックリストは表示しない
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            str_bl = BlackList.read_bl(self.request.user.profile.black_list)
            int_bl = BlackList.str_to_int(str_bl)
            context["black_list"] = int_bl
        except Profile.DoesNotExist:
            pass
        return context


# 新規投稿
class CreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "create.html"
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("app:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "投稿しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "投稿に失敗しました")


# 編集
class UpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "update.html"
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("app:index")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("あなたはこの投稿を編集できません")
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "変更を保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "変更の保存に失敗しました")


# 削除
class DeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "delete.html"
    model = Article
    success_url = reverse_lazy("app:index")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("あなたはこの投稿を削除できません")
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "投稿を削除しました")
        return super().delete(request, *args, **kwargs)
