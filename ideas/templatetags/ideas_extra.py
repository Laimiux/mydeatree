from django import template
from django.template import Context

from ideas.models import Idea


import datetime

register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
    "Removes all values of arg from the given string"
    return value.replace(arg, '')


@register.tag(name="current_time")
def do_current_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return CurrentTimeNode(format_string[1:-1])


@register.tag(name="top_ideas")
def do_top_ideas(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return TopIdeasNode(format_string[1:-1])    
    
    
class TopIdeasNode(template.Node):
    def __init__(self, format_string):
        self.format_string = str(format_string)
    def render(self, context):
        t = template.loader.get_template('show_top_ideas.html')
        ideas = Idea.objects.filter(owner=context['user'], parent=None)
        
        return t.render(Context({'idea_list' : ideas}))

class CurrentTimeNode(template.Node):
    def __init__(self, format_string):
        self.format_string = str(format_string)

    def render(self, context):
        now = datetime.datetime.now()
        return now.strftime(self.format_string)