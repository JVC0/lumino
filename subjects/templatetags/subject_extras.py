from django import template

register = template.Library()

@register.inclusion_tag('subjects/marks/student_label.html')
def student_label_list(student):
    return dict(student=student)

@register.inclusion_tag('subjects/marks/student_label.html')
def student_label(formset, form_index):
    student = formset.forms[form_index].instance.student
    return dict(student=student)

@register.inclusion_tag('subjects/marks/mark.html')
def pretty_mark(mark: int | None):
    if mark is None:
        css_class = ''
        mark_value = '_'
    else:
        css_class = 'text-danger' if mark < 5 else 'text-success'
        mark_value = mark
    return dict(mark=mark_value, css_class=css_class)


