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
def my_model_edit(request, template_name='myapp/my_model_form.html'):
    form = MyModelForm(request.POST or None, instance=mymodel)
    if form.is_valid():
        mymodel.save()
        return redirect('home')
    return render(request, template_name, {'form':form, 'mymodel':mymodel} )


