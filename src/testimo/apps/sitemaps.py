# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from oscar.core.loading import get_model
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured


Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')


class CustomSitemap(Sitemap):

    def get_obj_location(self, obj):
        return obj.get_absolute_url()

    def location(self, obj):
        location = self.get_obj_location(obj)
        return location


class HomeSitemap(CustomSitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return ['promotions:home', ]

    def get_obj_location(self, obj):
        return reverse(obj)


class ProductSitemap(CustomSitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        qs = Product.all.base_queryset()
        return qs

    @staticmethod
    def lastmod(item):
        return item.date_updated


class CategorySitemap(CustomSitemap):
    changefreq = 'monthly'
    priority = 1.0

    def items(self):
        return Category.objects.all()


class FlatPageSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.5

    def items(self):
        if not django_apps.is_installed('django.contrib.sites'):
            raise ImproperlyConfigured("FlatPageSitemap requires django.contrib.sites, which isn't installed.")
        mysite = django_apps.get_model('sites.Site')
        current_site = mysite.objects.get_current()
        return current_site.flatpage_set.filter(registration_required=False)


sitemaps = {
    'home': HomeSitemap,
    'flatpages': FlatPageSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
}

base_sitemaps = {}
for name, sitemap_class in sitemaps.items():
    base_sitemaps['{0}'.format(name)] = sitemap_class()
