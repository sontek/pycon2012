import deform

class BaseForm(deform.Form):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('buttons'):
            kwargs['buttons'] = ('submit', )

        super(BaseForm, self).__init__(*args, **kwargs)

class BootstrapForm(BaseForm):
    """ This form renders out twitter bootstrap templates """
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)

        for child in self.children:
            if isinstance(child.widget, deform.widget.TextInputWidget) or \
                isinstance(child.widget, deform.widget.TextAreaWidget):
                child.widget.css_class='xlarge'

class UNIForm(BaseForm):
    """ This form renders out uni-form style templates """
    def __init__(self, *args, **kwargs):
        kwargs['css_class'] = 'uniForm'

        super(UNIForm, self).__init__(*args, **kwargs)


class PyvoreForm(BootstrapForm):
    """ This is the standard form we should use through out our code, that way
    if we decide to swap our rendering later, we only have to do it in 1 place
    """
    pass
