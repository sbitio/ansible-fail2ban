import os
from ansible import utils
from ansible.utils.template import template
from ansible.runner.return_data import ReturnData
from ansible.callbacks import callback_plugins

class ActionModule(object):

    def __init__(self, runner):
        self.runner = runner

    def run(self, conn, tmp, module_name, module_args, inject, complex_args=None, **kwargs):

        JAIL_OPTIONS = ['logpath', 'ignoreregex', 'maxretry', 'bantime', 'findtime', 'action', 'port', 'protocol', 'filter']

        # Load up options.
        options  = {}
        if complex_args:
            options.update(complex_args)

        options.update(utils.parse_kv(module_args))

        # Collect vars for the template.
        jail_conf = dict()
        name = options.get('name')
        inject['name'] = name
        jail_conf['enabled'] = options.get('enabled', 'true')
        for option in JAIL_OPTIONS:
            if options.has_key(option):
                jail_conf[option] = options.get(option)
        inject['jail_conf'] = jail_conf

        action_path = utils.plugins.action_loader.find_plugin(module_name)
        src = os.path.realpath(os.path.dirname(action_path) + '/../templates/jail.j2')
        dest = os.path.join(inject['fail2ban_dir_parts'], '01_%s.jail' % (name))
        module_args = 'src=%s dest=%s' % (src, dest)
        handler = utils.plugins.action_loader.get('template', self.runner)
        return_data = handler.run(conn, tmp, 'template', module_args, inject)
        if return_data.result.has_key('failed'):
            return return_data

        # Dirty service notification.
        if return_data.result['changed']:
            cp = callback_plugins[0]
            handler_name = 'assemble jail.local'
            cp.playbook._flag_handler(cp.play, template(cp.play.basedir, handler_name, cp.task.module_vars), inject['inventory_hostname'])

        result = dict()
        result['changed'] = return_data.result['changed']
        if result['changed']:
            result['msg'] = 'Jail %s added.' % name
        return ReturnData(conn=conn, comm_ok=True, result=result)

