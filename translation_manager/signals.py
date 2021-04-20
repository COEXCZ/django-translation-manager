from django import dispatch

post_publish = dispatch.Signal(providing_args=["request"])
