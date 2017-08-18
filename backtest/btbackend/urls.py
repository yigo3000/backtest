"""btbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from backtest import views as backtest_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^backtest/start_backtest', backtest_views.start_backtest),
    url(r'^benchmark_portfolio/unit_net_value', backtest_views.benchmark_portfolio_unit_net_value),
    url(r'^portfolio/unit_net_value', backtest_views.portfolio_unit_net_value),
    url(r'^portfolio/delt_day_value', backtest_views.portfolio_delt_day_value),
    url(r'^summary', backtest_views.summary),
    url(r'^trades', backtest_views.trades)
]
