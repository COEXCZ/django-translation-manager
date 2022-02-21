from django import dispatch

post_publish = dispatch.Signal()

# DEPRECATED
post_save = dispatch.Signal()
