from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Escape_room', '0005_rename_solution_puzzle_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='difficulty',
        ),
    ]