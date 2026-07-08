TRANSLATIONS = {
    "en": {
        "backup_restore": "Backup & Restore",
        "data_catalog": "Data Catalog",
        "settings": "Settings",
        "create_backup": "Create SQLite backup",
        "restore_backup": "Restore SQLite backup",
    },
    "id": {
        "backup_restore": "Cadangan & Pemulihan",
        "data_catalog": "Katalog Data",
        "settings": "Pengaturan",
        "create_backup": "Buat cadangan SQLite",
        "restore_backup": "Pulihkan cadangan SQLite",
    }
}

def t(key, lang="en"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
