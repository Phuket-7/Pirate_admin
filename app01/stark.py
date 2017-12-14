print("启动")
from stark.service import v1
from app01 import models

v1.site.register(models.UserInfo)