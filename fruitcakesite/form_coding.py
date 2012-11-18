Miguel Araujo, Daniel Greenfield
maraujop.github.com
Co-leads of django-uni-form

Brian Rosner
James Tauber
Frank Wiles

www.codinghorror.com/blog/2008/07/spartan-programming.html

traditional (standard):

def my_view(request, template_name="myapp/my_form.html"):
	if request.method=='POST':
		form = myForm(request.POST) # form 1
		if form.is_valid():
			do_x()
			return redirect('/')
	else:
		form = MyForm()	# form 2
	return render(request, template_name, {'form': form} )


recommended ("easy views" 1):

    def my_view(request, template_name="myapp/my_form.html"):
	form = MyForm(request.POST or None)
	if form.is_valid():
		do_x()
		return redirect('home')
	return render(request, templatename, {'form', form} )

generally tradition is to use ModelForm:

    class MyModelForm(forms.Form):
    class Meta:
        model = MyModel
        fields = ['name']

easy views + ModelForm (1):

    def my_model_edit(request, slug=slug, template_name='myapp/my_model_form.html'):
    mymodel = get_object_or_404(MyModel, slug=slug)
    form = MyModelForm(request.POST or None, instance=mymodel)
    if form.is_valid():
        mymodel = form.save()
        mymodel.edited_at_djangocon = True
        mymodel.save()
        return redirect('home')
    return render(request, template_name, {'form':form, 'mymodel':mymodel} )

easy views + ModelForms (2):
using defaults in ModelForms rather than setting values in view.

def my_model_tiny_edit(request, template_name='myapp/my_model_form.html'):
    form = MyModelForm(request.POST or None, instance=mymodel)
    if form.is_valid():
        mymodel.save()
        return redirect('home')
    return render(request, template_name, {'form':form, 'mymodel':mymodel} )

On Request / Response:
https://docs.djangoproject.com/en/dev/ref/request-response/

Modifications:
- Use __init__() to change required to not, etc.
- Use form.fields dictionary to add fields to a form.
- Use "extra" parameter to a form call: form = MyModelForm(request.POST or None, exta["fred"])
- render() ?


HTML5? --> django-floppyforms by Bruno Renie @brutasse

import floppyforms as forms
class ExampleForm(forms.Form):
    username = forms.CharField(
        label = '',
        widget = forms.TextInput(
            attrs = {'placeholder':'@johndoe'},
        ),
    )

replaces normal widgets with HTML5 widgets.



