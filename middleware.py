class ArgumentLogMiddleware(object):
    def process_view(request,view,*args,**kwargs):
        print'Calling %s . %s' % (view.__module__,view.__name__)
        print'Arguments: %s '% (kwargs or(args,))