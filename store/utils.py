from django.utils.text import slugify


def create_slug(instance, Items, new_slug=None):
    # create slug for the  model which is being passed
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Items.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f'{slug}-{qs.first().id}'
        return create_slug(instance, Items, new_slug=new_slug)
    return slug
