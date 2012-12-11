from django import template
from django.template import Library, Node, TemplateSyntaxError
from django.template.base import Template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def softwraphtml(value, max_line_length=20):
    import re
    whitespace_re = re.compile('\s')
    new_value = []
    unbroken_chars = 0
    in_tag = False
    in_xhtml_entity = False
    for idx, char in enumerate(value):
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
            unbroken_chars = 0
        elif char == '&' and not in_tag:
            in_xhtml_entity = True
        elif char == ';' and in_xhtml_entity:
            in_xhtml_entity = False            
        elif whitespace_re.match(char):
            unbroken_chars = 0
        
        new_value.append(char)
        if not in_xhtml_entity:
            if unbroken_chars >= max_line_length-1 and not in_tag:
                new_value.append("<wbr/>")
                unbroken_chars = 0
            else:
                unbroken_chars += 1
    return mark_safe(''.join(new_value))


@register.tag
def page_index(parser, token):
    """
    Outputs the template with pagination
    
    Like a simple "include" tag, the ''page_index'' tag includes
    the contents of another file -- which must be created by you.
    It has to be 'templates/pagination/pagination.html'
    
    This function needs a few inputs
    {% page_index page_url %}
    page_url --> This should be '/page/' or '/blog/page/' or '?page='. URI for pages.
    
    Set the following variables in the context!
    current_page --> This is needed to show which button is active.
    number_of_pages --> Total number of pages
    
    {% page_index /page/ %}   
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError("'page_index' tag takes 1 argument")
    else:
        page_url = bits[1]
    return PageIndexNode(page_url)
  
     

class PageIndexNode(Node):
    def __init__(self, page_url):
        self.page_url = page_url
        
    def render(self, context):
        if context['number_of_pages'] > 1:
            context['number_of_pages'] = range(context['number_of_pages'])
        else:
            context['number_of_pages'] = ''
        context['page_url'] = self.page_url
        
        t = template.loader.get_template('pagination.html')
          
        return t.render(context)
