from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('phylodating', '0001_initial')
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY email VARCHAR(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY info_csv VARCHAR(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY unrooted_tree VARCHAR(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY rooted_tree_out VARCHAR(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY data_out VARCHAR(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY stats_out VARCHAR(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY plot VARCHAR(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY status VARCHAR(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY stdout LONGTEXT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY stderr LONGTEXT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY warnings LONGTEXT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job MODIFY cmd LONGTEXT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci"),
        migrations.RunSQL("ALTER TABLE bblab_django.phylodating_job CONVERT TO CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci")
    ]