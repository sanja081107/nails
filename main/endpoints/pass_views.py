from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


class PasswordChange(PasswordChangeView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = {
            'title': 'Изменение пароля',
            'body_title': 'Изменение пароля',
        }
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class PasswordChangeDone(PasswordChangeDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = {
            'title': 'Пароль изменен успешно',
            'body_title': 'Пароль изменен успешно',
        }
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class PasswordReset(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = {
            'title': 'Восстановление пароля',
            'body_title': 'Восстановление пароля',
        }
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class PasswordResetDone(PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = {
            'title': 'Восстановление пароля',
            'body_title': 'Восстановление пароля',
        }
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class PasswordResetConfirm(PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = {
            'title': 'Сброс пароля',
            'body_title': 'Сброс пароля',
        }
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class PasswordResetComplete(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = {
            'title': 'Сброс пароля выполнен',
            'body_title': 'Сброс пароля выполнен',
        }
        context = dict(list(context.items()) + list(c_def.items()))
        return context