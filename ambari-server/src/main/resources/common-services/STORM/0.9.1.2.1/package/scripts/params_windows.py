#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
from status_params import *

# server configurations
config = Script.get_config()

stack_is_hdp23_or_further = Script.is_hdp_stack_greater_or_equal("2.3")

hdp_root = os.path.abspath(os.path.join(os.environ["HADOOP_HOME"],".."))
conf_dir = os.environ["STORM_CONF_DIR"]
hadoop_user = config["configurations"]["cluster-env"]["hadoop.user.name"]
storm_user = hadoop_user

security_enabled = config['configurations']['cluster-env']['security_enabled']

if stack_is_hdp23_or_further:
  if security_enabled:
    storm_thrift_transport = config['configurations']['storm-site']['_storm.thrift.secure.transport']
  else:
    storm_thrift_transport = config['configurations']['storm-site']['_storm.thrift.nonsecure.transport']

service_map = {
  "nimbus" : nimbus_win_service_name,
  "supervisor" : supervisor_win_service_name,
  "ui" : ui_win_service_name
}
