from django import template
from django.template import Context

from django.contrib.auth.views import Login


@register.tag(name="set_login")
def do_set_login(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return LoginNode(format_string[1:-1])  
    
class LoginNode(template.Node):
    def __init__(self, format_string):
        self.format_string = str(format_string)
    def render(self, context):
    #    (request, template_name='registration/login.html',
   #       redirect_field_name=REDIRECT_FIELD_NAME,
  #        authentication_form=AuthenticationForm,
    #      current_app=None, extra_context=None)
        
        
        t = template.loader.get_template('login.html')
        
        return t.render(Context({'idea_list' : ideas}))
