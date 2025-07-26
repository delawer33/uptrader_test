from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="index.html"), name="about"
    ),
    path(
        "contacts/",
        TemplateView.as_view(template_name="index.html"),
        name="contacts",
    ),
    path(
        "about/purpose/",
        TemplateView.as_view(template_name="index.html"),
        name="purpose",
    ),
    # path(
    #     "about/purpose/purpose_detail_1",
    #     TemplateView.as_view(template_name="index.html"),
    #     name="purpose_detail_1",
    # ),
    path(
        "about/products/",
        TemplateView.as_view(template_name="index.html"),
        name="products",
    ),
    path(
        "about/products/product1/",
        TemplateView.as_view(template_name="index.html"),
        name="product1",
    ),
    path(
        "about/products/product2/",
        TemplateView.as_view(template_name="index.html"),
        name="product2",
    ),
    path(
        "about/products/product1/detail1/",
        TemplateView.as_view(template_name="index.html"),
        name="product_detail_1",
    ),
    path(
        "about/team/", TemplateView.as_view(template_name="index.html"), name="team"
    ),
    path(
        "address/",
        TemplateView.as_view(template_name="index.html"),
        name="address",
    ),
    path(
        "help/", TemplateView.as_view(template_name="index.html"), name="help"
    ),
]
