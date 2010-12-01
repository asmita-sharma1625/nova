# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time

import webob
from webob import exc

from nova import flags
from nova import rpc
from nova import utils
from nova import wsgi
from nova import context
from nova.api import cloud
from nova.api.openstack import faults
from nova.compute import api as compute_api
from nova.compute import instance_types
from nova.compute import power_state
import nova.api.openstack
import nova.image.service

FLAGS = flags.FLAGS


def _filter_params(inst_dict):
    """ Extracts all updatable parameters for a server update request """
    keys = dict(name='name', admin_pass='adminPass')
    new_attrs = {}
    for k, v in keys.items():
        if v in inst_dict:
            new_attrs[k] = inst_dict[v]
    return new_attrs


def _entity_list(entities):
    """ Coerces a list of servers into proper dictionary format """
    return dict(servers=entities)


def _entity_detail(inst):
    """ Maps everything to Rackspace-like attributes for return"""
    power_mapping = {
        power_state.NOSTATE: 'build',
        power_state.RUNNING: 'active',
        power_state.BLOCKED: 'active',
        power_state.PAUSED: 'suspended',
        power_state.SHUTDOWN: 'active',
        power_state.SHUTOFF: 'active',
        power_state.CRASHED: 'error'}
    inst_dict = {}

    mapped_keys = dict(status='state', imageId='image_id',
        flavorId='instance_type', name='server_name', id='id')

    for k, v in mapped_keys.iteritems():
        inst_dict[k] = inst[v]

    inst_dict['status'] = power_mapping[inst_dict['status']]
    inst_dict['addresses'] = dict(public=[], private=[])
    inst_dict['metadata'] = {}
    inst_dict['hostId'] = ''

    return dict(server=inst_dict)


def _entity_inst(inst):
    """ Filters all model attributes save for id and name """
    return dict(server=dict(id=inst['id'], name=inst['server_name']))


class Controller(wsgi.Controller):
    """ The Server API controller for the OpenStack API """

    _serialization_metadata = {
        'application/xml': {
            "attributes": {
                "server": ["id", "imageId", "name", "flavorId", "hostId",
                           "status", "progress", "progress"]}}}

    def __init__(self, db_driver=None):
        if not db_driver:
            db_driver = FLAGS.db_driver
        self.db_driver = utils.import_object(db_driver)
        self.network_manager = utils.import_object(FLAGS.network_manager)
        self.compute_api = compute_api.ComputeAPI()
        super(Controller, self).__init__()

    def index(self, req):
        """ Returns a list of server names and ids for a given user """
        return self._items(req, entity_maker=_entity_inst)

    def detail(self, req):
        """ Returns a list of server details for a given user """
        return self._items(req, entity_maker=_entity_detail)

    def _items(self, req, entity_maker):
        """Returns a list of servers for a given user.

        entity_maker - either _entity_detail or _entity_inst
        """
        user_id = req.environ['nova.context']['user']['id']
        ctxt = context.RequestContext(user_id, user_id)
        instance_list = self.db_driver.instance_get_all_by_user(ctxt, user_id)
        limited_list = nova.api.openstack.limited(instance_list, req)
        res = [entity_maker(inst)['server'] for inst in limited_list]
        return _entity_list(res)

    def show(self, req, id):
        """ Returns server details by server id """
        user_id = req.environ['nova.context']['user']['id']
        ctxt = context.RequestContext(user_id, user_id)
        inst = self.db_driver.instance_get_by_internal_id(ctxt, int(id))
        if inst:
            if inst.user_id == user_id:
                return _entity_detail(inst)
        raise faults.Fault(exc.HTTPNotFound())

    def delete(self, req, id):
        """ Destroys a server """
        user_id = req.environ['nova.context']['user']['id']
        ctxt = context.RequestContext(user_id, user_id)
        instance = self.db_driver.instance_get_by_internal_id(ctxt, int(id))
        if instance and instance['user_id'] == user_id:
            self.db_driver.instance_destroy(ctxt, id)
            return faults.Fault(exc.HTTPAccepted())
        return faults.Fault(exc.HTTPNotFound())

    def create(self, req):
        """ Creates a new server for a given user """
        env = self._deserialize(req.body, req)
        if not env:
            return faults.Fault(exc.HTTPUnprocessableEntity())

        user_id = req.environ['nova.context']['user']['id']
        ctxt = context.RequestContext(user_id, user_id)
        key_pair = self.db_driver.key_pair_get_all_by_user(None, user_id)[0]
        instances = self.compute_api.create_instances(ctxt,
            instance_types.get_by_flavor_id(env['server']['flavorId']),
            utils.import_object(FLAGS.image_service),
            env['server']['imageId'],
            self._get_network_topic(ctxt),
            name=env['server']['name'],
            description=env['server']['name'],
            key_name=key_pair['name'],
            key_data=key_pair['public_key'])
        return _entity_inst(instances[0])

    def update(self, req, id):
        """ Updates the server name or password """
        user_id = req.environ['nova.context']['user']['id']
        ctxt = context.RequestContext(user_id, user_id)

        inst_dict = self._deserialize(req.body, req)

        if not inst_dict:
            return faults.Fault(exc.HTTPUnprocessableEntity())

        instance = self.db_driver.instance_get_by_internal_id(ctxt, int(id))
        if not instance or instance.user_id != user_id:
            return faults.Fault(exc.HTTPNotFound())

        self.db_driver.instance_update(ctxt,
                                       int(id),
                                       _filter_params(inst_dict['server']))
        return faults.Fault(exc.HTTPNoContent())

    def action(self, req, id):
        """ multi-purpose method used to reboot, rebuild, and
        resize a server """
        user_id = req.environ['nova.context']['user']['id']
        ctxt = context.RequestContext(user_id, user_id)
        input_dict = self._deserialize(req.body, req)
        try:
            reboot_type = input_dict['reboot']['type']
        except Exception:
            raise faults.Fault(webob.exc.HTTPNotImplemented())
        inst_ref = self.db.instance_get_by_internal_id(ctxt, int(id))
        if not inst_ref or (inst_ref and not inst_ref.user_id == user_id):
            return faults.Fault(exc.HTTPUnprocessableEntity())
        cloud.reboot(id)

    def _get_network_topic(self, context):
        """Retrieves the network host for a project"""
        network_ref = self.network_manager.get_network(context)
        host = network_ref['host']
        if not host:
            host = rpc.call(context,
                            FLAGS.network_topic,
                            {"method": "set_network_host",
                             "args": {"network_id": network_ref['id']}})
        return self.db_driver.queue_get_for(context, FLAGS.network_topic, host)
