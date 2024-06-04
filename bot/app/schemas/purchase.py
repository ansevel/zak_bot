from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdditionalInfo(BaseModel):
    long_description: str
    short_description: Optional[str] = None


class Purchase(BaseModel):
    number: str
    object_info: str
    url: str
    customer: str
    end_datetime: datetime
    price: float
    is_active: bool = False
    subscribers: 'Optional[list[UserRead]]' = None
    preferences: Optional[list[AdditionalInfo]] = None
    requirements: Optional[list[AdditionalInfo]] = None
    restrictions: Optional[list[AdditionalInfo]] = None

    def common_data_message_text(self) -> str:
        return (
            f'<strong>Номер:</strong> {self.number}\n\n'
            f'<strong>Заказчик:</strong> {self.customer}\n\n'
            f'<strong>Объект закупки:</strong> {self.object_info}\n\n'
            f'<strong>url:</strong> {self.url}\n\n'
            '<strong>Дата и время окончания срока подачи заявок:</strong> '
            f'{self.end_datetime.strftime("%d.%m.%Y %H:%M")}\n\n'
            f'<strong>Начальная цена контракта:</strong> {self.price} '
            'руб.\n\n'
        )

    def add_long_additional_info(self, formatted_data: str) -> str:
        formatted_data += '<strong>Преимущества:</strong>\n'
        if self.preferences is not None:
            for pr in self.preferences:
                formatted_data += f'{pr.long_description}\n'
            formatted_data += '\n'
        else:
            formatted_data += 'Не установлены\n\n'

        formatted_data += '<strong>Требования к участникам:</strong>\n'
        if self.requirements is not None:
            for n, r in enumerate(self.requirements, start=1):
                formatted_data += f'{n}. {r.long_description}\n'
            formatted_data += '\n'
        else:
            formatted_data += 'Не установлены\n\n'

        formatted_data += '<strong>Ограничения и запреты:</strong>\n'
        if self.restrictions is not None:
            for n, r in enumerate(self.restrictions, start=1):
                formatted_data += f'{n}. {r.long_description}\n'
            formatted_data += '\n'
        else:
            formatted_data += 'Не установлены\n\n'
        return formatted_data


from app.schemas.user import UserRead
Purchase.model_rebuild()
