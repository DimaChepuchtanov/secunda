from repository.connect import LocalSessionDB
from repository.model import Base

from repository.organization import OrganizationRepository


async def create_table() -> bool:
    try:
        engine = LocalSessionDB().engine
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        return True
    except Exception as e:
        print("Ошибка создания базы данных, подробнее:", str(e))
        return False


async def insert_test_organization() -> bool:
    test_organization = [
        {"name": "Космические технологии", "phone": "+7 (495) 123-45-67"},
        {"name": "ВкусВилл Продукты", "phone": "8-800-555-12-34"},
        {"name": "СтройГарант", "phone": "+7 (812) 345-67-89"},
        {"name": "МедПрофи Центр", "phone": "+7 (383) 567-89-01"},
        {"name": "АвтоМир Сервис", "phone": "+7 (351) 234-56-78"},
        {"name": "ТехноПарк", "phone": "8-800-777-33-22"},
        {"name": "Бюро Путешествий 'Вокруг света'", "phone": "+7 (495) 987-65-43"},
        {"name": "Юридическая компания 'Право и Закон'", "phone": "+7 (343) 456-78-90"},
        {"name": "Дизайн-студия 'АртВзгляд'", "phone": "+7 (812) 654-32-10"},
        {"name": "Образовательный центр 'Знание'", "phone": "8-800-250-50-50"}
    ]

    count_add_organizations = 0
    do_not_add_organization = []

    for organization in test_organization:
        try:
            async with LocalSessionDB() as session:
                repo = OrganizationRepository(session=session.session)

                await repo.create_organization(
                    organization_data=organization
                )
            count_add_organizations += 1
        except Exception as e:
            print(str(e))
            do_not_add_organization.append(organization)

    print("="*50)
    print(f'{"Статистика добавления организаций":^50}')
    print("="*50)

    print("\n")
    print(f'{f"Добавлено организаций: {count_add_organizations}":^50}')
    print("\n")

    print("\n")
    print(f'{f"Не добавлено: {len(test_organization) - count_add_organizations}":^50}')
    print(*do_not_add_organization, sep="\n")
