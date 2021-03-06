########
# Copyright (C) 2019-2020 Dremio Corporation
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
########


from Dremio import Dremio
from DremioData import DremioData
from DremioFile import DremioFile
from DremioReader import DremioReader
from DremioWriter import DremioWriter
from DremioReportAcl import DremioReportAcl
from DremioReportReflections import DremioReportReflections
from DremioCascadeAcl import DremioCascadeAcl
from DremioDescribeJob import DremioDescribeJob
from DremioClonerConfig import DremioClonerConfig
from datetime import datetime
import logging
import sys
import json
import getpass


def main():
	config = None
	if len(sys.argv) != 2:
		print_usage()
	else:
		config = DremioClonerConfig(sys.argv[1])
		# Execute command
		if config.command == DremioClonerConfig.CMD_GET:
			get_dremio_environment(config)
		elif config.command == DremioClonerConfig.CMD_PUT:
			put_dremio_environment(config)
		elif config.command == DremioClonerConfig.CMD_REPORT_ACL:
			report_acl(config)
		elif config.command == DremioClonerConfig.CMD_CASCADE_ACL:
			cascade_acl(config)
		elif config.command == DremioClonerConfig.CMD_DESCRIBE_JOB:
			describe_job(config)
		elif config.command == DremioClonerConfig.CMD_REPORT_REFLECTIONS:
			report_reflections(config)
		else:
			print_usage()


def print_usage():
	print("""usage: dremio_cloner config_file
Make sure the config file is correct. """)


def get_dremio_environment(config):
	logging.info("Executing command 'get'.")
	if config.source_password is None or config.source_password == "":
		config.source_password = getpass.getpass("Enter password:")
	dremio = Dremio(config.source_endpoint, config.source_username, config.source_password, config.http_timeout, config.source_retry_timedout, config.source_verify_ssl)
	reader = DremioReader(dremio, config)
	dremio_data = reader.read_dremio_environment()
	file = DremioFile(config)
	file.save_dremio_environment(dremio_data)
	logging.info("Command 'get' finished with " + str(reader.get_errors_count()) + " error(s).")
	print("Done with " + str(reader.get_errors_count()) + " error(s). Please review log file for details.")


def put_dremio_environment(config):
	logging.info("Executing command 'put'.")
	file = DremioFile(config)
	dremio_data = file.read_dremio_environment()
	if config.target_password is None or config.target_password == "":
		config.target_password = getpass.getpass("Enter password:")
	dremio = Dremio(config.target_endpoint, config.target_username, config.target_password, config.http_timeout, verify_ssl=config.target_verify_ssl)
	writer = DremioWriter(dremio, dremio_data, config)
	writer.write_dremio_environment()
	logging.info("Command 'put' finished with " + str(writer.get_errors_count()) + " error(s).")
	print("Done with " + str(writer.get_errors_count()) + " error(s). Please review log file for details.")


def report_acl(config):
	logging.info("Executing command 'report-acl'.")
	if config.source_password is None or config.source_password == "":
		config.source_password = getpass.getpass("Enter password:")
	dremio = Dremio(config.source_endpoint, config.source_username, config.source_password, config.http_timeout, config.source_retry_timedout, config.source_verify_ssl)
	reader = DremioReader(dremio, config)
	dremio_data = reader.read_dremio_environment()
	dremio_report = DremioReportAcl(dremio, dremio_data, config)
	dremio_report.save_dremio_report_acl()
	logging.info("Command 'report-acl' finished with " + str(reader.get_errors_count()) + " error(s).")
	print("Done with " + str(reader.get_errors_count()) + " error(s). Please review log file for details.")


def report_reflections(config):
	logging.info("Executing command 'report-reflections'.")
	if config.source_password is None or config.source_password == "":
		config.source_password = getpass.getpass("Enter password:")
	dremio = Dremio(config.source_endpoint, config.source_username, config.source_password, config.http_timeout, config.source_retry_timedout, config.source_verify_ssl)
	dremio_report = DremioReportReflections(dremio, config)
	dremio_report.process_dremio_reflections()
	print("Done. Please review log file for details.")


def cascade_acl(config):
	logging.info("Executing command 'cascade-acl'.")
	if config.target_password is None or config.target_password == "":
		config.target_password = getpass.getpass("Enter password:")
	dremio = Dremio(config.target_endpoint, config.target_username, config.target_password, config.http_timeout, verify_ssl=config.target_verify_ssl)
	cascader = DremioCascadeAcl(dremio, config)
	cascader.cascade_acl()
	logging.info("Command 'cascade-acl' finished with " + str(cascader.get_errors_count()) + " error(s).")
	print("Done with " + str(cascader.get_errors_count()) + " error(s). Please review log file for details.")


def describe_job(config):
	logging.info("Executing command 'describe-job'.")
	if config.source_password is None or config.source_password == "":
		config.source_password = getpass.getpass("Enter password:")
	dremio = Dremio(config.source_endpoint, config.source_username, config.source_password, config.http_timeout, verify_ssl=config.source_verify_ssl)
	describer = DremioDescribeJob(dremio, config)
	if config.target_type == 'sql-dependencies':
		dremio_data = describer.describe_job_sql_dependencies()
	else:
		print_usage()


if __name__ == "__main__":
	main()
