import logging
from celery import task
from oscar.core.loading import get_model

ProductCategory = get_model('catalogue', 'ProductCategory')

logger = logging.getLogger('arcanum')


@task(name='handle_update_category_product')
def handle_update_category_product(category_id):
    logger.info(f"executing update category product")
    product_categories = ProductCategory.objects.filter(category_id=category_id)
    for product_category in product_categories:
        product_category.product.save()
