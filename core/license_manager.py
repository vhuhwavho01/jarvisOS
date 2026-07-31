import hashlib
import json
import os
import platform
import uuid
from datetime import datetime


class LicenseManager:

    FILE = "license.json"

    # =====================================================

    def machine_id(self):

        text = (

            platform.node()

            + platform.system()

            + platform.processor()

            + str(uuid.getnode())

        )

        return hashlib.sha256(

            text.encode()

        ).hexdigest()

    # =====================================================

    def create_license(

        self,

        owner,

        key,

        expiry

    ):

        data = {

            "owner": owner,

            "key": key,

            "machine": self.machine_id(),

            "expiry": expiry

        }

        with open(

            self.FILE,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4

            )

    # =====================================================

    def load(self):

        if not os.path.exists(

            self.FILE

        ):

            return None

        with open(

            self.FILE,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    # =====================================================

    def valid(self):

        data = self.load()

        if data is None:

            return False

        if data["machine"] != self.machine_id():

            return False

        expiry = datetime.strptime(

            data["expiry"],

            "%Y-%m-%d"

        )

        return datetime.now() <= expiry

    # =====================================================

    def days_remaining(self):

        data = self.load()

        if data is None:

            return 0

        expiry = datetime.strptime(

            data["expiry"],

            "%Y-%m-%d"

        )

        return max(

            0,

            (expiry - datetime.now()).days

        )

    # =====================================================

    def info(self):

        data = self.load()

        if data is None:

            return None

        data["days_remaining"] = self.days_remaining()

        data["valid"] = self.valid()

        return data