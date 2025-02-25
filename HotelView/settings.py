STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
] 
LOGIN_URL = 'hotel:login'
LOGIN_REDIRECT_URL = 'hotel:home'
LOGOUT_REDIRECT_URL = 'hotel:home' 