from django import forms
from .models import Release

class ReleaseForm(forms.Form):
    # releases = Release.objects.filter(generated__isnull=True)
    # release = forms.ChoiceField(choices=[(r.pk, r.name) for r in releases], 
    #                           widget = forms.Select(attrs = {'onchange' : "refresh();"}))
    release = forms.ChoiceField()
    def __init__(self, *args, **kwargs):
        super(ReleaseForm, self).__init__(*args, **kwargs)
        releases = Release.objects.filter(generated__isnull=True)
        choices = [(r.pk, r.name) for r in releases] 
        self.fields['release'].choices = choices 
        #release = forms.ChoiceField(choices=[(r.pk, r.name) for r in releases], 
        #                      widget = forms.Select(attrs = {'onchange' : "refresh();"}))

class ReleaseModelForm(forms.ModelForm):
    # releases = Release.objects.filter(generated__isnull=True)
    # release = forms.ChoiceField(choices=[(r.pk, r.name) for r in releases], 
    #                           widget = forms.Select(attrs = {'onchange' : "refresh();"}))
    release = forms.ChoiceField()
    class Meta:
        model = Release
        fields = ("release", "name", "ip", "port", "database", "user")   # NOTE: the trailing comma is required
        widgets = {
            'name': forms.TextInput(attrs={'readonly':'readonly'}),
            'ip': forms.TextInput(attrs={'readonly':'readonly'}),
            'port': forms.TextInput(attrs={'readonly':'readonly'}),
            'database': forms.TextInput(attrs={'readonly':'readonly'}),
            'user': forms.TextInput(attrs={'readonly':'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super(ReleaseForm, self).__init__(*args, **kwargs)   
        releases = Release.objects.filter(generated__isnull=True)
        choices = [(r.pk, r.name) for r in releases]     
        release = forms.ChoiceField(choices=choices)#, widget = forms.Select(attrs = {'onchange' : "refresh();"}))
        print("Executing init.")
        print(releases)
        print(releases[0].name)
        print(releases[0].ip)
        print(choices)
        self.fields['release'].choices = choices
        #self.fields['name'] = releases[0].name
        # self.fields['ip'] = releases[0].ip
        # self.fields['port'] = releases[0].port
        # self.fields['database'] = releases[0].database

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    choice = forms.ChoiceField(choices=[(release.pk, release.name) for release in Release.objects.all()])

class CompareForms(forms.Form):
    ip = forms.CharField(label='ip', max_length=100)
    choice = forms.ChoiceField(choices=[(release.pk, release.name) for release in Release.objects.all()])

class CompareFormsRelease(forms.Form):
    #release = forms.ChoiceField(choices=[(release.pk, release.name) for release in Release.objects.filter(generated__isnull=False)])
    #ip = forms.GenericIPAddressField(unpack_ipv4=True,initial='127.0.0.1')
    release = forms.ChoiceField()
    ip = forms.CharField(max_length=64,initial='127.0.0.1')
    port=forms.IntegerField(max_value=65535,initial='3306')
    #database = forms.CharField(max_length=32)
    user = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    #class Meta:
    #     model = Release
    #    fields = ("ip", "port", "database", "user", "password" )        
    def __init__(self, *args, **kwargs):
        super(CompareFormsRelease, self).__init__(*args, **kwargs)
        releases = Release.objects.filter(generated__isnull=False)
        choices = [(r.pk, r.name) for r in releases] 
        self.fields['release'].choices = choices 
        