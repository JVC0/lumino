import uuid

from django.template import Library
from django.urls import reverse

register = Library()


@register.inclusion_tag('modal.html')
def modal(
    btn_text,
    url,
    url_args=None,
    title='Attention',
    body='Are you sure you want to leave this account?',
    action='Continue',
    btn_classes='btn btn-primary',
    btn_icon='',
):
    url = reverse(url, args=url_args)
    modal_id = uuid.uuid4()
    return dict(
        modal_id=modal_id,
        title=title,
        body=body,
        action=action,
        url=url,
        btn_text=btn_text,
        btn_classes=btn_classes,
        btn_icon=btn_icon,
    )
