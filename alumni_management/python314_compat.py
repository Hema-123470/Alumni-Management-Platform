"""
Python 3.14 compatibility patches for Django.
This fixes the 'super' object attribute error in templates.
"""

import sys

# Only apply patches for Python 3.14+
if sys.version_info >= (3, 14):
    from django.template import context
    
    # Patch Context.__copy__ to work with Python 3.14
    original_copy = context.Context.__copy__
    
    def patched_copy(self):
        """Patched __copy__ method that works with Python 3.14."""
        duplicate = self.__class__(self._dict, current_app=self._current_app)
        duplicate.template = self.template
        duplicate.render_context = self.render_context
        return duplicate
    
    context.Context.__copy__ = patched_copy
    
    print("✓ Applied Python 3.14 compatibility patches for Django templates")
