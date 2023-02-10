from django.db import models

STATUS = [
    ("0", "Uploaded"),
    ("1", "Processing"),
    ("2", "Done"),
]
# test

class Input(models.Model):
    file = models.FileField(verbose_name="Fichier brut", upload_to="inputs")
    status = models.CharField(max_length=10, choices=STATUS, default="0")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Output(models.Model):
    input_fk = models.ForeignKey(Input, on_delete=models.CASCADE)
    file = models.FileField(
        verbose_name="Résultat", upload_to="outputs", null=True, blank=True
    )
    downloaded = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
