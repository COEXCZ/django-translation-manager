from django import dispatch

post_publish = dispatch.Signal(providing_args=["request"])

# DEPRECATED
post_save = dispatch.Signal(providing_args=["request"])
