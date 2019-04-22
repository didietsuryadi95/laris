import logging
from celery import task
from functools import reduce
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')

logger = logging.getLogger('testimo')


@task(name='handle_update_category_product')
def handle_update_category_product(category_id):
    logger.info(f"executing update category product")
    category = Category.objects.filter(pk=category_id).last()
    if category:
        categories = category.get_descendants_and_self() if not category.get_ancestors() \
            else reduce(lambda x, y: x + y, [c.get_descendants_and_self() for c in category.get_ancestors()
                                             if not c.get_ancestors()])
        product_categories = Product.objects.filter(categories__in=categories)
        for product in product_categories:
            product.save()
