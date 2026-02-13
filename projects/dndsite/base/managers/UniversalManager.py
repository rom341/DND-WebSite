from django.db import models

class UniversalManager(models.Manager):
    def create_from_template(self, template):
        field_names = [f.name for f in self.model._meta.fields if not f.primary_key]
        stats_data = {field: getattr(template, field) for field in field_names if hasattr(template, field)}        
        return self.create(**stats_data)