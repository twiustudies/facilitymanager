from flask_babel import Babel

babel = Babel()

<<<<<<< HEAD
# Unterstützte Sprachen,nur  eingeschraenkt
=======
# Unterstützte Sprachen, eingeschraekt
>>>>>>> 68db010 (changes)
LANGUAGES = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français"
}

def get_locale():
    """Ermittelt die bevorzugte Sprache des Nutzers basierend auf Browser-Einstellungen."""
    return request.accept_languages.best_match(LANGUAGES.keys())
