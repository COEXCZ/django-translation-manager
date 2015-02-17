from django import dispatch

post_save = dispatch.Signal(providing_args=["request"])