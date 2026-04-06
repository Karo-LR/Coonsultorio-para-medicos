from django.db import migrations, models


def normalize_recepcion_role(apps, schema_editor):
    Perfil = apps.get_model("core", "Perfil")
    Perfil.objects.filter(rol="recepcion").update(rol="recepcionista")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_cita_created_at_cita_updated_at_alter_cita_estado_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="perfil",
            name="rol",
            field=models.CharField(
                choices=[
                    ("admin", "Administrador"),
                    ("doctor", "Doctor"),
                    ("recepcionista", "Recepcionista"),
                ],
                default="recepcionista",
                max_length=20,
            ),
        ),
        migrations.RunPython(normalize_recepcion_role, migrations.RunPython.noop),
    ]
