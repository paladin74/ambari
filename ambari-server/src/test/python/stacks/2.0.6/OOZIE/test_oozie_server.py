#!/usr/bin/env python

'''
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
'''

import json
from mock.mock import MagicMock, call, patch
from stacks.utils.RMFTestCase import *
from resource_management.core import shell
from resource_management.core.exceptions import Fail
from resource_management.libraries import functions

@patch("platform.linux_distribution", new = MagicMock(return_value="Linux"))
class TestOozieServer(RMFTestCase):
  COMMON_SERVICES_PACKAGE_DIR = "OOZIE/4.0.0.2.0/package"
  STACK_VERSION = "2.0.6"
  UPGRADE_STACK_VERSION = "2.2"

  def test_configure_default(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                       classname = "OozieServer",
                       command = "configure",
                       config_file="default.json",
                       hdp_stack_version = self.STACK_VERSION,
                       target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    self.assert_configure_default()
    self.assertNoMoreResources()


  def test_configure_default_mysql(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                       classname = "OozieServer",
                       command = "configure",
                       config_file="default_oozie_mysql.json",
                       hdp_stack_version = self.STACK_VERSION,
                       target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    self.assertResourceCalled('HdfsResource', '/user/oozie',
        security_enabled = False,
        hadoop_bin_dir = '/usr/bin',
        keytab = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        user = 'hdfs',
        owner = 'oozie',
        hadoop_conf_dir = '/etc/hadoop/conf',
        type = 'directory',
        action = ['create_on_execute'], hdfs_site=self.getConfig()['configurations']['hdfs-site'], principal_name=UnknownConfigurationMock(), default_fs='hdfs://c6401.ambari.apache.org:8020',
        mode = 0775,
    )
    self.assertResourceCalled('HdfsResource', None,
        security_enabled = False,
        hadoop_bin_dir = '/usr/bin',
        keytab = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        user = 'hdfs',
        action = ['execute'], hdfs_site=self.getConfig()['configurations']['hdfs-site'], principal_name=UnknownConfigurationMock(), default_fs='hdfs://c6401.ambari.apache.org:8020',
        hadoop_conf_dir = '/etc/hadoop/conf',
    )
    self.assertResourceCalled('Directory', '/etc/oozie/conf',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              )
    self.assertResourceCalled('XmlConfig', 'oozie-site.xml',
                              group = 'hadoop',
                              conf_dir = '/etc/oozie/conf',
                              mode = 0664,
                              configuration_attributes = {u'final': {u'oozie.service.CallableQueueService.queue.size': u'true',
                                                                     u'oozie.service.PurgeService.purge.interval': u'true'}},
                              owner = 'oozie',
                              configurations = self.getConfig()['configurations']['oozie-site'],
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-env.sh',
                              content = InlineTemplate(self.getConfig()['configurations']['oozie-env']['content']),
                              owner = 'oozie',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-log4j.properties',
                              content = 'log4jproperties\nline2',
                              owner = 'oozie',
                              group = 'hadoop',
                              mode = 0644,
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/adminusers.txt',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/usr/lib/ambari-agent/DBConnectionVerification.jar',
                              content = DownloadSource('http://c6401.ambari.apache.org:8080/resources/DBConnectionVerification.jar'),
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/hadoop-config.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-default.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('Directory', '/etc/oozie/conf/action-conf',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/action-conf/hive.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/var/run/oozie/oozie.pid',
                              action = ['delete'],
                              not_if = u'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              )
    self.assertResourceCalled('Directory', '/usr/lib/oozie//var/tmp/oozie',
                              owner = 'oozie',
                              cd_access = 'a',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              )
    self.assertResourceCalled('Directory', '/var/run/oozie',
                              owner = 'oozie',
                              cd_access = 'a',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              )
    self.assertResourceCalled('Directory', '/var/log/oozie',
                              owner = 'oozie',
                              cd_access = 'a',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              )
    self.assertResourceCalled('Directory', '/var/tmp/oozie',
                              owner = 'oozie',
                              cd_access = 'a',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              )
    self.assertResourceCalled('Directory', '/hadoop/oozie/data',
                              owner = 'oozie',
                              cd_access = 'a',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie',
                              owner = 'oozie',
                              cd_access = 'a',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server/webapps/',
                              owner = 'oozie',
                              cd_access = 'a',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server/conf',
                              owner = 'oozie',
                              cd_access = 'a',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server',
                              owner = 'oozie',
                              recursive = True,
                              group = 'hadoop',
                              mode = 0755,
                              cd_access = 'a',
                              )
    self.assertResourceCalled('Directory', '/usr/lib/oozie/libext',
                              recursive = True,
                              )
    self.assertResourceCalled('Execute', ('tar', '-xvf', '/usr/lib/oozie/oozie-sharelib.tar.gz', '-C', '/usr/lib/oozie'),
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              sudo = True,
                              )
    self.assertResourceCalled('Execute', ('cp', '/usr/share/HDP-oozie/ext-2.2.zip', '/usr/lib/oozie/libext'),
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              sudo = True,
                              )
    self.assertResourceCalled('Execute', ('chown', u'oozie:hadoop', '/usr/lib/oozie/libext/ext-2.2.zip'),
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              sudo = True,
                              )
    self.assertResourceCalled('Execute', ('chown', '-RL', u'oozie:hadoop', '/var/lib/oozie/oozie-server/conf'),
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              sudo = True,
                              )
    self.assertResourceCalled('File', '/tmp/mysql-connector-java.jar',
                              content = DownloadSource('http://c6401.ambari.apache.org:8080/resources//mysql-jdbc-driver.jar'),
                              )
    self.assertResourceCalled('Execute', ('cp',
                                          '--remove-destination',
                                          '/tmp/mysql-connector-java.jar',
                                          '/usr/lib/oozie/libext/mysql-connector-java.jar'),
                              path = ['/bin', '/usr/bin/'],
                              sudo = True,
                              )
    self.assertResourceCalled('File', '/usr/lib/oozie/libext/mysql-connector-java.jar',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('Execute', 'ambari-sudo.sh cp /usr/lib/falcon/oozie/ext/falcon-oozie-el-extension-*.jar /usr/lib/oozie/libext',
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              )
    self.assertResourceCalled('Execute', 'ambari-sudo.sh chown oozie:hadoop /usr/lib/oozie/libext/falcon-oozie-el-extension-*.jar',
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              )
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/oozie-setup.sh prepare-war ',
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              user = 'oozie',
                              )
    self.assertResourceCalled('Execute', ('chown', '-R', u'oozie:hadoop', '/var/lib/oozie/oozie-server'),
        sudo = True,
    )

  @patch("os.path.isfile")
  def test_start_default(self, isfile_mock):
    isfile_mock.return_value = True
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                         classname = "OozieServer",
                         command = "start",
                         config_file="default.json",
                         hdp_stack_version = self.STACK_VERSION,
                         target = RMFTestCase.TARGET_COMMON_SERVICES
        )
    self.assert_configure_default()
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/ooziedb.sh create -sqlfile oozie.sql -run',
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        ignore_failures = True,
        user = 'oozie',
        )
    self.assertResourceCalled('Execute', ' hadoop --config /etc/hadoop/conf dfs -put /usr/lib/oozie/share /user/oozie ; hadoop --config /etc/hadoop/conf dfs -chmod -R 755 /user/oozie/share',
        not_if = shell.as_user(" hadoop --config /etc/hadoop/conf dfs -ls /user/oozie/share | awk 'BEGIN {count=0;} /share/ {count++} END {if (count > 0) {exit 0} else {exit 1}}'", "oozie"),
        user = u'oozie',
        path = ['/usr/bin:/usr/bin'],
        )
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/oozie-start.sh',
        environment = {'OOZIE_CONFIG': '/etc/oozie/conf'},
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        user = 'oozie',
        )
    self.assertNoMoreResources()


  def test_stop_default(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                         classname = "OozieServer",
                         command = "stop",
                         config_file="default.json",
                         hdp_stack_version = self.STACK_VERSION,
                         target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/oozie-stop.sh',
        environment = {'OOZIE_CONFIG': '/etc/oozie/conf'},
        only_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        user = 'oozie',
    )
    self.assertResourceCalled('File', '/var/run/oozie/oozie.pid',
        action = ['delete'],
    )
    self.assertNoMoreResources()


  def test_configure_secured(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                       classname = "OozieServer",
                       command = "configure",
                       config_file="secured.json",
                       hdp_stack_version = self.STACK_VERSION,
                       target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    self.assert_configure_secured()
    self.assertNoMoreResources()

  @patch("os.path.isfile")
  def test_start_secured(self, isfile_mock):
    isfile_mock.return_value = True
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                         classname = "OozieServer",
                         command = "start",
                         config_file="secured.json",
                         hdp_stack_version = self.STACK_VERSION,
                         target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    self.assert_configure_secured()
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/ooziedb.sh create -sqlfile oozie.sql -run',
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              ignore_failures = True,
                              user = 'oozie',
                              )
    self.assertResourceCalled('Execute', '/usr/bin/kinit -kt /etc/security/keytabs/oozie.service.keytab oozie/c6402.ambari.apache.org@EXAMPLE.COM; hadoop --config /etc/hadoop/conf dfs -put /usr/lib/oozie/share /user/oozie ; hadoop --config /etc/hadoop/conf dfs -chmod -R 755 /user/oozie/share',
                              not_if = shell.as_user("/usr/bin/kinit -kt /etc/security/keytabs/oozie.service.keytab oozie/c6402.ambari.apache.org@EXAMPLE.COM; hadoop --config /etc/hadoop/conf dfs -ls /user/oozie/share | awk 'BEGIN {count=0;} /share/ {count++} END {if (count > 0) {exit 0} else {exit 1}}'", "oozie"),
                              user = 'oozie',
                              path = ['/usr/bin:/usr/bin'],
                              )
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/oozie-start.sh',
                              environment = {'OOZIE_CONFIG': '/etc/oozie/conf'},
                              not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
                              user = 'oozie',
                              )
    self.assertNoMoreResources()

  def test_stop_secured(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                         classname = "OozieServer",
                         command = "stop",
                         config_file="secured.json",
                         hdp_stack_version = self.STACK_VERSION,
                         target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/oozie-stop.sh',
        environment = {'OOZIE_CONFIG': '/etc/oozie/conf'},
        only_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        user = 'oozie',
    )
    self.assertResourceCalled('File', '/var/run/oozie/oozie.pid',
        action = ['delete'],
    )
    self.assertNoMoreResources()


  def assert_configure_default(self):
    self.assertResourceCalled('HdfsResource', '/user/oozie',
        security_enabled = False,
        hadoop_conf_dir = '/etc/hadoop/conf',
        keytab = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        user = 'hdfs',
        owner = 'oozie',
        hadoop_bin_dir = '/usr/bin',
        type = 'directory',
        action = ['create_on_execute'], hdfs_site=self.getConfig()['configurations']['hdfs-site'], principal_name=UnknownConfigurationMock(), default_fs='hdfs://c6401.ambari.apache.org:8020',
        mode = 0775,
    )
    self.assertResourceCalled('HdfsResource', None,
        security_enabled = False,
        hadoop_bin_dir = '/usr/bin',
        keytab = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        user = 'hdfs',
        action = ['execute'], hdfs_site=self.getConfig()['configurations']['hdfs-site'], principal_name=UnknownConfigurationMock(), default_fs='hdfs://c6401.ambari.apache.org:8020',
        hadoop_conf_dir = '/etc/hadoop/conf',
    )
    self.assertResourceCalled('Directory', '/etc/oozie/conf',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True
    )
    self.assertResourceCalled('XmlConfig', 'oozie-site.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              mode = 0664,
                              conf_dir = '/etc/oozie/conf',
                              configurations = self.getConfig()['configurations']['oozie-site'],
                              configuration_attributes = self.getConfig()['configuration_attributes']['oozie-site']
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-env.sh',
                              owner = 'oozie',
                              content = InlineTemplate(self.getConfig()['configurations']['oozie-env']['content'])
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-log4j.properties',
                              owner = 'oozie',
                              group = 'hadoop',
                              mode = 0644,
                              content = 'log4jproperties\nline2'
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/adminusers.txt',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/hadoop-config.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-default.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('Directory', '/etc/oozie/conf/action-conf',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/action-conf/hive.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/var/run/oozie/oozie.pid',
                              action=["delete"],
                              not_if="ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1"
                              )
    self.assertResourceCalled('Directory', '/usr/lib/oozie//var/tmp/oozie',
        owner = 'oozie',
        group = 'hadoop',
        recursive = True,
        mode = 0755,
        cd_access='a'
    )
    self.assertResourceCalled('Directory', '/var/run/oozie',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/log/oozie',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/tmp/oozie',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/hadoop/oozie/data',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server/webapps/',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server/conf',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/usr/lib/oozie/libext',
        recursive = True,
    )
    self.assertResourceCalled('Execute', ('tar', '-xvf', '/usr/lib/oozie/oozie-sharelib.tar.gz', '-C', '/usr/lib/oozie'),
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        sudo = True,
    )
    self.assertResourceCalled('Execute', ('cp', '/usr/share/HDP-oozie/ext-2.2.zip', '/usr/lib/oozie/libext'),
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        sudo = True,
    )
    self.assertResourceCalled('Execute', ('chown', u'oozie:hadoop', '/usr/lib/oozie/libext/ext-2.2.zip'),
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        sudo = True,
    )
    self.assertResourceCalled('Execute', ('chown', '-RL', u'oozie:hadoop', '/var/lib/oozie/oozie-server/conf'),
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        sudo = True,
    )
    self.assertResourceCalled('Execute', 'ambari-sudo.sh cp /usr/lib/falcon/oozie/ext/falcon-oozie-el-extension-*.jar /usr/lib/oozie/libext',
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
    )
    self.assertResourceCalled('Execute', 'ambari-sudo.sh chown oozie:hadoop /usr/lib/oozie/libext/falcon-oozie-el-extension-*.jar',
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
    )
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/oozie-setup.sh prepare-war ',
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        user = 'oozie',
    )
    self.assertResourceCalled('Execute', ('chown', '-R', u'oozie:hadoop', '/var/lib/oozie/oozie-server'),
        sudo = True,
    )


  def assert_configure_secured(self):
    self.assertResourceCalled('HdfsResource', '/user/oozie',
        security_enabled = True,
        hadoop_conf_dir = '/etc/hadoop/conf',
        keytab = '/etc/security/keytabs/hdfs.headless.keytab',
        
        kinit_path_local = '/usr/bin/kinit',
        user = 'hdfs',
        owner = 'oozie',
        hadoop_bin_dir = '/usr/bin',
        type = 'directory',
        action = ['create_on_execute'], hdfs_site=self.getConfig()['configurations']['hdfs-site'], principal_name='hdfs', default_fs='hdfs://c6401.ambari.apache.org:8020',
        mode = 0775,
    )
    self.assertResourceCalled('HdfsResource', None,
        security_enabled = True,
        hadoop_bin_dir = '/usr/bin',
        keytab = '/etc/security/keytabs/hdfs.headless.keytab',
        
        kinit_path_local = '/usr/bin/kinit',
        user = 'hdfs',
        action = ['execute'], hdfs_site=self.getConfig()['configurations']['hdfs-site'], principal_name='hdfs', default_fs='hdfs://c6401.ambari.apache.org:8020',
        hadoop_conf_dir = '/etc/hadoop/conf',
    )
    self.assertResourceCalled('Directory', '/etc/oozie/conf',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True
                              )
    self.assertResourceCalled('XmlConfig', 'oozie-site.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              mode = 0664,
                              conf_dir = '/etc/oozie/conf',
                              configurations = self.getConfig()['configurations']['oozie-site'],
                              configuration_attributes = self.getConfig()['configuration_attributes']['oozie-site']
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-env.sh',
                              owner = 'oozie',
                              content = InlineTemplate(self.getConfig()['configurations']['oozie-env']['content'])
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-log4j.properties',
                              owner = 'oozie',
                              group = 'hadoop',
                              mode = 0644,
                              content = 'log4jproperties\nline2'
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/adminusers.txt',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/hadoop-config.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/oozie-default.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('Directory', '/etc/oozie/conf/action-conf',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/oozie/conf/action-conf/hive.xml',
                              owner = 'oozie',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/var/run/oozie/oozie.pid',
                              action=["delete"],
                              not_if="ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1"
    )
    self.assertResourceCalled('Directory', '/usr/lib/oozie//var/tmp/oozie',
        owner = 'oozie',
        group = 'hadoop',
        recursive = True,
        mode = 0755,
        cd_access='a'
    )
    self.assertResourceCalled('Directory', '/var/run/oozie',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/log/oozie',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/tmp/oozie',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/hadoop/oozie/data',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server/webapps/',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server/conf',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/var/lib/oozie/oozie-server',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True,
                              mode = 0755,
                              cd_access='a'
                              )
    self.assertResourceCalled('Directory', '/usr/lib/oozie/libext',
        recursive = True,
    )
    self.assertResourceCalled('Execute', ('tar', '-xvf', '/usr/lib/oozie/oozie-sharelib.tar.gz', '-C', '/usr/lib/oozie'),
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        sudo = True,
    )
    self.assertResourceCalled('Execute', ('cp', '/usr/share/HDP-oozie/ext-2.2.zip', '/usr/lib/oozie/libext'),
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        sudo = True,
    )
    self.assertResourceCalled('Execute', ('chown', u'oozie:hadoop', '/usr/lib/oozie/libext/ext-2.2.zip'),
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        sudo = True,
    )
    self.assertResourceCalled('Execute', ('chown', '-RL', u'oozie:hadoop', '/var/lib/oozie/oozie-server/conf'),
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        sudo = True,
    )
    self.assertResourceCalled('Execute', 'ambari-sudo.sh cp /usr/lib/falcon/oozie/ext/falcon-oozie-el-extension-*.jar /usr/lib/oozie/libext',
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
    )
    self.assertResourceCalled('Execute', 'ambari-sudo.sh chown oozie:hadoop /usr/lib/oozie/libext/falcon-oozie-el-extension-*.jar',
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
    )
    self.assertResourceCalled('Execute', 'cd /var/tmp/oozie && /usr/lib/oozie/bin/oozie-setup.sh prepare-war -secure',
        not_if = 'ls /var/run/oozie/oozie.pid >/dev/null 2>&1 && ps -p `cat /var/run/oozie/oozie.pid` >/dev/null 2>&1',
        user = 'oozie',
    )
    self.assertResourceCalled('Execute', ('chown', '-R', u'oozie:hadoop', '/var/lib/oozie/oozie-server'),
        sudo = True,
    )

    def test_configure_default_hdp22(self):
      config_file = "stacks/2.0.6/configs/default.json"
      with open(config_file, "r") as f:
        default_json = json.load(f)

      default_json['hostLevelParams']['stack_version']= '2.2'
      self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                       classname = "OozieServer",
                       command = "configure",
                       config_file="default.json",
                       hdp_stack_version = self.STACK_VERSION,
                       target = RMFTestCase.TARGET_COMMON_SERVICES
      )
      self.assert_configure_default()
      self.assertResourceCalled('Directory', '/etc/oozie/conf/action-conf/hive',
                              owner = 'oozie',
                              group = 'hadoop',
                              recursive = True
                              )
      self.assertResourceCalled('XmlConfig', 'hive-site',
                                owner = 'oozie',
                                group = 'hadoop',
                                mode = 0664,
                                conf_dir = '/etc/oozie/conf/action-conf/hive',
                                configurations = self.getConfig()['configurations']['hive-site'],
                                configuration_attributes = self.getConfig()['configuration_attributes']['hive-site']
      )
      self.assertResourceCalled('XmlConfig', 'tez-site',
                                owner = 'oozie',
                                group = 'hadoop',
                                mode = 0664,
                                conf_dir = '/etc/oozie/conf/action-conf/hive',
                                configurations = self.getConfig()['configurations']['tez-site'],
                                configuration_attributes = self.getConfig()['configuration_attributes']['tez-site']
      )
      self.assertNoMoreResources()


  @patch("resource_management.libraries.functions.security_commons.build_expectations")
  @patch("resource_management.libraries.functions.security_commons.get_params_from_filesystem")
  @patch("resource_management.libraries.functions.security_commons.validate_security_config_properties")
  @patch("resource_management.libraries.functions.security_commons.cached_kinit_executor")
  @patch("resource_management.libraries.script.Script.put_structured_out")
  def test_security_status(self, put_structured_out_mock, cached_kinit_executor_mock, validate_security_config_mock, get_params_mock, build_exp_mock):
    # Test that function works when is called with correct parameters
    security_params = {
      "oozie-site": {
        "oozie.authentication.type": "kerberos",
        "oozie.service.AuthorizationService.security.enabled": "true",
        "oozie.service.HadoopAccessorService.kerberos.enabled": "true",
        "local.realm": "EXAMPLE.COM",
        "oozie.authentication.kerberos.principal": "principal",
        "oozie.authentication.kerberos.keytab": "/path/to_keytab",
        "oozie.service.HadoopAccessorService.kerberos.principal": "principal",
        "oozie.service.HadoopAccessorService.keytab.file": "/path/to_keytab"}
    }

    result_issues = []
    props_value_check = {"oozie.authentication.type": "kerberos",
                         "oozie.service.AuthorizationService.security.enabled": "true",
                         "oozie.service.HadoopAccessorService.kerberos.enabled": "true"}
    props_empty_check = [ "local.realm",
                          "oozie.authentication.kerberos.principal",
                          "oozie.authentication.kerberos.keytab",
                          "oozie.service.HadoopAccessorService.kerberos.principal",
                          "oozie.service.HadoopAccessorService.keytab.file"]
    props_read_check = None

    get_params_mock.return_value = security_params
    validate_security_config_mock.return_value = result_issues

    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                       classname = "OozieServer",
                       command = "security_status",
                       config_file="secured.json",
                       hdp_stack_version = self.STACK_VERSION,
                       target = RMFTestCase.TARGET_COMMON_SERVICES
    )

    get_params_mock.assert_called_with("/etc/oozie/conf", {'oozie-site.xml': 'XML'})
    build_exp_mock.assert_called_with('oozie-site', props_value_check, props_empty_check, props_read_check)
    put_structured_out_mock.assert_called_with({"securityState": "SECURED_KERBEROS"})
    self.assertTrue(cached_kinit_executor_mock.call_count, 2)
    cached_kinit_executor_mock.assert_called_with('/usr/bin/kinit',
                                                  self.config_dict['configurations']['oozie-env']['oozie_user'],
                                                  security_params['oozie-site']['oozie.service.HadoopAccessorService.keytab.file'],
                                                  security_params['oozie-site']['oozie.service.HadoopAccessorService.kerberos.principal'],
                                                  self.config_dict['hostname'],
                                                  '/tmp')

    # Testing that the exception throw by cached_executor is caught
    cached_kinit_executor_mock.reset_mock()
    cached_kinit_executor_mock.side_effect = Exception("Invalid command")

    try:
      self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                         classname = "OozieServer",
                         command = "security_status",
                         config_file="secured.json",
                         hdp_stack_version = self.STACK_VERSION,
                         target = RMFTestCase.TARGET_COMMON_SERVICES
      )
    except:
      self.assertTrue(True)

    # Testing with a security_params which doesn't contains oozie-site
    empty_security_params = {}
    cached_kinit_executor_mock.reset_mock()
    get_params_mock.reset_mock()
    put_structured_out_mock.reset_mock()
    get_params_mock.return_value = empty_security_params

    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                       classname = "OozieServer",
                       command = "security_status",
                       config_file="secured.json",
                       hdp_stack_version = self.STACK_VERSION,
                       target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    put_structured_out_mock.assert_called_with({"securityIssuesFound": "Keytab file or principal are not set property."})

    # Testing with not empty result_issues
    result_issues_with_params = {
      'oozie-site': "Something bad happened"
    }

    validate_security_config_mock.reset_mock()
    get_params_mock.reset_mock()
    validate_security_config_mock.return_value = result_issues_with_params
    get_params_mock.return_value = security_params

    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                       classname = "OozieServer",
                       command = "security_status",
                       config_file="secured.json",
                       hdp_stack_version = self.STACK_VERSION,
                       target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    put_structured_out_mock.assert_called_with({"securityState": "UNSECURED"})

    # Testing with security_enable = false
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
                       classname = "OozieServer",
                       command = "security_status",
                       config_file="default.json",
                       hdp_stack_version = self.STACK_VERSION,
                       target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    put_structured_out_mock.assert_called_with({"securityState": "UNSECURED"})


  @patch("tarfile.open")
  @patch("os.path.isdir")
  @patch("os.path.exists")
  @patch("os.path.isfile")
  @patch("os.remove")
  @patch("os.chmod")
  @patch("shutil.rmtree", new = MagicMock())
  @patch("glob.iglob")
  @patch("shutil.copy2", new = MagicMock())
  def test_upgrade(self, glob_mock, chmod_mock, remove_mock,
      isfile_mock, exists_mock, isdir_mock, tarfile_open_mock):

    isdir_mock.return_value = True
    exists_mock.side_effect = [False,False,True]
    isfile_mock.return_value = True
    glob_mock.return_value = ["/usr/hdp/2.2.1.0-2187/hadoop/lib/hadoop-lzo-0.6.0.2.2.1.0-2187.jar"]

    prepare_war_stdout = """INFO: Adding extension: libext/mysql-connector-java.jar
    New Oozie WAR file with added 'JARs' at /var/lib/oozie/oozie-server/webapps/oozie.war"""

    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
     classname = "OozieServer", command = "pre_rolling_restart", config_file = "oozie-upgrade.json",
     hdp_stack_version = self.UPGRADE_STACK_VERSION,
     target = RMFTestCase.TARGET_COMMON_SERVICES,
     call_mocks = [(0, prepare_war_stdout)]
    )

    # 2 calls to tarfile.open (1 directories, read + write)
    self.assertTrue(tarfile_open_mock.called)
    self.assertEqual(tarfile_open_mock.call_count,2)

    self.assertTrue(chmod_mock.called)
    self.assertEqual(chmod_mock.call_count,1)
    chmod_mock.assert_called_once_with('/usr/hdp/current/oozie-server/libext-customer', 511)

    self.assertTrue(isfile_mock.called)
    self.assertEqual(isfile_mock.call_count,3)
    isfile_mock.assert_called_with('/usr/share/HDP-oozie/ext-2.2.zip')

    self.assertTrue(glob_mock.called)
    self.assertEqual(glob_mock.call_count,1)
    glob_mock.assert_called_with('/usr/hdp/2.2.1.0-2135/hadoop/lib/hadoop-lzo*.jar')

    self.assertResourceCalled('Execute', 'hdp-select set oozie-server 2.2.1.0-2135',)
    self.assertResourceCalled('HdfsResource', '/user/oozie/share',
        security_enabled = False,
        hadoop_bin_dir = '/usr/hdp/current/hadoop-client/bin',
        keytab = UnknownConfigurationMock(),
        default_fs = 'hdfs://c6401.ambari.apache.org:8020',
        user = 'hdfs',
        hdfs_site = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        principal_name = UnknownConfigurationMock(),
        recursive_chmod = True,
        owner = 'oozie',
        group = 'hadoop',
        hadoop_conf_dir = '/usr/hdp/current/hadoop-client/conf',
        type = 'directory',
        action = ['create_on_execute'],
        mode = 0755,
    )
    self.assertResourceCalled('HdfsResource', None,
        security_enabled = False,
        hadoop_bin_dir = '/usr/hdp/current/hadoop-client/bin',
        keytab = UnknownConfigurationMock(),
        default_fs = 'hdfs://c6401.ambari.apache.org:8020',
        hdfs_site = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        principal_name = UnknownConfigurationMock(),
        user = 'hdfs',
        action = ['execute'],
        hadoop_conf_dir = '/usr/hdp/current/hadoop-client/conf',
    )
    self.assertResourceCalled('Execute', '/usr/hdp/current/oozie-server/bin/ooziedb.sh upgrade -run', user='oozie')
    self.assertResourceCalled('Execute', '/usr/hdp/current/oozie-server/bin/oozie-setup.sh sharelib create -fs hdfs://c6401.ambari.apache.org:8020', user='oozie')

    self.assertNoMoreResources()

  @patch("tarfile.open")
  @patch("os.path.isdir")
  @patch("os.path.exists")
  @patch("os.path.isfile")
  @patch("os.remove")
  @patch("os.chmod")
  @patch("shutil.rmtree", new = MagicMock())
  @patch("glob.iglob")
  @patch("shutil.copy2", new = MagicMock())
  def test_upgrade_23(self, glob_mock, chmod_mock, remove_mock,
      isfile_mock, exists_mock, isdir_mock, tarfile_open_mock):

    isdir_mock.return_value = True
    exists_mock.side_effect = [False,False,True]
    isfile_mock.return_value = True
    glob_mock.return_value = ["/usr/hdp/2.2.1.0-2187/hadoop/lib/hadoop-lzo-0.6.0.2.2.1.0-2187.jar"]

    prepare_war_stdout = """INFO: Adding extension: libext/mysql-connector-java.jar
    New Oozie WAR file with added 'JARs' at /var/lib/oozie/oozie-server/webapps/oozie.war"""


    config_file = self.get_src_folder()+"/test/python/stacks/2.2/configs/oozie-upgrade.json"
    with open(config_file, "r") as f:
      json_content = json.load(f)
    version = '2.3.0.0-1234'
    json_content['commandParams']['version'] = version

    mocks_dict = {}
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
     classname = "OozieServer", command = "pre_rolling_restart", config_dict = json_content,
     hdp_stack_version = self.UPGRADE_STACK_VERSION,
     target = RMFTestCase.TARGET_COMMON_SERVICES,
     call_mocks = [(0, None), (0, None), (0, prepare_war_stdout)],
     mocks_dict = mocks_dict
    )

    # 2 calls to tarfile.open (1 directories, read + write)
    self.assertTrue(tarfile_open_mock.called)
    self.assertEqual(tarfile_open_mock.call_count,2)

    self.assertTrue(chmod_mock.called)
    self.assertEqual(chmod_mock.call_count,1)
    chmod_mock.assert_called_once_with('/usr/hdp/current/oozie-server/libext-customer', 511)

    self.assertTrue(isfile_mock.called)
    self.assertEqual(isfile_mock.call_count,3)
    isfile_mock.assert_called_with('/usr/share/HDP-oozie/ext-2.2.zip')

    self.assertTrue(glob_mock.called)
    self.assertEqual(glob_mock.call_count,1)
    glob_mock.assert_called_with('/usr/hdp/2.3.0.0-1234/hadoop/lib/hadoop-lzo*.jar')

    self.assertResourceCalled('Execute', 'hdp-select set oozie-server 2.3.0.0-1234')
    self.assertResourceCalled('HdfsResource', '/user/oozie/share',
        security_enabled = False,
        hadoop_bin_dir = '/usr/hdp/current/hadoop-client/bin',
        keytab = UnknownConfigurationMock(),
        default_fs = 'hdfs://c6401.ambari.apache.org:8020',
        user = 'hdfs',
        hdfs_site = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        principal_name = UnknownConfigurationMock(),
        recursive_chmod = True,
        owner = 'oozie',
        group = 'hadoop',
        hadoop_conf_dir = '/usr/hdp/current/hadoop-client/conf',
        type = 'directory',
        action = ['create_on_execute'],
        mode = 0755,
    )
    self.assertResourceCalled('HdfsResource', None,
        security_enabled = False,
        hadoop_bin_dir = '/usr/hdp/current/hadoop-client/bin',
        keytab = UnknownConfigurationMock(),
        default_fs = 'hdfs://c6401.ambari.apache.org:8020',
        hdfs_site = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        principal_name = UnknownConfigurationMock(),
        user = 'hdfs',
        action = ['execute'],
        hadoop_conf_dir = '/usr/hdp/current/hadoop-client/conf',
    )
    self.assertResourceCalled('Execute', '/usr/hdp/current/oozie-server/bin/ooziedb.sh upgrade -run',
        user = 'oozie',
    )
    self.assertResourceCalled('Execute', '/usr/hdp/current/oozie-server/bin/oozie-setup.sh sharelib create -fs hdfs://c6401.ambari.apache.org:8020', user='oozie')

    self.assertNoMoreResources()

    self.assertEquals(3, mocks_dict['call'].call_count)
    self.assertEquals(
      "conf-select create-conf-dir --package oozie --stack-version 2.3.0.0-1234 --conf-version 0",
       mocks_dict['call'].call_args_list[0][0][0])
    self.assertEquals(
      "conf-select set-conf-dir --package oozie --stack-version 2.3.0.0-1234 --conf-version 0",
       mocks_dict['call'].call_args_list[1][0][0])


  @patch("tarfile.open")
  @patch("os.path.isdir")
  @patch("os.path.exists")
  @patch("os.path.isfile")
  @patch("os.remove")
  @patch("os.chmod")
  @patch("shutil.rmtree", new = MagicMock())
  @patch("shutil.copy2", new = MagicMock())
  def test_downgrade_no_compression_library_copy(self, chmod_mock, remove_mock,
      isfile_mock, exists_mock, isdir_mock, tarfile_open_mock):

    isdir_mock.return_value = True
    exists_mock.return_value = False
    isfile_mock.return_value = True

    prepare_war_stdout = """INFO: Adding extension: libext/mysql-connector-java.jar
    New Oozie WAR file with added 'JARs' at /var/lib/oozie/oozie-server/webapps/oozie.war"""

    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
     classname = "OozieServer", command = "pre_rolling_restart", config_file = "oozie-downgrade.json",
     hdp_stack_version = self.UPGRADE_STACK_VERSION,
     target = RMFTestCase.TARGET_COMMON_SERVICES,
     call_mocks = [(0, prepare_war_stdout)])

    # 2 calls to tarfile.open (1 directories, read + write)
    self.assertTrue(tarfile_open_mock.called)
    self.assertEqual(tarfile_open_mock.call_count,2)

    self.assertTrue(chmod_mock.called)
    self.assertEqual(chmod_mock.call_count,1)
    chmod_mock.assert_called_once_with('/usr/hdp/current/oozie-server/libext-customer', 511)

    self.assertTrue(isfile_mock.called)
    self.assertEqual(isfile_mock.call_count,2)
    isfile_mock.assert_called_with('/usr/share/HDP-oozie/ext-2.2.zip')

    self.assertResourceCalled('Execute', 'hdp-select set oozie-server 2.2.0.0-0000')
    self.assertResourceCalled('HdfsResource', '/user/oozie/share',
        security_enabled = False,
        hadoop_bin_dir = '/usr/hdp/2.2.0.0-0000/hadoop/bin',
        keytab = UnknownConfigurationMock(),
        default_fs = 'hdfs://c6401.ambari.apache.org:8020',
        user = 'hdfs',
        hdfs_site = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        principal_name = UnknownConfigurationMock(),
        recursive_chmod = True,
        owner = 'oozie',
        group = 'hadoop',
        hadoop_conf_dir = '/usr/hdp/current/hadoop-client/conf',
        type = 'directory',
        action = ['create_on_execute'],
        mode = 0755,
    )
    self.assertResourceCalled('HdfsResource', None,
        security_enabled = False,
        hadoop_bin_dir = '/usr/hdp/2.2.0.0-0000/hadoop/bin',
        keytab = UnknownConfigurationMock(),
        default_fs = 'hdfs://c6401.ambari.apache.org:8020',
        hdfs_site = UnknownConfigurationMock(),
        kinit_path_local = '/usr/bin/kinit',
        principal_name = UnknownConfigurationMock(),
        user = 'hdfs',
        action = ['execute'],
        hadoop_conf_dir = '/usr/hdp/current/hadoop-client/conf',
    )
    self.assertResourceCalled('Execute', '/usr/hdp/current/oozie-server/bin/ooziedb.sh upgrade -run', user='oozie')
    self.assertResourceCalled('Execute', '/usr/hdp/current/oozie-server/bin/oozie-setup.sh sharelib create -fs hdfs://c6401.ambari.apache.org:8020', user='oozie')


  @patch("tarfile.open")
  @patch("os.path.isdir")
  @patch("os.path.exists")
  @patch("os.path.isfile")
  @patch("os.remove")
  @patch("os.chmod")
  @patch("shutil.rmtree", new = MagicMock())
  @patch("glob.iglob", new = MagicMock(return_value=["/usr/hdp/2.2.1.0-2187/hadoop/lib/hadoop-lzo-0.6.0.2.2.1.0-2187.jar"]))
  @patch("shutil.copy2")
  def test_upgrade_failed_prepare_war(self, shutil_copy_mock, chmod_mock, remove_mock,
      isfile_mock, exists_mock, isdir_mock, tarfile_open_mock):

    isdir_mock.return_value = True
    exists_mock.side_effect = [False,False,True]
    isfile_mock.return_value = True

    try:
      self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/oozie_server.py",
       classname = "OozieServer", command = "pre_rolling_restart", config_file = "oozie-upgrade.json",
       hdp_stack_version = self.UPGRADE_STACK_VERSION,
       target = RMFTestCase.TARGET_COMMON_SERVICES )

      self.fail("An invalid WAR preparation should have caused an error")
    except Fail,f:
      pass

