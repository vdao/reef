from reef import app
from reef import views

app.add_url_rule('/', view_func=views.home)

app.add_url_rule('/hello/', view_func=views.hello)
app.add_url_rule('/hello/<name>', view_func=views.hello)
