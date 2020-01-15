# Microsoft Azure Linux Agent
#
# Copyright 2019 Microsoft Corporation
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
#
# Requires Python 2.6+ and Openssl 1.0+
#

from azurelinuxagent.common.datacontract import DataContract, DataContractList


class TelemetryEventParam(DataContract):
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return isinstance(other, TelemetryEventParam) and other.name == self.name and other.value == self.value


class TelemetryEvent(DataContract):
    def __init__(self, eventId=None, providerId=None):
        self.eventId = eventId
        self.providerId = providerId
        self.parameters = DataContractList(TelemetryEventParam)

    # Checking if the particular param name is in the TelemetryEvent.
    def __contains__(self, param_name):
        return param_name in [param.name for param in self.parameters]

    def is_extension_event(self):
        # Events originating from the agent have "WALinuxAgent" as the Name parameter, or they don't have a Name
        # parameter, in the case of log and metric events. So, in case the Name parameter exists and it is not
        # "WALinuxAgent", it is an extension event.
        for param in self.parameters:
            if param.name == "Name":
                return param.value != "WALinuxAgent"
        return False


class TelemetryEventList(DataContract):
    def __init__(self):
        self.events = DataContractList(TelemetryEvent)
