
def add_styles(widget, styles):
    """ Helper function - adds CSS styles to widget

    """
    attrs = widget.attrs or {}
    if 'style' in attrs:
        attrs['style'] = '%s %s' % (attrs['style'], styles)
    else:
        attrs['style'] = styles
    widget.attrs = attrs