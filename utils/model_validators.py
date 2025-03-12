from django.core.exceptions import ValidationError

def validate_png(imagem):
    if not imagem.name.lower().endswith('.png'):
        raise ValidationError('Imagem precisa ser .png')