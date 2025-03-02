# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
LOGIN_URL = 'hotel:login'
LOGIN_REDIRECT_URL = 'hotel:home'
LOGOUT_REDIRECT_URL = 'hotel:home' 