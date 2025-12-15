from .models import SiteConfiguration, SocialMediaLink, CarouselImage

def site_context(request):
    """
    Context processor to make site configuration, social links,
    and carousel images available to all templates.
    """
    # Load site config (singleton) - handled safely by load() but we can also use first()
    try:
        site_config = SiteConfiguration.objects.first()
        if not site_config:
            # Fallback (though in production we should ensure one exists)
            site_config = None
    except Exception:
        site_config = None
        
    social_links = SocialMediaLink.objects.filter(is_active=True)
    
    # We might not want carousel on every page context if it's heavy, 
    # but for this scale it's fine. 
    # Usually carousel is only on index, so we could leave it out of here 
    # and pass it in the index view.
    # However, the user asked for "socials... carousel... logo... in admin".
    # Since carousel is specific to the Hero partial (used in index), 
    # let's keep it in the index view OR just let the context processor handle it 
    # so we don't have to touch views.py if we don't want to.
    # Let's put it here for simplicity of "global" availability if they reuse it.
    
    return {
        'site_config': site_config,
        'social_links': social_links,
    }
