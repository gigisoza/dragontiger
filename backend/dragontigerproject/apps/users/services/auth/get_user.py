from typing import Union

from backend.dragontigerproject.apps.users.services.docs.documents import User


async def get_user(email: str) -> Union[User, None]:
    return await User.find_one(User.email == email)
