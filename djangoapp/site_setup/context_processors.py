from site_setup.models import SiteSetup

def example_proc(request):
    return {
        'example': 'veio do exempo, o baguio funciona'
    }

def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': setup,
    }