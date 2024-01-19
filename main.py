# Copyright 2024 EvickaStudio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

from dotenv import load_dotenv

load_dotenv()

# Get the API key
pi_hole_api_key = os.getenv("PI-HOLE-API-KEY")
url = os.getenv("PI-HOLE-URL")  # e.g. http://pihole.local
disable_time = 30  # 30 seconds


from api import pihole

hole = pihole.API(url, pi_hole_api_key)

hole.disable_adblocker(disable_time)
