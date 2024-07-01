from datetime import datetime
from http import HTTPStatus

import httpx
from bs4 import BeautifulSoup

from app.constants.info_messages import BAD_RESPONSE, NO_RESPONSE
from app.constants.request import HEADERS, URL_PURCHASE_PREFIX
from app.core.exceptions import ParserConnectError
from app.schemas.purchase import AdditionalInfo, Purchase


async def get_response(number: str) -> httpx.Response:
    url = URL_PURCHASE_PREFIX + number.strip()
    try:
        async with httpx.AsyncClient(headers=HEADERS) as client:
            return await client.get(url)
    except httpx.ConnectError:
        raise ParserConnectError


async def get_purchase_from_web(number: str) -> Purchase:
    response = await get_response(number)
    if response is None:
        return {'errors': NO_RESPONSE}
    if response.status_code != HTTPStatus.OK:
        return {'errors': BAD_RESPONSE}
    return await parse_purchase(response)


async def parse_purchase(response: httpx.Response) -> Purchase:
    soup = BeautifulSoup(response.text, 'lxml-xml')
    purchase = {}
    common = soup.commonInfo
    purchase['number'] = common.purchaseNumber.text
    purchase['object_info'] = common.find('purchaseObjectInfo').text
    purchase['url'] = common.href.text
    customer_info = soup.find('customerRequirementsInfo')
    purchase['customer'] = customer_info.find('ns2:fullName').text
    notifications = soup.notificationInfo
    purchase['end_datetime'] = datetime.fromisoformat(
        notifications.find('endDT').text)
    purchase['price'] = notifications.find('maxPrice').text

    preferences = notifications.find_all('preferenseInfo')
    if preferences:
        purchase['preferences'] = []
        for preference in preferences:
            purchase['preferences'].append(
                AdditionalInfo(
                    long_description=preference.find('ns2:name').text
                )
            )

    requirements = notifications.find_all('requirementInfo')
    if requirements:
        purchase['requirements'] = []
        for requirement in requirements:
            req_item = requirement.find('ns2:name').text
            add_requirements = requirement.find('ns3:content')
            if add_requirements is not None:
                add_requirements = add_requirements.text
                req_item += f'\nДополнительные требования: {add_requirements}'
            purchase['requirements'].append(
                AdditionalInfo(long_description=req_item)
            )

    restrictions = notifications.find_all('restrictionInfo')
    if restrictions:
        purchase['restrictions'] = []
        for restriction in restrictions:
            purchase['restrictions'].append(
                AdditionalInfo(
                    long_description=restriction.find('ns2:name').text
                )
            )
    return Purchase(**purchase)
