# coding=utf-8

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator


class Base(TemplateView):
    """
    Support ajax method, like

    class X(Base):
        http_method_names = Base.http_method_names + {'ajax_get', 'ajax_post'}
        def ajax_get(self, request, *args, **kwargs):
            pass
    """
    page = ''
    login_required = False
    ajax_only = False
    http_method_names = set(TemplateView.http_method_names)
    ajax_content_type = None
    ajax_response_class = JsonResponse

    def dispatch(self, request, *args, **kwargs):
        if self.login_required:
            return method_decorator(login_required)(Base._dispatch)(self, request, *args, **kwargs)
        else:
            return self._dispatch(request, *args, **kwargs)

    def _dispatch(self, request, *args, **kwargs):
        is_ajax = request.is_ajax()
        method = request.method.lower()
        if not is_ajax and self.ajax_only:
            handler = self.http_method_not_allowed
        else:
            if is_ajax:
                method = 'ajax_{}'.format(method)

            if method in self.http_method_names:
                handler = getattr(self, method, self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    def render_ajax_resp(self, resp, encoder=None, safe=None, **kwargs):
        if self.ajax_content_type is not None:
            kwargs.setdefault('content_type', self.ajax_content_type)
        if encoder is not None:
            kwargs['encoder'] = encoder
        if safe is not None:
            kwargs['safe'] = safe

        return self.ajax_response_class(
            data=resp,
            **kwargs
        )

    def render_ajax(self, *args, **kwargs):
        resp = {'success': True}
        for arg in args:
            resp.update(arg)
        resp.update(**kwargs)
        return self.render_ajax_resp(resp)

    def render_ajax_fail(self, *args, **kwargs):
        args = ({'success': False},) + args
        return self.render_ajax(*args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        data = self.get_ajax_data(*args, **kwargs)
        return self.render_ajax(data=data)

    def get_ajax_data(self, *args, **kwargs):
        return {}

    def render_redirect(self, url, permanent=False, **resp_kwargs):
        kls = HttpResponsePermanentRedirect if permanent else HttpResponseRedirect
        return kls(url, **resp_kwargs)

    def raise_404(self, msg=None):
        raise Http404(msg)

    def render_400(self, msg=None):
        return HttpResponseBadRequest(msg)

    def render_403(self, msg=None):
        return HttpResponseForbidden(msg)

    def get_context_data(self, **kwargs):
        ctx = super(Base, self).get_context_data(**kwargs)
        if self.page:
            ctx.update({
                'page': self.page,
            })
        return ctx
